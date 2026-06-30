from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from pathlib import Path

import yaml

from skills.auto_tuning_skill.scripts.grid_search import generate_grid
from skills.auto_tuning_skill.scripts.parameter_space import load_parameter_space
from skills.auto_tuning_skill.scripts.random_search import generate_random
from skills.auto_tuning_skill.scripts.result_analyzer import choose_best
from skills.failure_diagnosis_skill.scripts.failure_classifier import write_repair_plan
from skills.human_review_skill.scripts.approval_gate import check_approval_gate


def _param_args(params: dict) -> list[str]:
    args = []
    for name, value in params.items():
        args.extend([f"--{name.replace('_', '-')}", str(value)])
    return args


def _load_task_settings(path: Path) -> dict:
    data = yaml.safe_load(path.read_text())
    return data if isinstance(data, dict) else {}


def run_experiments(
    source: Path | str,
    param_space_file: Path | str,
    budget: int,
    out: Path | str,
    method: str | None = None,
    require_approval: str | None = None,
    auto_approve_low_risk: bool = False,
) -> list[dict]:
    source = Path(source)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    log_path = out / "tuning.log"
    log_path.write_text(
        f"source={source}\nparam_space={param_space_file}\nbudget={budget}\nmethod={method or 'auto'}\n"
    )
    if require_approval:
        gate = check_approval_gate(out, require_approval, risk_level="low", auto_approve_low_risk=auto_approve_low_risk)
        if not gate["allowed"]:
            row = {
                "status": "blocked",
                "success": False,
                "error": gate["reason"],
                "approval_gate": gate,
            }
            with log_path.open("a") as handle:
                handle.write(f"blocked={gate['reason']}\n")
            write_repair_plan(out, "missing_human_approval", gate["reason"], "tuning experiments")
            return [row]
    (out / "trial_logs").mkdir(exist_ok=True)
    space = load_parameter_space(param_space_file)
    settings = _load_task_settings(Path(param_space_file))
    method = method or settings.get("tuning", {}).get("method", "random_search")
    experiments = generate_grid(space, budget) if method == "grid_search" else generate_random(space, budget, random_seed=0)

    rows: list[dict] = []
    for index, params in enumerate(experiments, start=1):
        trial_dir = out / "trial_logs" / f"trial_{index:03d}"
        trial_dir.mkdir(parents=True, exist_ok=True)
        command = [sys.executable, "main.py", *_param_args(params), "--output-dir", str(trial_dir)]
        started = time.perf_counter()
        try:
            proc = subprocess.run(command, cwd=source, capture_output=True, text=True, timeout=300, check=False)
            runtime = time.perf_counter() - started
            (trial_dir / "run_log.txt").write_text(f"COMMAND: {' '.join(command)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}\n")
            metrics_path = trial_dir / "metrics.json"
            metrics = json.loads(metrics_path.read_text()) if metrics_path.exists() else {}
            row = {"trial": index, **params, **metrics, "exit_code": proc.returncode, "trial_runtime": runtime}
            if proc.returncode != 0:
                row["success"] = False
                write_repair_plan(out, proc.stderr, proc.stdout, " ".join(command))
        except subprocess.TimeoutExpired as exc:
            row = {"trial": index, **params, "success": False, "failure_type": "timeout", "runtime": 300.0}
            write_repair_plan(out, "timeout", str(exc), " ".join(command))
        rows.append(row)
        with log_path.open("a") as handle:
            handle.write(json.dumps({"trial": index, "params": params, "status": row.get("status", "done"), "success": row.get("success")}) + "\n")

    fieldnames = sorted({key for row in rows for key in row})
    with (out / "tuning_results.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    best = choose_best(rows)
    (out / "best_parameters.json").write_text(json.dumps(best, indent=2))
    with log_path.open("a") as handle:
        handle.write(f"best_parameters={json.dumps(best, sort_keys=True)}\n")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--param-space", required=True)
    parser.add_argument("--budget", type=int, default=20)
    parser.add_argument("--out", required=True)
    parser.add_argument("--method")
    parser.add_argument("--require-approval", default=None)
    parser.add_argument("--auto-approve-low-risk", action="store_true")
    args = parser.parse_args()
    rows = run_experiments(
        args.source,
        args.param_space,
        args.budget,
        args.out,
        args.method,
        require_approval=args.require_approval,
        auto_approve_low_risk=args.auto_approve_low_risk,
    )
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
