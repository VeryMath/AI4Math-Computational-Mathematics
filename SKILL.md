---
name: invariant-computation
description: Use when a coding agent needs to compute, route, verify, or report topological, geometric, or algebraic invariants from complexes, filtrations, manifolds, knots, groups, ideals, polynomial systems, or mathematical source artifacts.
---

# Invariant Computation

This root `SKILL.md` is a compatibility entrypoint for platforms that expect one top-level Skill file. The shared Skill layer lives at:

```text
skills/invariant-computation/SKILL.md
```

Read that concrete Skill before computing or routing invariant computations. Keep platform adapters thin and improve the shared Skill layer first.

## Operating Boundary

- Inspect the object and requested invariant before choosing a backend.
- Build a representation checkpoint before executable commands.
- Ask before installs, source edits, long computations, API calls, or final mathematical claims.
- Report coefficient rings, conventions, backend versions, logs, validation checks, and limits.
