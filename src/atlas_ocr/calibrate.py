from __future__ import annotations

import json
from pathlib import Path

import cv2


TARGETS = ["timer", "blue_kills", "red_kills", "blue_gold", "red_gold", "minimap"]


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Interactive ROI calibration for Atlas HUD landmarks.")
    parser.add_argument("image", help="Path to screenshot/frame from replay spectator HUD")
    parser.add_argument("--out", default="configs/landmarks.json", help="Output path")
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
        "resolution": [int(frame.shape[1]), int(frame.shape[0])],
        "ui_scale": 1.0,
        "side": "spectator",
        "hud": rois,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Saved landmark template to {out_path}")


if __name__ == "__main__":
    main()
