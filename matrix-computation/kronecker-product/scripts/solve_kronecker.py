"""Kronecker product computation helpers for the Kronecker product skill."""

from __future__ import annotations

from typing import Sequence

import numpy as np  # pyright: ignore[reportMissingImports]

ArrayLike = Sequence[Sequence[float]] | np.ndarray


def _as_matrix(a: ArrayLike) -> np.ndarray:
    matrix = np.asarray(a, dtype=float)
    if matrix.ndim != 2:
        raise ValueError("Input must be a 2D array.")
    return matrix


def kronecker_product(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    """Compute the Kronecker product A ⊗ B.

    For A (m×n) and B (p×q), returns (mp × nq) matrix.
    """
    matrix_a = _as_matrix(a)
    matrix_b = _as_matrix(b)
    return np.kron(matrix_a, matrix_b)


def kronecker_sum(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    """Compute the Kronecker sum A ⊕ B = A ⊗ I + I ⊗ A.

    Args:
        a: Square matrix A (m×m)
        b: Square matrix B (n×n)

    Returns:
        Kronecker sum (mn × mn)
    """
    matrix_a = _as_matrix(a)
    matrix_b = _as_matrix(b)

    if matrix_a.shape[0] != matrix_a.shape[1]:
        raise ValueError("A must be square for Kronecker sum.")
    if matrix_b.shape[0] != matrix_b.shape[1]:
        raise ValueError("B must be square for Kronecker sum.")

    m, n = matrix_a.shape[0], matrix_b.shape[0]
    return np.kron(matrix_a, np.eye(n)) + np.kron(np.eye(m), matrix_b)


def verify_associativity(a: ArrayLike, b: ArrayLike, c: ArrayLike) -> bool:
    """Verify associativity: (A ⊗ B) ⊗ C = A ⊗ (B ⊗ C)."""
    matrix_a = _as_matrix(a)
    matrix_b = _as_matrix(b)
    matrix_c = _as_matrix(c)

    left = np.kron(np.kron(matrix_a, matrix_b), matrix_c)
    right = np.kron(matrix_a, np.kron(matrix_b, matrix_c))
    return np.allclose(left, right)


def verify_transpose(a: ArrayLike, b: ArrayLike) -> bool:
    """Verify (A ⊗ B)^T = A^T ⊗ B^T."""
    matrix_a = _as_matrix(a)
    matrix_b = _as_matrix(b)

    left = np.kron(matrix_a, matrix_b).T
    right = np.kron(matrix_a.T, matrix_b.T)
    return np.allclose(left, right)


def verify_product_rule(a: ArrayLike, b: ArrayLike, c: ArrayLike, d: ArrayLike) -> bool:
    """Verify (A ⊗ B)(C ⊗ D) = (AC) ⊗ (BD) when dimensions match."""
    matrix_a = _as_matrix(a)
    matrix_b = _as_matrix(b)
    matrix_c = _as_matrix(c)
    matrix_d = _as_matrix(d)

    # Check dimension compatibility
    if matrix_a.shape[1] != matrix_c.shape[0]:
        raise ValueError("A and C must have compatible dimensions.")
    if matrix_b.shape[1] != matrix_d.shape[0]:
        raise ValueError("B and D must have compatible dimensions.")

    left = np.kron(matrix_a, matrix_b) @ np.kron(matrix_c, matrix_d)
    right = np.kron(matrix_a @ matrix_c, matrix_b @ matrix_d)
    return np.allclose(left, right)


def verify_inverse(a: ArrayLike, b: ArrayLike) -> bool:
    """Verify (A ⊗ B)^{-1} = A^{-1} ⊗ B^{-1} for invertible matrices."""
    matrix_a = _as_matrix(a)
    matrix_b = _as_matrix(b)

    if matrix_a.shape[0] != matrix_a.shape[1]:
        raise ValueError("A must be square.")
    if matrix_b.shape[0] != matrix_b.shape[1]:
        raise ValueError("B must be square.")

    left = np.linalg.inv(np.kron(matrix_a, matrix_b))
    right = np.kron(np.linalg.inv(matrix_a), np.linalg.inv(matrix_b))
    return np.allclose(left, right)


def rank_kron(a: ArrayLike, b: ArrayLike) -> int:
    """Compute rank(A ⊗ B) = rank(A) * rank(B)."""
    matrix_a = _as_matrix(a)
    matrix_b = _as_matrix(b)

    rank_a = int(np.linalg.matrix_rank(matrix_a))
    rank_b = int(np.linalg.matrix_rank(matrix_b))
    return rank_a * rank_b


def determinant_kron(a: ArrayLike, b: ArrayLike) -> float:
    """Compute det(A ⊗ B) = det(A)^n * det(B)^m.

    Args:
        a: Square matrix A (m×m)
        b: Square matrix B (n×n)
    """
    matrix_a = _as_matrix(a)
    matrix_b = _as_matrix(b)

    if matrix_a.shape[0] != matrix_a.shape[1]:
        raise ValueError("A must be square.")
    if matrix_b.shape[0] != matrix_b.shape[1]:
        raise ValueError("B must be square.")

    m, n = matrix_a.shape[0], matrix_b.shape[0]
    det_a = float(np.linalg.det(matrix_a))
    det_b = float(np.linalg.det(matrix_b))
    return (det_a ** n) * (det_b ** m)


def trace_kron(a: ArrayLike, b: ArrayLike) -> float:
    """Compute tr(A ⊗ B) = tr(A) * tr(B)."""
    matrix_a = _as_matrix(a)
    matrix_b = _as_matrix(b)

    if matrix_a.shape[0] != matrix_a.shape[1]:
        raise ValueError("A must be square.")
    if matrix_b.shape[0] != matrix_b.shape[1]:
        raise ValueError("B must be square.")

    trace_a = float(np.trace(matrix_a))
    trace_b = float(np.trace(matrix_b))
    return trace_a * trace_b


def solve_kronecker_system(a: ArrayLike, b: ArrayLike, c: ArrayLike) -> np.ndarray:
    """Solve (A ⊗ B)x = c for x using vectorization.

    For equation (A ⊗ B)vec(X) = vec(C), finds X.
    """
    matrix_a = _as_matrix(a)
    matrix_b = _as_matrix(b)
    matrix_c = _as_matrix(c)

    kron_mat = np.kron(matrix_a, matrix_b)
    vec_c = matrix_c.ravel(order='F')
    vec_x = np.linalg.solve(kron_mat, vec_c)
    m, n = matrix_c.shape
    return vec_x.reshape((m, n), order='F')


def vec_operator(a: ArrayLike) -> np.ndarray:
    """Stack columns of matrix into a vector (column-wise vectorization)."""
    matrix = _as_matrix(a)
    return matrix.ravel(order='F')


def report_markdown(result: dict) -> str:
    """Generate a markdown report from Kronecker product results."""
    lines = ["### Kronecker Product Results"]
    for key, value in result.items():
        if isinstance(value, np.ndarray):
            lines.append(f"**{key}**: shape = {value.shape}")
        elif isinstance(value, float):
            lines.append(f"**{key}**: {value:.6e}")
        else:
            lines.append(f"**{key}**: {value}")
    return "\n".join(lines)


if __name__ == "__main__":
    # Example matrices
    A = np.array([
        [1.0, 2.0],
        [3.0, 4.0],
    ])

    B = np.array([
        [0.0, 5.0],
        [6.0, 7.0],
    ])

    C = np.array([
        [1.0, 0.0],
        [0.0, 1.0],
    ])

    print("Matrix A:")
    print(A)
    print("\nMatrix B:")
    print(B)

    print("\n" + "=" * 50)
    print("Kronecker Product A (x) B:")
    kron_AB = kronecker_product(A, B)
    print(kron_AB)
    print(f"Shape: {kron_AB.shape}")

    print("\n" + "=" * 50)
    print("Kronecker Sum A (+) B:")
    kron_sum = kronecker_sum(A, B)
    print(kron_sum)
    print(f"Shape: {kron_sum.shape}")

    print("\n" + "=" * 50)
    print("Property Verifications:")
    print(f"Associativity (A,B,C): {verify_associativity(A, B, C)}")
    print(f"Transpose property: {verify_transpose(A, B)}")
    print(f"Product rule (A,B,A,B): {verify_product_rule(A, B, A, B)}")
    print(f"Inverse property: {verify_inverse(A, C)}")

    print("\n" + "=" * 50)
    print("Derived Properties:")
    print(f"rank(A (x) B) = {rank_kron(A, B)}")
    print(f"det(A (x) B) = {determinant_kron(A, B):.6f}")
    print(f"tr(A (x) B) = {trace_kron(A, B):.6f}")
    print(f"tr(A) * tr(B) = {np.trace(A) * np.trace(B):.6f}")
