from atlas_ocr.io.config import load_config


def test_load_config_example() -> None:
    cfg = load_config("configs/example.yaml")
    assert cfg.sample_every_seconds == 5
    assert cfg.profile.hud.timer.w > 0
