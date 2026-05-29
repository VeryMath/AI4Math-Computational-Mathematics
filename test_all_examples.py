"""Test examples from all modules' examples.md files."""

import sys
import os

base = 'c:/Users/trw/my-ai-math/matrix-computation'
sys.path.insert(0, os.path.join(base, 'cholesky-decomposition/scripts'))
sys.path.insert(0, os.path.join(base, 'lu-decomposition/scripts'))
sys.path.insert(0, os.path.join(base, 'svd-decomposition/scripts'))
sys.path.insert(0, os.path.join(base, 'qr-decomposition/scripts'))
sys.path.insert(0, os.path.join(base, 'conjugate-gradient/scripts'))
sys.path.insert(0, os.path.join(base, 'eigenvalue-computation/scripts'))
sys.path.insert(0, os.path.join(base, 'generalized-minimal-residual/scripts'))

import numpy as np
from scipy.linalg import qr

print("=" * 80)
print("TESTING EXAMPLES FROM ALL MODULES")
print("=" * 80)

results = {}

# =============================================================================
# CHOLESKY EXAMPLES
# =============================================================================
print("\n### CHOLESKY EXAMPLES ###")

try:
    from solve_cholesky import factorize_cholesky, solve_cholesky, reconstruction_error

    # Example: Basic Cholesky decomposition
    A = np.array([[25., 15., -5.], [15., 18., 0.], [-5., 0., 11.]])
    L = factorize_cholesky(A)
    recon = reconstruction_error(A, L)
    print(f"Basic Cholesky: recon error = {recon:.2e}")

    b = np.array([1., 2., 3.])
    x = solve_cholesky(A, b)
    residual = np.linalg.norm(A @ x - b)
    print(f"Solve Ax=b: residual = {residual:.2e}")

    results['Cholesky'] = recon < 1e-10 and residual < 1e-10

except Exception as e:
    print(f"[ERROR] Cholesky: {e}")
    import traceback
    traceback.print_exc()
    results['Cholesky'] = False

# =============================================================================
# LU EXAMPLES
# =============================================================================
print("\n### LU EXAMPLES ###")

try:
    from solve_lu import factorize_lu, solve_lu, reconstruction_error, determinant_from_lu

    A = np.array([[2., 1., 1.], [4., -6., 0.], [-2., 7., 2.]])
    P, L, U = factorize_lu(A)
    recon = reconstruction_error(A, P, L, U)
    print(f"Basic LU: recon error = {recon:.2e}")

    b = np.array([5., -2., 9.])
    x = solve_lu(A, b)
    residual = np.linalg.norm(A @ x - b)
    print(f"Solve Ax=b: residual = {residual:.2e}")

    det = determinant_from_lu(A)
    print(f"Determinant: {det}")

    results['LU'] = recon < 1e-10 and residual < 1e-10

except Exception as e:
    print(f"[ERROR] LU: {e}")
    import traceback
    traceback.print_exc()
    results['LU'] = False

# =============================================================================
# SVD EXAMPLES
# =============================================================================
print("\n### SVD EXAMPLES ###")

try:
    from solve_svd import svd_decompose, rank_k_approximation, reconstruction_error

    A = np.array([[3., 1., 1.], [-1., 3., 1.]])
    U, s, Vt = svd_decompose(A)
    recon = reconstruction_error(A, U, s, Vt)
    print(f"Basic SVD: recon error = {recon:.2e}")
    print(f"Singular values: {s}")

    A_k1 = rank_k_approximation(A, k=1)
    print(f"Rank-1 approximation shape: {A_k1.shape}")

    results['SVD'] = recon < 1e-10

except Exception as e:
    print(f"[ERROR] SVD: {e}")
    import traceback
    traceback.print_exc()
    results['SVD'] = False

# =============================================================================
# QR EXAMPLES (selected from examples.md)
# =============================================================================
print("\n### QR EXAMPLES ###")

try:
    # Example 1: Complete QR
    A = np.array([[1., 2.], [3., 4.], [5., 6.]])
    Q, R = np.linalg.qr(A, mode='complete')
    orthog = np.linalg.norm(Q.T @ Q - np.eye(Q.shape[1]))
    print(f"Complete QR: orthogonality error = {orthog:.2e}")

    # Example 2: Reduced QR
    A = np.array([[1., 2., 3.], [4., 5., 6.], [7., 8., 10.]])
    Q, R = np.linalg.qr(A, mode='reduced')
    recon = np.linalg.norm(A - Q @ R)
    print(f"Reduced QR: recon error = {recon:.2e}")

    # Example 3: Least squares
    A = np.array([[1., 1.], [1., 2.], [1., 3.], [1., 4.]])
    b = np.array([5., 9., 15., 21.])
    Q, R = np.linalg.qr(A, mode='reduced')
    x = np.linalg.solve(R, Q.T @ b)
    residual = np.linalg.norm(A @ x - b)
    print(f"Least squares: residual = {residual:.2f}")

    # Example 4: QR with pivoting
    A = np.array([[1., 2., 3.], [4., 5., 6.], [7., 8., 9.]])
    Q, R, P = qr(A, pivoting=True, mode='economic')
    print(f"QR with pivoting: P = {P}")

    results['QR'] = orthog < 1e-10 and recon < 1e-10

except Exception as e:
    print(f"[ERROR] QR: {e}")
    import traceback
    traceback.print_exc()
    results['QR'] = False

# =============================================================================
# CONJUGATE GRADIENT EXAMPLES
# =============================================================================
print("\n### CONJUGATE GRADIENT EXAMPLES ###")

try:
    from solve_cg import conjugate_gradient

    # Example: Basic CG
    A = np.array([[4., 1.], [1., 3.]])
    b = np.array([1., 2.])
    x, info = conjugate_gradient(A, b, tol=1e-10)
    residual = np.linalg.norm(A @ x - b)
    print(f"Basic CG: iterations = {info['iterations']}, residual = {residual:.2e}")

    results['CG'] = info['converged'] and residual < 1e-8

except Exception as e:
    print(f"[ERROR] CG: {e}")
    import traceback
    traceback.print_exc()
    results['CG'] = False

# =============================================================================
# EIGENVALUE EXAMPLES
# =============================================================================
print("\n### EIGENVALUE EXAMPLES ###")

try:
    from solve_eigen import symmetric_eigen_decompose, power_method, grcar

    # Example: Symmetric eigenvalue
    A = np.array([[2., 1.], [1., 3.]])
    vals, vecs = symmetric_eigen_decompose(A)
    print(f"Symmetric eigenvalues: {vals}")

    # Example: Power method
    lambda_approx, v = power_method(A, tol=1e-10)
    print(f"Power method: lambda ≈ {lambda_approx:.4f}")

    # Example: Grcar matrix
    G = grcar(10)
    print(f"Grcar matrix shape: {G.shape}")

    results['Eigen'] = abs(lambda_approx - max(vals)) < 0.01

except Exception as e:
    print(f"[ERROR] Eigen: {e}")
    import traceback
    traceback.print_exc()
    results['Eigen'] = False

# =============================================================================
# GMRES EXAMPLES
# =============================================================================
print("\n### GMRES EXAMPLES ###")

try:
    from solve_gmres import gmres

    # Example: Basic GMRES
    A = np.array([[3., 2.], [1., 4.]])
    b = np.array([1., 2.])
    x, info = gmres(A, b, restart=10, tol=1e-10)
    residual = np.linalg.norm(A @ x - b)
    print(f"Basic GMRES: iterations = {info['iterations']}, residual = {residual:.2e}")

    results['GMRES'] = info['converged'] and residual < 1e-8

except Exception as e:
    print(f"[ERROR] GMRES: {e}")
    import traceback
    traceback.print_exc()
    results['GMRES'] = False

# =============================================================================
# ILL-CONDITIONED MATRIX EXAMPLES
# =============================================================================
print("\n### ILL-CONDITIONED MATRIX EXAMPLES ###")

try:
    # Hilbert matrix example (Cholesky/QR/SVD all handle this)
    def hilbert(n):
        return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)], dtype=float)

    H = hilbert(8)
    print(f"Hilbert(8) condition number: {np.linalg.cond(H):.2e}")

    # Test with Cholesky (should work but be sensitive)
    from solve_cholesky import robust_solve_cholesky
    b = np.ones(8)
    x_chol, report_chol = robust_solve_cholesky(H, b)
    print(f"Hilbert with Cholesky: method = {report_chol['method']}, residual = {report_chol['residual_norm']:.2e}")

    # Test with SVD (should be robust)
    from solve_svd import robust_solve_svd
    x_svd, report_svd = robust_solve_svd(H, b)
    print(f"Hilbert with SVD: method = {report_svd['method']}, residual = {report_svd['residual_norm']:.2e}")

    results['Ill-conditioned'] = True

except Exception as e:
    print(f"[ERROR] Ill-conditioned: {e}")
    import traceback
    traceback.print_exc()
    results['Ill-conditioned'] = False

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

for name, passed in results.items():
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {name}")

total = len(results)
passed_count = sum(results.values())
print(f"\nTotal: {passed_count}/{total} example categories passed")
