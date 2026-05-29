"""GMRES helpers for the GMRES skill."""

from __future__ import annotations

from typing import Callable, Sequence

import numpy as np  # pyright: ignore[reportMissingImports]

ArrayLike = Sequence[Sequence[float]] | np.ndarray


def _as_matvec(A: ArrayLike | Callable[[np.ndarray], np.ndarray]) -> Callable[[np.ndarray], np.ndarray]:
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

    def mv(x: np.ndarray) -> np.ndarray:
        return mat @ x

    return mv


def arnoldi(matvec: Callable[[np.ndarray], np.ndarray], v0: np.ndarray, m: int):
    n = v0.shape[0]
    V = np.zeros((n, m + 1), dtype=float)
    H = np.zeros((m + 1, m), dtype=float)
    V[:, 0] = v0 / float(np.linalg.norm(v0))
    for j in range(m):
        w = matvec(V[:, j])
        for i in range(j + 1):
            H[i, j] = float(np.dot(V[:, i], w))
            w = w - H[i, j] * V[:, i]
        H[j + 1, j] = float(np.linalg.norm(w))
        if H[j + 1, j] != 0.0:
            V[:, j + 1] = w / H[j + 1, j]
        else:
            return V, H
    return V, H


def gmres(
    A: ArrayLike | Callable[[np.ndarray], np.ndarray],
    b: ArrayLike,
    x0: ArrayLike | None = None,
    restart: int = 50,
    tol: float = 1e-8,
    maxiter: int | None = None,
):
    matvec = _as_matvec(A)
    b_arr = np.asarray(b, dtype=float)
    n = b_arr.shape[0]
    if x0 is None:
        x = np.zeros_like(b_arr)
    else:
        x = np.asarray(x0, dtype=float)

    if maxiter is None:
        maxiter = n

    iter_count = 0
    while iter_count < maxiter:
        r = b_arr - matvec(x)
        beta = float(np.linalg.norm(r))
        if beta <= tol:
            return x, {"iterations": iter_count, "residual_norm": beta, "converged": True}

        m = min(restart, maxiter - iter_count)
        V, H = arnoldi(matvec, r, m)
        # Solve least squares min || beta e1 - H y ||
        e1 = np.zeros((H.shape[0],), dtype=float)
        e1[0] = beta
        y, *_ = np.linalg.lstsq(H, e1, rcond=None)
        dx = V[:, : H.shape[1]] @ y
        x = x + dx
        iter_count += m
        r_norm = float(np.linalg.norm(b_arr - matvec(x)))
        if r_norm <= tol:
            return x, {"iterations": iter_count, "residual_norm": r_norm, "converged": True}

    return x, {"iterations": iter_count, "residual_norm": float(np.linalg.norm(b_arr - matvec(x))), "converged": False}


def report_markdown(info: dict) -> str:
    return "\n".join([
        f"Iterations: {info.get('iterations')}",
        f"Residual norm: {info.get('residual_norm'):.2e}",
        f"Converged: {info.get('converged')}",
    ])


if __name__ == "__main__":
    # simple demo with a non-symmetric matrix
    A = np.array([[3.0, 2.0], [1.0, 4.0]])
    b = np.array([1.0, 2.0])
    x, info = gmres(A, b, restart=10, tol=1e-10)
    print("x =", x)
    print(report_markdown(info))
    print("residual =", np.linalg.norm(A @ x - b))

    # heavy example runners were removed — see references/examples.md for usage and tests
