# PPA

The proximal point algorithm solves monotone inclusions and convex optimization by repeatedly solving regularized subproblems.

- Common inputs: objective, proximal center, proximal parameter, stopping tolerance.
- Hyperparameters: `proximal_parameter`, inner tolerance, outer tolerance, `max_iter`.
- Metrics: objective value, objective gap, step norm, iterations, runtime.
- Failure modes: weak proximal regularization, expensive inner solves, loose inner tolerances, ill conditioning.
