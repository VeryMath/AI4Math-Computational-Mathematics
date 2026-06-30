# Tuning Summary

## Status

Succeeded.

The approved deterministic grid search completed all 20 `(rho, alpha)` trials.

## Budget

```text
rho   = [0.1, 0.3, 1.0, 3.0, 10.0]
alpha = [1.0, 1.2, 1.5, 1.8]
trials = 20
successful trials = 20
valid trials = 9
```

Validity required:

```text
r_norm < eps_pri
s_norm < eps_dual
abs(final_objective - baseline_objective) <= 0.1
```

## Search Method

Deterministic grid search with the same Boyd Lasso problem regenerated for each trial using the original example seeds and dimensions.

Only `rho` and `alpha` were varied. The ADMM solver equations, stopping tolerances, problem size, and data generation were not changed.

## Best Parameters

```json
{
  "rho": 1.0,
  "alpha": 1.2,
  "iterations": 13,
  "final_objective": 17.269630223534392,
  "r_norm": 0.06635631967327256,
  "eps_pri": 0.08163775182046383,
  "s_norm": 0.059589267124141872,
  "eps_dual": 0.060479575782457246,
  "valid": true
}
```

The best valid trial is trial 10.

## Baseline vs Best

| Configuration | rho | alpha | Iterations | Final objective | Valid |
| --- | ---: | ---: | ---: | ---: | --- |
| Baseline | 1.0 | 1.0 | 15 | 17.2693553575 | true |
| Best tuned | 1.0 | 1.2 | 13 | 17.2696302235 | true |

Iteration reduction:

```text
15 -> 13
relative reduction = 13.33%
```

Objective difference:

```text
abs(17.2696302235 - 17.2693553575) = 0.0002748660
```

This is inside the approved objective tolerance of `0.1`.

## Evidence

- Plan: `tuning_plan.md`
- Tuning script: `run_tuning.m`
- Tuning log: `tuning.log`
- Trial table: `tuning_results.csv`
- Best parameters: `best_parameters.json`
- Figures:
  - `tuning_figures/tuning_iterations.svg`
  - `tuning_figures/tuning_objective.svg`

Top valid configurations by the approved metric:

| Trial | rho | alpha | Iterations | Final objective |
| ---: | ---: | ---: | ---: | ---: |
| 10 | 1.0 | 1.2 | 13 | 17.2696302235 |
| 9 | 1.0 | 1.0 | 15 | 17.2693553575 |
| 7 | 0.3 | 1.5 | 24 | 17.2495809434 |
| 6 | 0.3 | 1.2 | 29 | 17.2343725166 |
| 5 | 0.3 | 1.0 | 35 | 17.2336165633 |

## Important Non-Selected Fast Trials

Some configurations converged in fewer iterations but were rejected by the approved objective closeness constraint:

| Trial | rho | alpha | Iterations | Final objective | Reason |
| ---: | ---: | ---: | ---: | ---: | --- |
| 16 | 3.0 | 1.8 | 11 | 17.4779433123 | objective differs from baseline by more than 0.1 |
| 15 | 3.0 | 1.5 | 13 | 17.4824946493 | objective differs from baseline by more than 0.1 |

## Limitations

- This tuning round only explores a small grid for `rho` and `alpha`.
- The grid is enough to improve the baseline example, but not enough to claim global optimality.
- `ABSTOL` and `RELTOL` were not tuned because they are internal constants in `lasso.m`; changing them would require a separate source-modification approval.
- Runtime values are small and local-machine specific, so iteration count is the more meaningful comparison metric.

## Recommendation

Use `rho = 1.0` and `alpha = 1.2` as the tuned setting for this reproduced Boyd Lasso problem.

Keep the original `rho = 1.0`, `alpha = 1.0` result as the paper/example baseline.
