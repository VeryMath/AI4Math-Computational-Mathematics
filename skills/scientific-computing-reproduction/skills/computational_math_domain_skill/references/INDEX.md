# Computational Math Domain Routing Index

Use this index before creating a reproduction plan for a computational math repository whose domain is broader than continuous optimization.

## Domain Routing

| Trigger | Read | Do not |
| --- | --- | --- |
| ADMM, proximal, primal-dual, PPA, augmented Lagrangian, objective/residual logs | `domains/continuous-optimization.md`, then `continuous_optimization_skill/references/INDEX.md` | Do not treat continuous optimization as the whole project scope. It is one mature domain module. |
| Eigenvalue, singular value, Krylov, QR, LU, Cholesky, preconditioner, sparse solve | `domains/numerical-linear-algebra.md` | Do not report success from a solve without checking residual, conditioning, or reference error. |
| ODE, SDE, time stepping, Runge-Kutta, BDF, stability region, event handling | `domains/differential-equations.md` | Do not ignore time-step, tolerance, stiffness, or random seed evidence. |
| FEM, finite volume, mesh, weak form, Galerkin, stiffness matrix, boundary condition | `domains/pde-fem.md` | Do not run a PDE demo without identifying mesh/data dependencies and boundary conditions. |
| Monte Carlo, MCMC, particle filter, stochastic process, confidence interval, random seed | `domains/stochastic-simulation.md` | Do not compare stochastic outputs without seed, sample size, and uncertainty information. |
| Inverse problem, regularization, tomography, deconvolution, parameter estimation, adjoint | `domains/inverse-problems.md` | Do not claim recovery quality without metric, prior/regularizer, or data-noise assumptions. |

## Runtime Routing

| Trigger | Read | Do not |
| --- | --- | --- |
| `.m`, `.mlx`, MATLAB README commands, toolbox names | `matlab_runtime_skill/references/INDEX.md` | Do not make MATLAB the workflow driver; it is a runtime backend. |
| `requirements.txt`, `pyproject.toml`, `.py`, notebooks | `environment_deployment_skill/SKILL.md` | Do not install or upgrade dependencies before approval. |
| `Project.toml`, `.jl` | Static analysis plus `environment_deployment_skill/SKILL.md` | Do not auto-run Julia in the MVP unless explicitly approved. |
| `CMakeLists.txt`, `Makefile`, `.cpp`, `.c`, `.f90` | Static analysis plus `environment_deployment_skill/SKILL.md` | Do not build native code without a reviewed plan and timeout. |

## Evidence Checklist

Before finalizing a domain classification, collect at least two of:

- README or paper wording;
- file and function names;
- equations or update loops in code;
- dependency/toolbox names;
- output metrics and figure names;
- example commands or test names.

## Preflight Response Pattern

```text
Preflight: computational_math_domain_skill/references/INDEX.md -> domains/pde-fem.md
```

Then state the domain, evidence, runtime, and whether a specialist Skill exists.

