---
name: failure-diagnosis-skill
description: This skill should be used when an execution fails, an error occurs, a command times out, or the user asks to diagnose what went wrong with a computational math experiment.
---

# Failure Diagnosis Skill

Classifies execution failures and generates fix proposals conversationally.

For end-to-end computational math research-code reproduction workflows, this Skill should be selected by `computational_math_reproduction_workflow_skill` rather than used as the first entrypoint.

## Script

### failure_classifier
Input: `--stderr <text>`, `--stdout <text>`, `--out <path>`
Output: classified failure type (printed to stdout), `repair_plan.md` only if source/dependency/entrypoint/data changes needed

Classified failure types: dependency_error, version_conflict, missing_data, missing_entrypoint, timeout, numerical_failure, permission_error, high_risk_command, readme_unclear, unknown_error

```bash
python -m skills.failure_diagnosis_skill.scripts.failure_classifier --stderr "ModuleNotFoundError" --out /path/to/output
```

## Workflow

1. When an execution fails, run `failure_classifier` with stderr/stdout.
2. Explain the failure type and evidence in conversation.
3. If repair is needed (source edits, dependency changes, adapters, entrypoint changes), write `repair_plan.md` with a concise reference to `logs/run.log` — do not copy the full traceback.
4. If no repair is needed, explain in conversation and keep the original logs in `logs/run.log`.
5. Ask user how to proceed: attempt fix, adjust parameters, or escalate.
6. Do not apply high-risk fixes without explicit user approval.

## Output Rules

- Default: diagnose conversationally, keep original logs in `logs/run.log`, no `failure_analysis.md`.
- Only write `repair_plan.md` when source/dependency/entrypoint/data changes are needed.
- `repair_plan.md` must be short — reference `logs/run.log`, don't copy the full traceback.
