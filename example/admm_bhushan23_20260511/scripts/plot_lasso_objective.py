from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


RUN_DIR = Path(__file__).resolve().parents[1]


def main() -> None:
    csv_path = RUN_DIR / "results" / "lasso_objective.csv"
    fig_path = RUN_DIR / "figures" / "lasso_objective.png"

    rows = list(csv.DictReader(csv_path.open()))
    iterations = [int(row["iteration"]) for row in rows]
    objectives = [float(row["objective"]) for row in rows]

    fig_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(7, 4.2))
    plt.plot(iterations, objectives, marker="o", linewidth=1.8, markersize=4)
    plt.xlabel("Iteration")
    plt.ylabel("Lasso objective")
    plt.title("bhushan23/ADMM minimal Lasso objective trace")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=160)
    print(fig_path)


if __name__ == "__main__":
    main()
