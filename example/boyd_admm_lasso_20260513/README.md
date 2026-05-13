# Boyd ADMM Lasso Reproduction Example

This example captures a completed Skill-first reproduction, visualization, and tuning run for the Stanford Boyd ADMM Lasso MATLAB example.

## What It Demonstrates

- Domain routing to continuous optimization and ADMM.
- MATLAB runtime use through an approved run plan.
- Failure diagnosis when `grabcode` opened editor buffers without saving `.m` files.
- Compact repair approval and local source capture.
- Reproduction evidence with ADMM objective and residual histories.
- Visualization outputs for objective and residual convergence.
- Approved `rho` / `alpha` grid tuning with a separate tuning summary.

## Source

- Stanford ADMM examples: https://web.stanford.edu/~boyd/papers/admm/
- Solver page: https://web.stanford.edu/~boyd/papers/admm/lasso/lasso.html
- Example page: https://web.stanford.edu/~boyd/papers/admm/lasso/lasso_example.html

Local source recovered from the published MATLAB pages:

- `source/lasso.m`
- `source/lasso_example.m`

## Key Results

Baseline reproduction:

```text
rho = 1.0
alpha = 1.0
iterations = 15
final objective = 17.2693553575
r_norm = 0.0649905373 < eps_pri = 0.0818532325
s_norm = 0.0531550738 < eps_dual = 0.0601837113
```

Best approved tuned configuration:

```text
rho = 1.0
alpha = 1.2
iterations = 13
final objective = 17.2696302235
```

The tuned setting reduces the baseline iteration count from 15 to 13 while keeping the final objective within the approved `0.1` tolerance.

## Files

- `plan.md`: reproduction plan and approval scope.
- `repair_plan.md`: diagnosis and approved repair for unsaved MATLAB `grabcode` buffers.
- `RUN_SUMMARY.md`: baseline reproduction evidence.
- `logs/run.log`: MATLAB baseline run log.
- `results/lasso_history.csv`: raw Boyd ADMM iteration history.
- `results/convergence.csv`: normalized convergence data for repository visualization helpers.
- `figures/`: objective and residual convergence figures.
- `tuning/tuning_plan.md`: approved tuning plan.
- `tuning/tuning_results.csv`: all 20 tuning trials.
- `tuning/best_parameters.json`: selected tuned parameters.
- `tuning/TUNING_SUMMARY.md`: tuning evidence and interpretation.

## Re-run Notes

Baseline MATLAB run from this example directory:

```matlab
cd('example/boyd_admm_lasso_20260513/source');
run('lasso_example.m');
```

Tuning run:

```matlab
run('example/boyd_admm_lasso_20260513/tuning/run_tuning.m');
```

Regenerate tuning SVG figures:

```bash
conda run -n ai4math python example/boyd_admm_lasso_20260513/tuning/plot_tuning.py
```

This example is a reference artifact for the Skill-first workflow. It is not a separate CLI pipeline.
