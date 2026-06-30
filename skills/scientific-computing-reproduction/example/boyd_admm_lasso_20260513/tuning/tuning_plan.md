# Tuning Plan

## Goal

Tune the Boyd ADMM Lasso example after the baseline reproduction succeeded.

Baseline:

```text
rho = 1.0
alpha = 1.0
iterations = 15
final objective = 17.2693553575
r_norm = 0.0649905373 < eps_pri = 0.0818532325
s_norm = 0.0531550738 < eps_dual = 0.0601837113
```

## Parameter Space

Tune only ADMM runtime parameters exposed by the published solver call:

```text
rho   = [0.1, 0.3, 1.0, 3.0, 10.0]
alpha = [1.0, 1.2, 1.5, 1.8]
```

Budget: `5 * 4 = 20` trials.

No tolerance, problem size, data generation, stopping rule, or ADMM update equation will be changed in this tuning round.

## Search Method

Use deterministic grid search.

For every `(rho, alpha)` pair:

1. Recreate the same Lasso problem using the original Stanford example seeds and dimensions.
2. Run:

   ```matlab
   [x, history] = lasso(A, b, lambda, rho, alpha);
   ```

3. Record:
   - `rho`
   - `alpha`
   - iteration count
   - final objective
   - final `r_norm`, `eps_pri`
   - final `s_norm`, `eps_dual`
   - primal feasibility flag
   - dual feasibility flag
   - elapsed seconds

## Objective Metric

Primary objective:

- minimize iteration count among trials that satisfy both ADMM stopping criteria.

Validity constraints:

```text
r_norm < eps_pri
s_norm < eps_dual
abs(final_objective - baseline_objective) <= 0.1
```

Tie-breakers:

1. lower final objective;
2. lower elapsed time;
3. smaller `rho` if metrics are otherwise tied.

## Execution Plan

After approval, create and run a MATLAB tuning script under:

```text
outputs/boyd_admm_lasso_20260513/tuning/run_tuning.m
```

The script will use only the existing local source files:

```text
outputs/boyd_admm_lasso_20260513/source/lasso.m
outputs/boyd_admm_lasso_20260513/source/lasso_example.m
```

Expected outputs:

```text
tuning/tuning.log
tuning/tuning_results.csv
tuning/best_parameters.json
tuning/tuning_figures/tuning_iterations.svg
tuning/tuning_figures/tuning_objective.svg
tuning/TUNING_SUMMARY.md
```

Timeout: 300 seconds for the whole tuning run.

## Risks

- Risk level: low.
- Some `(rho, alpha)` combinations may converge more slowly or hit the internal `MAX_ITER = 1000`; those trials will be recorded, not retried.
- Because stopping tolerances remain fixed, a faster configuration may stop with a slightly different objective. The objective closeness constraint prevents accepting a fast but low-quality trial.
- This round does not tune `ABSTOL` or `RELTOL` because those are internal constants in `lasso.m` and changing them would be an algorithm-source modification.

## Approval Scope

Reply with exactly one of:

- `approve`: run the 20-trial deterministic grid search described above.
- `revise`: change the parameter grid, metric, budget, timeout, or output format.
- `reject`: stop tuning.
- `skip`: keep the baseline reproduction and do not tune now.
