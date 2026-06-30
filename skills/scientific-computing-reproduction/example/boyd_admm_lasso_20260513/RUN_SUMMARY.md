# Run Summary

## Status

Succeeded.

The Boyd Stanford ADMM Lasso example was reproduced in MATLAB R2025a after saving the two `grabcode` editor buffers as local `.m` files.

## Source

- Source page: https://web.stanford.edu/~boyd/papers/admm/
- Solver page: https://web.stanford.edu/~boyd/papers/admm/lasso/lasso.html
- Example page: https://web.stanford.edu/~boyd/papers/admm/lasso/lasso_example.html
- Local source copy:
  - `source/lasso.m`
  - `source/lasso_example.m`

## Commands Run

1. Checked MATLAB runtime/toolboxes with MATLAB MCP.
2. Ran `grabcode(...)` for the two Stanford Lasso pages.
3. Saved generated editor buffers as local source files after repair approval.
4. Checked local source files with MATLAB Code Analyzer.
5. Ran `lasso_example.m` with MATLAB MCP and saved logs, results, and figures.

## Evidence

- Log: `logs/run.log`
- Per-iteration history: `results/lasso_history.csv`
- MATLAB result file: `results/lasso_history.mat`
- Objective figure: `figures/lasso_objective.png`
- Residual figure: `figures/lasso_residuals.png`

Final metrics:

```text
Final iter: 15
Final objval: 17.2693553575
Final r_norm: 0.0649905372515
Final eps_pri: 0.0818532325451
Final s_norm: 0.0531550738298
Final eps_dual: 0.0601837113356
Primal satisfied: true
Dual satisfied: true
```

The final residuals satisfy the ADMM stopping criteria:

```text
r_norm < eps_pri
s_norm < eps_dual
```

## Results

The reproduced iteration count and final metrics match the published Stanford example closely:

- Published final iteration: 15.
- Reproduced final iteration: 15.
- Published final objective shown in the example log: about `17.27`.
- Reproduced final objective: `17.2693553575`.

## Figures

Generated:

- `figures/lasso_objective.png`
- `figures/lasso_residuals.png`
- `figures/convergence_objective.svg`
- `figures/convergence_residuals.svg`

The normalized convergence CSV used by the repository visualization helper is:

- `results/convergence.csv`

## Patches

No repository source files were modified.

Repair was limited to the run directory:

- `source/lasso.m`
- `source/lasso_example.m`

The repair saved MATLAB `grabcode` editor buffers that were generated but not automatically written to disk.

## Static Analysis Notes

MATLAB Code Analyzer reported only non-blocking style and compatibility notes:

- `lasso.m`: output variables should use comma separation in older-style multiple-output syntax; one preallocation warning.
- `lasso_example.m`: old `rand`/`randn` seed API is not recommended in modern MATLAB, but it was kept unchanged to preserve the published example.

## Limitations

- The source was recovered from MATLAB `grabcode` editor buffers rather than directly downloaded as `.m` files.
- The code uses old random seed calls intentionally, matching the published example.
- No tuning was performed in this run.
- No algorithmic changes or parameter changes were made.

## Optional Tuning Recommendation

Approved tuning was completed under `tuning/`.

Best valid tuned setting:

```text
rho = 1.0
alpha = 1.2
iterations = 13
final objective = 17.2696302235
```

See `tuning/TUNING_SUMMARY.md` for full tuning evidence.
