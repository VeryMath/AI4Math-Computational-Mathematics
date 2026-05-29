"""Runnable examples for CG skill.

Loads `solve_cg.py` by path and runs Hilbert, Poisson2D, and scaled diagonal examples,
calling the skill's `conjugate_gradient` where appropriate.
"""

from __future__ import annotations

import importlib.util
import os
import numpy as np
import scipy.sparse as sp
from scipy.sparse import diags
from scipy import linalg


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ROOT = os.path.join(os.path.dirname(__file__), '..', 'scripts')
ROOT = os.path.abspath(ROOT)
MOD_PATH = os.path.join(ROOT, 'solve_cg.py')

mod = load_module(MOD_PATH, 'solve_cg')


def hilbert(n: int):
    i = np.arange(1, n + 1)
    return np.array([[1.0 / (ii + jj - 1) for jj in i] for ii in i], dtype=float)


def poisson2d(n: int):
    N = n * n
    main = 4.0 * np.ones(N)
    off = -1.0 * np.ones(N)
    A = diags([main, off, off, off, off], [0, -1, 1, -n, n], shape=(N, N), format='csr')
    return A


def scaled_diag(n: int, scale: float = 1e-12):
    vals = np.concatenate((np.ones(n - 1), np.array([scale])))
    return diags(vals, 0, format='csr')


def run_cg_on(A, b, label):
    x, info = mod.conjugate_gradient(A, b, tol=1e-8, maxiter=1000)
    res = np.linalg.norm((A @ x) - b)
    print(f"{label}: info={info}, residual={res:.2e}")


def main():
    # Hilbert (dense small)
    H = hilbert(30)
    b = np.ones(30)
    # use dense direct solve for reference
    x_ref = linalg.solve(H, b)
    x, info = mod.conjugate_gradient(H, b, tol=1e-10, maxiter=1000)
    print('Hilbert(30): residual vs direct =', np.linalg.norm(x - x_ref))

    # Poisson 2D
    A = poisson2d(20)
    b = np.ones(A.shape[0])
    run_cg_on(A, b, 'Poisson2D(20)')

    # Scaled diagonal
    D = scaled_diag(200, scale=1e-12)
    b = np.ones(200)
    run_cg_on(D, b, 'ScaledDiag(200)')


if __name__ == '__main__':
    main()
