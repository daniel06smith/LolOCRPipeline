from __future__ import annotations

import json
from pathlib import Path

import typer

from atlas_ocr.insights.rules import run_rules
from atlas_ocr.io.config import load_config
from atlas_ocr.pipeline import AtlasPipeline

app = typer.Typer(add_completion=False)


@app.command()
def run(
    config: str = typer.Option(..., help="Path to YAML config."),
    source: str | None = typer.Option(None, help="Video path when source=video."),
    output: str = typer.Option("artifacts/extraction.json", help="Output JSON path."),
    max_samples: int | None = typer.Option(None, help="Cap processed samples for debugging."),
) -> None:
    cfg = load_config(config)
    pipeline = AtlasPipeline(cfg)
    frames = pipeline.run(source_path=source, max_samples=max_samples)
    insights = run_rules(frames)

    payload = {
        "frames": [f.model_dump() for f in frames],
        "insights": [i.model_dump() for i in insights],
    }

    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    typer.echo(f"Wrote {len(frames)} samples and {len(insights)} insights to {out_path}")


if __name__ == "__main__":
    app()
