from __future__ import annotations

import time
from collections.abc import Iterator

import numpy as np
from mss import mss


def iter_live_frames(sample_every_seconds: int, monitor_index: int = 1) -> Iterator[tuple[int, np.ndarray]]:
    with mss() as sct:
        mon = sct.monitors[monitor_index]
        start = time.time()
        next_capture = 0.0

        while True:
            now = time.time() - start
            if now >= next_capture:
                shot = sct.grab(mon)
                frame = np.array(shot)[:, :, :3]
                yield int(now), frame
                next_capture += sample_every_seconds
            time.sleep(0.02)
