"""Conjugate Gradient helpers for the CG skill."""

from __future__ import annotations

from typing import Callable, Sequence

import numpy as np  # pyright: ignore[reportMissingImports]

ArrayLike = Sequence[Sequence[float]] | np.ndarray


def _as_matrix_or_linop(A: ArrayLike | Callable[[np.ndarray], np.ndarray]) -> Callable[[np.ndarray], np.ndarray]:
    if callable(A):
        return A
    # support scipy.sparse matrices by using their .dot method
    try:
        import scipy.sparse as _sps

        if isinstance(A, _sps.spmatrix):
            return lambda x: A.dot(x)
    except Exception:
        pass

    mat = np.asarray(A, dtype=float)

    def matvec(x: np.ndarray) -> np.ndarray:
        return mat @ x

    return matvec


def conjugate_gradient(
    A: ArrayLike | Callable[[np.ndarray], np.ndarray],
    b: ArrayLike,
    x0: ArrayLike | None = None,
    tol: float = 1e-8,
    maxiter: int | None = None,
    M: Callable[[np.ndarray], np.ndarray] | None = None,
):
    """Simple Conjugate Gradient solver for SPD systems.

    A may be a dense matrix or a callable implementing matrix-vector product.
    Returns (x, info) where info contains iterations, residual_norm, converged.
    """
    matvec = _as_matrix_or_linop(A)
    b_arr = np.asarray(b, dtype=float)
    n = b_arr.shape[0]

    if x0 is None:
        x = np.zeros_like(b_arr)
    else:
        x = np.asarray(x0, dtype=float)

    if maxiter is None:
        maxiter = n

    r = b_arr - matvec(x)
    if M is not None:
        z = M(r)
    else:
        z = r
    p = z.copy()
    rz_old = float(np.dot(r, z))

    for k in range(1, maxiter + 1):
        Ap = matvec(p)
        alpha = rz_old / float(np.dot(p, Ap))
        x = x + alpha * p
        r = r - alpha * Ap
        residual_norm = float(np.linalg.norm(r))
        if residual_norm <= tol:
            return x, {"iterations": k, "residual_norm": residual_norm, "converged": True}

        if M is not None:
            z = M(r)
        else:
            z = r
        rz_new = float(np.dot(r, z))
        beta = rz_new / rz_old
        p = z + beta * p
        rz_old = rz_new

    return x, {"iterations": maxiter, "residual_norm": float(np.linalg.norm(b_arr - matvec(x))), "converged": False}


def report_markdown(info: dict) -> str:
    residual = info.get('residual_norm')
    residual_str = f"{residual:.2e}" if residual is not None else "N/A"
    return "\n".join([
        f"Iterations: {info.get('iterations')}",
        f"Residual norm: {residual_str}",
        f"Converged: {info.get('converged')}",
    ])


if __name__ == "__main__":
    # small demo
    A = np.array([[4.0, 1.0], [1.0, 3.0]])
    b = np.array([1.0, 2.0])

    x, info = conjugate_gradient(A, b, tol=1e-10)
    print("x =", x)
    print(report_markdown(info))
    print("residual =", np.linalg.norm(A @ x - b))

    # heavy examples and matrix generators belong in references/examples.md
