from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from skills.visualization_skill.scripts.svg_utils import write_line_chart


def _float(row: dict, key: str, default: float = 0.0) -> float:
    try:
        return float(row.get(key, default))
    except (TypeError, ValueError):
        return default


def plot_tuning(tuning_csv: Path | str, out: Path | str, metric: str = "runtime") -> list[Path]:
    tuning_csv = Path(tuning_csv)
    out = Path(out)
    rows = list(csv.DictReader(tuning_csv.open()))
    if not rows:
        return []
    trials = [_float(row, "trial", index) for index, row in enumerate(rows, start=1)]
    metric_values = [_float(row, metric, 0.0) for row in rows]
    best = []
    current = None
    for value in metric_values:
        current = value if current is None else min(current, value)
        best.append(current)
    figure_dir = out / "tuning" / "tuning_figures"
    figures = [
        write_line_chart(figure_dir / "tuning_runtime.svg", "Tuning Runtime by Trial", trials, {metric: metric_values}, metric),
        write_line_chart(figure_dir / "tuning_best_so_far.svg", "Best Feasible Metric So Far", trials, {"best_so_far": best}, metric),
    ]
    return figures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tuning-results", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--metric", default="runtime")
    args = parser.parse_args()
    print(json.dumps([str(path) for path in plot_tuning(args.tuning_results, args.out, args.metric)], indent=2))


if __name__ == "__main__":
    main()
