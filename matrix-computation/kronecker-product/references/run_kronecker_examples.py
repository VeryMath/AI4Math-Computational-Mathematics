"""Test complex and ill-conditioned Kronecker product examples."""

from __future__ import annotations

import sys
sys.path.insert(0, r"c:\Users\trw\my-ai-math\matrix-computation\kronecker-product\scripts")

from solve_kronecker import (
    kronecker_product,
    rank_kron,
    determinant_kron,
    trace_kron,
)

import numpy as np
from scipy.linalg import toeplitz, circulant
from scipy.special import comb
from scipy.sparse import csr_matrix, kron as sparse_kron


def hilbert(n: int) -> np.ndarray:
    return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)], dtype=float)


def laplacian_1d(n: int) -> np.ndarray:
    diag = 2 * np.ones(n)
    off_diag = -1 * np.ones(n - 1)
    return np.diag(diag) + np.diag(off_diag, k=1) + np.diag(off_diag, k=-1)


def pascal_matrix(n: int) -> np.ndarray:
    P = np.ones((n, n), dtype=float)
    for i in range(1, n):
        for j in range(1, n):
            P[i, j] = comb(i + j, i, exact=True)
    return P


def fibonacci_q_matrix(n: int) -> np.ndarray:
    Q = np.ones((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            Q[i, j] = comb(i + j, i, exact=True)
    return Q


def example_19_hilbert() -> bool:
    """Example 19: Hilbert矩阵的Kronecker积"""
    print("\n" + "=" * 60)
    print("Example 19: Hilbert Kronecker Product")
    print("=" * 60)

    all_pass = True
    for n in [3, 4]:
        H = hilbert(n)
        H_kron = kronecker_product(H, H)

        cond_H = np.linalg.cond(H)
        cond_H_kron = np.linalg.cond(H_kron)

        print(f"\nHilbert({n}) (x) Hilbert({n}):")
        print(f"  H shape: {H.shape}, H(x)H shape: {H_kron.shape}")
        print(f"  cond(H) = {cond_H:.6e}")
        print(f"  cond(H(x)H) = {cond_H_kron:.6e}")
        print(f"  cond(H(x)H) ≈ cond(H)^(2n) = {cond_H**(2*n):.6e}")

        # 验证条件数关系
        cond_check = cond_H_kron < cond_H**(2*n) * 1.1  # 允许10%误差
        print(f"  cond(H(x)H) < cond(H)^(2n)*1.1: {cond_check}")

        # 验证秩
        rank_H = np.linalg.matrix_rank(H)
        rank_H_kron = np.linalg.matrix_rank(H_kron)
        rank_check = rank_H_kron == rank_H * rank_H
        print(f"  rank(H(x)H) = rank(H)^2: {rank_check}")

        all_pass = all_pass and cond_check and rank_check

    print(f"\n[PASS]" if all_pass else "[FAIL]")
    return all_pass


def example_20_vandermonde() -> bool:
    """Example 20: Vandermonde矩阵的Kronecker积"""
    print("\n" + "=" * 60)
    print("Example 20: Vandermonde Kronecker Product")
    print("=" * 60)

    x = np.geomspace(0.1, 5.0, 4)
    y = np.geomspace(0.2, 3.0, 3)

    V_x = np.vander(x, N=len(x), increasing=True)
    V_y = np.vander(y, N=len(y), increasing=True)
    V_kron = kronecker_product(V_x, V_y)

    print(f"V_x shape: {V_x.shape}")
    print(f"V_y shape: {V_y.shape}")
    print(f"V_x (x) V_y shape: {V_kron.shape}")

    # 验证秩
    rank_Vx = np.linalg.matrix_rank(V_x)
    rank_Vy = np.linalg.matrix_rank(V_y)
    rank_Vkron = np.linalg.matrix_rank(V_kron)
    rank_check = rank_Vkron == rank_Vx * rank_Vy

    print(f"rank(V_x) × rank(V_y) = {rank_Vx * rank_Vy}")
    print(f"rank(V_x (x) V_y) = {rank_Vkron}")
    print(f"[PASS]" if rank_check else "[FAIL]")
    return rank_check


def example_21_toeplitz() -> bool:
    """Example 21: Toeplitz矩阵的Kronecker积"""
    print("\n" + "=" * 60)
    print("Example 21: Toeplitz Kronecker Product")
    print("=" * 60)

    def toeplitz_symmetric(n: int, rho: float = 0.8) -> np.ndarray:
        return toeplitz(rho ** np.arange(n))

    T3 = toeplitz_symmetric(3, rho=0.9)
    T4 = toeplitz_symmetric(4, rho=0.85)
    T_kron = kronecker_product(T3, T4)

    print(f"T3 shape: {T3.shape}")
    print(f"T4 shape: {T4.shape}")
    print(f"T3 (x) T4 shape: {T_kron.shape}")

    # 验证正定性（所有特征值大于0）
    eigs_Tkron = np.linalg.eigvals(T_kron)
    pos_def = np.all(eigs_Tkron > 0)
    print(f"T3 (x) T4 positive definite: {pos_def}")
    print(f"min eigenvalue: {np.min(eigs_Tkron):.6e}")

    # 验证特征值乘积性质
    eigs_T3 = np.linalg.eigvals(T3)
    eigs_T4 = np.linalg.eigvals(T4)
    eig_product = np.array([a * b for a in eigs_T3 for b in eigs_T4])

    # 需要排序后比较（可能有数值误差）
    eig_match = np.allclose(sorted(eigs_Tkron), sorted(eig_product), atol=1e-8)
    print(f"Eigenvalues match: {eig_match}")

    result = pos_def and eig_match
    print(f"[PASS]" if result else "[FAIL]")
    return result


def example_22_sparse() -> bool:
    """Example 22: 稀疏矩阵的Kronecker积"""
    print("\n" + "=" * 60)
    print("Example 22: Sparse Kronecker Product (2D Laplacian)")
    print("=" * 60)

    L3 = laplacian_1d(3)
    L4 = laplacian_1d(4)
    L_kron = kronecker_product(L3, L4)

    print(f"L3 shape: {L3.shape}")
    print(f"L4 shape: {L4.shape}")
    print(f"L3 (x) L4 shape: {L_kron.shape}")

    # 验证稀疏性
    density = np.count_nonzero(L_kron) / L_kron.size
    print(f"Density: {density:.4%}")
    print(f"Sparsity: {(1-density):.4%}")

    # 验证条件数
    cond_L3 = np.linalg.cond(L3)
    cond_L4 = np.linalg.cond(L4)
    cond_Lkron = np.linalg.cond(L_kron)

    print(f"cond(L3) = {cond_L3:.6f}")
    print(f"cond(L4) = {cond_L4:.6f}")
    print(f"cond(L3 (x) L4) = {cond_Lkron:.6f}")

    # 条件数关系（近似）
    cond_check = abs(cond_Lkron - cond_L3 * cond_L4) / (cond_L3 * cond_L4) < 0.1
    print(f"[PASS]" if cond_check else "[FAIL]")
    return cond_check


def example_23_pascal() -> bool:
    """Example 23: Pascal矩阵的Kronecker积"""
    print("\n" + "=" * 60)
    print("Example 23: Pascal Kronecker Product")
    print("=" * 60)

    P3 = pascal_matrix(3)
    P4 = pascal_matrix(4)
    P_kron = kronecker_product(P3, P4)

    print(f"P3:\n{P3}")
    print(f"P3 (x) P4 shape: {P_kron.shape}")

    # 验证行列式
    det_P3 = np.linalg.det(P3)
    det_P4 = np.linalg.det(P4)
    det_Pkron = np.linalg.det(P_kron)

    m, n = P3.shape[0], P4.shape[0]
    det_expected = (det_P3 ** n) * (det_P4 ** m)

    print(f"det(P3) = {det_P3:.0f}")
    print(f"det(P4) = {det_P4:.0f}")
    print(f"det(P3 (x) P4) = {det_Pkron:.0f}")
    print(f"det(P3)^n × det(P4)^m = {det_expected:.0f}")

    det_match = np.isclose(det_Pkron, det_expected, rtol=1e-8)
    print(f"[PASS]" if det_match else "[FAIL]")
    return det_match


def example_24_random() -> bool:
    """Example 24: 随机矩阵条件数分析"""
    print("\n" + "=" * 60)
    print("Example 24: Random Matrix Condition Analysis")
    print("=" * 60)

    rng = np.random.RandomState(42)
    A = rng.randn(5, 5)
    B = rng.randn(5, 5)
    AB_kron = kronecker_product(A, B)

    cond_A = np.linalg.cond(A)
    cond_B = np.linalg.cond(B)
    cond_ABkron = np.linalg.cond(AB_kron)

    print(f"cond(A) = {cond_A:.6e}")
    print(f"cond(B) = {cond_B:.6e}")
    print(f"cond(A (x) B) = {cond_ABkron:.6e}")
    print(f"cond(A) × cond(B) = {cond_A * cond_B:.6e}")

    # 条件数关系
    cond_check = np.isclose(cond_ABkron, cond_A * cond_B, rtol=0.1)
    print(f"[PASS]" if cond_check else "[FAIL]")
    return cond_check


def example_25_kronecker_sum() -> bool:
    """Example 25: Kronecker和的条件数"""
    print("\n" + "=" * 60)
    print("Example 25: Kronecker Sum Analysis")
    print("=" * 60)

    A = np.array([[100.0, 99.0], [99.0, 98.0]])
    B = np.array([[1.0, 0.99], [0.99, 0.98]])

    m, n = A.shape[0], B.shape[0]
    kron_sum = kronecker_product(A, np.eye(n)) + kronecker_product(np.eye(m), B)

    print(f"A shape: {A.shape}, B shape: {B.shape}")
    print(f"A (+) B shape: {kron_sum.shape}")

    # 特征值验证
    eig_A = np.linalg.eigvals(A)
    eig_B = np.linalg.eigvals(B)
    eig_sum = np.linalg.eigvals(kron_sum)

    # Kronecker和的特征值是 λ_i + μ_j 的组合
    expected_eigs = np.array([a + b for a in eig_A for b in eig_B])

    print(f"\nEigenvalues of A: {eig_A}")
    print(f"Eigenvalues of B: {eig_B}")

    eig_match = np.allclose(sorted(eig_sum, key=abs), sorted(expected_eigs, key=abs), atol=1e-10)
    print(f"Eigenvalues match: {eig_match}")

    print(f"[PASS]" if eig_match else "[FAIL]")
    return eig_match


def example_26_fibonacci() -> bool:
    """Example 26: Fibonacci矩阵的Kronecker积"""
    print("\n" + "=" * 60)
    print("Example 26: Fibonacci Q-Matrix Kronecker Product")
    print("=" * 60)

    Q3 = fibonacci_q_matrix(3)
    Q4 = fibonacci_q_matrix(4)
    Q_kron = kronecker_product(Q3, Q4)

    print(f"Q3:\n{Q3}")
    print(f"Q3 (x) Q4 shape: {Q_kron.shape}")

    # 验证特征值乘积性质
    eig_Q3 = np.linalg.eigvals(Q3)
    eig_Q4 = np.linalg.eigvals(Q4)
    eig_Qkron = np.linalg.eigvals(Q_kron)

    eig_product = np.array([a * b for a in eig_Q3 for b in eig_Q4])
    eig_match = np.allclose(sorted(eig_Qkron, key=abs), sorted(eig_product, key=abs), atol=1e-8)

    print(f"Eigenvalues match: {eig_match}")
    print(f"[PASS]" if eig_match else "[FAIL]")
    return eig_match


def example_27_circulant() -> bool:
    """Example 27: 循环矩阵的Kronecker积"""
    print("\n" + "=" * 60)
    print("Example 27: Circulant Kronecker Product")
    print("=" * 60)

    # 使用可逆矩阵以避免奇异问题
    C1 = circulant(np.array([1.0, 0.5, 0.3]))
    C2 = circulant(np.array([2.0, 0.8, 0.6, 0.4]))
    C_kron = kronecker_product(C1, C2)

    print(f"C1 shape: {C1.shape}")
    print(f"C2 shape: {C2.shape}")
    print(f"C1 (x) C2 shape: {C_kron.shape}")

    # 验证行列式性质（更容易验证）
    det_C1 = np.linalg.det(C1)
    det_C2 = np.linalg.det(C2)
    det_Ckron = np.linalg.det(C_kron)

    m, n = C1.shape[0], C2.shape[0]
    det_expected = (det_C1 ** n) * (det_C2 ** m)

    print(f"det(C1) = {det_C1:.6f}")
    print(f"det(C2) = {det_C2:.6f}")
    print(f"det(C1 (x) C2) = {det_Ckron:.6f}")
    print(f"det(C1)^n × det(C2)^m = {det_expected:.6f}")

    det_match = np.isclose(det_Ckron, det_expected)
    print(f"Determinant property: {det_match}")

    # 验证条件数关系
    cond_C1 = np.linalg.cond(C1)
    cond_C2 = np.linalg.cond(C2)
    cond_Ckron = np.linalg.cond(C_kron)

    cond_product = cond_C1 * cond_C2
    cond_match = np.isclose(cond_Ckron, cond_product, rtol=0.05)

    print(f"cond(C1) = {cond_C1:.6f}")
    print(f"cond(C2) = {cond_C2:.6f}")
    print(f"cond(C1 (x) C2) = {cond_Ckron:.6f}")
    print(f"cond(C1) × cond(C2) = {cond_product:.6f}")
    print(f"Condition number property: {cond_match}")

    result = det_match and cond_match
    print(f"[PASS]" if result else "[FAIL]")
    return result


def example_28_large_scale() -> bool:
    """Example 28: 大规模矩阵性能测试"""
    print("\n" + "=" * 60)
    print("Example 28: Large Scale Performance Test")
    print("=" * 60)

    import time

    # 测试中等规模
    m, n, p, q = 20, 20, 20, 20

    A = np.random.randn(m, n)
    B = np.random.randn(p, q)

    start = time.time()
    AB_kron = kronecker_product(A, B)
    elapsed = time.time() - start

    print(f"A shape: {A.shape}, B shape: {B.shape}")
    print(f"A (x) B shape: {AB_kron.shape}")
    print(f"Total elements: {AB_kron.size:,}")
    print(f"Memory: {AB_kron.nbytes / (1024*1024):.2f} MB")
    print(f"Time: {elapsed:.4f} seconds")

    # 验证维度
    shape_check = AB_kron.shape == (m * p, n * q)
    print(f"[PASS]" if shape_check else "[FAIL]")
    return shape_check


def main():
    """Run all complex matrix examples."""
    examples = [
        ("Hilbert Kronecker Product", example_19_hilbert),
        ("Vandermonde Kronecker Product", example_20_vandermonde),
        ("Toeplitz Kronecker Product", example_21_toeplitz),
        ("Sparse Kronecker Product", example_22_sparse),
        ("Pascal Kronecker Product", example_23_pascal),
        ("Random Matrix Analysis", example_24_random),
        ("Kronecker Sum Analysis", example_25_kronecker_sum),
        ("Fibonacci Q-Matrix", example_26_fibonacci),
        ("Circulant Kronecker Product", example_27_circulant),
        ("Large Scale Performance", example_28_large_scale),
    ]

    results = []
    for name, example in examples:
        try:
            result = example()
            results.append((name, result))
        except Exception as e:
            print(f"[FAIL] - Exception: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} - {name}")

    print(f"\nTotal: {passed}/{total} examples passed")

    if passed == total:
        print("All complex matrix examples passed!")
        return 0
    else:
        print(f"{total - passed} example(s) failed!")
        return 1


if __name__ == "__main__":
    exit(main())
