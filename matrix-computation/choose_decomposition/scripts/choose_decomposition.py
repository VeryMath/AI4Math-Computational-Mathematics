"""Top-level chooser to pick decomposition method and solve using skills.

Provides:
- choose_decomposition(A, b=None): recommends method and reason
- demonstrate_choice_and_solve(A, b): picks method, calls corresponding skill solver and returns (x, report, choice)

The chooser uses simple heuristics based on shape, symmetry, SPD check, condition number and numerical rank.
"""
from __future__ import annotations

import importlib.util
import os
import sys
from typing import Any

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

# helper to load skill script modules

def _load_module(name: str, rel_path: str):
    path = os.path.join(ROOT, rel_path)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module spec for '{path}'")
    mod = importlib.util.module_from_spec(spec)
    # spec.loader is not None here
    spec.loader.exec_module(mod)  # type: ignore[attr-defined]
    return mod

# Lazy load skill modules when needed. If loading fails (e.g. broken scipy),
# we'll fall back to simple numpy-based implementations where possible.
_MODULE_PATHS = {
    'cholesky': os.path.join('matrix-computation', 'cholesky-decomposition', 'scripts', 'solve_cholesky.py'),
    'lu': os.path.join('matrix-computation', 'lu-decomposition', 'scripts', 'solve_lu.py'),
    'qr': os.path.join('matrix-computation', 'qr-decomposition', 'scripts', 'solve_qr.py'),
    'svd': os.path.join('matrix-computation', 'svd-decomposition', 'scripts', 'solve_svd.py'),
}


def _try_load_skill(name: str):
    try:
        return _load_module(f'skill_{name}', os.path.join('matrix-computation', f'{name}-decomposition'.replace('_', '-'), 'scripts', f'solve_{name}.py'))
    except Exception:
        # attempt using explicit mapping
        try:
            return _load_module(f'skill_{name}', _MODULE_PATHS[name])
        except Exception:
            return None


def _analyze(A: np.ndarray) -> dict:
    A = np.asarray(A, dtype=float)
    if A.ndim != 2:
        raise ValueError("A must be 2D")
    m, n = A.shape
    symmetric = m == n and np.allclose(A, A.T, atol=1e-10, rtol=1e-10)
    cond = float(np.linalg.cond(A)) if A.size else float('inf')
    rank = int(np.linalg.matrix_rank(A))
    is_spd = False
    if symmetric:
        try:
            np.linalg.cholesky(A)
            is_spd = True
        except np.linalg.LinAlgError:
            is_spd = False
    return {
        'shape': (m, n),
        'symmetric': symmetric,
        'is_spd': is_spd,
        'cond': cond,
        'rank': rank,
    }


def choose_decomposition(A: Any, b: Any = None) -> dict:
    """Recommend decomposition and reasoning.

    Returns dict with keys: method ('cholesky'|'lu'|'qr'|'svd'), reason, info
    """
    A = np.asarray(A, dtype=float)
    info = _analyze(A)
    m, n = info['shape']
    cond = info['cond']
    is_spd = info['is_spd']

    # Heuristic decision rules
    if m != n:
        if m > n:  # overdetermined
            if cond < 1e12:
                reason = f'超定系统（m>n），条件数适中（{cond:.2e}），优先 QR（快速且稳定）'
                return {'method': 'qr', 'reason': reason, 'info': info}
            # underdetermined or very ill-conditioned
        reason = '非方阵，使用 SVD（最稳健的长方形与最小二乘方法）'
        return {'method': 'svd', 'reason': reason, 'info': info}

    # square matrix
    if is_spd:
        if cond < 1e12:
            reason = f'SPD 且 condition number 较小（{cond:.2e}），优先 Cholesky'
            return {'method': 'cholesky', 'reason': reason, 'info': info}
        if cond < 1e16:
            reason = f'SPD 但较病态（{cond:.2e}），尝试 Cholesky + 正则化'
            return {'method': 'cholesky_tikhonov', 'reason': reason, 'info': info}
        reason = f'SPD 但极病态（{cond:.2e}），回退到 SVD 更稳健'
        return {'method': 'svd', 'reason': reason, 'info': info}

    # not SPD
    if cond < 1e12:
        reason = f'方阵但非 SPD，condition 数合理（{cond:.2e}），使用 LU'
        return {'method': 'lu', 'reason': reason, 'info': info}
    if cond < 1e15:
        reason = f'方阵但非 SPD，较病态（{cond:.2e}），使用 QR 更稳定'
        return {'method': 'qr', 'reason': reason, 'info': info}
    reason = f'方阵但病态（{cond:.2e}），使用 SVD 截断/伪逆'
    return {'method': 'svd', 'reason': reason, 'info': info}


def demonstrate_choice_and_solve(A: Any, b: Any):
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)
    choice = choose_decomposition(A, b)
    method = choice['method']
    # Attempt to load the skill module; if it's not available (or importing it
    # fails), fall back to a simple numpy-based solver.
    mod = _try_load_skill('cholesky') if method.startswith('cholesky') else None

    if method == 'cholesky' or method == 'cholesky_tikhonov':
        if mod is not None:
            alpha = None if method == 'cholesky' else 1e-8
            x, report = mod.robust_solve_cholesky(A, b, alpha=alpha)
            report = {'chosen': method, **report}
            return x, report, choice

        # numpy fallback
        try:
            L = np.linalg.cholesky(A)
            y = np.linalg.solve(L, b)
            x = np.linalg.solve(L.T, y)
            report = {'chosen': 'cholesky_numpy', 'method': 'cholesky_numpy', 'residual_norm': float(np.linalg.norm(A @ x - b)), 'cond': float(np.linalg.cond(A))}
            return x, report, choice
        except np.linalg.LinAlgError:
            # try small regularization
            alpha = 1e-8
            A_reg = A + alpha * np.eye(A.shape[0])
            try:
                L = np.linalg.cholesky(A_reg)
                y = np.linalg.solve(L, b)
                x = np.linalg.solve(L.T, y)
                report = {'chosen': 'cholesky_numpy_tikhonov', 'alpha': alpha, 'residual_norm': float(np.linalg.norm(A_reg @ x - b)), 'cond_reg': float(np.linalg.cond(A_reg))}
                return x, report, choice
            except Exception:
                x = np.linalg.pinv(A) @ b
                report = {'chosen': 'pinv_fallback', 'residual_norm': float(np.linalg.norm(A @ x - b)), 'cond': float(np.linalg.cond(A))}
                return x, report, choice

    if method == 'lu':
        mod = _try_load_skill('lu')
        if mod is not None:
            x, report = mod.robust_solve_lu(A, b)
            report = {'chosen': 'lu', **report}
            return x, report, choice
        # numpy fallback: try direct solve then pinv
        try:
            x = np.linalg.solve(A, b)
            report = {'chosen': 'lu_numpy_solve', 'residual_norm': float(np.linalg.norm(A @ x - b)), 'cond': float(np.linalg.cond(A))}
            return x, report, choice
        except Exception:
            x = np.linalg.pinv(A) @ b
            report = {'chosen': 'pinv_fallback', 'residual_norm': float(np.linalg.norm(A @ x - b)), 'cond': float(np.linalg.cond(A))}
            return x, report, choice

    if method == 'qr':
        mod = _try_load_skill('qr')
        if mod is not None:
            # Use QR with pivoting for rank-deficient or ill-conditioned cases
            pivoting = cond > 1e12 or info['rank'] < min(m, n)
            x, report = mod.robust_solve_qr(A, b, pivoting=pivoting)
            report = {'chosen': 'qr', **report}
            return x, report, choice
        # numpy fallback: use lstsq or pinv
        try:
            x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
            report = {'chosen': 'qr_numpy_lstsq', 'residual_norm': float(np.linalg.norm(A @ x - b)), 'cond': float(np.linalg.cond(A)), 'rank': int(rank)}
            return x, report, choice
        except Exception:
            x = np.linalg.pinv(A) @ b
            report = {'chosen': 'pinv_fallback', 'residual_norm': float(np.linalg.norm(A @ x - b)), 'cond': float(np.linalg.cond(A))}
            return x, report, choice

    # default to svd
    mod = _try_load_skill('svd')
    if mod is not None:
        x, report = mod.robust_solve_svd(A, b)
        report = {'chosen': 'svd', **report}
        return x, report, choice

    # numpy pseudoinverse fallback
    x = np.linalg.pinv(A) @ b
    report = {'chosen': 'svd_pinv_numpy', 'residual_norm': float(np.linalg.norm(A @ x - b)), 'cond': float(np.linalg.cond(A))}
    return x, report, choice


if __name__ == '__main__':
    # demo matrices
    def hilbert(n):
        return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)], dtype=float)

    def lotkin(n):
        A = np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)], dtype=float)
        A[0, :] = 1.0
        return A

    def vandermonde_geom(n):
        x = np.geomspace(0.1, 10, n)
        return np.vander(x, N=n, increasing=True)

    tests = [
        ('Hilbert 5', hilbert(5)),
        ('Hilbert 12', hilbert(12)),
        ('Lotkin 8', lotkin(8)),
        ('Vandermonde 12', vandermonde_geom(12)),
        ('Rank-def 3x2', np.array([[1.0,2.0],[2.0,4.0],[3.0,6.0]])),
    ]

    for name, A in tests:
        b = np.ones(A.shape[0])
        choice = choose_decomposition(A, b)
        print('==', name, '==')
        print('choice:', choice['method'])
        print('reason:', choice['reason'])
        x, report, _ = demonstrate_choice_and_solve(A, b)
        print('report:')
        for k, v in report.items():
            print(' ', k, ':', v)
        print('residual ||Ax-b|| =', np.linalg.norm(A @ x - b))
        print()
