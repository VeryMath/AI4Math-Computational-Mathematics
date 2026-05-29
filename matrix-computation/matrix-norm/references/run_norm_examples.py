"""Test script for all matrix norm examples."""

from __future__ import annotations

import numpy as np  # pyright: ignore[reportMissingImports]


def example_1_frobenius_norm() -> bool:
    """Example 1: Frobenius范数"""
    print("=" * 60)
    print("Example 1: Frobenius范数")
    print("=" * 60)

    A = np.array([
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
        [7.0, 8.0, 9.0],
    ])

    fro_norm = np.linalg.norm(A, ord='fro')
    print(f"Frobenius norm: {fro_norm:.6f}")

    # 手动计算验证
    manual = np.sqrt(np.sum(A**2))
    print(f"Manual calculation: {manual:.6f}")

    is_correct = np.isclose(fro_norm, manual)
    print("[PASS]" if is_correct else "[FAIL]")
    return is_correct


def example_2_spectral_norm() -> bool:
    """Example 2: 谱范数(2-范数)"""
    print("\n" + "=" * 60)
    print("Example 2: 谱范数(2-范数)")
    print("=" * 60)

    A = np.array([
        [3.0, 1.0],
        [1.0, 2.0],
    ])

    spec_norm = np.linalg.norm(A, ord=2)
    print(f"Spectral norm: {spec_norm:.6f}")

    # 通过SVD验证
    u, s, vt = np.linalg.svd(A)
    print(f"Max singular value: {s[0]:.6f}")

    is_correct = np.isclose(spec_norm, s[0])
    print("[PASS]" if is_correct else "[FAIL]")
    return is_correct


def example_3_1_inf_norm() -> bool:
    """Example 3: 1-范数和∞-范数"""
    print("\n" + "=" * 60)
    print("Example 3: 1-范数和∞-范数")
    print("=" * 60)

    A = np.array([
        [1.0, -2.0, 3.0],
        [-4.0, 5.0, -6.0],
    ])

    norm_1 = np.linalg.norm(A, ord=1)
    norm_inf = np.linalg.norm(A, ord=np.inf)

    print(f"1-norm (max column sum): {norm_1:.6f}")
    # 手动验证列和
    col_sums = np.sum(np.abs(A), axis=0)
    print(f"Column sums: {col_sums}")
    print(f"Max column sum: {np.max(col_sums):.6f}")

    print(f"\nInfinity-norm (max row sum): {norm_inf:.6f}")
    # 手动验证行和
    row_sums = np.sum(np.abs(A), axis=1)
    print(f"Row sums: {row_sums}")
    print(f"Max row sum: {np.max(row_sums):.6f}")

    is_correct = np.isclose(norm_1, np.max(col_sums)) and np.isclose(norm_inf, np.max(row_sums))
    print("[PASS]" if is_correct else "[FAIL]")
    return is_correct


def example_4_nuclear_norm() -> bool:
    """Example 4: 核范数(Nuclear Norm)"""
    print("\n" + "=" * 60)
    print("Example 4: 核范数(Nuclear Norm)")
    print("=" * 60)

    A = np.array([
        [3.0, 1.0],
        [1.0, 2.0],
    ])

    nuc_norm = np.linalg.norm(A, ord='nuc')
    print(f"Nuclear norm: {nuc_norm:.6f}")

    # 通过SVD验证
    u, s, vt = np.linalg.svd(A)
    print(f"Sum of singular values: {np.sum(s):.6f}")

    is_correct = np.isclose(nuc_norm, np.sum(s))
    print("[PASS]" if is_correct else "[FAIL]")
    return is_correct


def example_5_p_norm() -> bool:
    """Example 5: 一般p-范数"""
    print("\n" + "=" * 60)
    print("Example 5: 一般p-范数")
    print("=" * 60)

    A = np.array([
        [2.0, 1.0],
        [1.0, 2.0],
    ])

    # 1-范数, 2-范数, ∞-范数
    results = {}
    for p in [1, 2, np.inf]:
        norm_p = np.linalg.norm(A, ord=p)
        results[p if p != np.inf else 'inf'] = norm_p
        print(f"||A||_{p if p != np.inf else 'inf'} = {norm_p:.6f}")

    # 验证几个基本性质
    # 2-norm <= 1-norm for this matrix should hold
    is_correct = results[2] <= results[1] + 1e-10
    print("[PASS]" if is_correct else "[FAIL]")
    return is_correct


def example_6_condition_number() -> bool:
    """Example 6: 条件数与数值稳定性"""
    print("\n" + "=" * 60)
    print("Example 6: 条件数与数值稳定性")
    print("=" * 60)

    # 条件数良好的矩阵
    A_well = np.array([
        [1.0, 0.0],
        [0.0, 1.0],
    ])
    kappa_well = np.linalg.cond(A_well)
    print(f"Well-conditioned: kappa(A) = {kappa_well:.2f}")

    # 条件数较差的矩阵
    A_poor = np.array([
        [1.0, 1.0],
        [1.0, 1.000001],
    ])
    kappa_poor = np.linalg.cond(A_poor)
    print(f"Poor-conditioned: kappa(A) = {kappa_poor:.2e}")

    # 不同范数的条件数
    A = np.array([
        [2.0, 1.0],
        [1.0, 2.0],
    ])
    print(f"\nCondition numbers for different norms:")
    for p in [1, 2, np.inf]:
        kappa = np.linalg.cond(A, p=p)
        print(f"kappa_{p if p != np.inf else 'inf'}(A) = {kappa:.6f}")

    # 验证单位矩阵条件数为1
    is_correct = np.isclose(kappa_well, 1.0) and kappa_poor > 1e6
    print("[PASS]" if is_correct else "[FAIL]")
    return is_correct


def example_7_frobenius_distance() -> bool:
    """Example 7: Frobenius距离"""
    print("\n" + "=" * 60)
    print("Example 7: Frobenius距离")
    print("=" * 60)

    A = np.array([
        [1.0, 2.0],
        [3.0, 4.0],
    ])

    B = np.array([
        [1.1, 2.1],
        [2.9, 4.1],
    ])

    distance_fro = np.linalg.norm(A - B, ord='fro')
    print(f"Frobenius distance: {distance_fro:.6f}")
    print(f"Relative distance: {distance_fro / np.linalg.norm(A, ord='fro'):.4%}")

    # 手动验证
    manual = np.sqrt(np.sum((A - B)**2))
    is_correct = np.isclose(distance_fro, manual)
    print("[PASS]" if is_correct else "[FAIL]")
    return is_correct


def example_8_spectral_distance() -> bool:
    """Example 8: 谱距离"""
    print("\n" + "=" * 60)
    print("Example 8: 谱距离")
    print("=" * 60)

    A = np.array([
        [3.0, 1.0],
        [1.0, 2.0],
    ])

    B = np.array([
        [3.0, 1.0],
        [1.0, 2.001],
    ])

    distance_spec = np.linalg.norm(A - B, ord=2)
    print(f"Spectral distance: {distance_spec:.8f}")

    # 通过SVD验证
    diff = A - B
    u, s, vt = np.linalg.svd(diff)
    print(f"Max singular value of diff: {s[0]:.8f}")

    is_correct = np.isclose(distance_spec, s[0])
    print("[PASS]" if is_correct else "[FAIL]")
    return is_correct


def example_9_orthogonal_matrix() -> bool:
    """Example 9: 正交矩阵的范数"""
    print("\n" + "=" * 60)
    print("Example 9: 正交矩阵的范数")
    print("=" * 60)

    # 生成随机正交矩阵
    A = np.random.randn(3, 3)
    Q, _ = np.linalg.qr(A)

    print("Orthogonal matrix Q (first row):")
    print(Q[0, :])

    norm_2 = np.linalg.norm(Q, ord=2)
    norm_fro = np.linalg.norm(Q, ord='fro')
    expected_fro = np.sqrt(3)

    print(f"\n||Q||_2 = {norm_2:.6f} (expected: 1)")
    print(f"||Q||_F = {norm_fro:.6f} (expected: {expected_fro:.6f})")
    print(f"||Q||_1 = {np.linalg.norm(Q, ord=1):.6f}")
    print(f"||Q||_inf = {np.linalg.norm(Q, ord=np.inf):.6f}")

    # 验证正交矩阵性质
    is_correct = np.isclose(norm_2, 1.0) and np.isclose(norm_fro, expected_fro)
    print("[PASS]" if is_correct else "[FAIL]")
    return is_correct


def example_10_diagonal_matrix() -> bool:
    """Example 10: 对角矩阵的范数"""
    print("\n" + "=" * 60)
    print("Example 10: 对角矩阵的范数")
    print("=" * 60)

    D = np.diag([1.0, 2.0, 3.0])

    print("Diagonal matrix D:")
    print(D)

    norm_2 = np.linalg.norm(D, ord=2)
    norm_fro = np.linalg.norm(D, ord='fro')
    norm_1 = np.linalg.norm(D, ord=1)
    norm_inf = np.linalg.norm(D, ord=np.inf)

    expected_2 = 3.0  # max |d_i|
    expected_fro = np.sqrt(1 + 4 + 9)  # sqrt(sum d_i^2)
    expected_1 = 3.0  # max |d_i|

    print(f"\n||D||_2 = {norm_2:.6f} (max |d_i| = {expected_2:.6f})")
    print(f"||D||_F = {norm_fro:.6f} (sqrt(sum d_i^2) = {expected_fro:.6f})")
    print(f"||D||_1 = {norm_1:.6f} (max |d_i| = {expected_1:.6f})")
    print(f"||D||_inf = {norm_inf:.6f} (max |d_i| = {expected_1:.6f})")

    is_correct = (np.isclose(norm_2, expected_2) and
                  np.isclose(norm_fro, expected_fro) and
                  np.isclose(norm_1, expected_1) and
                  np.isclose(norm_inf, expected_1))
    print("[PASS]" if is_correct else "[FAIL]")
    return is_correct


def example_11_frobenius_spectral_inequality() -> bool:
    """Example 11: Frobenius与谱范数的关系"""
    print("\n" + "=" * 60)
    print("Example 11: Frobenius与谱范数的关系")
    print("=" * 60)

    np.random.seed(42)
    A = np.random.randn(4, 3)

    fro = np.linalg.norm(A, ord='fro')
    spec = np.linalg.norm(A, ord=2)

    print(f"Frobenius norm: {fro:.6f}")
    print(f"Spectral norm: {spec:.6f}")
    bound = np.sqrt(min(A.shape)) * spec
    print(f"sqrt(min(m,n)) * ||A||_2: {bound:.6f}")
    print(f"\nInequality check:")
    check1 = spec <= fro
    check2 = fro <= bound
    print(f"||A||_2 <= ||A||_F: {check1}")
    print(f"||A||_F <= sqrt(min(m,n)) * ||A||_2: {check2}")

    is_correct = check1 and check2
    print("[PASS]" if is_correct else "[FAIL]")
    return is_correct


def example_12_norm_inequality() -> bool:
    """Example 12: 范数关系不等式"""
    print("\n" + "=" * 60)
    print("Example 12: 范数关系不等式")
    print("=" * 60)

    A = np.array([
        [2.0, 1.0, 3.0],
        [1.0, 4.0, 1.0],
    ])

    spec = np.linalg.norm(A, ord=2)
    norm_1 = np.linalg.norm(A, ord=1)
    norm_inf = np.linalg.norm(A, ord=np.inf)

    print(f"||A||_2: {spec:.6f}")
    bound = np.sqrt(norm_1 * norm_inf)
    print(f"sqrt(||A||_1 * ||A||_inf): {bound:.6f}")

    is_correct = spec <= bound + 1e-10
    print(f"Inequality holds: {is_correct}")
    print("[PASS]" if is_correct else "[FAIL]")
    return is_correct


def example_13_rank1_nuclear() -> bool:
    """Example 13: 秩1矩阵的核范数"""
    print("\n" + "=" * 60)
    print("Example 13: 秩1矩阵的核范数")
    print("=" * 60)

    u = np.array([1.0, 2.0, 3.0]).reshape(-1, 1)
    v = np.array([2.0, 1.0, 0.5]).reshape(-1, 1)

    A = u @ v.T  # Rank-1 matrix

    print("Rank-1 matrix A = u @ v^T:")
    print(A)
    print(f"Rank of A: {np.linalg.matrix_rank(A)}")

    spec = np.linalg.norm(A, ord=2)
    nuc = np.linalg.norm(A, ord='nuc')
    print(f"\n||A||_2 = {spec:.6f}")
    print(f"||A||_* = {nuc:.6f}")

    is_correct = np.isclose(spec, nuc)
    print(f"For rank-1 matrix: ||A||_2 = ||A||_*: {is_correct}")
    print("[PASS]" if is_correct else "[FAIL]")
    return is_correct


def example_14_hilbert() -> bool:
    """Example 14: Hilbert矩阵的范数和条件数"""
    print("\n" + "=" * 60)
    print("Example 14: Hilbert矩阵的范数和条件数")
    print("=" * 60)

    def hilbert(n: int) -> np.ndarray:
        return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)], dtype=float)

    conds = []
    for n in [3, 5, 8]:
        H = hilbert(n)
        fro = np.linalg.norm(H, ord='fro')
        spec = np.linalg.norm(H, ord=2)
        cond = np.linalg.cond(H)
        conds.append(cond)

        print(f"\nHilbert({n}):")
        print(f"  Frobenius norm: {fro:.6e}")
        print(f"  Spectral norm: {spec:.6e}")
        print(f"  Condition number: {cond:.6e}")

    # Hilbert矩阵条件数应随n增大而增大
    all_correct = conds[0] < conds[1] < conds[2]
    print(f"\nCondition numbers grow with n: {conds}")
    print(f"[PASS]" if all_correct else "[FAIL]")
    return all_correct


def example_15_vandermonde() -> bool:
    """Example 15: Vandermonde矩阵的范数"""
    print("\n" + "=" * 60)
    print("Example 15: Vandermonde矩阵的范数")
    print("=" * 60)

    x = np.geomspace(0.1, 10, 10)
    V = np.vander(x, N=len(x), increasing=True)

    print(f"Vandermonde matrix shape: {V.shape}")
    fro = np.linalg.norm(V, ord='fro')
    spec = np.linalg.norm(V, ord=2)
    cond = np.linalg.cond(V)

    print(f"Frobenius norm: {fro:.6e}")
    print(f"Spectral norm: {spec:.6e}")
    print(f"Condition number: {cond:.6e}")

    # Vandermonde矩阵通常条件数很大
    is_correct = cond > 1e5
    print("[PASS]" if is_correct else "[FAIL]")
    return is_correct


def main():
    """Run all examples and report results."""
    examples = [
        example_1_frobenius_norm,
        example_2_spectral_norm,
        example_3_1_inf_norm,
        example_4_nuclear_norm,
        example_5_p_norm,
        example_6_condition_number,
        example_7_frobenius_distance,
        example_8_spectral_distance,
        example_9_orthogonal_matrix,
        example_10_diagonal_matrix,
        example_11_frobenius_spectral_inequality,
        example_12_norm_inequality,
        example_13_rank1_nuclear,
        example_14_hilbert,
        example_15_vandermonde,
    ]

    results = []
    for example in examples:
        try:
            result = example()
            results.append((example.__name__, result))
        except Exception as e:
            print(f"[FAIL] - Exception: {e}")
            results.append((example.__name__, False))

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
        print("All examples passed!")
        return 0
    else:
        print(f"{total - passed} example(s) failed!")
        return 1


if __name__ == "__main__":
    exit(main())
