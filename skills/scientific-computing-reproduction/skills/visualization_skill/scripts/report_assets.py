from __future__ import annotations

import argparse
import json
from pathlib import Path


def write_visualization_report(run: Path | str, figures: list[Path | str]) -> Path:
    run = Path(run)
    run.mkdir(parents=True, exist_ok=True)
    body = ["# Visualization Report", ""]
    if not figures:
        body.append("No figures were generated.")
    for figure in figures:
        figure = Path(figure)
        rel = figure.relative_to(run) if figure.is_absolute() and run in figure.parents else figure
        body.append(f"- `{rel}`")
        body.append("")
        body.append(f"![{figure.stem}]({rel})")
        body.append("")
    path = run / "visualization_report.md"
    path.write_text("\n".join(body))
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    parser.add_argument("--figures", nargs="*", default=[])
    args = parser.parse_args()
    print(write_visualization_report(args.run, args.figures))


if __name__ == "__main__":
    main()
