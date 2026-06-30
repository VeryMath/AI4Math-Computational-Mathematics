from __future__ import annotations

import argparse
import csv
import json
import platform
import subprocess
import sys
from pathlib import Path


def _read_json(path: Path):
    return json.loads(path.read_text()) if path.exists() else None


def _first_existing(*paths: Path) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def _pip_freeze() -> str:
    try:
        proc = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True, timeout=60, check=False)
        return proc.stdout
    except subprocess.TimeoutExpired:
        return "pip freeze timed out"


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _format_commands(executions: list[dict]) -> str:
    if not executions:
        return "No commands recorded."
    lines = []
    for item in executions:
        command = item.get("command", [])
        command_text = " ".join(command) if isinstance(command, list) else str(command)
        lines.append(
            f"- `{command_text}` -> {item.get('status', 'unknown')}"
            f" (exit_code={item.get('exit_code')}, runtime={item.get('runtime', 0):.3f}s)"
        )
    return "\n".join(lines)


def _status(executions: list[dict]) -> str:
    if not executions:
        return "not run"
    statuses = {item.get("status") for item in executions}
    if statuses == {"success"}:
        return "success"
    if "success" in statuses:
        return "partial"
    return "failed"


def _source_summary(run: Path) -> str:
    analysis = _read_json(run / "repo_analysis.json") or {}
    source = analysis.get("repo_path", "not recorded")
    language = analysis.get("language", "unknown")
    algorithms = analysis.get("detected_algorithms", [])
    return f"- source: `{source}`\n- language: {language}\n- detected_algorithms: {', '.join(algorithms) if algorithms else 'not identified'}"


def _result_summary(run: Path) -> str:
    collected = _read_json(run / "collected_results.json") or {}
    metrics = collected.get("parsed_metrics", {})
    if not metrics:
        return collected.get("parse_note", "No parsed metrics.")
    return "```json\n" + json.dumps(metrics, indent=2) + "\n```"


def _evidence_summary(run: Path) -> str:
    candidates = [
        run / "plan.md",
        run / "repo_analysis.json",
        run / "run_plan.json",
        run / "execution_log.jsonl",
        run / "run_log.txt",
        run / "collected_results.json",
    ]
    existing = [path.relative_to(run).as_posix() for path in candidates if path.exists()]
    return "\n".join(f"- `{path}`" for path in existing) if existing else "No evidence artifacts recorded."


def _limitations(run: Path) -> str:
    limitations = []
    matlab_report = _read_json(run / "matlab_environment_report.json") or {}
    if matlab_report.get("execution_mode") == "static-only":
        limitations.append("MATLAB/Octave execution was not available in this environment.")
    if not (run / "tuning" / "tuning_results.csv").exists():
        limitations.append("Tuning was not run.")
    return "\n".join(f"- {item}" for item in limitations) if limitations else "No major limitations recorded."


def write_reports(run: Path | str) -> list[Path]:
    """Write compact Markdown reports for the minimal output tree.

    Generates only:
    - plan.md
    - RUN_SUMMARY.md
    - tuning/TUNING_SUMMARY.md (if tuning was run)
    """
    run = Path(run)
    run.mkdir(parents=True, exist_ok=True)
    tuning_dir = run / "tuning"
    best_path = _first_existing(tuning_dir / "best_parameters.json", run / "best_parameters.json")
    best = _read_json(best_path) if best_path else {}
    tuning_rows = []
    tuning_csv = _first_existing(tuning_dir / "tuning_results.csv", run / "tuning_results.csv")
    if tuning_csv:
        tuning_rows = list(csv.DictReader(tuning_csv.open()))
    figures = sorted((run / "figures").glob("*.svg")) if (run / "figures").exists() else []
    figure_links = "\n".join(f"![{path.stem}](figures/{path.name})" for path in figures)
    executions = _read_jsonl(run / "execution_log.jsonl")

    reports = {
        "RUN_SUMMARY.md": f"""# Run Summary

## Status
{_status(executions)}

## Source
{_source_summary(run)}

## Commands Run
{_format_commands(executions)}

## Evidence
{_evidence_summary(run)}

## Results
{_result_summary(run)}

## Figures
{figure_links or 'No figures generated.'}

## Patches
No patches were applied.

## Limitations
{_limitations(run)}

## Optional Tuning Recommendation
Propose tuning only after the human approves a `tuning/tuning_plan.md`.
""",
    }

    if tuning_rows:
        reports["tuning/TUNING_SUMMARY.md"] = f"""# Tuning Summary

## Status
{{status}}

## Budget
{{budget}}

## Search Method
{{method}}

## Best Parameters
```
{json.dumps(best, indent=2)}
```

## Baseline vs Best
{{baseline_vs_best}}

## Evidence
{{evidence}}

## Limitations
{{limitations}}
"""

    written = []
    for name, body in reports.items():
        path = run / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)
        written.append(path)
    return written


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    args = parser.parse_args()
    print(json.dumps([str(path) for path in write_reports(args.run)], indent=2))


if __name__ == "__main__":
    main()
