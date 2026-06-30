# Domain Card: Continuous Optimization

Use when code optimizes objective functions with iterative first-order, splitting, primal-dual, proximal, or augmented-Lagrangian methods.

Common evidence:

- variables such as objective, gradient, proximal operator, residual, dual variable, penalty, tolerance;
- algorithms such as ADMM, PPA, proximal gradient, PDHG, Chambolle-Pock, coordinate descent;
- plots of objective value, primal residual, dual residual, feasibility, gap, or KKT metrics.

Validation signals:

- objective or merit function trend;
- constraint feasibility;
- primal/dual residuals;
- comparison with paper baseline or known solver;
- reproducible stopping criterion.

Failure risks:

- scaling-sensitive parameters;
- residuals with unclear definitions;
- convergence claimed from exit code only;
- tuning before minimal reproduction is established.

Mature specialist:

- `continuous_optimization_skill`

