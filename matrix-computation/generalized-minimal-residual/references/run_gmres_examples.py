"""Runnable examples for GMRES skill.

Loads `solve_gmres.py` by path and runs Grcar, convection-diffusion, and near-singular
non-symmetric examples using the skill's `gmres` implementation.
"""

from __future__ import annotations

import importlib.util
import os
import numpy as np
from scipy.sparse import diags


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ROOT = os.path.join(os.path.dirname(__file__), '..', 'scripts')
ROOT = os.path.abspath(ROOT)
MOD_PATH = os.path.join(ROOT, 'solve_gmres.py')

mod = load_module(MOD_PATH, 'solve_gmres')


def grcar(n: int):
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


def convection_diffusion(n: int, eps: float = 1e-2):
    main = (2.0 + eps) * np.ones(n)
    lower = -1.0 * np.ones(n - 1)
    upper = (-1.0 + 0.5) * np.ones(n - 1)
    A = diags([main, lower, upper], [0, -1, 1], shape=(n, n), format='csr')
    return A


def main():
    # Grcar
    A = grcar(120)
    b = np.ones(120)
    x, info = mod.gmres(A, b, restart=40, tol=1e-8, maxiter=200)
    print('Grcar(120):', info, 'residual=', np.linalg.norm(A @ x - b))

    # Convection-diffusion
    A2 = convection_diffusion(200)
    b2 = np.ones(A2.shape[0])
    x, info = mod.gmres(A2, b2, restart=50, tol=1e-8, maxiter=500)
    print('ConvectionDiffusion(200):', info, 'residual=', np.linalg.norm(A2 @ x - b2))

    # Near-singular nonsymmetric
    n = 200
    D = diags([np.concatenate((np.ones(n - 1), np.array([1e-12])))], [0], shape=(n, n), format='csr')
    D = D.toarray()
    for i in range(n - 1):
        D[i, i + 1] = 1e-6
    b3 = np.ones(n)
    x, info = mod.gmres(D, b3, restart=50, tol=1e-10, maxiter=500)
    print('NearSingularNonsymm(200):', info, 'residual=', np.linalg.norm(D @ x - b3))


if __name__ == '__main__':
    main()
