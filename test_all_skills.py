"""Comprehensive test of all matrix computation skill functions."""

import sys
import os

# Add all script directories to path
base = 'c:/Users/trw/my-ai-math/matrix-computation'
sys.path.insert(0, os.path.join(base, 'cholesky-decomposition/scripts'))
sys.path.insert(0, os.path.join(base, 'lu-decomposition/scripts'))
sys.path.insert(0, os.path.join(base, 'svd-decomposition/scripts'))
sys.path.insert(0, os.path.join(base, 'qr-decomposition/scripts'))
sys.path.insert(0, os.path.join(base, 'conjugate-gradient/scripts'))
sys.path.insert(0, os.path.join(base, 'eigenvalue-computation/scripts'))
sys.path.insert(0, os.path.join(base, 'generalized-minimal-residual/scripts'))

import numpy as np

print("=" * 80)
print("COMPREHENSIVE TEST OF ALL MATRIX COMPUTATION SKILLS")
print("=" * 80)

results = {}

# =============================================================================
# CHOLESKY DECOMPOSITION
# =============================================================================
print("\n" + "=" * 80)
print("CHOLESKY DECOMPOSITION")
print("=" * 80)

try:
    from solve_cholesky import (
        is_symmetric, is_spd, factorize_cholesky,
        solve_cholesky, robust_solve_cholesky, reconstruction_error
    )

    # Test 1: is_symmetric
    A_sym = np.array([[1., 2.], [2., 3.]])
    A_nonsym = np.array([[1., 2.], [3., 4.]])
    test1 = is_symmetric(A_sym) and not is_symmetric(A_nonsym)
    print(f"[{'PASS' if test1 else 'FAIL'}] is_symmetric")

    # Test 2: is_spd
    A_spd = np.array([[4., 1.], [1., 3.]])
    A_sym_not_spd = np.array([[1., 2.], [2., 1.]])
    test2 = is_spd(A_spd) and not is_spd(A_sym_not_spd)
    print(f"[{'PASS' if test2 else 'FAIL'}] is_spd")

    # Test 3: factorize_cholesky
    L = factorize_cholesky(A_spd)
    recon = reconstruction_error(A_spd, L)
    test3 = recon < 1e-10
    print(f"[{'PASS' if test3 else 'FAIL'}] factorize_cholesky (recon error: {recon:.2e})")

    # Test 4: solve_cholesky
    b = np.array([1., 2.])
    x = solve_cholesky(A_spd, b)
    residual = np.linalg.norm(A_spd @ x - b)
    test4 = residual < 1e-10
    print(f"[{'PASS' if test4 else 'FAIL'}] solve_cholesky (residual: {residual:.2e})")

    # Test 5: robust_solve_cholesky (well-conditioned)
    x, report = robust_solve_cholesky(A_spd, b)
    test5 = report['method'] == 'cholesky' and report['residual_norm'] < 1e-10
    print(f"[{'PASS' if test5 else 'FAIL'}] robust_solve_cholesky (method: {report['method']})")

    results['Cholesky'] = all([test1, test2, test3, test4, test5])

except Exception as e:
    print(f"[ERROR] Cholesky: {e}")
    results['Cholesky'] = False

# =============================================================================
# LU DECOMPOSITION
# =============================================================================
print("\n" + "=" * 80)
print("LU DECOMPOSITION")
print("=" * 80)

try:
    from solve_lu import (
        factorize_lu, solve_lu, robust_solve_lu,
        reconstruction_error, determinant_from_lu, inverse_from_lu
    )

    A = np.array([[2., 1., 1.], [4., -6., 0.], [-2., 7., 2.]])
    b = np.array([5., -2., 9.])

    # Test 1: factorize_lu
    P, L, U = factorize_lu(A)
    recon = reconstruction_error(A, P, L, U)
    test1 = recon < 1e-10
    print(f"[{'PASS' if test1 else 'FAIL'}] factorize_lu (recon error: {recon:.2e})")

    # Test 2: solve_lu
    x = solve_lu(A, b)
    residual = np.linalg.norm(A @ x - b)
    test2 = residual < 1e-10
    print(f"[{'PASS' if test2 else 'FAIL'}] solve_lu (residual: {residual:.2e})")

    # Test 3: determinant_from_lu
    det = determinant_from_lu(A)
    expected_det = np.linalg.det(A)
    test3 = abs(det - expected_det) < 1e-8
    print(f"[{'PASS' if test3 else 'FAIL'}] determinant_from_lu (det: {det:.4f}, expected: {expected_det:.4f})")

    # Test 4: inverse_from_lu
    A_inv = inverse_from_lu(A)
    test4 = np.allclose(A @ A_inv, np.eye(3), atol=1e-10)
    print(f"[{'PASS' if test4 else 'FAIL'}] inverse_from_lu")

    # Test 5: robust_solve_lu
    x, report = robust_solve_lu(A, b)
    test5 = report['method'] == 'lu' and report['residual_norm'] < 1e-10
    print(f"[{'PASS' if test5 else 'FAIL'}] robust_solve_lu (method: {report['method']})")

    results['LU'] = all([test1, test2, test3, test4, test5])

except Exception as e:
    print(f"[ERROR] LU: {e}")
    results['LU'] = False

# =============================================================================
# SVD DECOMPOSITION
# =============================================================================
print("\n" + "=" * 80)
print("SVD DECOMPOSITION")
print("=" * 80)

try:
    from solve_svd import (
        svd_decompose, rank_k_approximation, retained_energy_ratio,
        pseudoinverse_svd, solve_least_squares_svd, robust_solve_svd,
        reconstruction_error
    )

    A = np.array([[3., 1., 1.], [-1., 3., 1.]])
    b = np.array([1., 2.])

    # Test 1: svd_decompose
    U, s, Vt = svd_decompose(A)
    recon = reconstruction_error(A, U, s, Vt)
    test1 = recon < 1e-10
    print(f"[{'PASS' if test1 else 'FAIL'}] svd_decompose (recon error: {recon:.2e})")

    # Test 2: rank_k_approximation
    A_k = rank_k_approximation(A, k=1)
    test2 = A_k.shape == A.shape
    print(f"[{'PASS' if test2 else 'FAIL'}] rank_k_approximation")

    # Test 3: retained_energy_ratio
    energy = retained_energy_ratio(s, k=1)
    test3 = 0 < energy <= 1
    print(f"[{'PASS' if test3 else 'FAIL'}] retained_energy_ratio (energy: {energy:.4f})")

    # Test 4: pseudoinverse_svd
    A_pinv = pseudoinverse_svd(A)
    test4 = np.allclose(A @ A_pinv @ A, A, atol=1e-10)
    print(f"[{'PASS' if test4 else 'FAIL'}] pseudoinverse_svd")

    # Test 5: solve_least_squares_svd
    x = solve_least_squares_svd(A, b)
    test5 = x.shape == (3,)  # Should have 3 elements
    print(f"[{'PASS' if test5 else 'FAIL'}] solve_least_squares_svd (solution shape: {x.shape})")

    # Test 6: robust_solve_svd
    x, report = robust_solve_svd(A, b)
    test6 = 'residual_norm' in report
    print(f"[{'PASS' if test6 else 'FAIL'}] robust_solve_svd (residual: {report.get('residual_norm', 'N/A'):.2e})")

    results['SVD'] = all([test1, test2, test3, test4, test5, test6])

except Exception as e:
    print(f"[ERROR] SVD: {e}")
    results['SVD'] = False

# =============================================================================
# QR DECOMPOSITION
# =============================================================================
print("\n" + "=" * 80)
print("QR DECOMPOSITION")
print("=" * 80)

try:
    from solve_qr import (
        qr_decompose, qr_decompose_pivoting, solve_least_squares_qr,
        estimate_rank_qr, orthogonal_residual, reconstruct_from_qr,
        robust_solve_qr, qr_gram_schmidt
    )

    A = np.array([[1., 2.], [3., 4.], [5., 6.]])

    # Test 1: qr_decompose (reduced)
    Q, R = qr_decompose(A, mode='reduced')
    recon = np.linalg.norm(A - reconstruct_from_qr(Q, R))
    orthog = orthogonal_residual(Q)
    test1 = recon < 1e-10 and orthog < 1e-10
    print(f"[{'PASS' if test1 else 'FAIL'}] qr_decompose reduced (recon: {recon:.2e}, orthog: {orthog:.2e})")

    # Test 2: qr_decompose (complete)
    Q, R = qr_decompose(A, mode='complete')
    orthog = orthogonal_residual(Q)
    test2 = orthog < 1e-10 and Q.shape == (3, 3)
    print(f"[{'PASS' if test2 else 'FAIL'}] qr_decompose complete (orthog: {orthog:.2e}, Q shape: {Q.shape})")

    # Test 3: qr_decompose_pivoting
    A_square = np.array([[1., 2., 3.], [4., 5., 6.], [7., 8., 9.]])
    Q, R, P = qr_decompose_pivoting(A_square)
    test3 = len(P) == 3
    print(f"[{'PASS' if test3 else 'FAIL'}] qr_decompose_pivoting")

    # Test 4: solve_least_squares_qr
    A_ls = np.array([[1., 1.], [1., 2.], [1., 3.], [1., 4.]])
    b_ls = np.array([5., 9., 15., 21.])
    x = solve_least_squares_qr(A_ls, b_ls)
    test4 = x.shape == (2,)
    print(f"[{'PASS' if test4 else 'FAIL'}] solve_least_squares_qr (solution: {x})")

    # Test 5: estimate_rank_qr
    A_rankdef = np.array([[1., 2., 3.], [2., 4., 6.], [3., 6., 9.]])
    rank_est = estimate_rank_qr(A_rankdef)
    test5 = rank_est <= 2  # Should detect rank deficiency
    print(f"[{'PASS' if test5 else 'FAIL'}] estimate_rank_qr (estimated rank: {rank_est}, expected: 1)")

    # Test 6: robust_solve_qr
    A_r = np.array([[1., 2.], [3., 4.], [5., 6.]])
    b_r = np.array([7., 8., 9.])
    x, report = robust_solve_qr(A_r, b_r, pivoting=False)
    test6 = report['orthogonality_error'] < 1e-10
    print(f"[{'PASS' if test6 else 'FAIL'}] robust_solve_qr (orthog error: {report['orthogonality_error']:.2e})")

    # Test 7: qr_gram_schmidt
    A_gs = np.array([[1., 1., 0.], [1., 0., 1.], [0., 1., 1.]], dtype=float)
    Q, R = qr_gram_schmidt(A_gs, modified=True)
    orthog = orthogonal_residual(Q)
    test7 = orthog < 1e-10
    print(f"[{'PASS' if test7 else 'FAIL'}] qr_gram_schmidt (orthog: {orthog:.2e})")

    results['QR'] = all([test1, test2, test3, test4, test5, test6, test7])

except Exception as e:
    print(f"[ERROR] QR: {e}")
    import traceback
    traceback.print_exc()
    results['QR'] = False

# =============================================================================
# CONJUGATE GRADIENT
# =============================================================================
print("\n" + "=" * 80)
print("CONJUGATE GRADIENT")
print("=" * 80)

try:
    from solve_cg import conjugate_gradient, report_markdown

    A = np.array([[4., 1.], [1., 3.]])
    b = np.array([1., 2.])

    # Test 1: conjugate_gradient
    x, info = conjugate_gradient(A, b, tol=1e-10)
    residual = np.linalg.norm(A @ x - b)
    test1 = info['converged'] and residual < 1e-8
    print(f"[{'PASS' if test1 else 'FAIL'}] conjugate_gradient (converged: {info['converged']}, residual: {residual:.2e})")

    results['CG'] = test1

except Exception as e:
    print(f"[ERROR] CG: {e}")
    results['CG'] = False

# =============================================================================
# EIGENVALUE COMPUTATION
# =============================================================================
print("\n" + "=" * 80)
print("EIGENVALUE COMPUTATION")
print("=" * 80)

try:
    from solve_eigen import (
        grcar, clustered_symmetric, eigen_decompose,
        symmetric_eigen_decompose, power_method
    )

    A = np.array([[2., 1.], [1., 3.]])

    # Test 1: symmetric_eigen_decompose
    vals, vecs = symmetric_eigen_decompose(A)
    # Verify: A @ v = lambda @ v
    test1 = np.allclose(A @ vecs[:, 0], vals[0] * vecs[:, 0], atol=1e-10)
    print(f"[{'PASS' if test1 else 'FAIL'}] symmetric_eigen_decompose (eigenvalues: {vals})")

    # Save symmetric eigenvalues for power_method test
    symmetric_eigenvals = vals.copy()

    # Test 2: eigen_decompose (general)
    A_nonsym = np.array([[2., 1.], [-1., 3.]])
    vals, vecs = eigen_decompose(A_nonsym)
    test2 = len(vals) == 2
    print(f"[{'PASS' if test2 else 'FAIL'}] eigen_decompose (eigenvalues: {vals})")

    # Test 3: power_method
    lambda_approx, v = power_method(A)
    # Should approximate the largest eigenvalue (use symmetric eigenvalues for symmetric matrix)
    expected_max = max(symmetric_eigenvals)
    test3 = abs(lambda_approx - expected_max) < 0.01
    print(f"[{'PASS' if test3 else 'FAIL'}] power_method (approx: {lambda_approx:.4f}, expected max: {expected_max:.4f})")

    # Test 4: grcar matrix generator
    G = grcar(5)
    test4 = G.shape == (5, 5)
    print(f"[{'PASS' if test4 else 'FAIL'}] grcar (shape: {G.shape})")

    # Test 5: clustered_symmetric
    C = clustered_symmetric(10, clusters=3)
    test5 = C.shape == (10, 10) and np.allclose(C, C.T)
    print(f"[{'PASS' if test5 else 'FAIL'}] clustered_symmetric (shape: {C.shape}, symmetric: {np.allclose(C, C.T)})")

    results['Eigen'] = all([test1, test2, test3, test4, test5])

except Exception as e:
    print(f"[ERROR] Eigen: {e}")
    import traceback
    traceback.print_exc()
    results['Eigen'] = False

# =============================================================================
# GMRES
# =============================================================================
print("\n" + "=" * 80)
print("GMRES")
print("=" * 80)

try:
    from solve_gmres import gmres, report_markdown

    # Non-symmetric matrix
    A = np.array([[3., 2.], [1., 4.]])
    b = np.array([1., 2.])

    # Test 1: gmres
    x, info = gmres(A, b, restart=10, tol=1e-10)
    residual = np.linalg.norm(A @ x - b)
    test1 = info['converged'] and residual < 1e-8
    print(f"[{'PASS' if test1 else 'FAIL'}] gmres (converged: {info['converged']}, residual: {residual:.2e})")

    results['GMRES'] = test1

except Exception as e:
    print(f"[ERROR] GMRES: {e}")
    import traceback
    traceback.print_exc()
    results['GMRES'] = False

# =============================================================================
# CHOOSE DECOMPOSITION
# =============================================================================
print("\n" + "=" * 80)
print("CHOOSE DECOMPOSITION")
print("=" * 80)

try:
    sys.path.insert(0, os.path.join(base, 'choose_decomposition/scripts'))
    from choose_decomposition import choose_decomposition, demonstrate_choice_and_solve

    # Test 1: SPD matrix -> should choose Cholesky
    A_spd = np.array([[4., 1.], [1., 3.]])
    b = np.array([1., 2.])
    choice = choose_decomposition(A_spd, b)
    test1 = choice['method'] in ['cholesky', 'cholesky_tikhonov']
    print(f"[{'PASS' if test1 else 'FAIL'}] choose_decomposition for SPD (method: {choice['method']})")

    # Test 2: Non-SPD square -> should choose LU or SVD
    A_nonspd = np.array([[2., 1.], [3., 4.]])
    choice = choose_decomposition(A_nonspd, b)
    test2 = choice['method'] in ['lu', 'svd']
    print(f"[{'PASS' if test2 else 'FAIL'}] choose_decomposition for non-SPD (method: {choice['method']})")

    # Test 3: Rectangular -> should choose SVD
    A_rect = np.array([[1., 2.], [3., 4.], [5., 6.]])
    b_rect = np.array([1., 2., 3.])
    choice = choose_decomposition(A_rect, b_rect)
    test3 = choice['method'] == 'svd'
    print(f"[{'PASS' if test3 else 'FAIL'}] choose_decomposition for rectangular (method: {choice['method']})")

    # Test 4: demonstrate_choice_and_solve
    x, report, choice = demonstrate_choice_and_solve(A_spd, b)
    test4 = 'residual_norm' in report
    print(f"[{'PASS' if test4 else 'FAIL'}] demonstrate_choice_and_solve (residual: {report.get('residual_norm', 'N/A'):.2e})")

    results['Choose'] = all([test1, test2, test3, test4])

except Exception as e:
    print(f"[ERROR] Choose: {e}")
    import traceback
    traceback.print_exc()
    results['Choose'] = False

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
print(f"\nTotal: {passed_count}/{total} modules passed")

if passed_count == total:
    print("\nAll skill functions are working correctly!")
else:
    print(f"\nWarning: {total - passed_count} module(s) have issues.")
