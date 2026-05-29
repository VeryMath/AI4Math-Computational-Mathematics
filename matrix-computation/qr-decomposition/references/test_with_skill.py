"""Test QR decomposition using the skill's own functions."""

import sys
sys.path.insert(0, 'c:/Users/trw/my-ai-math/matrix-computation/qr-decomposition/scripts')

import numpy as np
from solve_qr import (
    qr_decompose,
    qr_decompose_pivoting,
    solve_least_squares_qr,
    estimate_rank_qr,
    reconstruct_from_qr,
    orthogonal_residual,
    robust_solve_qr,
    qr_gram_schmidt,
    hilbert,
)

print("=" * 70)
print("TESTING QR DECOMPOSITION SKILL FUNCTIONS")
print("=" * 70)

# Test 1: qr_decompose (reduced mode)
print("\n### Test 1: qr_decompose (reduced) ###")
A = np.array([[1., 2.], [3., 4.], [5., 6.]])
Q, R = qr_decompose(A, mode='reduced')
print(f"A shape: {A.shape}, Q shape: {Q.shape}, R shape: {R.shape}")
reconstruction = reconstruct_from_qr(Q, R)
orthog = orthogonal_residual(Q)
print(f"Reconstruction error: {np.linalg.norm(A - reconstruction):.2e}")
print(f"Orthogonality error: {orthog:.2e}")
test1_pass = np.allclose(A, Q @ R, atol=1e-10)
print(f"PASS: {test1_pass}")

# Test 2: qr_decompose (complete mode)
print("\n### Test 2: qr_decompose (complete) ###")
Q, R = qr_decompose(A, mode='complete')
print(f"Q shape: {Q.shape}, R shape: {R.shape}")
print(f"Q is square: {Q.shape[0] == Q.shape[1]}")
orthog = orthogonal_residual(Q)
print(f"Orthogonality error: {orthog:.2e}")
test2_pass = orthog < 1e-10
print(f"PASS: {test2_pass}")

# Test 3: qr_decompose_pivoting
print("\n### Test 3: qr_decompose_pivoting ###")
A = np.array([[1., 2., 3.], [4., 5., 6.], [7., 8., 9.]])
Q, R, P = qr_decompose_pivoting(A)
print(f"A shape: {A.shape}, Q shape: {Q.shape}, R shape: {R.shape}")
print(f"Permutation P: {P}")
print(f"Diagonal of R: {np.abs(np.diag(R))}")
test3_pass = Q.shape == (3, 3) and len(P) == 3
print(f"PASS: {test3_pass}")

# Test 4: solve_least_squares_qr
print("\n### Test 4: solve_least_squares_qr ###")
A = np.array([[1., 1.], [1., 2.], [1., 3.], [1., 4.]])
b = np.array([5., 9., 15., 21.])  # Data doesn't fit perfectly
x = solve_least_squares_qr(A, b)
residual = np.linalg.norm(A @ x - b)
print(f"Solution x: {x}")
print(f"Residual: {residual:.2e}")
# Data: (1,5), (2,9), (3,15), (4,21) - not perfectly linear
test4_pass = residual < 2.0  # Reasonable for this data
print(f"PASS: {test4_pass} (data doesn't fit perfectly)")

# Test 5: estimate_rank_qr
print("\n### Test 5: estimate_rank_qr ###")
# Rank-deficient matrix
A = np.array([[1., 2., 3.], [2., 4., 6.], [3., 6., 9.]])
rank_est = estimate_rank_qr(A)
print(f"Matrix has linearly dependent columns (rank should be 1)")
print(f"Estimated rank: {rank_est}")
test5_pass = rank_est <= 2  # Should detect rank deficiency
print(f"PASS: {test5_pass}")

# Test 6: robust_solve_qr (without pivoting)
print("\n### Test 6: robust_solve_qr (no pivoting) ###")
A = np.array([[1., 2.], [3., 4.], [5., 6.]])
b = np.array([7., 8., 9.])
x, report = robust_solve_qr(A, b, pivoting=False)
print(f"Solution x: {x}")
print(f"Method: {report['method']}")
print(f"Rank estimate: {report['rank_estimate']}")
print(f"Rank deficient: {report['rank_deficient']}")
print(f"Orthogonality error: {report['orthogonality_error']:.2e}")
print(f"Reconstruction error: {report['reconstruction_error']:.2e}")
print(f"Residual norm: {report['residual_norm']:.2e}")
test6_pass = report['orthogonality_error'] < 1e-10
print(f"PASS: {test6_pass}")

# Test 7: robust_solve_qr (with pivoting)
print("\n### Test 7: robust_solve_qr (with pivoting) ###")
x, report = robust_solve_qr(A, b, pivoting=True)
print(f"Solution x: {x}")
print(f"Method: {report['method']}")
print(f"Rank estimate: {report['rank_estimate']}")
print(f"Residual norm: {report['residual_norm']:.2e}")
test7_pass = report['method'] == 'qr_pivoting'
print(f"PASS: {test7_pass}")

# Test 8: qr_gram_schmidt (modified)
print("\n### Test 8: qr_gram_schmidt (modified=True) ###")
A = np.array([[1., 1., 0.], [1., 0., 1.], [0., 1., 1.]], dtype=float)
Q, R = qr_gram_schmidt(A, modified=True)
orthog = orthogonal_residual(Q)
recon_error = np.linalg.norm(A - Q @ R)
print(f"Orthogonality error: {orthog:.2e}")
print(f"Reconstruction error: {recon_error:.2e}")
test8_pass = orthog < 1e-10 and recon_error < 1e-10
print(f"PASS: {test8_pass}")

# Test 9: qr_gram_schmidt (classical)
print("\n### Test 9: qr_gram_schmidt (modified=False, classical) ###")
Q, R = qr_gram_schmidt(A, modified=False)
orthog = orthogonal_residual(Q)
recon_error = np.linalg.norm(A - Q @ R)
print(f"Orthogonality error: {orthog:.2e}")
print(f"Reconstruction error: {recon_error:.2e}")
test9_pass = recon_error < 1e-10
print(f"PASS: {test9_pass}")

# Test 10: hilbert function
print("\n### Test 10: hilbert function ###")
H = hilbert(4)
print(f"Hilbert matrix (4x4):\n{H}")
print(f"Expected H[0,0] = 1.0, got {H[0,0]}")
print(f"Expected H[3,3] = 1/7 ≈ 0.1429, got {H[3,3]:.4f}")
test10_pass = np.isclose(H[0,0], 1.0) and np.isclose(H[3,3], 1/7)
print(f"PASS: {test10_pass}")

# Test 11: robust_solve_qr with rank-deficient matrix
print("\n### Test 11: robust_solve_qr with rank-deficient matrix ###")
A = np.array([[1., 2.], [2., 4.], [3., 6.]])
b = np.array([1., 2., 3.])
x, report = robust_solve_qr(A, b, pivoting=True)
print(f"Matrix columns are linearly dependent")
print(f"Rank estimate: {report['rank_estimate']}")
print(f"Rank deficient: {report['rank_deficient']}")
print(f"Residual norm: {report['residual_norm']:.2e}")
test11_pass = report['rank_deficient'] == True and report['rank_estimate'] <= 2
print(f"PASS: {test11_pass}")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
results = {
    "Test 1 (qr_decompose reduced)": test1_pass,
    "Test 2 (qr_decompose complete)": test2_pass,
    "Test 3 (qr_decompose_pivoting)": test3_pass,
    "Test 4 (solve_least_squares_qr)": test4_pass,
    "Test 5 (estimate_rank_qr)": test5_pass,
    "Test 6 (robust_solve_qr no pivot)": test6_pass,
    "Test 7 (robust_solve_qr with pivot)": test7_pass,
    "Test 8 (qr_gram_schmidt modified)": test8_pass,
    "Test 9 (qr_gram_schmidt classical)": test9_pass,
    "Test 10 (hilbert)": test10_pass,
    "Test 11 (robust_solve_qr rank-deficient)": test11_pass,
}

for name, passed in results.items():
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status}: {name}")

total = len(results)
passed_count = sum(results.values())
print(f"\nTotal: {passed_count}/{total} tests passed using skill functions")
