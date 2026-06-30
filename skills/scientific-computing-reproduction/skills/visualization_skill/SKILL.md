---
name: visualization-skill
description: This skill should be used when the user asks to plot results, visualize convergence, generate charts, or create figures for optimization algorithms and tuning experiments.
---

# Visualization Skill

Generates SVG plots for convergence and tuning results.

For end-to-end computational math research-code reproduction workflows, this Skill should be selected by `computational_math_reproduction_workflow_skill` rather than used as the first entrypoint.

## Scripts

### convergence_plotter
Input: `--convergence-csv <path>`. Output: SVG files under `figures/`

```bash
python -m skills.visualization_skill.scripts.convergence_plotter --convergence-csv convergence.csv --out /path/to/output
```

### tuning_plotter
Input: `--tuning-csv <path>`. Output: SVG files under `tuning/tuning_figures/` for approved tuning runs, or another agent-selected figure directory for one-off plotting.

```bash
python -m skills.visualization_skill.scripts.tuning_plotter --tuning-csv tuning_results.csv --out /path/to/output
```

## Workflow

1. After running experiments or tuning, generate convergence plots
2. Present figures to user
3. Ask if user wants different metrics visualized
