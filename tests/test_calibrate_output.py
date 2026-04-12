from pathlib import Path

from atlas_ocr.calibrate import _write_landmarks


def test_write_landmarks_yaml(tmp_path: Path) -> None:
    out = tmp_path / "landmarks.yaml"
    payload = {"source": "video", "profile": {"resolution": [1920, 1080]}}
    _write_landmarks(payload, out)
    text = out.read_text(encoding="utf-8")
    assert "source: video" in text


def test_write_landmarks_json(tmp_path: Path) -> None:
    out = tmp_path / "landmarks.json"
    payload = {"source": "video"}
    _write_landmarks(payload, out)
    text = out.read_text(encoding="utf-8")
    assert '"source": "video"' in text
