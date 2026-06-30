from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _float_or_none(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def choose_best(rows: list[dict], primary_metric: str = "runtime", direction: str = "minimize", feasibility_threshold: float | None = 1e-4) -> dict:
    candidates = [row for row in rows if str(row.get("success", True)).lower() in {"true", "1", "yes"}]
    if feasibility_threshold is not None:
        feasible = []
        for row in candidates:
            residuals = [_float_or_none(row.get("primal_residual")), _float_or_none(row.get("dual_residual")), _float_or_none(row.get("objective_gap"))]
            present = [value for value in residuals if value is not None]
            if not present or all(value <= feasibility_threshold for value in present):
                feasible.append(row)
        if feasible:
            candidates = feasible
    reverse = direction == "maximize"
    return sorted(candidates, key=lambda row: _float_or_none(row.get(primary_metric)) or float("inf"), reverse=reverse)[0] if candidates else {}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--primary-metric", default="runtime")
    parser.add_argument("--direction", default="minimize")
    args = parser.parse_args()
    rows = list(csv.DictReader(Path(args.csv).open()))
    print(json.dumps(choose_best(rows, args.primary_metric, args.direction), indent=2))


if __name__ == "__main__":
    main()
