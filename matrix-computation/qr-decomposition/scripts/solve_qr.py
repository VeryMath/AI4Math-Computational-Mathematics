"""QR helpers for the QR decomposition skill."""

from __future__ import annotations

from typing import Sequence

import numpy as np  # pyright: ignore[reportMissingImports]

ArrayLike = Sequence[Sequence[float]] | np.ndarray


def _as_matrix(a: ArrayLike) -> np.ndarray:
    matrix = np.asarray(a, dtype=float)
    if matrix.ndim != 2:
        raise ValueError("A must be a 2D array.")
    return matrix


def qr_decompose(a: ArrayLike, mode: str = "reduced") -> tuple[np.ndarray, np.ndarray]:
    """Return Q and R matrices from QR decomposition.

    Args:
        a: Input matrix.
        mode: 'reduced', 'complete', 'r', or 'raw'.
              'reduced' returns economic QR (default).
              'complete' returns full Q (m x m).
              'r' returns only R.
              'raw' returns raw Householder factors.

    Returns:
        Tuple (Q, R) where Q is orthogonal/semi-orthogonal and R is upper triangular.
    """
    matrix = _as_matrix(a)
    return np.linalg.qr(matrix, mode=mode)  # type: ignore[reportCallIssue]


def qr_decompose_pivoting(a: ArrayLike) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """QR decomposition with column pivoting (rank-revealing).

    Returns (Q, R, P) where P is the permutation vector.
    """
    from scipy import linalg
    matrix = _as_matrix(a)
    Q, R, P = linalg.qr(matrix, pivoting=True, mode="economic")  # type: ignore[reportAssignmentType]
    return Q, R, P  # type: ignore[reportReturnType]


def solve_least_squares_qr(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    """Solve least squares min ||Ax - b|| using QR decomposition."""
    matrix = _as_matrix(a)
    rhs = np.asarray(b, dtype=float)
    Q, R = qr_decompose(matrix, mode="reduced")
    return np.linalg.solve(R, Q.T @ rhs)


def estimate_rank_qr(a: ArrayLike, tol: float | None = None) -> int:
    """Estimate numerical rank using QR with column pivoting."""
    Q, R, P = qr_decompose_pivoting(a)
    diag_r = np.abs(np.diag(R))
    if tol is None:
        tol = max(R.shape[0], R.shape[1]) * np.finfo(R.dtype).eps * diag_r[0]
    return int(np.sum(diag_r > tol))


def orthogonal_projection(q: np.ndarray) -> np.ndarray:
    """Return projection matrix onto the column space of Q."""
    return q @ q.T


def reconstruct_from_qr(Q: np.ndarray, R: np.ndarray) -> np.ndarray:
    """Reconstruct original matrix from Q and R."""
    return Q @ R


def orthogonal_residual(Q: np.ndarray) -> float:
    """Return ||Q^T Q - I|| as a measure of orthogonality."""
    m, k = Q.shape
    if k < m:
        return float(np.linalg.norm(Q.T @ Q - np.eye(k)))
    return float(np.linalg.norm(Q.T @ Q - np.eye(m)))


def robust_solve_qr(a: ArrayLike, b: ArrayLike, pivoting: bool = False) -> tuple[np.ndarray, dict]:
    """Robust QR-based solver with diagnostics.

    Returns (x, report) where report contains diagnostics.
    """
    matrix = _as_matrix(a)
    rhs = np.asarray(b, dtype=float)

    if pivoting:
        Q, R, P = qr_decompose_pivoting(matrix)
        diag_r = np.abs(np.diag(R))
        tol = max(matrix.shape) * np.finfo(R.dtype).eps * diag_r[0]
        rank = int(np.sum(diag_r > tol))
        method = "qr_pivoting"
    else:
        Q, R = qr_decompose(matrix, mode="reduced")
        diag_r = np.abs(np.diag(R))
        tol = max(matrix.shape) * np.finfo(R.dtype).eps * diag_r[0]
        rank = int(np.sum(diag_r > tol))
        method = "qr"

    if rank < min(matrix.shape):
        rank_deficient = True
        # Truncated least squares
        k = rank
        Qk = Q[:, :k]
        Rk = R[:k, :k]  # Use square submatrix for solve
        x_trunc = np.linalg.solve(Rk, Qk.T @ rhs)
        # Pad with zeros to match original column count
        x = np.zeros(matrix.shape[1], dtype=float)
        x[:k] = x_trunc
    else:
        rank_deficient = False
        x = np.linalg.solve(R, Q.T @ rhs)

    report: dict = {
        "method": method,
        "rank_estimate": rank,
        "rank_deficient": rank_deficient,
        "orthogonality_error": orthogonal_residual(Q),
        "reconstruction_error": float(np.linalg.norm(matrix - Q @ R)),
        "residual_norm": float(np.linalg.norm(matrix @ x - rhs)),
    }
    return x, report


def report_markdown(report: dict) -> str:
    lines = [
        f"Method: {report.get('method', 'N/A')}",
        f"Rank estimate: {report.get('rank_estimate', 'N/A')}",
        f"Rank deficient: {report.get('rank_deficient', 'N/A')}",
        f"Orthogonality error ||Q^T Q - I||: {report.get('orthogonality_error', 'N/A'):.2e}",
        f"Reconstruction error ||A - QR||: {report.get('reconstruction_error', 'N/A'):.2e}",
        f"Residual ||Ax - b||: {report.get('residual_norm', 'N/A'):.2e}",
    ]
    return "\n".join(lines)


def qr_gram_schmidt(a: ArrayLike, modified: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """Classical or modified Gram-Schmidt orthogonalization.

    Args:
        a: Input matrix.
        modified: Use modified Gram-Schmidt (default) for better numerical stability.

    Returns:
        Tuple (Q, R) where Q is orthonormal and R is upper triangular.
    """
    matrix = _as_matrix(a)
    m, n = matrix.shape
    Q = np.zeros((m, n), dtype=float)
    R = np.zeros((n, n), dtype=float)

    for j in range(n):
        v = matrix[:, j].copy()
        if modified:
            for i in range(j):
                R[i, j] = np.dot(Q[:, i], v)
                v = v - R[i, j] * Q[:, i]
        else:
            for i in range(j):
                R[i, j] = np.dot(Q[:, i], matrix[:, j])
                v = v - R[i, j] * Q[:, i]
        R[j, j] = np.linalg.norm(v)
        Q[:, j] = v / R[j, j] if R[j, j] > 1e-15 else v

    return Q, R


def hilbert(n: int) -> np.ndarray:
    """Return the n x n Hilbert matrix."""
    return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)], dtype=float)


if __name__ == "__main__":
    A = np.array(
        [
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 10.0],
        ]
    )
    b = np.array([1.0, 2.0, 3.0])

    Q, R = qr_decompose(A)
    print("Q =\n", Q)
    print("R =\n", R)
    print("orthogonality error =", orthogonal_residual(Q))
    print("reconstruction error =", np.linalg.norm(A - Q @ R))

    x, report = robust_solve_qr(A, b)
    print("\nLeast squares x =", x)
    print(report_markdown(report))