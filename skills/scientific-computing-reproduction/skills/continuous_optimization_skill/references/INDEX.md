# Continuous Optimization Reference Index

Use this index before classifying a repository or explaining algorithm evidence. The purpose is to route the agent to the smallest relevant reference card instead of rereading every optimization note.

## Function And Symbol Routing

| Trigger | Read | Why |
| --- | --- | --- |
| `rho`, `dual`, `primal`, `u`, `z`, `augmented Lagrangian`, `soft_threshold` near split variables | `admm.md` | ADMM evidence usually appears as primal/dual residuals, penalty parameters, and split-variable updates. |
| `prox`, `proximal`, `shrink`, `soft_threshold`, `ISTA`, `FISTA`, `gradient step` | `proximal_gradient.md` | Proximal-gradient methods combine smooth-gradient steps with proximal operators. |
| `PPA`, `proximal point`, `resolvent`, implicit update, monotone operator language | `ppa.md` | PPA evidence often looks like implicit regularized subproblems rather than explicit gradient steps. |
| `primal`, `dual`, `saddle`, `Chambolle`, `Pock`, `PDHG`, `extragradient` | `primal_dual_method.md` | Primal-dual methods couple primal and dual updates around saddle-point structure. |

## Task-Level Routing

| Trigger | Read | Do not |
| --- | --- | --- |
| The repository has multiple candidate algorithms | Relevant cards for each detected family | Do not force a single label before recording competing evidence. |
| Detector confidence is low | `admm.md`, `proximal_gradient.md`, `ppa.md`, `primal_dual_method.md` as needed | Do not ask the user to classify before checking README, papers, and update equations. |
| A run produced convergence logs | The card for the detected algorithm | Do not report success without identifying the metric meaning, such as objective, residual, feasibility, or gap. |
| Tuning is being proposed | The card for the detected algorithm plus the relevant default parameter-space config | Do not start tuning before reproduction succeeds or partially succeeds and the human approves. |

## Evidence Checklist

Before reporting an algorithm classification, collect at least two evidence types when available:

- code identifiers or update equations;
- README, paper, or comment language;
- logged metrics such as objective, residual, feasibility, or gap;
- parameter names such as `rho`, step size, relaxation, penalty, or tolerance;
- data-flow evidence showing which variables are primal, dual, auxiliary, or residual state.

## Preflight Response Pattern

When this index influences a classification, state a compact preflight line in conversation:

```text
Preflight: continuous_optimization_skill/references/INDEX.md -> admm.md
```

Then summarize the evidence and uncertainty. If evidence is ambiguous, route to human review instead of inventing certainty.

