from atlas_ocr.utils.time_utils import parse_game_time, parse_int


def test_parse_game_time() -> None:
    assert parse_game_time("12:34") == 754
    assert parse_game_time("abc") is None


def test_parse_int() -> None:
    assert parse_int("1,234") == 1234
    assert parse_int("--") is None
