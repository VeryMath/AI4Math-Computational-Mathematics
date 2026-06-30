# Proximal Gradient

Proximal gradient methods handle composite objectives with smooth and nonsmooth terms.

- Common inputs: gradient oracle, proximal operator, step size, tolerance.
- Hyperparameters: `step_size`, line search flag, `tol`, `max_iter`.
- Metrics: objective value, objective gap, gradient mapping norm, iterations, runtime.
- Failure modes: step size too large, missing Lipschitz estimate, inaccurate proximal operator, slow convergence from poor scaling.
