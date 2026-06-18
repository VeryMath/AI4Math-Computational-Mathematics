---
name: report-generation-skill
description: This skill should be used when the user asks to generate a report, summarize results, write up findings, or create documentation for a computational math reproduction or tuning experiment.
---

# Report Generation Skill

Generates compact Markdown reports for the Skill-first Codex workflow.

For end-to-end computational math research-code reproduction workflows, this Skill should be selected by `computational_math_reproduction_workflow_skill` rather than used as the first entrypoint.

## Report Types

Four compact Markdown report types:

### 1. plan.md

```markdown
# Reproduction Plan

## Goal

## Selected Source

## Minimal Command To Run

## Expected Outputs

## Risks

## Approval Scope

Reply with approve / revise / reject / skip.
```

### 2. repair_plan.md

```markdown
# Repair Plan

## Failure Summary

## Evidence

## Proposed Minimal Repair

## Files To Modify

## What Will Not Be Changed

## Patch / Rollback Plan

Reply with approve / revise / reject / skip.
```

### 3. RUN_SUMMARY.md

```markdown
# Run Summary

## Status

## Source

## Commands Run

## Evidence

## Results

## Figures

## Patches

## Limitations

## Optional Tuning Recommendation
```

### 4. tuning/TUNING_SUMMARY.md

```markdown
# Tuning Summary

## Status

## Budget

## Search Method

## Best Parameters

## Baseline vs Best

## Evidence

## Limitations
```

## Workflow

1. Draft `plan.md` before execution when a durable plan is useful.
2. After reproduction, write `RUN_SUMMARY.md` with status, evidence, limits, and next options.
3. If tuning was approved and run, write `tuning/TUNING_SUMMARY.md`.
4. Ask the user if conclusions are acceptable or if sections need revision.

## Optional Helper

### report_writer
Input: `--run <path>` — run directory with execution logs, optional tuning outputs, and figures.

```bash
python -m skills.report_generation_skill.scripts.report_writer --run /path/to/output
```
