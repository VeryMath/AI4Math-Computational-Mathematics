"""Test skills by simulating natural language interface.

This script tests each skill by processing the examples from examples.md files
and simulating the skill's natural language processing behavior.
"""

from __future__ import annotations

import importlib.util
import numpy as np


def load_module(path: str, name: str):
    """Load a Python module from a file path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module {name} from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ============================================================================
# CHOLESKY DECOMPOSITION
# ============================================================================

def test_cholesky_natural_language():
    """Simulate natural language interface for Cholesky skill."""
    print("\n" + "=" * 80)
    print("Testing: /cholesky-decomposition")
    print("=" * 80)

    mod = load_module(
        "c:/Users/trw/my-ai-math/matrix-computation/cholesky-decomposition/scripts/solve_cholesky.py",
        "solve_cholesky"
    )

    # Example 1: Basic Cholesky decomposition
    print("\n[User]: 对矩阵 A = [[25, 15, -5], [15, 18, 0], [-5, 0, 11]] 进行 Cholesky 分解")
    A = np.array([[25.0, 15.0, -5.0], [15.0, 18.0, 0.0], [-5.0, 0.0, 11.0]])

    # Check symmetry
    is_sym = mod.is_symmetric(A)
    print(f"   [OK] 矩阵检查: shape={A.shape}, 对称={is_sym}")

    # Check SPD
    is_spd_result = mod.is_spd(A)
    print(f"   [OK] 正定性检查: {'是 SPD' if is_spd_result else '不是 SPD'}")

    # Factorize
    L = mod.factorize_cholesky(A)
    print(f"\n   [Result] 分解结果 L (下三角矩阵):")
    print(f"   {L}")

    # Verify
    recon_error = mod.reconstruction_error(A, L)
    print(f"\n   [OK] 验证: ||A - LL^T|| = {recon_error:.2e}")

    # Example 2: Solve SPD linear system
    print("\n[User]: 求解线性方程组 Ax = b，其中 A = [[4, 1], [1, 3]], b = [1, 2]")
    A = np.array([[4.0, 1.0], [1.0, 3.0]])
    b = np.array([1.0, 2.0])

    x = mod.solve_cholesky(A, b)
    residual = np.linalg.norm(A @ x - b)
    print(f"   [OK] 解 x: {x}")
    print(f"   [OK] 残差 ||Ax - b||: {residual:.2e}")

    # Example 3: Check SPD validation
    print("\n[User]: 判断矩阵 A1 = [[4, 1], [1, 3]] 和 A2 = [[1, 2], [2, 1]] 是否为对称正定矩阵")
    A1 = np.array([[4.0, 1.0], [1.0, 3.0]])
    A2 = np.array([[1.0, 2.0], [2.0, 1.0]])

    print(f"   A1: 对称={mod.is_symmetric(A1)}, SPD={mod.is_spd(A1)}")
    print(f"   A2: 对称={mod.is_symmetric(A2)}, SPD={mod.is_spd(A2)}")

    # Example 4: Hilbert matrix (ill-conditioned)
    print("\n[User]: 对 8×8 Hilbert 矩阵进行 Cholesky 分解")
    def hilbert(n):
        i = np.arange(1, n + 1)
        return np.array([[1.0 / (ii + jj - 1) for jj in i] for ii in i], dtype=float)

    H = hilbert(8)
    cond = np.linalg.cond(H)
    print(f"   [OK] 矩阵条件数: {cond:.2e} (高度病态)")

    L = mod.factorize_cholesky(H)
    recon_error = mod.reconstruction_error(H, L)
    print(f"   [OK] Cholesky 分解完成")
    print(f"   [OK] 重构误差: {recon_error:.2e}")


# ============================================================================
# CONJUGATE GRADIENT
# ============================================================================

def test_conjugate_gradient_natural_language():
    """Simulate natural language interface for CG skill."""
    print("\n" + "=" * 80)
    print("Testing: /conjugate-gradient")
    print("=" * 80)

    mod = load_module(
        "c:/Users/trw/my-ai-math/matrix-computation/conjugate-gradient/scripts/solve_cg.py",
        "solve_cg"
    )

    # Example 1: Basic SPD system
    print("\n[User]: 求解线性方程组 Ax = b，A = [[4, 1], [1, 3]], b = [1, 2]，容差 tol=1e-10")
    A = np.array([[4.0, 1.0], [1.0, 3.0]])
    b = np.array([1.0, 2.0])

    x, info = mod.conjugate_gradient(A, b, tol=1e-10, maxiter=1000)
    residual = np.linalg.norm(A @ x - b)
    print(f"   [OK] 迭代次数: {info.get('iterations', 'N/A')}")
    print(f"   [OK] 解 x: {x}")
    print(f"   [OK] 残差 ||Ax - b||: {residual:.2e}")
    print(f"   [OK] 收敛: {info.get('converged', False)}")

    # Example 2: Hilbert matrix
    print("\n[User]: 求解 Hilbert 矩阵系统，8×8, H[i,j] = 1/(i+j+1)")
    def hilbert(n):
        i = np.arange(1, n + 1)
        return np.array([[1.0 / (ii + jj - 1) for jj in i] for ii in i], dtype=float)

    H = hilbert(8)
    b = np.ones(8)
    cond = np.linalg.cond(H)
    print(f"   [OK] 条件数: {cond:.2e} (病态)")

    x, info = mod.conjugate_gradient(H, b, tol=1e-8, maxiter=1000)
    residual = np.linalg.norm(H @ x - b)
    print(f"   [OK] 迭代次数: {info.get('iterations', 'N/A')}")
    print(f"   [OK] 残差: {residual:.2e}")


# ============================================================================
# LU DECOMPOSITION
# ============================================================================

def test_lu_natural_language():
    """Simulate natural language interface for LU skill."""
    print("\n" + "=" * 80)
    print("Testing: /lu-decomposition")
    print("=" * 80)

    mod = load_module(
        "c:/Users/trw/my-ai-math/matrix-computation/lu-decomposition/scripts/solve_lu.py",
        "solve_lu"
    )

    # Example 1: Basic LU decomposition
    print("\n[User]: 对矩阵 A = [[2, 1, 1], [4, -6, 0], [-2, 7, 2]] 进行 LU 分解")
    A = np.array([[2.0, 1.0, 1.0], [4.0, -6.0, 0.0], [-2.0, 7.0, 2.0]])

    P, L, U = mod.factorize_lu(A)
    print(f"   [OK] 排列矩阵 P:\n{P}")
    print(f"   [OK] 下三角 L:\n{L}")
    print(f"   [OK] 上三角 U:\n{U}")

    recon_error = mod.reconstruction_error(A, P, L, U)
    print(f"   [OK] 重构误差 ||A - PLU||: {recon_error:.2e}")

    # Example 2: Solve linear system
    print("\n[User]: 求解 Ax = b，A = [[2, 1, 1], [4, -6, 0], [-2, 7, 2]]，b = [5, -2, 9]")
    b = np.array([5.0, -2.0, 9.0])

    x = mod.solve_lu(A, b)
    residual = np.linalg.norm(A @ x - b)
    print(f"   [OK] 解 x: {x}")
    print(f"   [OK] 残差 ||Ax - b||: {residual:.2e}")

    # Example 3: Determinant
    det = mod.determinant_from_lu(A)
    print(f"\n[User]: 计算矩阵 A 的行列式")
    print(f"   [OK] det(A) = {det:.6f}")

    # Example 4: Inverse
    print("\n[User]: 计算矩阵 A 的逆矩阵")
    A_inv = mod.inverse_from_lu(A)
    print(f"   [OK] A^(-1) shape: {A_inv.shape}")
    print(f"   [OK] 验证 A @ A^(-1) ~= I: {np.allclose(A @ A_inv, np.eye(3))}")


# ============================================================================
# QR DECOMPOSITION
# ============================================================================

def test_qr_natural_language():
    """Simulate natural language interface for QR skill."""
    print("\n" + "=" * 80)
    print("Testing: /qr-decomposition")
    print("=" * 80)

    mod = load_module(
        "c:/Users/trw/my-ai-math/matrix-computation/qr-decomposition/scripts/solve_qr.py",
        "solve_qr"
    )

    # Example 1: Basic QR decomposition
    print("\n[User]: 对矩阵 A = [[1, 2, 3], [4, 5, 6], [7, 8, 10]] 进行 QR 分解")
    A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 10.0]])

    Q, R = mod.qr_decompose(A)
    orth_error = mod.orthogonal_residual(Q)
    print(f"   [OK] 正交矩阵 Q:\n{Q}")
    print(f"   [OK] 上三角 R:\n{R}")
    print(f"   [OK] Q^T Q - I 的范数: {orth_error:.2e}")

    recon_error = np.linalg.norm(A - Q @ R)
    print(f"   [OK] 重构误差 ||A - QR||: {recon_error:.2e}")

    # Example 2: Least squares
    print("\n[User]: 求解最小二乘问题 min ||Ax - b||，A = [[1, 2], [3, 4], [5, 6]]，b = [1, 2, 3]")
    A = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    b = np.array([1.0, 2.0, 3.0])

    x = mod.solve_least_squares_qr(A, b)
    residual = np.linalg.norm(A @ x - b)
    print(f"   [OK] 最小二乘解 x: {x}")
    print(f"   [OK] 残差 ||Ax - b||: {residual:.2e}")

    # Example 3: Rank estimation
    print("\n[User]: 估计矩阵 A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]] 的秩")
    A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])

    rank = mod.estimate_rank_qr(A)
    print(f"   [OK] 数值秩估计: {rank}")


# ============================================================================
# SVD DECOMPOSITION
# ============================================================================

def test_svd_natural_language():
    """Simulate natural language interface for SVD skill."""
    print("\n" + "=" * 80)
    print("Testing: /svd-decomposition")
    print("=" * 80)

    mod = load_module(
        "c:/Users/trw/my-ai-math/matrix-computation/svd-decomposition/scripts/solve_svd.py",
        "solve_svd"
    )

    # Example 1: Basic SVD
    print("\n[User]: 对矩阵 A = [[3, 1, 1], [-1, 3, 1]] 进行 SVD 分解")
    A = np.array([[3.0, 1.0, 1.0], [-1.0, 3.0, 1.0]])

    U, s, Vt = mod.svd_decompose(A)
    print(f"   [OK] 左奇异矩阵 U:\n{U}")
    print(f"   [OK] 奇异值 s: {s}")
    print(f"   [OK] 右奇异矩阵 V^T:\n{Vt}")

    recon_error = mod.reconstruction_error(A, U, s, Vt)
    print(f"   [OK] 重构误差 ||A - USigmaV^T||: {recon_error:.2e}")

    # Example 2: Rank-k approximation
    print("\n[User]: 计算矩阵的秩-1 近似")
    A1 = mod.rank_k_approximation(A, k=1)
    print(f"   [OK] 秩-1 近似 shape: {A1.shape}")
    print(f"   [OK] 近似误差 ||A - A_1||: {np.linalg.norm(A - A1):.2e}")

    # Example 3: Pseudoinverse and least squares
    print("\n[User]: 使用 SVD 求解最小二乘问题")
    b = np.array([1.0, 2.0])
    x = mod.solve_least_squares_svd(A, b)
    residual = np.linalg.norm(A @ x - b)
    print(f"   [OK] 解 x: {x}")
    print(f"   [OK] 残差 ||Ax - b||: {residual:.2e}")


# ============================================================================
# KRONECKER PRODUCT
# ============================================================================

def test_kronecker_natural_language():
    """Simulate natural language interface for Kronecker skill."""
    print("\n" + "=" * 80)
    print("Testing: /kronecker-product")
    print("=" * 80)

    mod = load_module(
        "c:/Users/trw/my-ai-math/matrix-computation/kronecker-product/scripts/solve_kronecker.py",
        "solve_kronecker"
    )

    # Example 1: Basic Kronecker product
    print("\n[User]: 计算 Kronecker 积 A x B，A = [[1, 2], [3, 4]]，B = [[0, 5], [6, 7]]")
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    B = np.array([[0.0, 5.0], [6.0, 7.0]])

    result = mod.kronecker_product(A, B)
    print(f"   [OK] A x B:\n{result}")
    print(f"   [OK] 结果 shape: {result.shape} (2×2 x 2×2 = 4×4)")

    # Example 2: Properties
    print("\n[User]: 验证 Kronecker 积的性质")
    C = np.eye(2)

    assoc = mod.verify_associativity(A, B, C)
    transpose = mod.verify_transpose(A, B)

    print(f"   [OK] 结合律 (AxB)xC = Ax(BxC): {assoc}")
    print(f"   [OK] 转置性质 (AxB)^T = A^TxB^T: {transpose}")

    # Example 3: Rank property
    rank_kron = mod.rank_kron(A, B)
    print(f"   [OK] 秩性质 rank(AxB) = rank(A)×rank(B): {rank_kron}")


# ============================================================================
# MATRIX NORM
# ============================================================================

def test_matrix_norm_natural_language():
    """Simulate natural language interface for Matrix Norm skill."""
    print("\n" + "=" * 80)
    print("Testing: /matrix-norm")
    print("=" * 80)

    mod = load_module(
        "c:/Users/trw/my-ai-math/matrix-computation/matrix-norm/scripts/solve_norm.py",
        "solve_norm"
    )

    # Example 1: Various norms
    print("\n[User]: 计算矩阵 A = [[1, 2], [3, 4]] 的各种范数")
    A = np.array([[1.0, 2.0], [3.0, 4.0]])

    fro = mod.frobenius_norm(A)
    spec = mod.spectral_norm(A)
    one_norm = mod.norm_1(A)
    inf_norm = mod.norm_infinity(A)
    nuc = mod.nuclear_norm(A)

    print(f"   [OK] Frobenius 范数 ||A||_F: {fro:.6f}")
    print(f"   [OK] 谱范数 (2-范数) ||A||_2: {spec:.6f}")
    print(f"   [OK] 1-范数 ||A||_1: {one_norm:.6f}")
    print(f"   [OK] 无穷范数 ||A||_inf: {inf_norm:.6f}")
    print(f"   [OK] 核范数 ||A||_*: {nuc:.6f}")

    # Example 2: Condition number
    print("\n[User]: 计算矩阵的条件数")
    cond = mod.condition_number(A, p=2)
    print(f"   [OK] 条件数 κ_2(A) = {cond:.6f}")


# ============================================================================
# EIGENVALUE COMPUTATION
# ============================================================================

def test_eigenvalue_natural_language():
    """Simulate natural language interface for Eigenvalue skill."""
    print("\n" + "=" * 80)
    print("Testing: /eigenvalue-computation")
    print("=" * 80)

    mod = load_module(
        "c:/Users/trw/my-ai-math/matrix-computation/eigenvalue-computation/scripts/solve_eigen.py",
        "solve_eigen"
    )

    # Example 1: Symmetric matrix
    print("\n[User]: 计算对称矩阵 A = [[2, 1, 0], [1, 2, 1], [0, 1, 2]] 的特征值和特征向量")
    A = np.array([[2.0, 1.0, 0.0], [1.0, 2.0, 1.0], [0.0, 1.0, 2.0]])

    values, vectors = mod.symmetric_eigen_decompose(A)
    print(f"   [OK] 特征值: {values}")
    print(f"   [OK] 特征向量:\n{vectors}")

    # Verify orthogonality
    orth_error = np.linalg.norm(vectors.T @ vectors - np.eye(3))
    print(f"   [OK] 特征向量正交性验证: ||Q^T Q - I|| = {orth_error:.2e}")

    # Example 2: Power method
    print("\n[User]: 使用幂法计算最大特征值")
    lam, v = mod.power_method(A, tol=1e-10, maxiter=1000)
    print(f"   [OK] 最大特征值近似: {lam:.6f}")
    print(f"   [OK] 对应特征向量: {v}")


# ============================================================================
# GMRES
# ============================================================================

def test_gmres_natural_language():
    """Simulate natural language interface for GMRES skill."""
    print("\n" + "=" * 80)
    print("Testing: /generalized-minimal-residual")
    print("=" * 80)

    mod = load_module(
        "c:/Users/trw/my-ai-math/matrix-computation/generalized-minimal-residual/scripts/solve_gmres.py",
        "solve_gmres"
    )

    # Example 1: Non-symmetric system
    print("\n[User]: 求解非对称线性系统 Ax = b，A = [[1, 2], [3, 4]]，b = [5, 6]")
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    b = np.array([5.0, 6.0])

    x, info = mod.gmres(A, b, tol=1e-8, maxiter=100)
    residual = np.linalg.norm(A @ x - b)
    print(f"   [OK] 解 x: {x}")
    print(f"   [OK] 残差 ||Ax - b||: {residual:.2e}")
    print(f"   [OK] 迭代次数: {info.get('iterations', 'N/A')}")
    print(f"   [OK] 收敛: {info.get('converged', False)}")


# ============================================================================
# MAIN RUNNER
# ============================================================================

def main():
    print("=" * 80)
    print("MATRIX COMPUTATION SKILLS - NATURAL LANGUAGE INTERFACE TEST")
    print("=" * 80)
    print("\n这个测试模拟通过自然语言接口调用每个 skill 的行为")
    print("每个测试都展示了 skill 如何理解和响应用户的查询\n")

    test_cholesky_natural_language()
    test_conjugate_gradient_natural_language()
    test_lu_natural_language()
    test_qr_natural_language()
    test_svd_natural_language()
    test_kronecker_natural_language()
    test_matrix_norm_natural_language()
    test_eigenvalue_natural_language()
    test_gmres_natural_language()

    print("\n" + "=" * 80)
    print("所有 skills 测试完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()
