---
name: auto-tuning-skill
description: This skill should be used when the user asks to tune parameters, run hyperparameter search, optimize algorithm settings, or find the best configuration for a computational math method.
---

# Auto Tuning Skill

Use this Skill after a computational math reproduction has succeeded or partially succeeded and the human has approved tuning. Codex proposes the tuning plan from the reproduction evidence, explains the parameter space and budget, and waits for approval before running experiments.

This Skill is not a first entrypoint and is not launched through a user-facing CLI pipeline. For end-to-end work, `computational_math_reproduction_workflow_skill` selects this Skill when tuning becomes appropriate.

## Tuning Gate

Tuning must not start until:

- reproduction has succeeded or produced enough partial evidence to define a meaningful metric;
- Codex writes `tuning/tuning_plan.md`;
- the human approves the tuning plan in conversation or through an approval log.

Budget increases, expanded parameter spaces, dependency changes, and source edits require another approval.

## Output Layout

Put tuning artifacts under the run directory:

```text
tuning/
├── tuning_plan.md
├── tuning_results.csv
├── best_parameters.json
├── tuning.log
├── tuning_figures/
└── TUNING_SUMMARY.md
```

## Optional Helper

`skills/auto_tuning_skill/scripts/experiment_runner.py` is an optional helper for repeatable grid search or random search after approval. It is a tool Codex may call, not the workflow driver.

Typical helper use:

```bash
python -m skills.auto_tuning_skill.scripts.experiment_runner \
  --source /path/to/repo \
  --param-space /path/to/parameter_space.yaml \
  --budget 20 \
  --out outputs/<run_id>/tuning \
  --method random_search \
  --require-approval tuning_plan
```

The helper writes `tuning_results.csv` and `best_parameters.json`. Codex should also keep a concise `tuning.log`, generate figures under `tuning/tuning_figures/` when metrics are available, and write `TUNING_SUMMARY.md`.

## Workflow

1. Read the reproduction evidence: command, metrics, logs, runtime, residuals, failures, and limitations.
2. Decide whether tuning is meaningful. If reproduction failed completely, return to failure diagnosis instead.
3. Draft `tuning/tuning_plan.md` with parameter space, search method, budget, objective metric, constraints, stop conditions, and risks.
4. Ask the human to `approve`, `revise`, `reject`, or `skip`.
5. Run only the approved tuning scope, optionally using `experiment_runner.py --require-approval tuning_plan`.
6. Save `tuning_results.csv`, `best_parameters.json`, `tuning.log`, and any figures.
7. Write `tuning/TUNING_SUMMARY.md` with best parameters, metric evidence, failed trials, and whether the result changes the reproduction conclusion.
