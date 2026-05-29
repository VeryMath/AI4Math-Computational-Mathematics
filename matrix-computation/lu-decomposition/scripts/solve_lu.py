"""LU decomposition helpers for the LU decomposition skill."""

from __future__ import annotations

from typing import Sequence

import numpy as np  # pyright: ignore[reportMissingImports]
from scipy.linalg import lu, lu_factor, lu_solve  # pyright: ignore[reportMissingImports]

ArrayLike = Sequence[Sequence[float]] | np.ndarray


def _as_square_matrix(a: ArrayLike) -> np.ndarray:
    matrix = np.asarray(a, dtype=float)
    if matrix.ndim != 2:
        raise ValueError("A must be a 2D array.")
    rows, cols = matrix.shape
    if rows != cols:
        raise ValueError("A must be square for LU decomposition.")
    return matrix


def factorize_lu(a: ArrayLike) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return P, L, U such that A = P @ L @ U (SciPy convention)."""
    matrix = _as_square_matrix(a)
    return lu(matrix)


def solve_lu(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    """Solve A x = b with LU factorization."""
    matrix = _as_square_matrix(a)
    rhs = np.asarray(b, dtype=float)
    lu_matrix, piv = lu_factor(matrix)
    return lu_solve((lu_matrix, piv), rhs)


def robust_solve_lu(a: ArrayLike, b: ArrayLike) -> tuple[np.ndarray, dict]:
    """Robust LU-based solver with condition-number-aware fallback.

    Returns (x, report) where report contains diagnostics.
    """
    matrix = _as_square_matrix(a)
    rhs = np.asarray(b, dtype=float)

    cond = float(np.linalg.cond(matrix))
    report: dict = {"method": "lu", "cond": cond}

    if cond < 1e8:
        x = solve_lu(matrix, rhs)
        report["residual_norm"] = float(np.linalg.norm(matrix @ x - rhs))
        return x, report

    if cond < 1e12:
        row_norms = np.linalg.norm(matrix, axis=1)
        col_norms = np.linalg.norm(matrix, axis=0)
        Dr = np.diag(1.0 / np.where(row_norms == 0, 1.0, row_norms))
        Dc = np.diag(1.0 / np.where(col_norms == 0, 1.0, col_norms))
        A_eq = Dr @ matrix @ Dc
        lu_mat, piv = lu_factor(A_eq)
        x_eq = lu_solve((lu_mat, piv), Dr @ rhs)
        x = Dc @ x_eq
        report["method"] = "equilibrated_lu"
        report["residual_norm"] = float(np.linalg.norm(matrix @ x - rhs))
        return x, report

    x = np.linalg.pinv(matrix) @ rhs
    report["method"] = "svd_fallback"
    report["residual_norm"] = float(np.linalg.norm(matrix @ x - rhs))
    return x, report



def report_markdown(report: dict) -> str:
    lines = [
        f"Method: {report.get('method', 'N/A')}",
        f"Condition number: {report.get('cond', 'N/A'):.2e}" if isinstance(report.get('cond'), float) else f"Condition number: {report.get('cond', 'N/A')}",
    ]
    if "residual_norm" in report:
        lines.append(f"Residual ||Ax - b||: {report['residual_norm']:.2e}")
    if "alpha" in report:
        lines.append(f"Regularization alpha: {report['alpha']}")
    return "\n".join(lines)


def reconstruction_error(a: ArrayLike, p: np.ndarray, l: np.ndarray, u: np.ndarray) -> float:
    """Compute ||A - P L U|| to verify factorization accuracy (SciPy convention A = P @ L @ U)."""
    matrix = np.asarray(a, dtype=float)
    return float(np.linalg.norm(matrix - p @ l @ u))


def determinant_from_lu(a: ArrayLike) -> float:
    p, _, u = factorize_lu(a)
    sign = int(round(float(np.linalg.det(p))))
    return float(sign * np.prod(np.diag(u)))


def inverse_from_lu(a: ArrayLike) -> np.ndarray:
    matrix = _as_square_matrix(a)
    identity = np.eye(matrix.shape[0], dtype=float)
    return solve_lu(matrix, identity)


if __name__ == "__main__":
    A = np.array(
        [
            [2.0, 1.0, 1.0],
            [4.0, -6.0, 0.0],
            [-2.0, 7.0, 2.0],
        ]
    )
    b = np.array([5.0, -2.0, 9.0])

    P, L, U = factorize_lu(A)
    print("P =\n", P)
    print("L =\n", L)
    print("U =\n", U)
    print("reconstruction error =", reconstruction_error(A, P, L, U))
    print("x =", solve_lu(A, b))
