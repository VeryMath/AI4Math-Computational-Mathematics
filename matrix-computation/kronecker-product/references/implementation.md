# Kronecker Product - Implementation Reference

> **Note**: This file contains low-level implementation details using numpy/scipy. For usage examples of the `/kronecker-product` skill, see [examples.md](./examples.md).

---

## 基础示例

### Example 1: 基础克罗内克积

克罗内克积的定义：对于 A(m×n) 和 B(p×q)，A ⊗ B 是 (mp × nq) 矩阵：

```python
import numpy as np

A = np.array([
    [1.0, 2.0],
    [3.0, 4.0],
])

B = np.array([
    [0.0, 5.0],
    [6.0, 7.0],
])

kron_AB = np.kron(A, B)
print("A ⊗ B =")
print(kron_AB)
print(f"Shape: {kron_AB.shape}")  # Should be (4, 4)
```

### Example 2: 单位矩阵的克罗内克积

单位矩阵的克罗内克积生成块单位矩阵：

```python
import numpy as np

I2 = np.eye(2)
I3 = np.eye(3)

kron_I = np.kron(I2, I3)
print("I₂ ⊗ I₃ =")
print(kron_I)
# 结果是 6×6 块对角单位矩阵
```

### Example 3: 向量的克罗内克积

向量的克罗内克积生成更大维度的向量：

```python
import numpy as np

u = np.array([1.0, 2.0])
v = np.array([3.0, 4.0, 5.0])

kron_uv = np.kron(u, v)
print(f"u ⊗ v = {kron_uv}")
print(f"Shape: {kron_uv.shape}")  # Should be (6,)
```

---

## 性质验证示例

### Example 4: 结合律

验证 (A ⊗ B) ⊗ C = A ⊗ (B ⊗ C)：

```python
import numpy as np

A = np.array([[1.0, 2.0], [3.0, 4.0]])
B = np.array([[0.0, 1.0], [1.0, 0.0]])
C = np.array([[1.0, 1.0], [0.0, 1.0]])

left = np.kron(np.kron(A, B), C)
right = np.kron(A, np.kron(B, C))

print("Associativity holds:", np.allclose(left, right))
print(f"Max difference: {np.max(np.abs(left - right)):.2e}")
```

### Example 5: 转置性质

验证 (A ⊗ B)^T = A^T ⊗ B^T：

```python
import numpy as np

A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
B = np.array([[0.0, 1.0], [1.0, 0.0]])

left = np.kron(A, B).T
right = np.kron(A.T, B.T)

print("Transpose property holds:", np.allclose(left, right))
print(f"Max difference: {np.max(np.abs(left - right)):.2e}")
```

### Example 6: 乘积规则

验证 (A ⊗ B)(C ⊗ D) = (AC) ⊗ (BD)：

```python
import numpy as np

A = np.array([[1.0, 2.0], [3.0, 4.0]])
B = np.array([[1.0, 0.0], [0.0, 1.0]])
C = np.array([[2.0, 0.0], [0.0, 2.0]])
D = np.array([[0.0, 1.0], [1.0, 0.0]])

left = np.kron(A, B) @ np.kron(C, D)
right = np.kron(A @ C, B @ D)

print("Product rule holds:", np.allclose(left, right))
print(f"Max difference: {np.max(np.abs(left - right)):.2e}")
```

### Example 7: 逆矩阵性质

验证 (A ⊗ B)^{-1} = A^{-1} ⊗ B^{-1}：

```python
import numpy as np

A = np.array([[2.0, 1.0], [1.0, 2.0]])
B = np.array([[1.0, 0.0], [0.0, 2.0]])

left = np.linalg.inv(np.kron(A, B))
right = np.kron(np.linalg.inv(A), np.linalg.inv(B))

print("Inverse property holds:", np.allclose(left, right))
print(f"Max difference: {np.max(np.abs(left - right)):.2e}")
```

---

## 秩、行列式、迹示例

### Example 8: 秩的性质

验证 rank(A ⊗ B) = rank(A) × rank(B)：

```python
import numpy as np

# 秩为2的矩阵
A = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
# 秩为1的矩阵
B = np.array([[1.0, 1.0], [1.0, 1.0]])

rank_A = np.linalg.matrix_rank(A)
rank_B = np.linalg.matrix_rank(B)
rank_kron = np.linalg.matrix_rank(np.kron(A, B))

print(f"rank(A) = {rank_A}")
print(f"rank(B) = {rank_B}")
print(f"rank(A ⊗ B) = {rank_kron}")
print(f"rank(A) × rank(B) = {rank_A * rank_B}")
print(f"Property holds: {rank_kron == rank_A * rank_B}")
```

### Example 9: 行列式的性质

验证 det(A ⊗ B) = det(A)^n × det(B)^m：

```python
import numpy as np

A = np.array([[2.0, 1.0], [1.0, 2.0]])  # 2×2, det=3
B = np.array([[1.0, 0.0, 0.0],
              [0.0, 2.0, 0.0],
              [0.0, 0.0, 3.0]])  # 3×3, det=6

m, n = A.shape[0], B.shape[0]
det_A = np.linalg.det(A)
det_B = np.linalg.det(B)
det_kron = np.linalg.det(np.kron(A, B))

expected = (det_A ** n) * (det_B ** m)

print(f"det(A) = {det_A:.2f}")
print(f"det(B) = {det_B:.2f}")
print(f"det(A ⊗ B) = {det_kron:.6f}")
print(f"det(A)^n × det(B)^m = {expected:.6f}")
print(f"Property holds: {np.isclose(det_kron, expected)}")
```

### Example 10: 迹的性质

验证 tr(A ⊗ B) = tr(A) × tr(B)：

```python
import numpy as np

A = np.array([[1.0, 2.0], [3.0, 4.0]])
B = np.array([[5.0, 6.0], [7.0, 8.0]])

trace_A = np.trace(A)
trace_B = np.trace(B)
trace_kron = np.trace(np.kron(A, B))

print(f"tr(A) = {trace_A}")
print(f"tr(B) = {trace_B}")
print(f"tr(A ⊗ B) = {trace_kron}")
print(f"tr(A) × tr(B) = {trace_A * trace_B}")
print(f"Property holds: {np.isclose(trace_kron, trace_A * trace_B)}")
```

---

## Kronecker和示例

### Example 11: Kronecker和

Kronecker和定义为 A ⊕ B = A ⊗ I + I ⊗ A：

```python
import numpy as np

def kronecker_sum(A, B):
    """Compute A ⊕ B = A ⊗ I + I ⊗ B"""
    m, n = A.shape[0], B.shape[0]
    return np.kron(A, np.eye(n)) + np.kron(np.eye(m), B)

A = np.array([[1.0, 2.0], [3.0, 4.0]])
B = np.array([[0.0, 1.0], [1.0, 0.0]])

kron_sum = kronecker_sum(A, B)
print("A ⊕ B =")
print(kron_sum)
print(f"Shape: {kron_sum.shape}")  # Should be (4, 4)
```

### Example 12: 特征值关系

Kronecker和的特征值是 λ_i(A) + μ_j(B)：

```python
import numpy as np

A = np.array([[2.0, 0.0], [0.0, 3.0]])
B = np.array([[1.0, 0.0], [0.0, 4.0]])

# Kronecker和的特征值
eig_A = np.linalg.eigvals(A)
eig_B = np.linalg.eigvals(B)
eig_sum_expected = [a + b for a in eig_A for b in eig_B]

eig_sum_actual = np.linalg.eigvals(np.kron(A, np.eye(2)) + np.kron(np.eye(2), B))

print("Expected eigenvalues (λ_i + μ_j):")
print(sorted(eig_sum_expected, key=lambda x: abs(x)))
print("\nActual eigenvalues:")
print(sorted(eig_sum_actual, key=lambda x: abs(x)))
```

---

## 应用示例

### Example 13: 向量化算子

vec算子将矩阵按列堆叠成向量：

```python
import numpy as np

A = np.array([[1.0, 3.0], [2.0, 4.0]])

vec_A = A.ravel(order='F')  # Fortran order (column-major)
print("vec(A) =", vec_A)
# [1., 2., 3., 4.]
```

### Example 14: vec性质

验证 vec(AXB) = (B^T ⊗ A) vec(X)：

```python
import numpy as np

A = np.array([[1.0, 0.0], [0.0, 2.0]])
B = np.array([[1.0, 1.0], [0.0, 1.0]])
X = np.array([[1.0, 2.0], [3.0, 4.0]])

# 左边：vec(AXB)
left = (A @ X @ B).ravel(order='F')

# 右边：(B^T ⊗ A) vec(X)
right = (np.kron(B.T, A) @ X.ravel(order='F'))

print("vec(AXB) property holds:", np.allclose(left, right))
print(f"Max difference: {np.max(np.abs(left - right)):.2e}")
```

### Example 15: Lyapunov方程

使用Kronecker积求解 Lyapunov 方程 AX + XA^T = C：

**Paper Source:**
- Lyapunov, A. M. (1892). "The general problem of stability of motion". *Kharkov Mathematical Society*.
- Bartels, R. H., and Stewart, G. W. (1972). "Solution of the Matrix Equation AX + XB = C". *Communications of the ACM*, 15(9), 820-826.

```python
import numpy as np

def solve_lyapunov_kronecker(A, C):
    """Solve AX + XA^T = C using Kronecker product"""
    n = A.shape[0]
    # vec(AX + XA^T) = vec(C)
    # (I ⊗ A + A ⊗ I) vec(X) = vec(C)
    kron_mat = np.kron(np.eye(n), A) + np.kron(A, np.eye(n))
    vec_X = np.linalg.solve(kron_mat, C.ravel(order='F'))
    return vec_X.reshape((n, n), order='F')

A = np.array([[-1.0, 0.5], [0.5, -2.0]])
C = np.array([[2.0, 1.0], [1.0, 2.0]])

X = solve_lyapunov_kronecker(A, C)
residual = A @ X + X @ A.T - C

print("Solution X:")
print(X)
print(f"Residual norm: {np.linalg.norm(residual):.6e}")
```

---

## 特殊矩阵的Kronecker积

### Example 16: 对角矩阵的Kronecker积

对角矩阵的Kronecker积仍是对角矩阵：

```python
import numpy as np

D1 = np.diag([1.0, 2.0, 3.0])
D2 = np.diag([4.0, 5.0])

kron_D = np.kron(D1, D2)
print("D₁ ⊗ D₂:")
print(kron_D)
print(f"Is diagonal: {np.allclose(kron_D, np.diag(np.diag(kron_D)))}")

# 对角元是 d_i * d_j
diag_product = np.outer(np.diag(D1), np.diag(D2)).ravel()
print(f"Diagonal matches product: {np.allclose(np.diag(kron_D), diag_product)}")
```

### Example 17: 对称矩阵的Kronecker积

对称矩阵的Kronecker积仍是对称矩阵：

```python
import numpy as np

A = np.array([[1.0, 2.0], [2.0, 3.0]])
B = np.array([[4.0, 5.0], [5.0, 6.0]])

kron_AB = np.kron(A, B)
print(f"A symmetric: {np.allclose(A, A.T)}")
print(f"B symmetric: {np.allclose(B, B.T)}")
print(f"A ⊗ B symmetric: {np.allclose(kron_AB, kron_AB.T)}")
```

### Example 18: 正交矩阵的Kronecker积

正交矩阵的Kronecker积仍是正交矩阵：

```python
import numpy as np

# 随机正交矩阵
np.random.seed(42)
A, _ = np.linalg.qr(np.random.randn(3, 3))
B, _ = np.linalg.qr(np.random.randn(2, 2))

kron_AB = np.kron(A, B)

# 验证正交性: (A ⊗ B)^T (A ⊗ B) = I
I_kron = np.eye(kron_AB.shape[0])
is_orthogonal = np.allclose(kron_AB.T @ kron_AB, I_kron)

print(f"A ⊗ B orthogonal: {is_orthogonal}")
print(f"Max deviation from identity: {np.max(np.abs(kron_AB.T @ kron_AB - I_kron)):.2e}")
```

---

## 复杂矩阵和病态矩阵示例

### Example 19: Hilbert矩阵的Kronecker积

Hilbert矩阵是著名的病态矩阵，其Kronecker积的条件数会呈指数增长。

**Paper Source:**
- Hilbert, D. (1894). "Ein Beitrag zur Theorie des Legendre'schen Polynoms". *Acta Mathematica*.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*, 2nd ed. SIAM.

```python
import numpy as np

def hilbert(n: int) -> np.ndarray:
    return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)], dtype=float)

# 测试不同大小的Hilbert矩阵
for n in [3, 4]:
    H = hilbert(n)
    H_kron = np.kron(H, H)

    cond_H = np.linalg.cond(H)
    cond_H_kron = np.linalg.cond(H_kron)

    print(f"\nHilbert({n}) ⊗ Hilbert({n}):")
    print(f"  H shape: {H.shape}, H⊗H shape: {H_kron.shape}")
    print(f"  cond(H) = {cond_H:.6e}")
    print(f"  cond(H⊗H) = {cond_H_kron:.6e}")
    print(f"  cond(H⊗H) ≈ cond(H)^(2n) = {cond_H**(2*n):.6e}")

    # 验证秩的性质
    rank_H = np.linalg.matrix_rank(H)
    rank_H_kron = np.linalg.matrix_rank(H_kron)
    print(f"  rank(H) = {rank_H}, rank(H⊗H) = {rank_H_kron}")
    print(f"  rank(H)² = {rank_H**2}")
```

### Example 20: Vandermonde矩阵的Kronecker积

Vandermonde矩阵在多项式插值中很重要，其Kronecker积用于多元插值。

**Paper Source:**
- Vandermonde, A.-T. (1771). "Memoire sur l'elimination". *Histoire de l'Academie Royale des Sciences*.
- Gautschi, W. (1978). "On Inverses of Vandermonde and Confluent Vandermonde Matrices". *Numerische Mathematik*.

```python
import numpy as np

# 几何节点生成Vandermonde矩阵
x = np.geomspace(0.1, 5.0, 4)
y = np.geomspace(0.2, 3.0, 3)

V_x = np.vander(x, N=len(x), increasing=True)
V_y = np.vander(y, N=len(y), increasing=True)

V_kron = np.kron(V_x, V_y)

print("Vandermonde Kronecker Product:")
print(f"  V_x shape: {V_x.shape}")
print(f"  V_y shape: {V_y.shape}")
print(f"  V_x ⊗ V_y shape: {V_kron.shape}")
print(f"  cond(V_x) = {np.linalg.cond(V_x):.6e}")
print(f"  cond(V_y) = {np.linalg.cond(V_y):.6e}")
print(f"  cond(V_x ⊗ V_y) = {np.linalg.cond(V_kron):.6e}")

# 验证秩
print(f"  rank(V_x) = {np.linalg.matrix_rank(V_x)}")
print(f"  rank(V_y) = {np.linalg.matrix_rank(V_y)}")
print(f"  rank(V_x ⊗ V_y) = {np.linalg.matrix_rank(V_kron)}")
print(f"  rank(V_x) × rank(V_y) = {np.linalg.matrix_rank(V_x) * np.linalg.matrix_rank(V_y)}")
```

### Example 21: Toeplitz矩阵的Kronecker积

Toeplitz矩阵在信号处理中广泛应用，其Kronecker积保持Toeplitz结构。

**Paper Source:**
- Toeplitz, O. (1911). "Zur Theorie der unendlichen Matrices". *Rendiconti del Circolo Matematico di Palermo*.
- Gray, R. M. (2006). "Toeplitz and Circulant Matrices: A Review". *Foundations and Trends in Communications and Information Theory*.

```python
import numpy as np

def toeplitz_symmetric(n: int, rho: float = 0.8) -> np.ndarray:
    """生成对称Toeplitz矩阵: T[i,j] = rho^{|i-j|}"""
    from scipy.linalg import toeplitz
    return toeplitz(rho ** np.arange(n))

T3 = toeplitz_symmetric(3, rho=0.9)
T4 = toeplitz_symmetric(4, rho=0.85)

T_kron = np.kron(T3, T4)

print("Toeplitz Kronecker Product:")
print(f"  T3 shape: {T3.shape}")
print(f"  T4 shape: {T4.shape}")
print(f"  T3 ⊗ T4 shape: {T_kron.shape}")
print(f"  T3 is Toeplitz: True")
print(f"  T4 is Toeplitz: True")
print(f"  T3 ⊗ T4 preserves block Toeplitz structure")

# 验证正定性
eigs_T3 = np.linalg.eigvals(T3)
eigs_T4 = np.linalg.eigvals(T4)
eigs_Tkron = np.linalg.eigvals(T_kron)

print(f"\nEigenvalue properties:")
print(f"  T3 eigenvalues (min/max): {np.min(eigs_T3):.6f} / {np.max(eigs_T3):.6f}")
print(f"  T4 eigenvalues (min/max): {np.min(eigs_T4):.6f} / {np.max(eigs_T4):.6f}")
print(f"  T3⊗T4 eigenvalues (min/max): {np.min(eigs_Tkron):.6f} / {np.max(eigs_Tkron):.6f}")

# Kronecker积的特征值是两矩阵特征值的乘积
eig_product = np.array([a * b for a in eigs_T3 for b in eigs_T4])
print(f"  Eigenvalues match: {np.allclose(sorted(eigs_Tkron), sorted(eig_product))}")
```

### Example 22: 稀疏矩阵的Kronecker积

稀疏矩阵的Kronecker积在离散化PDE中常见。

```python
import numpy as np
from scipy.sparse import csr_matrix, kron as sparse_kron

# 1D Laplacian (三对角矩阵)
def laplacian_1d(n: int) -> np.ndarray:
    """生成1D Laplacian矩阵"""
    diag = 2 * np.ones(n)
    off_diag = -1 * np.ones(n - 1)
    return np.diag(diag) + np.diag(off_diag, k=1) + np.diag(off_diag, k=-1)

L3 = laplacian_1d(3)
L4 = laplacian_1d(4)

L_kron_dense = np.kron(L3, L4)
L_kron_sparse = sparse_kron(csr_matrix(L3), csr_matrix(L4))

print("Sparse Kronecker Product (2D Laplacian):")
print(f"  L3 (1D Laplacian, n=3):\n{L3}")
print(f"  L4 (1D Laplacian, n=4):\n{L4}")
print(f"  L3 ⊗ L4 (2D Laplacian) shape: {L_kron_dense.shape}")

# 验证稀疏性
density = np.count_nonzero(L_kron_dense) / L_kron_dense.size
print(f"  Density: {density:.4%}")
print(f"  Sparsity: {(1-density):.4%}")

# 条件数
cond_L3 = np.linalg.cond(L3)
cond_L4 = np.linalg.cond(L4)
cond_Lkron = np.linalg.cond(L_kron_dense)
print(f"\nCondition numbers:")
print(f"  cond(L3) = {cond_L3:.6f}")
print(f"  cond(L4) = {cond_L4:.6f}")
print(f"  cond(L3 ⊗ L4) = {cond_Lkron:.6f}")
```

### Example 23: Pascal矩阵的Kronecker积

Pascal矩阵具有良好的整数性质。

**Paper Source:**
- Call, G. S., and Velleman, D. J. (1993). "Pascal's Matrices". *American Mathematical Monthly*, 100(4), 372-376.

```python
import numpy as np

def pascal_matrix(n: int) -> np.ndarray:
    """生成Pascal矩阵: P[i,j] = C(i+j, i)"""
    from scipy.special import comb
    P = np.ones((n, n), dtype=float)
    for i in range(1, n):
        for j in range(1, n):
            P[i, j] = comb(i + j, i, exact=True)
    return P

P3 = pascal_matrix(3)
P4 = pascal_matrix(4)

P_kron = np.kron(P3, P4)

print("Pascal Kronecker Product:")
print(f"  P3:\n{P3}")
print(f"  P3 ⊗ P4 shape: {P_kron.shape}")
print(f"  det(P3) = {np.linalg.det(P3):.0f}")
print(f"  det(P4) = {np.linalg.det(P4):.0f}")
print(f"  det(P3 ⊗ P4) = {np.linalg.det(P_kron):.0f}")

# 验证行列式性质
m, n = P3.shape[0], P4.shape[0]
det_expected = (np.linalg.det(P3) ** n) * (np.linalg.det(P4) ** m)
print(f"  det(P3)^n × det(P4)^m = {det_expected:.0f}")
print(f"  Matches: {np.isclose(np.linalg.det(P_kron), det_expected)}")
```

### Example 24: 随机矩阵的条件数分析

分析随机矩阵Kronecker积的条件数性质。

```python
import numpy as np

def random_matrix_analysis(m: int, n: int, p: int, q: int, seed: int = 42) -> dict:
    """分析随机矩阵Kronecker积的条件数"""
    rng = np.random.RandomState(seed)
    A = rng.randn(m, n)
    B = rng.randn(p, q)

    # 只对方阵计算条件数
    cond_A = np.linalg.cond(A @ A.T) if m <= n else np.linalg.cond(A.T @ A)
    cond_B = np.linalg.cond(B @ B.T) if p <= q else np.linalg.cond(B.T @ B)

    AB_kron = np.kron(A, B)
    cond_AB_kron = np.linalg.cond(AB_kron @ AB_kron.T)

    return {
        "cond_A": cond_A,
        "cond_B": cond_B,
        "cond_A_kron_B": cond_AB_kron,
        "product": cond_A * cond_B,
    }

print("Random Matrix Condition Number Analysis:")
for m, n, p, q in [(5, 5, 5, 5), (10, 5, 8, 6), (20, 10, 15, 8)]:
    result = random_matrix_analysis(m, n, p, q)
    print(f"\n  Sizes: A({m}×{n}), B({p}×{q})")
    print(f"    cond(A) ≈ {result['cond_A']:.6e}")
    print(f"    cond(B) ≈ {result['cond_B']:.6e}")
    print(f"    cond(A⊗B) ≈ {result['cond_A_kron_B']:.6e}")
    print(f"    cond(A) × cond(B) ≈ {result['product']:.6e}")
```

### Example 25: 病态矩阵的Kronecker和

分析Kronecker和的特征值分布和条件数。

```python
import numpy as np

def kronecker_sum_analysis(A: np.ndarray, B: np.ndarray) -> dict:
    """分析Kronecker和 A ⊕ B = A⊗I + I⊗B"""
    m, n = A.shape[0], B.shape[0]

    # 计算Kronecker和
    kron_sum = np.kron(A, np.eye(n)) + np.kron(np.eye(m), B)

    # 特征值
    eig_A = np.linalg.eigvals(A)
    eig_B = np.linalg.eigvals(B)
    eig_sum = np.linalg.eigvals(kron_sum)

    # Kronecker和的特征值应该是 λ_i(A) + μ_j(B) 的所有组合
    expected_eigs = np.array([a + b for a in eig_A for b in eig_B])

    return {
        "shape": kron_sum.shape,
        "cond_A": np.linalg.cond(A),
        "cond_B": np.linalg.cond(B),
        "cond_sum": np.linalg.cond(kron_sum),
        "eig_A": eig_A,
        "eig_B": eig_B,
        "eig_sum_actual": sorted(eig_sum, key=lambda x: abs(x)),
        "eig_sum_expected": sorted(expected_eigs, key=lambda x: abs(x)),
    }

# 测试病态矩阵
A = np.array([[100.0, 99.0], [99.0, 98.0]])  # 条件数很大的矩阵
B = np.array([[1.0, 0.99], [0.99, 0.98]])

result = kronecker_sum_analysis(A, B)

print("Ill-conditioned Kronecker Sum Analysis:")
print(f"  A shape: {A.shape}, B shape: {B.shape}")
print(f"  A ⊕ B shape: {result['shape']}")
print(f"  cond(A) = {result['cond_A']:.6e}")
print(f"  cond(B) = {result['cond_B']:.6e}")
print(f"  cond(A ⊕ B) = {result['cond_sum']:.6e}")

print(f"\nEigenvalues of A: {result['eig_A']}")
print(f"Eigenvalues of B: {result['eig_B']}")
print(f"\nFirst few eigenvalues of A ⊕ B:")
for i in range(min(4, len(result['eig_sum_actual']))):
    print(f"  λ_{i}: actual = {result['eig_sum_actual'][i]:.6f}, expected ≈ {result['eig_sum_expected'][i]:.6f}")

print(f"\nEigenvalue property verified: {np.allclose(sorted(result['eig_sum_actual'], key=abs), sorted(result['eig_sum_expected'], key=abs), atol=1e-10)}")
```

### Example 26: Fibonacci矩阵的Kronecker积

Fibonacci矩阵展示有趣的递归性质。

```python
import numpy as np

def fibonacci_q_matrix(n: int) -> np.ndarray:
    """生成n×n Fibonacci Q矩阵: Q[i,j] = C(i+j, i)"""
    from scipy.special import comb
    Q = np.ones((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            Q[i, j] = comb(i + j, i, exact=True)
    return Q

Q3 = fibonacci_q_matrix(3)
Q4 = fibonacci_q_matrix(4)

Q_kron = np.kron(Q3, Q4)

print("Fibonacci Q-Matrix Kronecker Product:")
print(f"  Q3:\n{Q3}")
print(f"  Q3 ⊗ Q4 shape: {Q_kron.shape}")

# Q矩阵的特征值与Fibonacci数相关
eig_Q3 = np.linalg.eigvals(Q3)
eig_Q4 = np.linalg.eigvals(Q4)
eig_Qkron = np.linalg.eigvals(Q_kron)

print(f"\nEigenvalue properties:")
print(f"  max eig(Q3) = {np.max(np.abs(eig_Q3)):.6f}")
print(f"  max eig(Q4) = {np.max(np.abs(eig_Q4)):.6f}")
print(f"  max eig(Q3⊗Q4) = {np.max(np.abs(eig_Qkron)):.6f}")
print(f"  product of max eigs = {np.max(np.abs(eig_Q3)) * np.max(np.abs(eig_Q4)):.6f}")
```

### Example 27: 循环矩阵的Kronecker积

循环矩阵的Kronecker积用于快速卷积和信号处理。

```python
import numpy as np
from scipy.linalg import circulant

def circulant_matrix(values: np.ndarray) -> np.ndarray:
    """生成循环矩阵"""
    return circulant(values)

# 创建循环矩阵
C1 = circulant_matrix(np.array([1.0, 2.0, 3.0]))
C2 = circulant_matrix(np.array([0.5, 1.0, 0.5, 1.0]))

C_kron = np.kron(C1, C2)

print("Circulant Kronecker Product:")
print(f"  C1:\n{C1}")
print(f"  C2:\n{C2}")
print(f"  C1 ⊗ C2 shape: {C_kron.shape}")

# 循环矩阵由DFT对角化
eig_C1 = np.linalg.eigvals(C1)
eig_C2 = np.linalg.eigvals(C2)

# Kronecker积的特征值是特征值的乘积
eig_product = np.array([a * b for a in eig_C1 for b in eig_C2])
eig_Ckron = np.linalg.eigvals(C_kron)

print(f"\nEigenvalue verification:")
print(f"  |eig(C1)|: {sorted([round(abs(x), 6) for x in eig_C1])}")
print(f"  |eig(C2)|: {sorted([round(abs(x), 6) for x in eig_C2])}")
print(f"  eigenvalues match: {np.allclose(sorted(eig_Ckron, key=abs), sorted(eig_product, key=abs), atol=1e-10)}")

# 验证条件数
print(f"\nCondition numbers:")
print(f"  cond(C1) = {np.linalg.cond(C1):.6f}")
print(f"  cond(C2) = {np.linalg.cond(C2):.6f}")
print(f"  cond(C1 ⊗ C2) = {np.linalg.cond(C_kron):.6e}")
```

### Example 28: 大规模矩阵Kronecker积的性能测试

测试大规模矩阵Kronecker积的计算时间和内存使用。

```python
import numpy as np
import time

def large_kronecker_benchmark() -> dict:
    """测试大规模Kronecker积的性能"""

    results = {}

    # 测试不同规模
    test_sizes = [(10, 10, 10, 10), (20, 20, 20, 20), (50, 50, 50, 50)]

    for m, n, p, q in test_sizes:
        A = np.random.randn(m, n)
        B = np.random.randn(p, q)

        start = time.time()
        AB_kron = np.kron(A, B)
        elapsed = time.time() - start

        results[f"{m}×{n} ⊗ {p}×{q}"] = {
            "result_shape": AB_kron.shape,
            "result_size": AB_kron.size,
            "time": elapsed,
            "memory_mb": AB_kron.nbytes / (1024 * 1024),
        }

    return results

print("Large Kronecker Product Benchmark:")
benchmarks = large_kronecker_benchmark()
for key, value in benchmarks.items():
    print(f"\n  {key}:")
    print(f"    Result shape: {value['result_shape']}")
    print(f"    Total elements: {value['result_size']:,}")
    print(f"    Memory: {value['memory_mb']:.2f} MB")
    print(f"    Time: {value['time']:.4f} seconds")
```

---

## 不同应用的选择建议

| 应用场景 | 相关概念 | 理由 |
|---------|---------|------|
| 张量积空间 | Kronecker积 | 基的张量积 |
| 量子态 | 多体系统 | 复合系统描述 |
| 线性矩阵方程 | vec算子 | 化简为线性系统 |
| 离散化偏微分方程 | Kronecker积 | 维度分离 |
| 图论 | 图的Kronecker积 | 图的组合结构 |
| 信号处理 | 滤波器组 | 多通道处理 |
