"""Test the kronecker-product skill using its functions."""

import sys
sys.path.insert(0, r"c:\Users\trw\my-ai-math\matrix-computation\kronecker-product\scripts")

from solve_kronecker import (
    kronecker_product,
    kronecker_sum,
    verify_associativity,
    verify_transpose,
    verify_product_rule,
    verify_inverse,
    rank_kron,
    determinant_kron,
    trace_kron,
    vec_operator,
)

import numpy as np

print("=" * 60)
print("Testing kronecker-product skill functions")
print("=" * 60)

# Example 1: 基础克罗内克积
print("\n--- Example 1: Kronecker Product ---")
A = np.array([[1.0, 2.0], [3.0, 4.0]])
B = np.array([[0.0, 5.0], [6.0, 7.0]])
kron_AB = kronecker_product(A, B)
print(f"A shape: {A.shape}, B shape: {B.shape}")
print(f"A (x) B shape: {kron_AB.shape} (expected: (4, 4))")
print(f"[PASS]" if kron_AB.shape == (4, 4) else "[FAIL]")

# Example 2: 手动验证第一个元素
print("\n--- Example 2: Element Verification ---")
# A ⊗ B = [[a11*B, a12*B], [a21*B, a22*B]]
# B = [[0, 5], [6, 7]]
print(f"kron_AB[0,0] = {kron_AB[0, 0]} (expected: 1*0 = 0)")
print(f"kron_AB[0,1] = {kron_AB[0, 1]} (expected: 1*5 = 5)")
print(f"kron_AB[1,0] = {kron_AB[1, 0]} (expected: 3*0 = 6)")  # 修正期望值
is_correct = (np.isclose(kron_AB[0, 0], 0) and
              np.isclose(kron_AB[0, 1], 5) and
              np.isclose(kron_AB[1, 0], 6))  # 修正期望值
print(f"[PASS]" if is_correct else "[FAIL]")

# Example 3: 结合律
print("\n--- Example 3: Associativity ---")
C = np.eye(2)
assoc = verify_associativity(A, B, C)
print(f"(A (x) B) (x) C = A (x) (B (x) C): {assoc}")
print(f"[PASS]" if assoc else "[FAIL]")

# Example 4: 转置性质
print("\n--- Example 4: Transpose Property ---")
trans = verify_transpose(A, B)
print(f"(A (x) B)^T = A^T (x) B^T: {trans}")
print(f"[PASS]" if trans else "[FAIL]")

# Example 5: 乘积规则
print("\n--- Example 5: Product Rule ---")
prod = verify_product_rule(A, B, A, B)
print(f"(A (x) B)(A (x) B) = (AA) (x) (BB): {prod}")
print(f"[PASS]" if prod else "[FAIL]")

# Example 6: 逆矩阵性质
print("\n--- Example 6: Inverse Property ---")
inv = verify_inverse(A, C)
print(f"(A (x) I)^-1 = A^-1 (x) I^-1: {inv}")
print(f"[PASS]" if inv else "[FAIL]")

# Example 7: 秩的性质
print("\n--- Example 7: Rank Property ---")
rank_A = np.linalg.matrix_rank(A)
rank_B = np.linalg.matrix_rank(B)
rank_k = rank_kron(A, B)
print(f"rank(A) = {rank_A}, rank(B) = {rank_B}")
print(f"rank(A (x) B) = {rank_k}")
print(f"rank(A) * rank(B) = {rank_A * rank_B}")
print(f"[PASS]" if rank_k == rank_A * rank_B else "[FAIL]")

# Example 8: 行列式的性质
print("\n--- Example 8: Determinant Property ---")
det_A = np.linalg.det(A)
det_B = np.linalg.det(B)
det_k = determinant_kron(A, B)
m, n = A.shape[0], B.shape[0]
expected = (det_A ** n) * (det_B ** m)
print(f"det(A) = {det_A:.2f}, det(B) = {det_B:.2f}")
print(f"det(A (x) B) = {det_k:.6f}")
print(f"det(A)^n * det(B)^m = {expected:.6f}")
print(f"[PASS]" if np.isclose(det_k, expected) else "[FAIL]")

# Example 9: 迹的性质
print("\n--- Example 9: Trace Property ---")
trace_A = np.trace(A)
trace_B = np.trace(B)
trace_k = trace_kron(A, B)
print(f"tr(A) = {trace_A}, tr(B) = {trace_B}")
print(f"tr(A (x) B) = {trace_k:.6f}")
print(f"tr(A) * tr(B) = {trace_A * trace_B:.6f}")
print(f"[PASS]" if np.isclose(trace_k, trace_A * trace_B) else "[FAIL]")

# Example 10: Kronecker和
print("\n--- Example 10: Kronecker Sum ---")
kron_sum = kronecker_sum(A, B)
print(f"A (+) B shape: {kron_sum.shape} (expected: (4, 4))")
print(f"[PASS]" if kron_sum.shape == (4, 4) else "[FAIL]")

# Example 11: 向量克罗内克积
print("\n--- Example 11: Vector Kronecker Product ---")
u = np.array([1.0, 2.0])
v = np.array([3.0, 4.0, 5.0])
kron_uv = kronecker_product(u.reshape(-1, 1), v.reshape(-1, 1))
print(f"u shape: ({len(u)},), v shape: ({len(v)},)")
print(f"u (x) v shape: {kron_uv.shape} (expected: (6, 1))")
print(f"[PASS]" if kron_uv.shape == (6, 1) else "[FAIL]")

# Example 12: 对角矩阵的克罗内克积
print("\n--- Example 12: Diagonal Matrices ---")
D1 = np.diag([1.0, 2.0, 3.0])
D2 = np.diag([4.0, 5.0])
kron_D = kronecker_product(D1, D2)
print(f"D1 (x) D2 is diagonal: {np.allclose(kron_D, np.diag(np.diag(kron_D)))}")
print(f"[PASS]" if np.allclose(kron_D, np.diag(np.diag(kron_D))) else "[FAIL]")

# Example 13: 对称矩阵
print("\n--- Example 13: Symmetric Matrices ---")
S1 = np.array([[1.0, 2.0], [2.0, 3.0]])
S2 = np.array([[4.0, 5.0], [5.0, 6.0]])
kron_S = kronecker_product(S1, S2)
print(f"S1 symmetric: {np.allclose(S1, S1.T)}")
print(f"S2 symmetric: {np.allclose(S2, S2.T)}")
print(f"S1 (x) S2 symmetric: {np.allclose(kron_S, kron_S.T)}")
print(f"[PASS]" if np.allclose(kron_S, kron_S.T) else "[FAIL]")

print("\n" + "=" * 60)
print("All kronecker-product skill tests completed!")
print("=" * 60)
