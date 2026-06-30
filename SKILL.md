---
name: ai4math-computational-mathematics
description: Route AI4Math computational mathematics tasks to the appropriate bundled skill package.
---

# AI4Math Computational Mathematics

Use this repository as a routing layer for computational mathematics workflows.

## Packages

- `skills/finite-element-analysis/`: finite element analysis prompts and
  examples. Read its `README.md` and numbered `SKILL*.md` files before use.
- `skills/invariant-computation/`: route, compute, and validate algebraic,
  topological, geometric, TDA, and certified numerical invariants. Read its
  `SKILL.md`, README, and references before use.
- `skills/least-squares/`: least-squares regression, curve fitting, and
  parameter estimation. Read its `SKILL.md`, `README.md`, and examples before
  use.
- `skills/scientific-computing-reproduction/`: computational mathematics
  research-code reproduction, runtime planning, failure diagnosis, tuning,
  visualization, and evidence-backed reporting. Read its `SKILL.md`, README,
  and nested `skills/registry.yaml` before use.

Prefer package-local instructions over this router when running a concrete
workflow.
