from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path

from skills.matlab_runtime_skill.scripts.matlab_runtime import make_matlab_run_plans


HIGH_RISK_TOKENS = ("sudo", "rm -rf", "curl", "wget", "| bash", "mkfs", "chmod 777")


def risk_level(command: str) -> str:
    lowered = command.lower()
    return "high" if any(token in lowered for token in HIGH_RISK_TOKENS) else "low"


def _python_cmd(script: str) -> list[str]:
    return [sys.executable, script]


def _is_matlab_command(command: str) -> bool:
    return bool(command.strip().lower().startswith(("matlab ", "octave ")))


def make_run_plans(analysis: dict) -> list[dict]:
    source = Path(analysis["repo_path"])
    plans: list[dict] = []

    for command in analysis.get("readme_commands", []):
        if _is_matlab_command(command):
            continue
        plans.append(
            {
                "command": shlex.split(command),
                "working_dir": str(source),
                "reason": "README provides an explicit run command.",
                "expected_outputs": ["stdout", "stderr", "result files"],
                "timeout_seconds": 300,
                "risk_level": risk_level(command),
            }
        )

    plans.extend(make_matlab_run_plans(analysis))

    priority = ["examples/", "demo.py", "main.py", "tests/", "scripts/", "benchmarks/"]
    entrypoints = analysis.get("candidate_entrypoints", [])
    for item in priority:
        if item not in entrypoints:
            continue
        if item.endswith(".py"):
            command = _python_cmd(item)
            reason = f"Detected standard Python entrypoint {item}."
        elif item == "tests/":
            command = ["pytest", "tests"]
            reason = "Detected tests directory."
        else:
            scripts = sorted((source / item.rstrip("/")).glob("*.py"))
            if not scripts:
                continue
            command = _python_cmd(str(scripts[0].relative_to(source)))
            reason = f"Detected Python script under {item}."
        plans.append(
            {
                "command": command,
                "working_dir": str(source),
                "reason": reason,
                "expected_outputs": ["metrics.json", "convergence.csv", "stdout", "stderr"],
                "timeout_seconds": 300,
                "risk_level": risk_level(" ".join(command)),
            }
        )

    return plans


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()
    analysis = json.loads(Path(args.analysis).read_text())
    plans = make_run_plans(analysis)
    print(json.dumps(plans, indent=2))
    if args.out:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "run_plan.json").write_text(json.dumps(plans, indent=2))


if __name__ == "__main__":
    main()
