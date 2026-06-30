from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path


DEPENDENCY_FILES = ["requirements.txt", "pyproject.toml", "setup.py", "environment.yml", "setup.cfg"]


def create_deployment_plan(source: Path | str, run_role: str = "controller") -> dict:
    source = Path(source)
    dependency_files = [name for name in DEPENDENCY_FILES if (source / name).exists()]
    if run_role == "controller":
        strategy = "shared_conda"
        environment_name = "ai4math"
        prefix = "conda run -n ai4math"
        install_action = 'conda run -n ai4math python -m pip install -e ".[dev]"'
    else:
        strategy = "isolated_python_env_if_approved"
        environment_name = "outputs/{run_id}/.venv"
        prefix = "{venv}/bin/python"
        install_action = "install declared dependency files only after approval"
    return {
        "run_role": run_role,
        "source": str(source),
        "strategy": strategy,
        "environment_name": environment_name,
        "recommended_command_prefix": prefix,
        "dependency_files": dependency_files,
        "install_action": install_action,
        "python_executable": sys.executable,
        "python_version": sys.version.split()[0],
        "os": platform.platform(),
        "warnings": [] if dependency_files else ["No dependency file detected."],
    }


def write_environment_report(run: Path | str, plan: dict) -> Path:
    run = Path(run)
    run.mkdir(parents=True, exist_ok=True)
    (run / "deployment_plan.json").write_text(json.dumps(plan, indent=2))
    body = f"""# Environment Report

## Deployment Plan

- role: {plan.get('run_role')}
- strategy: {plan.get('strategy')}
- environment: {plan.get('environment_name')}
- command prefix: `{plan.get('recommended_command_prefix')}`
- install action: {plan.get('install_action')}

## Runtime

- Python: {plan.get('python_version')}
- executable: `{plan.get('python_executable')}`
- OS: {plan.get('os')}

## Dependencies

- detected files: {plan.get('dependency_files', [])}
- warnings: {plan.get('warnings', [])}
"""
    path = run / "environment_report.md"
    path.write_text(body)
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--run-role", default="controller", choices=["controller", "reproduction"])
    args = parser.parse_args()
    plan = create_deployment_plan(args.source, args.run_role)
    write_environment_report(args.out, plan)
    print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()
