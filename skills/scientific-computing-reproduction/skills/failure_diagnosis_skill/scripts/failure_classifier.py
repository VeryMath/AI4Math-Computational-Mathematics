from __future__ import annotations

import argparse
import json
from pathlib import Path


def classify_failure(stderr: str, stdout: str = "") -> dict:
    text = f"{stderr}\n{stdout}".lower()
    if "modulenotfounderror" in text or "no module named" in text:
        kind = "dependency_error"
    elif "version conflict" in text or "resolutionimpossible" in text:
        kind = "version_conflict"
    elif "no such file" in text or "file not found" in text:
        kind = "missing_data"
    elif "can't open file" in text or "missing_entrypoint" in text:
        kind = "missing_entrypoint"
    elif "timeout" in text or "timed out" in text:
        kind = "timeout"
    elif "nan" in text or "diverge" in text or "overflow" in text:
        kind = "numerical_failure"
    elif "permission denied" in text:
        kind = "permission_error"
    elif "high_risk_command" in text or "sudo" in text or "rm -rf" in text:
        kind = "high_risk_command"
    elif "readme" in text and "unclear" in text:
        kind = "readme_unclear"
    else:
        kind = "unknown_error"
    high = kind in {"high_risk_command", "version_conflict", "missing_data", "permission_error", "unknown_error"}
    return {
        "failure_type": kind,
        "summary": text[:500],
        "risk_level": "high" if high else "medium",
        "requires_human_confirmation": high,
    }


def write_repair_plan(out: Path | str, stderr: str, stdout: str = "", command: str = "") -> Path | None:
    """Write repair_plan.md only if source/dependency/entrypoint/data changes are needed.

    Returns None if no repair is needed.
    """
    out = Path(out)
    result = classify_failure(stderr, stdout)
    requires_repair = result["requires_human_confirmation"]
    if not requires_repair:
        return None
    out.mkdir(parents=True, exist_ok=True)
    body = f"""# Repair Plan

## Failure Summary
{result['summary'] or 'No stderr/stdout evidence was captured.'}

## Failure Type
{result['failure_type']}

## Evidence
Command: `{command}`
See `logs/run.log` for full stdout/stderr.

## Proposed Minimal Repair
Review dependencies, entrypoints, data availability, and numerical settings.

## Files To Modify
{{files_to_modify}}

## What Will Not Be Changed
{{what_will_not_be_changed}}

## Patch / Rollback Plan
{{patch_rollback_plan}}

Reply with approve / revise / reject / skip.
"""
    path = out / "repair_plan.md"
    path.write_text(body)
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stderr", default="")
    parser.add_argument("--stdout", default="")
    parser.add_argument("--out")
    args = parser.parse_args()
    result = classify_failure(args.stderr, args.stdout)
    if args.out:
        write_repair_plan(args.out, args.stderr, args.stdout)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
