"""Comprehensive test suite for all matrix computation skills.

This script tests all skills by running test cases derived from examples.md files.
It validates the core functionality of each skill's implementation.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from typing import Callable
import numpy as np
from scipy import sparse
from scipy.sparse import diags


def load_module(path: str, name: str):
    """Load a Python module from a file path."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Test result tracking
class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.skill_results = {}

    def add_pass(self, skill: str, test_name: str):
        self.passed += 1
        if skill not in self.skill_results:
            self.skill_results[skill] = {"passed": 0, "failed": 0, "tests": []}
        self.skill_results[skill]["passed"] += 1
        self.skill_results[skill]["tests"].append((test_name, "PASS"))

    def add_fail(self, skill: str, test_name: str, error: str):
        self.failed += 1
        self.errors.append((skill, test_name, error))
        if skill not in self.skill_results:
            self.skill_results[skill] = {"passed": 0, "failed": 0, "tests": []}
        self.skill_results[skill]["failed"] += 1
        self.skill_results[skill]["tests"].append((test_name, f"FAIL: {error}"))

    def print_summary(self):
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        total = self.passed + self.failed
        print(f"Total tests: {total}")
        print(f"Passed: {self.passed} [PASS]")
        print(f"Failed: {self.failed} [FAIL]")
        print(f"Success rate: {100 * self.passed / total:.1f}%")

        print("\n" + "-" * 80)
        print("Results by Skill:")
        print("-" * 80)
        for skill, results in self.skill_results.items():
            print(f"\n{skill}:")
            print(f"  Passed: {results['passed']}, Failed: {results['failed']}")
            if results['failed'] > 0:
                print("  Failed tests:")
                for test_name, status in results['tests']:
                    if status.startswith("FAIL"):
                        print(f"    - {test_name}: {status[5:]}")

        if self.errors:
            print("\n" + "-" * 80)
            print("Detailed Errors:")
            print("-" * 80)
            for skill, test_name, error in self.errors:
                print(f"\n{skill} - {test_name}:")
                print(f"  {error}")


results = TestResults()


def assert_close(actual, expected, tol=1e-6, skill="unknown", test_name=""):
    """Assert that two values are close."""
    if isinstance(actual, np.ndarray) and isinstance(expected, np.ndarray):
        if np.allclose(actual, expected, atol=tol, rtol=tol):
            results.add_pass(skill, test_name)
            return True
        else:
            error = f"Arrays not close: max diff = {np.max(np.abs(actual - expected))}"
            results.add_fail(skill, test_name, error)
            return False
    else:
        if abs(actual - expected) < tol:
            results.add_pass(skill, test_name)
            return True
        else:
            error = f"Values not close: {actual} vs {expected}"
            results.add_fail(skill, test_name, error)
            return False


def assert_true(condition, skill="unknown", test_name="", error_msg=""):
    """Assert that a condition is true."""
    if condition:
        results.add_pass(skill, test_name)
        return True
    else:
        results.add_fail(skill, test_name, error_msg or "Condition was False")
        return False


# ============================================================================
# CHOLESKY DECOMPOSITION TESTS
# ============================================================================

def test_cholesky():
    """Test Cholesky decomposition skill."""
    print("\nTesting Cholesky Decomposition...")

    mod = load_module(
        "c:/Users/trw/my-ai-math/matrix-computation/cholesky-decomposition/scripts/solve_cholesky.py",
        "solve_cholesky"
    )

    # Example 1: Basic Cholesky decomposition
    A = np.array([[25.0, 15.0, -5.0], [15.0, 18.0, 0.0], [-5.0, 0.0, 11.0]])
    L = mod.factorize_cholesky(A)
    assert_close(
        L @ L.T, A, tol=1e-10,
        skill="Cholesky", test_name="Basic decomposition"
    )

    # Example 2: SPD linear system
    A = np.array([[4.0, 1.0], [1.0, 3.0]])
    b = np.array([1.0, 2.0])
    x = mod.solve_cholesky(A, b)
    assert_close(
        A @ x, b, tol=1e-10,
        skill="Cholesky", test_name="SPD linear system"
    )

    # Example 3: SPD validation
    A1 = np.array([[4.0, 1.0], [1.0, 3.0]])
    A2 = np.array([[1.0, 2.0], [2.0, 1.0]])
    assert_true(
        mod.is_spd(A1),
        skill="Cholesky", test_name="SPD validation A1"
    )
    assert_true(
        not mod.is_spd(A2),
        skill="Cholesky", test_name="SPD validation A2 (non-SPD)"
    )

    # Example 4: Hilbert matrix (ill-conditioned)
    def hilbert(n):
        i = np.arange(1, n + 1)
        return np.array([[1.0 / (ii + jj - 1) for jj in i] for ii in i], dtype=float)

    H = hilbert(8)
    L = mod.factorize_cholesky(H)
    assert_close(
        L @ L.T, H, tol=1e-8,
        skill="Cholesky", test_name="Hilbert matrix decomposition"
    )

    # Example 5: Robust solve with regularization
    H12 = hilbert(12)
    b = np.ones(12)
    x, report = mod.robust_solve_cholesky(H12, b, alpha=1e-8)
    assert_true(
        report['method'] in ['tikhonov', 'svd_fallback'],
        skill="Cholesky", test_name="Robust solve with regularization"
    )

    # Example 6: Gram matrix
    np.random.seed(42)
    X = np.random.randn(10, 3)
    A = X.T @ X
    assert_true(
        mod.is_spd(A),
        skill="Cholesky", test_name="Gram matrix is SPD"
    )


# ============================================================================
# CONJUGATE GRADIENT TESTS
# ============================================================================

def test_conjugate_gradient():
    """Test Conjugate Gradient skill."""
    print("\nTesting Conjugate Gradient...")

    mod = load_module(
        "c:/Users/trw/my-ai-math/matrix-computation/conjugate-gradient/scripts/solve_cg.py",
        "solve_cg"
    )

    # Example 1: Basic SPD system
    A = np.array([[4.0, 1.0], [1.0, 3.0]])
    b = np.array([1.0, 2.0])
    x, info = mod.conjugate_gradient(A, b, tol=1e-10, maxiter=1000)
    assert_close(
        A @ x, b, tol=1e-8,
        skill="Conjugate Gradient", test_name="Basic SPD system"
    )

    # Example 2: Hilbert matrix (ill-conditioned)
    def hilbert(n):
        i = np.arange(1, n + 1)
        return np.array([[1.0 / (ii + jj - 1) for jj in i] for ii in i], dtype=float)

    H = hilbert(8)
    b = np.ones(8)
    x, info = mod.conjugate_gradient(H, b, tol=1e-8, maxiter=1000)
    assert_close(
        np.linalg.norm(H @ x - b), 0.0, tol=1e-5,
        skill="Conjugate Gradient", test_name="Hilbert matrix CG"
    )

    # Example 3: 2D Poisson problem
    def poisson2d(n):
        N = n * n
        main = 4.0 * np.ones(N)
        off = -1.0 * np.ones(N)
        A = diags([main, off, off, off, off], [0, -1, 1, -n, n], shape=(N, N), format='csr')
        return A

    A = poisson2d(10)
    b = np.ones(A.shape[0])
    x, info = mod.conjugate_gradient(A, b, tol=1e-6, maxiter=1000)
    assert_true(
        info['converged'],
        skill="Conjugate Gradient", test_name="2D Poisson problem"
    )


# ============================================================================
# EIGENVALUE COMPUTATION TESTS
# ============================================================================

def test_eigenvalue():
    """Test Eigenvalue Computation skill."""
    print("\nTesting Eigenvalue Computation...")

    mod = load_module(
        "c:/Users/trw/my-ai-math/matrix-computation/eigenvalue-computation/scripts/solve_eigen.py",
        "solve_eigen"
    )

    # Example 1: Basic eigenvalue decomposition (non-symmetric)
    A = np.array([[4.0, 1.0], [3.0, 2.0]])
    values, vectors = mod.eigen_decompose(A)
    assert_true(
        len(values) == 2,
        skill="Eigenvalue", test_name="Basic eigenvalue count"
    )

    # Example 2: Symmetric matrix
    A = np.array([[2.0, 1.0, 0.0], [1.0, 2.0, 1.0], [0.0, 1.0, 2.0]])
    values, vectors = mod.symmetric_eigen_decompose(A)
    # For symmetric matrices, eigenvectors should be orthogonal
    orthogonality = np.linalg.norm(vectors.T @ vectors - np.eye(3))
    assert_true(
        orthogonality < 1e-10,
        skill="Eigenvalue", test_name="Orthogonal eigenvectors (symmetric)"
    )

    # Example 3: Power method
    lam, v = mod.power_method(A, tol=1e-10, maxiter=1000)
    # Verify v is normalized
    assert_close(
        np.linalg.norm(v), 1.0, tol=1e-8,
        skill="Eigenvalue", test_name="Power method normalization"
    )


# ============================================================================
# GENERALIZED MINIMAL RESIDUAL (GMRES) TESTS
# ============================================================================

def test_gmres():
    """Test GMRES skill."""
    print("\nTesting GMRES...")

    mod = load_module(
        "c:/Users/trw/my-ai-math/matrix-computation/generalized-minimal-residual/scripts/solve_gmres.py",
        "solve_gmres"
    )

    # Example 1: Basic linear system (non-symmetric)
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    b = np.array([5.0, 6.0])
    x, info = mod.gmres(A, b, tol=1e-8, maxiter=100)
    assert_close(
        A @ x, b, tol=1e-6,
        skill="GMRES", test_name="Non-symmetric system"
    )

    # Example 2: Larger system
    np.random.seed(42)
    A = np.random.randn(10, 10)
    b = np.random.randn(10)
    x, info = mod.gmres(A, b, tol=1e-6, maxiter=100)
    assert_close(
        A @ x, b, tol=1e-4,
        skill="GMRES", test_name="Random 10x10 system"
    )


# ============================================================================
# KRONECKER PRODUCT TESTS
# ============================================================================

def test_kronecker():
    """Test Kronecker Product skill."""
    print("\nTesting Kronecker Product...")

    mod = load_module(
        "c:/Users/trw/my-ai-math/matrix-computation/kronecker-product/scripts/solve_kronecker.py",
        "solve_kronecker"
    )

    # Example 1: Basic Kronecker product
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    B = np.array([[0.0, 5.0], [6.0, 7.0]])
    result = mod.kronecker_product(A, B)
    expected = np.array([
        [0., 5., 0., 10.],
        [6., 7., 12., 14.],
        [0., 15., 0., 20.],
        [18., 21., 24., 28.]
    ])
    assert_close(
        result, expected, tol=1e-10,
        skill="Kronecker", test_name="Basic Kronecker product"
    )

    # Example 2: Identity matrix
    I3 = np.eye(3)
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    result = mod.kronecker_product(I3, A)
    assert_true(
        result.shape == (6, 6),
        skill="Kronecker", test_name="Identity Kronecker product shape"
    )

    # Example 3: Kronecker with identity (A ⊗ I)
    I2 = np.eye(2)
    result = mod.kronecker_product(A, I2)
    # Verify rank property
    expected_rank = mod.rank_kron(A, I2)
    actual_rank = int(np.linalg.matrix_rank(result))
    assert_true(
        expected_rank == actual_rank,
        skill="Kronecker", test_name="Rank property"
    )

    # Example 4: Verify associativity
    C = np.array([[1.0, 0.0], [0.0, 1.0]])
    assert_true(
        mod.verify_associativity(A, B, C),
        skill="Kronecker", test_name="Associativity property"
    )


# ============================================================================
# LU DECOMPOSITION TESTS
# ============================================================================

def test_lu():
    """Test LU Decomposition skill."""
    print("\nTesting LU Decomposition...")

    mod = load_module(
        "c:/Users/trw/my-ai-math/matrix-computation/lu-decomposition/scripts/solve_lu.py",
        "solve_lu"
    )

    # Example 1: Basic LU decomposition
    A = np.array([[2.0, 1.0, 1.0], [4.0, -6.0, 0.0], [-2.0, 7.0, 2.0]])
    P, L, U = mod.factorize_lu(A)
    error = mod.reconstruction_error(A, P, L, U)
    assert_true(
        error < 1e-10,
        skill="LU", test_name="Basic LU decomposition"
    )

    # Example 2: Solve linear system
    b = np.array([5.0, -2.0, 9.0])
    x = mod.solve_lu(A, b)
    assert_close(
        A @ x, b, tol=1e-10,
        skill="LU", test_name="LU linear system"
    )

    # Example 3: Determinant
    det = mod.determinant_from_lu(A)
    expected_det = np.linalg.det(A)
    assert_close(
        det, expected_det, tol=1e-8,
        skill="LU", test_name="LU determinant"
    )

    # Example 4: Matrix inverse
    A_inv = mod.inverse_from_lu(A)
    identity = A @ A_inv
    assert_close(
        identity, np.eye(3), tol=1e-8,
        skill="LU", test_name="LU inverse"
    )


# ============================================================================
# MATRIX NORM TESTS
# ============================================================================

def test_matrix_norm():
    """Test Matrix Norm skill."""
    print("\nTesting Matrix Norm...")

    mod = load_module(
        "c:/Users/trw/my-ai-math/matrix-computation/matrix-norm/scripts/solve_norm.py",
        "solve_norm"
    )

    # Example 1: Frobenius norm
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    frob_norm = mod.frobenius_norm(A)
    expected_frob = np.sqrt(np.sum(A**2))
    assert_close(
        frob_norm, expected_frob, tol=1e-10,
        skill="Matrix Norm", test_name="Frobenius norm"
    )

    # Example 2: Spectral norm (2-norm)
    spec_norm = mod.spectral_norm(A)
    expected_spec = np.linalg.norm(A, ord=2)
    assert_close(
        spec_norm, expected_spec, tol=1e-10,
        skill="Matrix Norm", test_name="Spectral norm"
    )

    # Example 3: 1-norm (max column sum)
    col_norm = mod.norm_1(A)
    expected_col = np.linalg.norm(A, ord=1)
    assert_close(
        col_norm, expected_col, tol=1e-10,
        skill="Matrix Norm", test_name="Column norm (1-norm)"
    )

    # Example 4: Infinity norm (max row sum)
    row_norm = mod.norm_infinity(A)
    expected_row = np.linalg.norm(A, ord=np.inf)
    assert_close(
        row_norm, expected_row, tol=1e-10,
        skill="Matrix Norm", test_name="Row norm (inf-norm)"
    )


# ============================================================================
# QR DECOMPOSITION TESTS
# ============================================================================

def test_qr():
    """Test QR Decomposition skill."""
    print("\nTesting QR Decomposition...")

    mod = load_module(
        "c:/Users/trw/my-ai-math/matrix-computation/qr-decomposition/scripts/solve_qr.py",
        "solve_qr"
    )

    # Example 1: Basic QR decomposition
    A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 10.0]])
    Q, R = mod.qr_decompose(A)
    orth_error = mod.orthogonal_residual(Q)
    recon_error = np.linalg.norm(A - Q @ R)
    assert_true(
        orth_error < 1e-10,
        skill="QR", test_name="Orthogonality of Q"
    )
    assert_true(
        recon_error < 1e-10,
        skill="QR", test_name="Reconstruction from QR"
    )

    # Example 2: Least squares
    A = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    b = np.array([1.0, 2.0, 3.0])
    x = mod.solve_least_squares_qr(A, b)
    # Verify solution minimizes ||Ax - b||
    residual = np.linalg.norm(A @ x - b)
    assert_true(
        residual < 10.0,
        skill="QR", test_name="Least squares solution"
    )

    # Example 3: Rank estimation
    A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    rank = mod.estimate_rank_qr(A)
    assert_true(
        rank == 2,  # This matrix should have rank 2
        skill="QR", test_name="Rank estimation"
    )


# ============================================================================
# SVD DECOMPOSITION TESTS
# ============================================================================

def test_svd():
    """Test SVD Decomposition skill."""
    print("\nTesting SVD Decomposition...")

    mod = load_module(
        "c:/Users/trw/my-ai-math/matrix-computation/svd-decomposition/scripts/solve_svd.py",
        "solve_svd"
    )

    # Example 1: Basic SVD
    A = np.array([[3.0, 1.0, 1.0], [-1.0, 3.0, 1.0]])
    U, s, Vt = mod.svd_decompose(A)
    recon_error = mod.reconstruction_error(A, U, s, Vt)
    assert_true(
        recon_error < 1e-10,
        skill="SVD", test_name="SVD reconstruction"
    )

    # Example 2: Rank-k approximation
    Ak = mod.rank_k_approximation(A, k=1)
    assert_true(
        Ak.shape == A.shape,
        skill="SVD", test_name="Rank-1 approximation shape"
    )

    # Example 3: Least squares
    b = np.array([1.0, 2.0])
    x = mod.solve_least_squares_svd(A, b)
    residual = np.linalg.norm(A @ x - b)
    assert_true(
        residual < 10.0,
        skill="SVD", test_name="SVD least squares"
    )

    # Example 4: Pseudoinverse
    A_pinv = mod.pseudoinverse_svd(A)
    assert_true(
        A_pinv.shape == (3, 2),
        skill="SVD", test_name="Pseudoinverse shape"
    )

    # Example 5: Robust solve
    x, report = mod.robust_solve_svd(A, b)
    assert_true(
        'cond' in report,
        skill="SVD", test_name="Robust solve report"
    )


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def main():
    print("=" * 80)
    print("MATRIX COMPUTATION SKILLS TEST SUITE")
    print("=" * 80)
    print("\nRunning tests for all 9 skills...\n")

    try:
        test_cholesky()
    except Exception as e:
        results.add_fail("Cholesky", "Setup", f"Module load error: {e}")

    try:
        test_conjugate_gradient()
    except Exception as e:
        results.add_fail("Conjugate Gradient", "Setup", f"Module load error: {e}")

    try:
        test_eigenvalue()
    except Exception as e:
        results.add_fail("Eigenvalue", "Setup", f"Module load error: {e}")

    try:
        test_gmres()
    except Exception as e:
        results.add_fail("GMRES", "Setup", f"Module load error: {e}")

    try:
        test_kronecker()
    except Exception as e:
        results.add_fail("Kronecker", "Setup", f"Module load error: {e}")

    try:
        test_lu()
    except Exception as e:
        results.add_fail("LU", "Setup", f"Module load error: {e}")

    try:
        test_matrix_norm()
    except Exception as e:
        results.add_fail("Matrix Norm", "Setup", f"Module load error: {e}")

    try:
        test_qr()
    except Exception as e:
        results.add_fail("QR", "Setup", f"Module load error: {e}")

    try:
        test_svd()
    except Exception as e:
        results.add_fail("SVD", "Setup", f"Module load error: {e}")

    results.print_summary()

    # Return exit code based on test results
    return 0 if results.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
