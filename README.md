# Atlas Replay OCR Pipeline (MVP)

Modular OCR/CV extraction pipeline for League of Legends replay coaching.

## What this MVP does

- Supports **video input** (`.mp4`) and **live desktop capture**.
- Extracts key HUD signals using OCR:
  - game timer
  - blue/red kills
  - blue/red team gold
- Produces structured JSON timeline (time-bucketed samples).
- Runs first-pass coaching insight rules:
  - objective setup risk proxy
  - overextension/death spike proxy

## Stack

- Python 3.11
- `uv` for dependency management
- OpenCV + NumPy
- Tesseract (via `pytesseract`)
- Typer CLI

## Quick start

```bash
uv venv
uv pip install -e .[dev]
```

> On Windows, install Tesseract separately and set `tesseract_cmd` in config.

## Calibrate HUD coordinates

Take one spectator HUD screenshot at your target resolution/UI scale.

```bash
uv run atlas-calibrate path/to/frame.png --out configs/landmarks.json
```

This creates ROI JSON with `[x, y, w, h]` values. Keep crops tight.

## Config

Use `configs/example.yaml` as a base.

Key settings:
- `sample_every_seconds`: extraction interval for time-bucketing (default 5)
- `source`: `video` or `live`
- `profile.hud.*`: ROI coordinates

## Run pipeline (video)

```bash
uv run atlas-ocr run \
  --config configs/example.yaml \
  --source path/to/replay_capture.mp4 \
  --output artifacts/extraction.json
```

## Run pipeline (live capture)

Set `source: live` in config, then:

```bash
uv run atlas-ocr run --config configs/example.yaml --output artifacts/extraction.json
```

(Stop with Ctrl+C after desired capture duration.)


## Test with a single sample frame

1. Save one replay screenshot/frame as `tests/fixtures/sample_frame.png`.
2. Create ROIs for that frame:
   ```bash
   uv run atlas-calibrate tests/fixtures/sample_frame.png --out tests/fixtures/sample_frame_config.yaml
   ```
   (You can rename JSON->YAML format manually, or create the YAML directly using `configs/example.yaml` as template.)
3. Create `tests/fixtures/sample_frame_expected.json` with values you expect from that frame.
4. Run the integration test:
   ```bash
   uv run pytest -m integration -k sample_frame -q
   ```

The test skips automatically if fixture files are missing.

## Project layout

```text
src/atlas_ocr/
  capture/      # video/live frame sources
  cv/           # OCR preprocessing + OCR engine
  insights/     # rule-based insight layer
  io/           # config loading
  models/       # pydantic schemas
  utils/        # parsing helpers
  cli.py        # command-line entrypoint
  calibrate.py  # interactive ROI selection tool
```

## Next recommended steps

1. Add minimap entity detection (champion/ward/objective CV models).
2. Add side-aware/mirrored profiles for blue vs red POV.
3. Add event inference layer (death/objective/tower timelines).
4. Expand insight rules with player-level context.
