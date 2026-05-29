"""Matrix norm computation helpers for the matrix norm skill."""

from __future__ import annotations

from typing import Sequence

import numpy as np  # pyright: ignore[reportMissingImports]

ArrayLike = Sequence[Sequence[float]] | np.ndarray


def _as_matrix(a: ArrayLike) -> np.ndarray:
    matrix = np.asarray(a, dtype=float)
    if matrix.ndim != 2:
        raise ValueError("A must be a 2D array.")
    return matrix


def frobenius_norm(a: ArrayLike) -> float:
    """Compute the Frobenius norm ||A||_F = sqrt(sum(|a_ij|^2))."""
    matrix = _as_matrix(a)
    return float(np.linalg.norm(matrix, ord="fro"))


def spectral_norm(a: ArrayLike) -> float:
    """Compute the spectral norm (2-norm) ||A||_2 = sigma_max(A)."""
    matrix = _as_matrix(a)
    return float(np.linalg.norm(matrix, ord=2))


def norm_1(a: ArrayLike) -> float:
    """Compute the 1-norm ||A||_1 = max_j sum_i |a_ij| (maximum column sum)."""
    matrix = _as_matrix(a)
    return float(np.linalg.norm(matrix, ord=1))


def norm_infinity(a: ArrayLike) -> float:
    """Compute the infinity-norm ||A||_inf = max_i sum_j |a_ij| (maximum row sum)."""
    matrix = _as_matrix(a)
    return float(np.linalg.norm(matrix, ord=np.inf))


def nuclear_norm(a: ArrayLike) -> float:
    """Compute the nuclear norm ||A||_* = sum_i sigma_i(A) (sum of singular values)."""
    matrix = _as_matrix(a)
    return float(np.linalg.norm(matrix, ord="nuc"))


def p_norm(a: ArrayLike, p: float) -> float:
    """Compute the p-norm ||A||_p = max_{||x||_p=1} ||Ax||_p."""
    matrix = _as_matrix(a)
    return float(np.linalg.norm(matrix, ord=p))


def condition_number(a: ArrayLike, p: float | str | None = None) -> float:
    """Compute the condition number kappa(A) = ||A|| * ||A^(-1)||.

    Args:
        a: Input matrix (must be square)
        p: Norm type to use (2, 1, np.inf, 'fro', etc.). Defaults to 2-norm.

    Returns:
        Condition number, or inf if matrix is singular.
    """
    matrix = _as_matrix(a)
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Condition number requires a square matrix.")
    if p is None:
        p = 2
    return float(np.linalg.cond(matrix, p=p))


def matrix_distance_frobenius(a: ArrayLike, b: ArrayLike) -> float:
    """Compute Frobenius distance between two matrices ||A - B||_F."""
    matrix_a = _as_matrix(a)
    matrix_b = _as_matrix(b)
    if matrix_a.shape != matrix_b.shape:
        raise ValueError("Matrices must have the same shape.")
    return float(np.linalg.norm(matrix_a - matrix_b, ord="fro"))


def matrix_distance_spectral(a: ArrayLike, b: ArrayLike) -> float:
    """Compute spectral distance between two matrices ||A - B||_2."""
    matrix_a = _as_matrix(a)
    matrix_b = _as_matrix(b)
    if matrix_a.shape != matrix_b.shape:
        raise ValueError("Matrices must have the same shape.")
    return float(np.linalg.norm(matrix_a - matrix_b, ord=2))


def compute_all_norms(a: ArrayLike) -> dict[str, float]:
    """Compute all common norms and return as a dictionary."""
    matrix = _as_matrix(a)
    norms: dict[str, float] = {
        "frobenius": frobenius_norm(matrix),
        "spectral": spectral_norm(matrix),
        "1-norm": norm_1(matrix),
        "infinity-norm": norm_infinity(matrix),
        "nuclear": nuclear_norm(matrix),
    }
    # Add condition number if square
    if matrix.shape[0] == matrix.shape[1]:
        norms["condition_number_2"] = condition_number(matrix, p=2)
    return norms


def report_markdown(norms: dict[str, float]) -> str:
    """Generate a markdown report from computed norms."""
    lines = ["### Matrix Norms"]
    lines.append("| Norm Type | Value |")
    lines.append("|-----------|-------|")
    for name, value in norms.items():
        lines.append(f"| {name} | {value:.6e} |")
    return "\n".join(lines)


def norm_comparison_table(a: ArrayLike) -> str:
    """Generate a comparison table of all norms with theoretical bounds."""
    norms = compute_all_norms(a)
    fro = norms["frobenius"]
    spec = norms["spectral"]
    nuc = norms["nuclear"]
    m, n = _as_matrix(a).shape
    min_dim = min(m, n)

    lines = ["### Norm Comparison and Bounds"]
    lines.append(f"| Property | Value |")
    lines.append(f"|----------|-------|")
    lines.append(f"| Frobenius norm ||A||_F | {fro:.6e} |")
    lines.append(f"| Spectral norm ||A||_2 | {spec:.6e} |")
    lines.append(f"| Nuclear norm ||A||_* | {nuc:.6e} |")
    lines.append(f"| sqrt(min(m,n)) * ||A||_2 | {np.sqrt(min_dim) * spec:.6e} |")
    lines.append(f"| ||A||_F <= sqrt(min(m,n)) * ||A||_2 | {fro <= np.sqrt(min_dim) * spec} |")
    lines.append(f"| ||A||_2 <= ||A||_F | {spec <= fro} |")
    lines.append(f"| ||A||_* <= sqrt(min(m,n)) * ||A||_F | {nuc <= np.sqrt(min_dim) * fro} |")
    return "\n".join(lines)


if __name__ == "__main__":
    # Example matrices
    A = np.array(
        [
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0],
        ]
    )

    B = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )

    print("Matrix A:")
    print(A)
    print("\nMatrix B:")
    print(B)

    print("\n" + "=" * 50)
    print("Frobenius norms:")
    print(f"||A||_F = {frobenius_norm(A):.6e}")
    print(f"||B||_F = {frobenius_norm(B):.6e}")

    print("\nSpectral norms:")
    print(f"||A||_2 = {spectral_norm(A):.6e}")
    print(f"||B||_2 = {spectral_norm(B):.6e}")

    print("\n1-norm (max column sum):")
    print(f"||A||_1 = {norm_1(A):.6e}")
    print(f"||B||_1 = {norm_1(B):.6e}")

    print("\nInfinity-norm (max row sum):")
    print(f"||A||_inf = {norm_infinity(A):.6e}")
    print(f"||B||_inf = {norm_infinity(B):.6e}")

    print("\nNuclear norm:")
    print(f"||A||_* = {nuclear_norm(A):.6e}")
    print(f"||B||_* = {nuclear_norm(B):.6e}")

    print("\nCondition number (2-norm):")
    print(f"kappa(A) = {condition_number(A, p=2):.6e}")
    print(f"kappa(B) = {condition_number(B, p=2):.6e}")

    print("\nDistance between A and B:")
    print(f"||A - B||_F = {matrix_distance_frobenius(A, B):.6e}")
    print(f"||A - B||_2 = {matrix_distance_spectral(A, B):.6e}")

    print("\n" + "=" * 50)
    print(norm_comparison_table(A))
