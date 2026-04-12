from atlas_ocr.insights.rules import run_rules
from atlas_ocr.models.schema import FrameExtraction


def test_rules_emit_expected_signals() -> None:
    frames = [
        FrameExtraction(timestamp_s=295, game_time_s=300, blue_gold=10000, red_gold=14050, blue_kills=3, red_kills=5),
        FrameExtraction(timestamp_s=300, game_time_s=305, blue_gold=10100, red_gold=14300, blue_kills=3, red_kills=7),
    ]
    insights = run_rules(frames)
    kinds = {i.kind for i in insights}
    assert "objective_setup" in kinds
    assert "overextension_proxy" in kinds
