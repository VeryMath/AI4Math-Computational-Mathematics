# Primal-Dual Method

Primal-dual methods update primal and dual variables together for saddle-point and constrained optimization formulations.

- Common inputs: primal objective, dual objective or constraint operator, step sizes, relaxation.
- Hyperparameters: `primal_step_size`, `dual_step_size`, `relaxation`, `tol`, `max_iter`.
- Metrics: primal residual, dual residual, gap, objective value, iterations, runtime.
- Failure modes: unstable step-size product, residual imbalance, bad operator norm estimate, infeasible constraints.
