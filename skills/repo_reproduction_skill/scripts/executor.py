from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

from skills.failure_diagnosis_skill.scripts.failure_classifier import write_repair_plan
from skills.human_review_skill.scripts.approval_gate import check_approval_gate


def _resolve_command(command: list[str]) -> list[str]:
    if command and command[0] == "python" and shutil.which("python") is None:
        return [sys.executable, *command[1:]]
    return command


def execute_plans(
    plans: list[dict],
    out: Path | str,
    require_approval: str | None = None,
    auto_approve_low_risk: bool = False,
) -> list[dict]:
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    log_path = out / "run_log.txt"
    jsonl_path = out / "execution_log.jsonl"
    runtime_log_path = out / "logs" / "run.log"
    results = []

    with log_path.open("a") as log_file, jsonl_path.open("a") as jsonl:
        for index, plan in enumerate(plans, start=1):
            started = time.perf_counter()
            command = _resolve_command(plan["command"])
            gate = None
            if require_approval:
                gate = check_approval_gate(
                    out,
                    require_approval,
                    risk_level=plan.get("risk_level", "low"),
                    auto_approve_low_risk=auto_approve_low_risk,
                )
            if gate and not gate["allowed"]:
                result = {
                    "index": index,
                    "command": command,
                    "status": "blocked",
                    "exit_code": None,
                    "runtime": 0.0,
                    "error": gate["reason"],
                    "approval_gate": gate,
                }
                write_repair_plan(out, "missing_human_approval", gate["reason"], " ".join(command))
            elif plan.get("risk_level") == "high":
                result = {"index": index, "command": command, "status": "failed", "exit_code": None, "runtime": 0.0, "error": "high_risk_command"}
                write_repair_plan(out, "high_risk_command", "Command marked high risk.", " ".join(command))
            else:
                try:
                    proc = subprocess.run(
                        command,
                        cwd=plan["working_dir"],
                        capture_output=True,
                        text=True,
                        timeout=int(plan.get("timeout_seconds", 300)),
                        check=False,
                    )
                    runtime = time.perf_counter() - started
                    status = "success" if proc.returncode == 0 else "failed"
                    result = {
                        "index": index,
                        "command": command,
                        "status": status,
                        "exit_code": proc.returncode,
                        "runtime": runtime,
                        "stdout": proc.stdout[-4000:],
                        "stderr": proc.stderr[-4000:],
                    }
                    if status != "success":
                        write_repair_plan(out, proc.stderr, proc.stdout, " ".join(command))
                except subprocess.TimeoutExpired as exc:
                    runtime = time.perf_counter() - started
                    result = {
                        "index": index,
                        "command": command,
                        "status": "timeout",
                        "exit_code": None,
                        "runtime": runtime,
                        "stdout": (exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
                        "stderr": (exc.stderr or "")[-4000:] if isinstance(exc.stderr, str) else "",
                    }
                    write_repair_plan(out, "timeout", result["stdout"], " ".join(command))
            log_file.write(f"COMMAND {index}: {' '.join(command)}\nSTATUS: {result['status']}\n")
            log_file.write(f"STDOUT:\n{result.get('stdout', '')}\nSTDERR:\n{result.get('stderr', '')}\n\n")
            if plan.get("runtime") == "MATLAB":
                runtime_log_path.parent.mkdir(parents=True, exist_ok=True)
                with runtime_log_path.open("a") as runtime_log:
                    runtime_log.write(f"COMMAND {index}: {' '.join(command)}\nSTATUS: {result['status']}\n")
                    runtime_log.write(f"STDOUT:\n{result.get('stdout', '')}\nSTDERR:\n{result.get('stderr', '')}\n\n")
            jsonl.write(json.dumps(result) + "\n")
            results.append(result)
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--require-approval", default=None)
    parser.add_argument("--auto-approve-low-risk", action="store_true")
    args = parser.parse_args()
    plans = json.loads(Path(args.plan).read_text())
    results = execute_plans(
        plans,
        args.out,
        require_approval=args.require_approval,
        auto_approve_low_risk=args.auto_approve_low_risk,
    )
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
