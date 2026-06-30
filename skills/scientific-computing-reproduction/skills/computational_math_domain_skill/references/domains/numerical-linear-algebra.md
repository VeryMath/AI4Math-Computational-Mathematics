# Domain Card: Numerical Linear Algebra

Use when code centers on matrix factorizations, sparse solves, eigen/singular value computations, iterative methods, or preconditioning.

Common evidence:

- QR, LU, Cholesky, SVD, eigensolver, Krylov, GMRES, CG, Lanczos, Arnoldi;
- sparse matrix assembly or matrix-free operators;
- condition numbers, residual norms, backward error, orthogonality checks.

Validation signals:

- residual norm such as `||Ax-b||`;
- relative error against a reference solution;
- conditioning or stability discussion;
- iteration counts and convergence tolerances;
- performance evidence for sparse or structured problems.

Failure risks:

- ill-conditioning hidden by small examples;
- dense fallback for sparse problems;
- non-reproducible randomized factorizations;
- comparing wall time without hardware/context.

