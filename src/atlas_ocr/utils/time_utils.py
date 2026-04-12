from __future__ import annotations

import re


def parse_game_time(text: str) -> int | None:
    cleaned = re.sub(r"[^0-9:]", "", text)
    if ":" not in cleaned:
        return None
    parts = cleaned.split(":")
    if len(parts) != 2:
        return None
    mm, ss = parts
    if not (mm.isdigit() and ss.isdigit()):
        return None
    return int(mm) * 60 + int(ss)


def parse_int(text: str) -> int | None:
    digits = re.sub(r"[^0-9]", "", text)
    return int(digits) if digits else None
