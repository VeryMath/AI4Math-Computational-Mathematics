from __future__ import annotations

import csv
from pathlib import Path

from skills.visualization_skill.scripts.svg_utils import write_line_chart


RUN = Path(__file__).resolve().parents[1]
BASELINE_OBJECTIVE = 17.2693553575


def main() -> None:
    rows = list(csv.DictReader((RUN / "tuning" / "tuning_results.csv").open()))
    trials = [float(row["trial"]) for row in rows]
    iterations = [float(row["iterations"]) for row in rows]
    objectives = [float(row["final_objective"]) for row in rows]

    best_valid_so_far: list[float] = []
    current_best: float | None = None
    for row, iteration_count in zip(rows, iterations):
        if row["valid"] in {"1", "true", "True"}:
            current_best = iteration_count if current_best is None else min(current_best, iteration_count)
        best_valid_so_far.append(current_best if current_best is not None else iteration_count)

    figure_dir = RUN / "tuning" / "tuning_figures"
    figures = [
        write_line_chart(
            figure_dir / "tuning_iterations.svg",
            "ADMM Tuning Iterations by Trial",
            trials,
            {"iterations": iterations, "best_valid_so_far": best_valid_so_far},
            "iterations",
        ),
        write_line_chart(
            figure_dir / "tuning_objective.svg",
            "ADMM Tuning Final Objective by Trial",
            trials,
            {
                "final_objective": objectives,
                "baseline": [BASELINE_OBJECTIVE] * len(trials),
                "baseline_plus_0.1": [BASELINE_OBJECTIVE + 0.1] * len(trials),
                "baseline_minus_0.1": [BASELINE_OBJECTIVE - 0.1] * len(trials),
            },
            "objective",
        ),
    ]
    for figure in figures:
        print(figure)


if __name__ == "__main__":
    main()
