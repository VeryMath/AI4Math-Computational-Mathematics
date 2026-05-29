"""Runnable examples for eigen-decomposition skill.

Loads the skill module by file path and runs three representative examples:
- Grcar (non-normal)
- Clustered symmetric
- Near-Jordan (near-defective)

This script is intended to be run manually for verification.
"""

from __future__ import annotations

import importlib.util
import os
import numpy as np
from scipy import linalg


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ROOT = os.path.join(os.path.dirname(__file__), '..', 'scripts')
ROOT = os.path.abspath(ROOT)
MOD_PATH = os.path.join(ROOT, 'solve_eigen.py')

mod = load_module(MOD_PATH, 'solve_eigen')


def residuals(A, vals, vecs, k=5):
    res = []
    for i in range(min(k, len(vals))):
        v = vecs[:, i]
        lam = vals[i]
        res.append(np.linalg.norm(A @ v - lam * v))
    return res


def main():
    np.random.seed(42)
    # Grcar
    A = mod.grcar(80)
    vals, vecs = linalg.eig(A)
    print('Grcar(80) sample eigen residuals:', residuals(A, vals, vecs))

    # Clustered symmetric
    B = mod.clustered_symmetric(80, clusters=6, eps=1e-10)
    w, v = np.linalg.eigh(B)
    print('ClusteredSymmetric(80) sample residuals:', residuals(B, w, v))

    # Near-Jordan
    J = np.diag(np.linspace(1.0, 1.0 + 1e-6, 30))
    for i in range(29):
        J[i, i + 1] = 1e-7
    vals, vecs = linalg.eig(J)
    print('NearJordan(30) sample residuals:', residuals(J, vals, vecs))


if __name__ == '__main__':
    main()
