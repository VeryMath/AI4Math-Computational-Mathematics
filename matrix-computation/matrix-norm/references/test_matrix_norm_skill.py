"""Test the matrix-norm skill using its functions."""

import sys
sys.path.insert(0, r"c:\Users\trw\my-ai-math\matrix-computation\matrix-norm\scripts")

from solve_norm import (
    frobenius_norm,
    spectral_norm,
    norm_1,
    norm_infinity,
    nuclear_norm,
    p_norm,
    condition_number,
    matrix_distance_frobenius,
    matrix_distance_spectral,
    compute_all_norms,
    report_markdown,
    norm_comparison_table,
)

import numpy as np

print("=" * 60)
print("Testing matrix-norm skill functions")
print("=" * 60)

# Example 1: Frobenius范数
print("\n--- Example 1: Frobenius范数 ---")
A = np.array([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
    [7.0, 8.0, 9.0],
])
fro = frobenius_norm(A)
manual = np.sqrt(np.sum(A**2))
print(f"||A||_F = {fro:.6f}")
print(f"Manual = {manual:.6f}")
print(f"[PASS]" if np.isclose(fro, manual) else "[FAIL]")

# Example 2: 谱范数
print("\n--- Example 2: 谱范数 ---")
B = np.array([
    [3.0, 1.0],
    [1.0, 2.0],
])
spec = spectral_norm(B)
u, s, vt = np.linalg.svd(B)
print(f"||B||_2 = {spec:.6f}")
print(f"Max singular value = {s[0]:.6f}")
print(f"[PASS]" if np.isclose(spec, s[0]) else "[FAIL]")

# Example 3: 1-范数和∞-范数
print("\n--- Example 3: 1-范数和∞-范数 ---")
C = np.array([
    [1.0, -2.0, 3.0],
    [-4.0, 5.0, -6.0],
])
n1 = norm_1(C)
ninf = norm_infinity(C)
col_sums = np.sum(np.abs(C), axis=0)
row_sums = np.sum(np.abs(C), axis=1)
print(f"||C||_1 = {n1:.6f}, max col sum = {np.max(col_sums):.6f}")
print(f"||C||_inf = {ninf:.6f}, max row sum = {np.max(row_sums):.6f}")
print(f"[PASS]" if (np.isclose(n1, np.max(col_sums)) and np.isclose(ninf, np.max(row_sums))) else "[FAIL]")

# Example 4: 核范数
print("\n--- Example 4: 核范数 ---")
nuc = nuclear_norm(B)
u, s, vt = np.linalg.svd(B)
print(f"||B||_* = {nuc:.6f}")
print(f"Sum of singular values = {np.sum(s):.6f}")
print(f"[PASS]" if np.isclose(nuc, np.sum(s)) else "[FAIL]")

# Example 5: p-范数
print("\n--- Example 5: p-范数 ---")
D = np.array([
    [2.0, 1.0],
    [1.0, 2.0],
])
for p in [1, 2, np.inf]:
    val = p_norm(D, p)
    print(f"||D||_{p if p != np.inf else 'inf'} = {val:.6f}")

# Example 6: 条件数
print("\n--- Example 6: 条件数 ---")
I = np.eye(2)
kappa_i = condition_number(I, p=2)
print(f"kappa(I) = {kappa_i:.2f}")
print(f"[PASS]" if np.isclose(kappa_i, 1.0) else "[FAIL]")

# Example 7: Frobenius距离
print("\n--- Example 7: Frobenius距离 ---")
E = np.array([[1.0, 2.0], [3.0, 4.0]])
F = np.array([[1.1, 2.1], [2.9, 4.1]])
dist_fro = matrix_distance_frobenius(E, F)
print(f"||E - F||_F = {dist_fro:.6f}")
manual = np.sqrt(np.sum((E - F)**2))
print(f"[PASS]" if np.isclose(dist_fro, manual) else "[FAIL]")

# Example 8: 谱距离
print("\n--- Example 8: 谱距离 ---")
dist_spec = matrix_distance_spectral(B, B + np.array([[0, 0], [0, 0.001]]))
print(f"||B - (B+0.001)||_2 = {dist_spec:.8f}")

# Example 9: 正交矩阵
print("\n--- Example 9: 正交矩阵 ---")
rng = np.random.RandomState(42)
Q, _ = np.linalg.qr(rng.randn(3, 3))
print(f"||Q||_2 = {spectral_norm(Q):.6f} (expected 1)")
print(f"||Q||_F = {frobenius_norm(Q):.6f} (expected {np.sqrt(3):.6f})")
print(f"[PASS]" if (np.isclose(spectral_norm(Q), 1.0) and np.isclose(frobenius_norm(Q), np.sqrt(3))) else "[FAIL]")

# Example 10: 对角矩阵
print("\n--- Example 10: 对角矩阵 ---")
Diag = np.diag([1.0, 2.0, 3.0])
print(f"||D||_2 = {spectral_norm(Diag):.6f} (max |d_i| = 3)")
print(f"||D||_F = {frobenius_norm(Diag):.6f}")
print(f"[PASS]" if (np.isclose(spectral_norm(Diag), 3.0)) else "[FAIL]")

# Example 11: 范数不等式
print("\n--- Example 11: 范数不等式 ---")
rng = np.random.RandomState(42)
G = rng.randn(4, 3)
fro_G = frobenius_norm(G)
spec_G = spectral_norm(G)
print(f"||G||_2 <= ||G||_F: {spec_G <= fro_G}")
bound = np.sqrt(min(G.shape)) * spec_G
print(f"||G||_F <= sqrt(min(m,n))*||G||_2: {fro_G <= bound}")
print(f"[PASS]" if (spec_G <= fro_G and fro_G <= bound) else "[FAIL]")

# Example 12: compute_all_norms
print("\n--- Example 12: compute_all_norms ---")
norms = compute_all_norms(A)
print(report_markdown(norms))

# Example 13: norm_comparison_table
print("\n--- Example 13: norm_comparison_table ---")
print(norm_comparison_table(A))

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
