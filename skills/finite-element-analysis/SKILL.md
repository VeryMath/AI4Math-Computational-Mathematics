---
name: finite-element-analysis
description: Use when a coding agent needs to explain, derive, or run finite element analysis workflows, including mesh discretization, element and basis selection, PDE strong-to-weak form conversion, matrix assembly, boundary-condition handling, sparse solves, and result review for teaching or small reproducible examples.
---

# Finite Element Analysis

Use this top-level entrypoint for finite element analysis tasks. Route to the
package-local modules instead of duplicating their detailed rules.

## Routing

- `SKILL1.md`: geometry discretization, element choice, and basis/shape
  function selection.
- `SKILL2.md`: converting PDE strong forms into standard finite element weak
  forms.
- `SKILL3.md`: assembly, boundary conditions, sparse linear solves, and result
  review for small FEM workflows.

## Workflow

1. Restate the physical field, domain, governing equation, boundary conditions,
   and requested output.
2. Select the relevant FEM stage from the routing table.
3. Follow the selected module's constraints and output format.
4. Keep derivation, discretization, solver execution, and interpretation
   separate so the user can approve or revise each stage.

Use `README.md` and `examples.md` for package overview and examples.
