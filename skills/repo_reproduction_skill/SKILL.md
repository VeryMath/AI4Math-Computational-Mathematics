---
name: repo-reproduction-skill
description: This skill should be used when the user asks to analyze, reproduce, or run a computational math repository. Use when inspecting source code, detecting algorithms, planning runs, executing experiments, or collecting results from optimization code.
---

# Repo Reproduction Skill

Analyzes a computational math repository, generates run plans, executes them, and collects results.

For end-to-end computational math research-code reproduction workflows, this Skill should be selected by `computational_math_reproduction_workflow_skill` rather than used as the first entrypoint.

## Scripts

### repo_analyzer
Analyzes source code directory. Input: `--source <path>`, `--out <path>`. Writes analysis summary to `plan.md` fields (source path, language, entrypoints, detected algorithms, risks) — does not write `repo_analysis.json` by default.

```bash
python -m skills.repo_reproduction_skill.scripts.repo_analyzer --source /path/to/repo --out /path/to/output
```

### run_planner
Generates candidate run plans from the analysis. Input: `--analysis <dict or json>`, `--out <path>`. Outputs compact plan fields for `plan.md` — does not write `run_plan.json` by default.

```bash
python -m skills.repo_reproduction_skill.scripts.run_planner --analysis /path/to/analysis.json --out /path/to/output
```

### executor
Executes an approved run plan. Input: `--command <str>`, `--out <path>`, `--timeout <int>`. Writes stdout/stderr to `logs/run.log` and returns exit code. Does not write `run_plan.json` or `execution_log.jsonl` by default.

```bash
python -m skills.repo_reproduction_skill.scripts.executor --command "python main.py" --out /path/to/output --timeout 300
```

### result_collector
Scans executed output for result files and extracts metrics. Input: `--source`, `--out`. Writes results to `results/` — does not write `collected_results.json` by default.

```bash
python -m skills.repo_reproduction_skill.scripts.result_collector --source /path/to/repo --out /path/to/output
```

## Output Rules

- Do not write `repo_analysis.json` by default. Summarize analysis in conversation and in `plan.md` fields.
- Do not write `run_plan.json` by default. Use compact plan fields.
- Execution logs go to `logs/run.log`.
- Results go to `results/`.
- Figures go to `figures/`.
- Patches go to `patches/`.

## Workflow

1. Run `repo_analyzer` to understand the repository.
2. Summarize findings in conversation and in `plan.md` fields.
3. Generate candidate command(s) and present to user for approval.
4. Run `executor` with the approved command.
5. Run `result_collector` to gather results under `results/`.
