"""SVD helpers for the SVD decomposition skill."""

from __future__ import annotations

from typing import Sequence

import numpy as np  # pyright: ignore[reportMissingImports]

ArrayLike = Sequence[Sequence[float]] | np.ndarray


def _as_matrix(a: ArrayLike) -> np.ndarray:
    matrix = np.asarray(a, dtype=float)
    if matrix.ndim != 2:
        raise ValueError("A must be a 2D array.")
    return matrix


def svd_decompose(a: ArrayLike, full_matrices: bool = False) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return U, singular values, and V^T."""
    matrix = _as_matrix(a)
    return np.linalg.svd(matrix, full_matrices=full_matrices)


def rank_k_approximation(a: ArrayLike, k: int) -> np.ndarray:
    """Return the rank-k approximation of A."""
    u, singular_values, vt = svd_decompose(a, full_matrices=False)
    if k < 1 or k > singular_values.shape[0]:
        raise ValueError("k must satisfy 1 <= k <= min(m, n).")
    return u[:, :k] @ np.diag(singular_values[:k]) @ vt[:k, :]


def retained_energy_ratio(singular_values: ArrayLike, k: int) -> float:
    values = np.asarray(singular_values, dtype=float)
    total = float(np.sum(values**2))
    if total == 0.0:
        return 0.0
    return float(np.sum(values[:k] ** 2) / total)


def pseudoinverse_svd(a: ArrayLike, rcond: float | None = None) -> np.ndarray:
    """Return the Moore-Penrose pseudoinverse."""
    matrix = _as_matrix(a)
    if rcond is None:
        return np.linalg.pinv(matrix)
    return np.linalg.pinv(matrix, rcond=rcond)


def solve_least_squares_svd(a: ArrayLike, b: ArrayLike, rcond: float | None = None) -> np.ndarray:
    """Solve a least-squares problem with the pseudoinverse."""
    return pseudoinverse_svd(a, rcond=rcond) @ np.asarray(b, dtype=float)


def robust_solve_svd(a: ArrayLike, b: ArrayLike, rcond: float | None = None) -> tuple[np.ndarray, dict]:
    """Robust SVD-based solver with condition-number diagnostics.

    Returns (x, report) where report contains diagnostics.
    """
    matrix = _as_matrix(a)
    rhs = np.asarray(b, dtype=float)

    u, s, vt = np.linalg.svd(matrix, full_matrices=False)
    cond = float(s[0] / s[-1]) if s[-1] > 0 else float("inf")

    if rcond is None:
        rcond = max(matrix.shape) * np.finfo(s.dtype).eps

    effective_rcond = rcond * s[0]
    numerical_rank = int(np.sum(s > effective_rcond))

    s_pinv = np.where(s > effective_rcond, 1.0 / s, 0.0)
    x = vt.T @ (s_pinv[:, np.newaxis] * u.T) @ rhs

    report: dict = {
        "method": "svd_truncated" if numerical_rank < min(matrix.shape) else "svd",
        "cond": cond,
        "numerical_rank": numerical_rank,
        "rcond": rcond,
        "residual_norm": float(np.linalg.norm(matrix @ x - rhs)),
    }
    return x, report


def report_markdown(report: dict) -> str:
    lines = [
        f"Method: {report.get('method', 'N/A')}",
        f"Condition number: {report.get('cond', 'N/A'):.2e}" if isinstance(report.get('cond'), float) else f"Condition number: {report.get('cond', 'N/A')}",
    ]
    if "numerical_rank" in report:
        lines.append(f"Numerical rank: {report['numerical_rank']}")
    if "residual_norm" in report:
        lines.append(f"Residual ||Ax - b||: {report['residual_norm']:.2e}")
    return "\n".join(lines)


def reconstruction_error(a: ArrayLike, u: np.ndarray, singular_values: np.ndarray, vt: np.ndarray) -> float:
    matrix = _as_matrix(a)
    sigma = np.diag(singular_values)
    return float(np.linalg.norm(matrix - u @ sigma @ vt))


if __name__ == "__main__":
    A = np.array(
        [
            [3.0, 1.0, 1.0],
            [-1.0, 3.0, 1.0],
        ]
    )
    b = np.array([1.0, 2.0])

    U, s, Vt = svd_decompose(A)
    print("U =\n", U)
    print("s =\n", s)
    print("Vt =\n", Vt)
    print("reconstruction error =", reconstruction_error(A, U, s, Vt))
    print("rank-1 approximation =\n", rank_k_approximation(A, 1))
    print("least squares x =", solve_least_squares_svd(A, b))
