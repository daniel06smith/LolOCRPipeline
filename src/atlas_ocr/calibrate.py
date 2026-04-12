from __future__ import annotations

import json
from pathlib import Path

import cv2
import yaml


TARGETS = ["timer", "blue_kills", "red_kills", "blue_gold", "red_gold", "minimap"]


def _write_landmarks(payload: dict, out_path: Path) -> None:
    if out_path.suffix.lower() in {".yaml", ".yml"}:
        out_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    else:
        out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Interactive ROI calibration for Atlas HUD landmarks.")
    parser.add_argument("image", help="Path to screenshot/frame from replay spectator HUD")
    parser.add_argument("--out", default="configs/landmarks.json", help="Output path (.json or .yaml)")
    args = parser.parse_args()

    frame = cv2.imread(args.image)
    if frame is None:
        raise RuntimeError(f"Could not load image: {args.image}")

    rois: dict[str, dict[str, int]] = {}
    for target in TARGETS:
        xywh = cv2.selectROI(f"Select ROI: {target}", frame, showCrosshair=True)
        cv2.destroyWindow(f"Select ROI: {target}")
        x, y, w, h = [int(v) for v in xywh]
        rois[target] = {"x": x, "y": y, "w": w, "h": h}

    out = {
        "sample_every_seconds": 5,
        "source": "video",
        "profile": {
            "resolution": [int(frame.shape[1]), int(frame.shape[0])],
            "ui_scale": 1.0,
            "side": "spectator",
            "hud": rois,
        },
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    _write_landmarks(out, out_path)
    print(f"Saved landmark template to {out_path}")


if __name__ == "__main__":
    main()
