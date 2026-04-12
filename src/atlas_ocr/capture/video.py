from __future__ import annotations

from collections.abc import Iterator

import cv2
import numpy as np


def iter_video_frames(path: str, sample_every_seconds: int) -> Iterator[tuple[int, np.ndarray]]:
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video: {path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    stride = max(1, int(round(fps * sample_every_seconds)))

    frame_idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if frame_idx % stride == 0:
            ts = int(frame_idx / fps)
            yield ts, frame
        frame_idx += 1

    cap.release()
