# Domain Card: PDE And FEM

Use when code solves PDEs using finite elements, finite volume, finite difference, spectral methods, or mesh-based discretizations.

Common evidence:

- mesh, elements, nodes, boundary conditions, weak form, stiffness matrix, mass matrix;
- Galerkin, FEM, FVM, FDM, DG, multigrid;
- solution fields, error norms, refinement studies.

Validation signals:

- mesh refinement or convergence order;
- error against manufactured or analytic solution;
- residual or conservation checks;
- boundary condition verification;
- comparison with paper figures or benchmark data.

Failure risks:

- missing mesh/data files;
- boundary conditions not matching paper setup;
- visual plot without numerical error;
- memory/runtime blowup from unbounded mesh refinement.

