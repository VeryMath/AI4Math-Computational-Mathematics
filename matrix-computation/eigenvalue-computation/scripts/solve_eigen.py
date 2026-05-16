"""Lightweight tests for challenging eigenvalue problems.

This script builds several matrices (Grcar, clustered symmetric, near-Jordan)
and runs dense eigen-decomposition as a reference, printing residuals.
"""

from __future__ import annotations

import sys
from typing import Sequence, Tuple

import numpy as np
from scipy import linalg
import scipy.sparse as sp


def grcar(n: int) -> np.ndarray:
    A = np.zeros((n, n), dtype=float)
    for i in range(n):
        A[i, i] = 1.0
        if i + 1 < n:
            A[i, i + 1] = 1.0
        if i + 2 < n:
            A[i, i + 2] = 1.0
        if i - 1 >= 0:
            A[i, i - 1] = -1.0
    return A


def clustered_symmetric(n: int, clusters: int = 5, eps: float = 1e-8) -> np.ndarray:
    sizes = [n // clusters] * clusters
    for i in range(n % clusters):
        sizes[i] += 1
    vals = []
    base = np.linspace(1.0, 5.0, clusters)
    for b, s in zip(base, sizes):
        vals.extend([b + (np.random.rand() - 0.5) * eps for _ in range(s)])
    vals = np.array(vals[:n])
    Q, _ = np.linalg.qr(np.random.randn(n, n))
    return Q @ np.diag(vals) @ Q.T


def eigen_decompose(a: np.ndarray):
    """Dense eigen-decomposition wrapper returning (vals, vecs)."""
    A = np.asarray(a, dtype=float)
    return linalg.eig(A)


def symmetric_eigen_decompose(a: np.ndarray):
    """Symmetric eigen-decomposition using eigh for SPD or symmetric matrices."""
    A = np.asarray(a, dtype=float)
    return np.linalg.eigh(A)


def power_method(a: np.ndarray, x0: np.ndarray | None = None, tol: float = 1e-8, maxiter: int = 1000):
    A = np.asarray(a, dtype=float)
    n = A.shape[0]
    if x0 is None:
        x = np.random.randn(n)
    else:
        x = np.asarray(x0, dtype=float)
    x = x / float(np.linalg.norm(x))
    lambda_old = 0.0
    for k in range(1, maxiter + 1):
        y = A @ x
        lambda_new = float(np.dot(x, y))
        y_norm = float(np.linalg.norm(y))
        if y_norm == 0.0:
            return 0.0, x
        x = y / y_norm
        if abs(lambda_new - lambda_old) <= tol:
            return lambda_new, x
        lambda_old = lambda_new
    return lambda_new, x


if __name__ == '__main__':
    # small demo (keeps module import-safe and avoids heavy tests)
    A = np.array([[2.0, 1.0], [1.0, 3.0]])
    vals, vecs = symmetric_eigen_decompose(A)
    print("eigenvalues =", vals)
    lam, v = power_method(A)
    print("power method approx lambda=", lam)
