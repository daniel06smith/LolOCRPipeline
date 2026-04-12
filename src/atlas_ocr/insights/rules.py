from __future__ import annotations

from atlas_ocr.models.schema import FrameExtraction, Insight


def objective_setup_insights(frames: list[FrameExtraction]) -> list[Insight]:
    """Simple MVP rule: flag large gold deficits near objective spawn windows."""
    objective_windows = {300, 600, 900, 1200, 1500}  # dragons/baron simplistic placeholders
    insights: list[Insight] = []

    for frame in frames:
        if frame.game_time_s is None or frame.blue_gold is None or frame.red_gold is None:
            continue
        nearest = min(objective_windows, key=lambda x: abs(x - frame.game_time_s))
        if abs(nearest - frame.game_time_s) > 20:
            continue

        gold_diff = frame.blue_gold - frame.red_gold
        if abs(gold_diff) >= 3000:
            losing_side = "Blue" if gold_diff < 0 else "Red"
            insights.append(
                Insight(
                    kind="objective_setup",
                    severity="medium",
                    timestamp_s=frame.timestamp_s,
                    message=(
                        f"{losing_side} side entered an objective window with ~{abs(gold_diff)} gold deficit; "
                        "contest risk is high."
                    ),
                )
            )
    return insights


def overextension_proxy_insights(frames: list[FrameExtraction]) -> list[Insight]:
    """Proxy heuristic until minimap/player tracking is added."""
    insights: list[Insight] = []
    for prev, cur in zip(frames, frames[1:], strict=False):
        if None in (prev.blue_kills, prev.red_kills, cur.blue_kills, cur.red_kills):
            continue
        blue_delta = cur.blue_kills - prev.blue_kills
        red_delta = cur.red_kills - prev.red_kills
        if blue_delta >= 2 or red_delta >= 2:
            side = "Blue" if red_delta >= 2 else "Red"
            insights.append(
                Insight(
                    kind="overextension_proxy",
                    severity="low",
                    timestamp_s=cur.timestamp_s,
                    message=(
                        f"{side} side conceded multiple kills between samples; review map state for overextension."
                    ),
                )
            )
    return insights


def run_rules(frames: list[FrameExtraction]) -> list[Insight]:
    return [*objective_setup_insights(frames), *overextension_proxy_insights(frames)]
