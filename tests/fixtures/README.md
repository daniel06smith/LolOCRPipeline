# Sample Frame Fixtures

Drop your local files here (not committed with real game data):

- `sample_frame.png` — one screenshot/frame from replay spectator HUD.
- `sample_frame_config.yaml` — ROI config aligned to this frame's resolution/UI scale.
- `sample_frame_expected.json` — expected extracted values.

Example expected JSON:

```json
{
  "game_time_s": 754,
  "blue_kills": 8,
  "red_kills": 6,
  "blue_gold": 25400,
  "red_gold": 24800
}
```

Run:

```bash
uv run pytest -m integration -k sample_frame -q
```
