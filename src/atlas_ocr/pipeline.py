from __future__ import annotations

from collections.abc import Iterable

import cv2
import numpy as np

from atlas_ocr.capture.live import iter_live_frames
from atlas_ocr.capture.video import iter_video_frames
from atlas_ocr.cv.ocr_engine import OCREngine
from atlas_ocr.cv.preprocess import for_ocr
from atlas_ocr.models.schema import FrameExtraction, PipelineConfig, ROI
from atlas_ocr.utils.time_utils import parse_game_time, parse_int


def crop(frame: np.ndarray, roi: ROI) -> np.ndarray:
    return frame[roi.y : roi.y + roi.h, roi.x : roi.x + roi.w]


class AtlasPipeline:
    def __init__(self, config: PipelineConfig) -> None:
        self.config = config
        self.ocr = OCREngine(tesseract_cmd=config.tesseract_cmd)

    def _extract_one(self, timestamp_s: int, frame: np.ndarray) -> FrameExtraction:
        hud = self.config.profile.hud

        timer_img = for_ocr(crop(frame, hud.timer))
        blue_kills_img = for_ocr(crop(frame, hud.blue_kills))
        red_kills_img = for_ocr(crop(frame, hud.red_kills))
        blue_gold_img = for_ocr(crop(frame, hud.blue_gold))
        red_gold_img = for_ocr(crop(frame, hud.red_gold))

        timer_text = self.ocr.read_digits(timer_img)
        blue_kills_text = self.ocr.read_digits(blue_kills_img)
        red_kills_text = self.ocr.read_digits(red_kills_img)
        blue_gold_text = self.ocr.read_digits(blue_gold_img)
        red_gold_text = self.ocr.read_digits(red_gold_img)

        return FrameExtraction(
            timestamp_s=timestamp_s,
            game_time_s=parse_game_time(timer_text),
            blue_kills=parse_int(blue_kills_text),
            red_kills=parse_int(red_kills_text),
            blue_gold=parse_int(blue_gold_text),
            red_gold=parse_int(red_gold_text),
        )

    def run(self, source_path: str | None = None, max_samples: int | None = None) -> list[FrameExtraction]:
        if self.config.source == "video":
            if not source_path:
                raise ValueError("source_path is required when source=video")
            stream: Iterable[tuple[int, np.ndarray]] = iter_video_frames(
                source_path,
                sample_every_seconds=self.config.sample_every_seconds,
            )
        else:
            stream = iter_live_frames(self.config.sample_every_seconds)

        out: list[FrameExtraction] = []
        for idx, (ts, frame) in enumerate(stream):
            out.append(self._extract_one(ts, frame))
            if max_samples is not None and idx + 1 >= max_samples:
                break

        return out


def save_debug_crops(frame: np.ndarray, config: PipelineConfig, out_dir: str) -> None:
    from pathlib import Path

    path = Path(out_dir)
    path.mkdir(parents=True, exist_ok=True)
    hud = config.profile.hud
    for name in ["timer", "blue_kills", "red_kills", "blue_gold", "red_gold", "minimap"]:
        roi = getattr(hud, name)
        cv2.imwrite(str(path / f"{name}.png"), crop(frame, roi))
