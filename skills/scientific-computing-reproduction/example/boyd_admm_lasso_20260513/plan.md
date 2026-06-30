# Reproduction Plan

## Goal

Reproduce the Stanford Boyd ADMM Lasso example as a compact first ADMM experiment.

Target problem:

```text
minimize 0.5 * ||A x - b||_2^2 + lambda * ||x||_1
```

The solver is ADMM with augmented Lagrangian parameter `rho = 1.0` and relaxation parameter `alpha = 1.0`.

## Selected Source

- Source page: https://web.stanford.edu/~boyd/papers/admm/
- Example group: Lasso
- Solver page: https://web.stanford.edu/~boyd/papers/admm/lasso/lasso.html
- Example page: https://web.stanford.edu/~boyd/papers/admm/lasso/lasso_example.html
- Reference paper: Distributed Optimization and Statistical Learning via the Alternating Direction Method of Multipliers, Boyd, Parikh, Chu, Peleato, and Eckstein.

Domain classification:

- Candidate domain: continuous optimization.
- Algorithm family: ADMM / augmented Lagrangian splitting.
- Mature specialist Skill: `continuous_optimization_skill`.

Runtime classification:

- Backend: MATLAB.
- Local execution route: MATLAB MCP is available.
- Detected MATLAB version: MATLAB R2025a.
- Expected toolbox needs: base MATLAB only for this Lasso example; no CVX dependency is indicated for this example.

## Source Evidence

The Stanford ADMM page states that most scripts stand alone in MATLAB unless otherwise noted, and that example outputs include primal residual, primal feasibility tolerance, dual residual, dual feasibility tolerance, objective values, and plots.

The Lasso solver returns `history.objval`, `history.r_norm`, `history.s_norm`, `history.eps_pri`, and `history.eps_dual`.

The Lasso example uses:

```matlab
randn('seed', 0);
rand('seed', 0);
m = 1500;
n = 5000;
p = 100/n;
lambda = 0.1 * norm(A' * b, 'inf');
[x history] = lasso(A, b, lambda, 1.0, 1.0);
```

The published example log stops after 15 iterations with objective near `17.27`, `r_norm = 0.0650`, `eps_pri = 0.0819`, `s_norm = 0.0532`, and `eps_dual = 0.0602`.

## Minimal Command To Run

After approval, create a local run copy under:

```text
outputs/boyd_admm_lasso_20260513/source/
```

Use MATLAB to obtain the published scripts with `grabcode`, then run the example from that local run copy:

```matlab
cd('outputs/boyd_admm_lasso_20260513/source');
grabcode('https://web.stanford.edu/~boyd/papers/admm/lasso/lasso.html');
grabcode('https://web.stanford.edu/~boyd/papers/admm/lasso/lasso_example.html');
diary('../logs/run.log');
run('lasso_example.m');
save('../results/lasso_history.mat', 'history', 'x');
writetable(struct2table(history), '../results/lasso_history.csv');
saveas(1, '../figures/lasso_objective.png');
saveas(2, '../figures/lasso_residuals.png');
diary off;
```

If `grabcode` is unavailable in R2025a or the published HTML cannot be converted directly, stop and write `repair_plan.md` before creating an adapter or manual script extraction.

## Expected Outputs

- `logs/run.log`: MATLAB console output from the Lasso example.
- `results/lasso_history.mat`: MATLAB result structure and final solution vector.
- `results/lasso_history.csv`: per-iteration objective and residual history.
- `figures/lasso_objective.png`: objective value by iteration.
- `figures/lasso_residuals.png`: primal and dual residual curves with tolerances.
- `RUN_SUMMARY.md`: status, metrics, evidence, limitations, and optional tuning recommendation.

## Validation Signals

Primary validation:

- The run terminates successfully without source edits.
- Final iteration count is close to the published 15 iterations.
- Final objective is close to the published value near `17.27`.
- Final residuals satisfy ADMM stopping criteria:
  - `r_norm < eps_pri`
  - `s_norm < eps_dual`

Secondary validation:

- Objective and residual figures are generated.
- The history fields are complete for every iteration.
- Any numerical differences are explained by MATLAB version, sparse matrix behavior, or random number stream compatibility.

## Risks

- Risk level: low.
- The example is old MATLAB 7.7 published code, so `grabcode` compatibility is the main risk.
- Random streams from old MATLAB releases may not match R2025a exactly even with the same seed calls.
- Figure handles may differ if MATLAB opens figures in a different order.
- The source is external; no code will be executed until this plan is approved.

## Approval Scope

Reply with exactly one of:

- `approve`: fetch the two Lasso MATLAB scripts into the run directory and execute only the minimal MATLAB example above.
- `revise`: change the selected example, runtime route, outputs, timeout, or validation criteria.
- `reject`: stop this reproduction.
- `skip`: do not run now; keep the plan as a candidate.
