from __future__ import annotations

import csv
from pathlib import Path
import sys

import numpy as np


RUN_DIR = Path("/Users/conanxu/Scientific Computing Reproduction & Auto-Tuning /outputs/admm_bhushan23_20260511")
SOURCE_DIR = RUN_DIR / "source" / "ADMM"
sys.path.insert(0, str(SOURCE_DIR))

from admm import ADMM


def main() -> None:
    np.random.seed(0)
    num_iterations = 20
    n_samples = 100
    n_features = 20

    a_matrix = np.random.randn(n_samples, n_features)
    b_vector = np.random.randn(n_samples, 1)
    solver = ADMM(a_matrix, b_vector, parallel=False)

    objectives = [float(solver.LassoObjective())]
    for _ in range(num_iterations):
        solver.step()
        objectives.append(float(solver.LassoObjective()))

    out = RUN_DIR / "results" / "lasso_objective.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["iteration", "objective"])
        for iteration, value in enumerate(objectives):
            writer.writerow([iteration, value])

    print("initial_objective", objectives[0])
    print("final_objective", objectives[-1])
    print("min_objective", min(objectives))
    print("wrote", out)


if __name__ == "__main__":
    main()
