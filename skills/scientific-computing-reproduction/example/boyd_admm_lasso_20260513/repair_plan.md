# Repair Plan

## Failure Summary

The approved MATLAB run failed before the Lasso example could start:

```text
错误使用 run (第 74 行)
未找到 lasso_example.m。
```

`grabcode` exists in MATLAB R2025a, but in this MCP/headless execution it did not create `lasso.m` or `lasso_example.m` under `outputs/boyd_admm_lasso_20260513/source/`.

## Evidence

- MATLAB diagnostic: `which('grabcode')` returns `/Applications/MATLAB_R2025a.app/toolbox/matlab/codetools/grabcode.m`.
- `outputs/boyd_admm_lasso_20260513/source/` contains no generated files after the two `grabcode(...)` calls.
- `logs/run.log` exists but contains no useful run table because the failure happened before the example script was found.

## Proposed Minimal Repair

Create a local, reproducible source copy from the same Stanford published HTML pages, without changing the ADMM algorithm:

1. Fetch the two selected HTML pages:
   - `https://web.stanford.edu/~boyd/papers/admm/lasso/lasso.html`
   - `https://web.stanford.edu/~boyd/papers/admm/lasso/lasso_example.html`
2. Extract only the MATLAB code blocks from the published pages into:
   - `outputs/boyd_admm_lasso_20260513/source/lasso.m`
   - `outputs/boyd_admm_lasso_20260513/source/lasso_example.m`
3. Run static MATLAB Code Analyzer checks on both generated `.m` files.
4. Re-run the same Lasso example and save the same outputs planned earlier:
   - `logs/run.log`
   - `results/lasso_history.mat`
   - `results/lasso_history.csv`
   - `figures/lasso_objective.png`
   - `figures/lasso_residuals.png`
   - `RUN_SUMMARY.md`

## Files To Modify

Only files under `outputs/boyd_admm_lasso_20260513/`:

- `source/lasso.m`
- `source/lasso_example.m`
- optional extraction helper/log under `patches/`
- generated logs, results, figures, and `RUN_SUMMARY.md`

No repository Skill files, global MATLAB configuration, dependency files, or external source repositories will be modified.

## What Will Not Be Changed

- No ADMM equations, stopping criteria, `rho`, `alpha`, tolerances, or problem dimensions will be changed.
- No MATLAB toolboxes or global PATH/MCP configuration will be installed or edited.
- No tuning will be started in this repair step.

## Patch / Rollback Plan

The repair is confined to the run directory. To roll back, ignore or delete `outputs/boyd_admm_lasso_20260513/source/`, `results/`, `figures/`, and `logs/` for this run.

Reply with `approve`, `revise`, `reject`, or `skip`.
