"""Cholesky decomposition helpers for Cholesky decomposition skill."""

from __future__ import annotations

from typing import Sequence

import numpy as np  # pyright: ignore[reportMissingImports]
from scipy.linalg import cho_factor, cho_solve  # pyright: ignore[reportMissingImports]

ArrayLike = Sequence[Sequence[float]] | np.ndarray


def _as_square_matrix(a: ArrayLike) -> np.ndarray:
    matrix = np.asarray(a, dtype=float)
    if matrix.ndim != 2:
        raise ValueError("A must be a 2D array.")
    rows, cols = matrix.shape
    if rows != cols:
        raise ValueError("A must be square for Cholesky decomposition.")
    return matrix


def is_symmetric(a: ArrayLike, tol: float = 1e-10) -> bool:
    matrix = _as_square_matrix(a)
    return bool(np.allclose(matrix, matrix.T, atol=tol, rtol=tol))


def is_spd(a: ArrayLike, tol: float = 1e-10) -> bool:
    matrix = _as_square_matrix(a)
    if not is_symmetric(matrix, tol=tol):
        return False
    try:
        np.linalg.cholesky(matrix)
    except np.linalg.LinAlgError:
        return False
    return True


def factorize_cholesky(a: ArrayLike, lower: bool = True) -> np.ndarray:
    """Return the Cholesky factor L or R."""
    matrix = _as_square_matrix(a)
    factor = np.linalg.cholesky(matrix)
    return factor if lower else factor.T


def solve_cholesky(a: ArrayLike, b: ArrayLike, lower: bool = True) -> np.ndarray:
    """Solve A x = b for SPD A."""
    matrix = _as_square_matrix(a)
    rhs = np.asarray(b, dtype=float)
    factor, lower_flag = cho_factor(matrix, lower=lower, check_finite=True)
    return cho_solve((factor, lower_flag), rhs)


def robust_solve_cholesky(a: ArrayLike, b: ArrayLike, alpha: float | None = None) -> tuple[np.ndarray, dict]:
    """Robust Cholesky solver with condition-number diagnostics and Tikhonov fallback.

    Returns (x, report) where report contains diagnostics.
    """
    matrix = _as_square_matrix(a)
    rhs = np.asarray(b, dtype=float)

    cond = float(np.linalg.cond(matrix))
    report: dict = {"method": "cholesky", "cond": cond}

    if cond < 1e12:
        x = solve_cholesky(matrix, rhs)
        report["residual_norm"] = float(np.linalg.norm(matrix @ x - rhs))
        return x, report

    if alpha is None:
        alpha = 1e-8

    A_reg = matrix + alpha * np.eye(matrix.shape[0])
    report["method"] = "tikhonov"
    report["alpha"] = alpha
    report["cond_regularized"] = float(np.linalg.cond(A_reg))

    try:
        x = solve_cholesky(A_reg, rhs)
        report["residual_norm"] = float(np.linalg.norm(A_reg @ x - rhs))
        return x, report
    except np.linalg.LinAlgError:
        x = np.linalg.pinv(matrix) @ rhs
        report["method"] = "svd_fallback"
        report["residual_norm"] = float(np.linalg.norm(matrix @ x - rhs))
        return x, report


def report_markdown(report: dict) -> str:
    lines = [
        f"Method: {report.get('method', 'N/A')}",
        f"Condition number: {report.get('cond', 'N/A'):.2e}" if isinstance(report.get('cond'), float) else f"Condition number: {report.get('cond', 'N/A')}",
    ]
    if "alpha" in report:
        lines.append(f"Regularization alpha: {report['alpha']}")
    if "residual_norm" in report:
        lines.append(f"Residual ||Ax - b||: {report['residual_norm']:.2e}")
    return "\n".join(lines)


def reconstruction_error(a: ArrayLike, factor: np.ndarray, lower: bool = True) -> float:
    matrix = np.asarray(a, dtype=float)
    if lower:
        return float(np.linalg.norm(matrix - factor @ factor.T))
    else:
        return float(np.linalg.norm(matrix - factor.T @ factor))


if __name__ == "__main__":
    A = np.array(
        [
            [25.0, 15.0, -5.0],
            [15.0, 18.0, 0.0],
            [-5.0, 0.0, 11.0],
        ]
    )
    b = np.array([1.0, 2.0, 3.0])

    L = factorize_cholesky(A)
    print("L =\n", L)
    print("reconstruction error =", reconstruction_error(A, L))
    print("x =", solve_cholesky(A, b))
