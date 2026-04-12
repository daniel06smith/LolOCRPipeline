from __future__ import annotations

from pathlib import Path

import yaml

from atlas_ocr.models.schema import PipelineConfig


def load_config(path: str | Path) -> PipelineConfig:
    with Path(path).open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return PipelineConfig.model_validate(raw)
