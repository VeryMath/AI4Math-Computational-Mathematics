from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from skills.visualization_skill.scripts.svg_utils import write_line_chart


def _to_float(row: dict, key: str) -> float | None:
    try:
        return float(row[key])
    except (KeyError, TypeError, ValueError):
        return None


def _first_float(row: dict, keys: list[str]) -> float | None:
    for key in keys:
        value = _to_float(row, key)
        if value is not None:
            return value
    return None


def plot_convergence(convergence_csv: Path | str, out: Path | str) -> list[Path]:
    convergence_csv = Path(convergence_csv)
    out = Path(out)
    rows = list(csv.DictReader(convergence_csv.open()))
    if not rows:
        return []
    x_values = [_first_float(row, ["iteration", "iter"]) or index for index, row in enumerate(rows, start=1)]
    figures = []
    objective = [_first_float(row, ["objective_value", "objective"]) for row in rows]
    objective_values = [value for value in objective if value is not None]
    if len(objective_values) == len(rows):
        figures.append(write_line_chart(out / "figures" / "convergence_objective.svg", "Objective Convergence", x_values, {"objective": objective_values}, "objective"))
    residual_series = {}
    for key in ["primal_residual", "dual_residual", "objective_gap", "step_norm"]:
        values = [_to_float(row, key) for row in rows]
        if all(value is not None for value in values):
            residual_series[key] = [float(value) for value in values]
    if residual_series:
        figures.append(write_line_chart(out / "figures" / "convergence_residuals.svg", "Residual / Gap Convergence", x_values, residual_series, "residual / gap"))
    return figures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--convergence", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    print(json.dumps([str(path) for path in plot_convergence(args.convergence, args.out)], indent=2))


if __name__ == "__main__":
    main()
