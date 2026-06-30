# ADMM

ADMM solves structured convex optimization problems by splitting variables and alternating primal and dual updates.

- Common inputs: objective terms, linear constraints, penalty parameter, stopping tolerance.
- Hyperparameters: `rho`, relaxation `alpha`, `tol`, `max_iter`.
- Metrics: objective value, primal residual, dual residual, iterations, runtime.
- Failure modes: poor `rho`, residual imbalance, ill-conditioned subproblems, infeasible data, non-convex model assumptions.
