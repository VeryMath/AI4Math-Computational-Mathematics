from __future__ import annotations

import argparse
import json
from pathlib import Path


CHECKPOINTS = {
    "task_understanding": ("01_task_understanding.md", "Task Understanding Checkpoint"),
    "run_plan": ("02_run_plan_review.md", "Run Plan Checkpoint"),
    "failure_fix": ("03_failure_fix_review.md", "Failure Fix Checkpoint"),
    "tuning_plan": ("04_tuning_plan_review.md", "Tuning Plan Checkpoint"),
    "final": ("05_final_review.md", "Final Review Checkpoint"),
    "algorithm_match": ("06_algorithm_match_review.md", "Algorithm Match Review"),
}


def _list_value(value: object) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value) if value else "not identified"
    return str(value) if value not in (None, "") else "not identified"


def _task_understanding(context: dict) -> str:
    fields = ["domain", "algorithm_family", "problem_type", "expected_goal", "metrics", "uncertainties"]
    lines = ["## Task Interpretation"]
    lines.extend(f"- {field}: {_list_value(context.get(field))}" for field in fields)
    return "\n".join(lines)


def _run_plan(context: dict) -> str:
    lines = ["## Candidate Commands"]
    plans = context.get("plans", [])
    if not plans:
        lines.append("- No candidate commands identified yet.")
    for index, plan in enumerate(plans, start=1):
        command = plan.get("command", [])
        command_text = " ".join(command) if isinstance(command, list) else str(command)
        lines.extend(
            [
                f"{index}. `{command_text}`",
                f"   - reason: {_list_value(plan.get('reason'))}",
                f"   - risk: {_list_value(plan.get('risk_level'))}",
                f"   - timeout_seconds: {_list_value(plan.get('timeout_seconds'))}",
                f"   - expected_outputs: {_list_value(plan.get('expected_outputs'))}",
            ]
        )
    return "\n".join(lines)


def _failure_fix(context: dict) -> str:
    fields = ["failure_type", "evidence", "proposed_fix", "risk_level", "requires_source_change"]
    lines = ["## Failure Diagnosis"]
    lines.extend(f"- {field}: {_list_value(context.get(field))}" for field in fields)
    return "\n".join(lines)


def _tuning_plan(context: dict) -> str:
    fields = ["method", "budget", "metric", "constraints", "parameter_space", "stop_condition"]
    lines = ["## Tuning Proposal"]
    lines.extend(f"- {field}: {_list_value(context.get(field))}" for field in fields)
    return "\n".join(lines)


def _final_review(context: dict) -> str:
    fields = ["status", "evidence", "metrics", "figures", "limitations", "conclusion"]
    lines = ["## Reproduction Conclusion"]
    lines.extend(f"- {field}: {_list_value(context.get(field))}" for field in fields)
    return "\n".join(lines)


def _algorithm_match(context: dict) -> str:
    lines = ["## External Algorithm Candidates"]
    candidates = context.get("candidates", [])
    if not candidates:
        lines.append("- No external candidates recorded.")
    for index, candidate in enumerate(candidates, start=1):
        name = candidate.get("name") or candidate.get("title") or f"candidate {index}"
        lines.extend(
            [
                f"{index}. {name}",
                f"   - source: {_list_value(candidate.get('source'))}",
                f"   - match_evidence: {_list_value(candidate.get('match_evidence'))}",
                f"   - code_available: {_list_value(candidate.get('code_available'))}",
            ]
        )
    return "\n".join(lines)


SECTION_RENDERERS = {
    "task_understanding": _task_understanding,
    "run_plan": _run_plan,
    "failure_fix": _failure_fix,
    "tuning_plan": _tuning_plan,
    "final": _final_review,
    "algorithm_match": _algorithm_match,
}


def write_checkpoint(run: Path | str, checkpoint_type: str, context: dict | None = None) -> Path:
    """Write a legacy numbered checkpoint file (debug-only).

    This function is retained for debug/legacy use only. The default workflow
    does not write numbered checkpoint files. Use compact artifacts
    (plan.md, repair_plan.md, tuning/tuning_plan.md) instead.
    """
    run = Path(run)
    context = context or {}
    directory = run / "checkpoints"
    directory.mkdir(parents=True, exist_ok=True)
    filename, title = CHECKPOINTS[checkpoint_type]
    rendered = SECTION_RENDERERS[checkpoint_type](context)
    body = f"""# {title}

## Decision Needed
Reply with exactly one decision: `approve`, `revise`, `reject`, or `skip`.

{rendered}
"""
    path = directory / filename
    path.write_text(body)
    return path


def write_all_checkpoints(run: Path | str, context: dict | None = None) -> list[Path]:
    return [write_checkpoint(run, key, context) for key in CHECKPOINTS]


def main() -> None:
    parser = argparse.ArgumentParser(description="Legacy checkpoint writer (debug-only). Default workflow uses compact artifacts instead.")
    parser.add_argument("--type", choices=list(CHECKPOINTS) + ["all"], required=True)
    parser.add_argument("--run", required=True)
    parser.add_argument("--context-json", default="{}")
    args = parser.parse_args()
    context = json.loads(args.context_json)
    paths = write_all_checkpoints(args.run, context) if args.type == "all" else [write_checkpoint(args.run, args.type, context)]
    print(json.dumps([str(path) for path in paths], indent=2))


if __name__ == "__main__":
    main()
