from __future__ import annotations

import json
from pathlib import Path

import cv2
import pytest

from atlas_ocr.io.config import load_config
from atlas_ocr.pipeline import AtlasPipeline

FIXTURE_DIR = Path("tests/fixtures")
FRAME_PATH = FIXTURE_DIR / "sample_frame.png"
EXPECT_PATH = FIXTURE_DIR / "sample_frame_expected.json"
CONFIG_PATH = FIXTURE_DIR / "sample_frame_config.yaml"


@pytest.mark.integration
def test_sample_frame_extraction_matches_expected() -> None:
    """Integration test for one known-good frame.

    To run this test, provide:
    - tests/fixtures/sample_frame.png
    - tests/fixtures/sample_frame_config.yaml
    - tests/fixtures/sample_frame_expected.json
    """
    missing = [p for p in (FRAME_PATH, EXPECT_PATH, CONFIG_PATH) if not p.exists()]
    if missing:
        pytest.skip(f"Missing fixture(s): {', '.join(str(p) for p in missing)}")

    frame = cv2.imread(str(FRAME_PATH))
    if frame is None:
        pytest.fail(f"Failed to load frame: {FRAME_PATH}")

    cfg = load_config(CONFIG_PATH)
    pipeline = AtlasPipeline(cfg)
    extraction = pipeline._extract_one(timestamp_s=0, frame=frame)

    expected = json.loads(EXPECT_PATH.read_text(encoding="utf-8"))
    actual = extraction.model_dump()

    # strict compare for fields you care about. Any omitted expected key is ignored.
    for key, expected_value in expected.items():
        assert actual.get(key) == expected_value, f"Mismatch for {key}: {actual.get(key)} != {expected_value}"
