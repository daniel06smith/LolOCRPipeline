from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ROI(BaseModel):
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    w: int = Field(gt=0)
    h: int = Field(gt=0)


class HUDLandmarks(BaseModel):
    timer: ROI
    blue_kills: ROI
    red_kills: ROI
    blue_gold: ROI
    red_gold: ROI
    minimap: ROI


class ProfileConfig(BaseModel):
    resolution: tuple[int, int]
    ui_scale: float = Field(gt=0)
    side: Literal["blue", "red", "spectator"] = "spectator"
    hud: HUDLandmarks


class PipelineConfig(BaseModel):
    sample_every_seconds: int = Field(default=5, ge=1)
    source: Literal["video", "live"]
    tesseract_cmd: str | None = None
    profile: ProfileConfig
    tracked_player: str | None = None


class FrameExtraction(BaseModel):
    timestamp_s: int
    game_time_s: int | None = None
    blue_kills: int | None = None
    red_kills: int | None = None
    blue_gold: int | None = None
    red_gold: int | None = None


class Insight(BaseModel):
    kind: str
    severity: Literal["low", "medium", "high"]
    timestamp_s: int
    message: str
