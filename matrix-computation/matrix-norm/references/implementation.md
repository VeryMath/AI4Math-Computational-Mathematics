# Matrix Norm - Implementation Reference

> **Note**: This file contains low-level implementation details using numpy/scipy. For usage examples of the `/matrix-norm` skill, see [examples.md](./examples.md).

---

## 基础示例

### Example 1: Frobenius范数

Frobenius范数是最常用的矩阵范数，定义为元素平方和的平方根：

$$\|A\|_F = \sqrt{\sum_{i,j} |a_{ij}|^2}$$

```python
import numpy as np

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
```

### Example 2: 谱范数(2-范数)

谱范数是矩阵的最大奇异值：

$$\|A\|_2 = \sigma_{\max}(A)$$

```python
import numpy as np

A = np.array([
    [3.0, 1.0],
    [1.0, 2.0],
])

spec_norm = np.linalg.norm(A, ord=2)
print(f"Spectral norm: {spec_norm:.6f}")

# 通过SVD验证
u, s, vt = np.linalg.svd(A)
print(f"Max singular value: {s[0]:.6f}")
```

### Example 3: 1-范数和∞-范数

1-范数是最大列和，∞-范数是最大行和：

$$\|A\|_1 = \max_j \sum_i |a_{ij}|, \quad \|A\|_\infty = \max_i \sum_j |a_{ij}|$$

```python
import numpy as np

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
```

### Example 4: 核范数(Nuclear Norm)

核范数是所有奇异值之和：

$$\|A\|_* = \sum_i \sigma_i(A)$$

```python
import numpy as np

A = np.array([
    [3.0, 1.0],
    [1.0, 2.0],
])

nuc_norm = np.linalg.norm(A, ord='nuc')
print(f"Nuclear norm: {nuc_norm:.6f}")

# 通过SVD验证
u, s, vt = np.linalg.svd(A)
print(f"Sum of singular values: {np.sum(s):.6f}")
```

### Example 5: 一般p-范数

对于 $p \geq 1$：

$$\|A\|_p = \max_{\|x\|_p=1} \|Ax\|_p$$

```python
import numpy as np

A = np.array([
    [2.0, 1.0],
    [1.0, 2.0],
])

# 1-范数, 2-范数, ∞-范数
for p in [1, 2, np.inf]:
    norm_p = np.linalg.norm(A, ord=p)
    print(f"||A||_{p if p != np.inf else 'inf'} = {norm_p:.6f}")
```

---

## 条件数示例

### Example 6: 条件数与数值稳定性

条件数 $\kappa(A) = \|A\| \cdot \|A^{-1}\|$ 衡量矩阵对扰动的敏感性：

```python
import numpy as np

# 条件数良好的矩阵
A_well = np.array([
    [1.0, 0.0],
    [0.0, 1.0],
])
print(f"Well-conditioned: kappa(A) = {np.linalg.cond(A_well):.2f}")

# 条件数较差的矩阵
A_poor = np.array([
    [1.0, 1.0],
    [1.0, 1.000001],
])
print(f"Poor-conditioned: kappa(A) = {np.linalg.cond(A_poor):.2e}")

# 不同范数的条件数
A = np.array([
    [2.0, 1.0],
    [1.0, 2.0],
])
print(f"\nCondition numbers for different norms:")
for p in [1, 2, np.inf, 'fro']:
    if p != 'fro':
        kappa = np.linalg.cond(A, p=p)
        print(f"kappa_{p if p != np.inf else 'inf'}(A) = {kappa:.6f}")
```

---

## 矩阵距离示例

### Example 7: Frobenius距离

```python
import numpy as np

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
```

### Example 8: 谱距离

```python
import numpy as np

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
```

---

## 特殊矩阵范数性质

### Example 9: 正交矩阵的范数

对于正交矩阵 $Q$，满足 $Q^T Q = I$：

- $\|Q\|_2 = 1$
- $\|Q\|_F = \sqrt{n}$ (n×n正交矩阵)

```python
import numpy as np

# 生成随机正交矩阵
A = np.random.randn(3, 3)
Q, _ = np.linalg.qr(A)

print("Orthogonal matrix Q:")
print(Q)

print(f"\n||Q||_2 = {np.linalg.norm(Q, ord=2):.6f} (expected: 1)")
print(f"||Q||_F = {np.linalg.norm(Q, ord='fro'):.6f} (expected: {np.sqrt(3):.6f})")
print(f"||Q||_1 = {np.linalg.norm(Q, ord=1):.6f}")
print(f"||Q||_inf = {np.linalg.norm(Q, ord=np.inf):.6f}")
```

### Example 10: 对角矩阵的范数

对于对角矩阵 $D = \text{diag}(d_1, ..., d_n)$：

- $\|D\|_2 = \max_i |d_i|$
- $\|D\|_F = \sqrt{\sum_i d_i^2}$
- $\|D\|_1 = \|D\|_\infty = \max_i |d_i|$

```python
import numpy as np

D = np.diag([1.0, 2.0, 3.0])

print("Diagonal matrix D:")
print(D)

print(f"\n||D||_2 = {np.linalg.norm(D, ord=2):.6f} (max |d_i|)")
print(f"||D||_F = {np.linalg.norm(D, ord='fro'):.6f} (sqrt(sum d_i^2))")
print(f"||D||_1 = {np.linalg.norm(D, ord=1):.6f} (max |d_i|)")
print(f"||D||_inf = {np.linalg.norm(D, ord=np.inf):.6f} (max |d_i|)")
```

---

## 范数不等式验证

### Example 11: Frobenius与谱范数的关系

理论性质：$\|A\|_2 \leq \|A\|_F \leq \sqrt{\min(m,n)} \|A\|_2$

```python
import numpy as np

A = np.random.randn(4, 3)

fro = np.linalg.norm(A, ord='fro')
spec = np.linalg.norm(A, ord=2)

print(f"Frobenius norm: {fro:.6f}")
print(f"Spectral norm: {spec:.6f}")
print(f"sqrt(min(m,n)) * ||A||_2: {np.sqrt(min(A.shape)) * spec:.6f}")
print(f"\nInequality check:")
print(f"||A||_2 <= ||A||_F: {spec <= fro}")
print(f"||A||_F <= sqrt(min(m,n)) * ||A||_2: {fro <= np.sqrt(min(A.shape)) * spec}")
```

### Example 12: 范数关系不等式

理论性质：$\|A\|_2 \leq \sqrt{\|A\|_1 \|A\|_\infty}$

```python
import numpy as np

A = np.array([
    [2.0, 1.0, 3.0],
    [1.0, 4.0, 1.0],
])

spec = np.linalg.norm(A, ord=2)
norm_1 = np.linalg.norm(A, ord=1)
norm_inf = np.linalg.norm(A, ord=np.inf)

print(f"||A||_2: {spec:.6f}")
print(f"sqrt(||A||_1 * ||A||_inf): {np.sqrt(norm_1 * norm_inf):.6f}")
print(f"Inequality holds: {spec <= np.sqrt(norm_1 * norm_inf)}")
```

---

## 低秩矩阵的范数

### Example 13: 秩1矩阵的核范数

对于秩1矩阵 $A = uv^T$，有 $\|A\|_* = \|A\|_2$：

```python
import numpy as np

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
print(f"For rank-1 matrix: ||A||_2 = ||A||_*: {np.isclose(spec, nuc)}")
```

---

## 病态矩阵示例

### Example 14: Hilbert矩阵的范数和条件数

**Paper Source:**
- Hilbert, D. (1894). "Ein Beitrag zur Theorie des Legendre'schen Polynoms". *Acta Mathematica*.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*, 2nd ed. SIAM.

```python
import numpy as np

def hilbert(n: int) -> np.ndarray:
    return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)], dtype=float)

for n in [3, 5, 8]:
    H = hilbert(n)
    fro = np.linalg.norm(H, ord='fro')
    spec = np.linalg.norm(H, ord=2)
    cond = np.linalg.cond(H)

    print(f"\nHilbert({n}):")
    print(f"  Frobenius norm: {fro:.6e}")
    print(f"  Spectral norm: {spec:.6e}")
    print(f"  Condition number: {cond:.6e}")
```

### Example 15: Vandermonde矩阵的范数

**Paper Source:**
- Vandermonde, A.-T. (1771). "Memoire sur l'elimination". *Histoire de l'Academie Royale des Sciences*.
- Gautschi, W. (1978). "On Inverses of Vandermonde and Confluent Vandermonde Matrices". *Numerische Mathematik*.

```python
import numpy as np

x = np.geomspace(0.1, 10, 10)
V = np.vander(x, N=len(x), increasing=True)

print(f"Vandermonde matrix shape: {V.shape}")
print(f"Frobenius norm: {np.linalg.norm(V, ord='fro'):.6e}")
print(f"Spectral norm: {np.linalg.norm(V, ord=2):.6e}")
print(f"Condition number: {np.linalg.cond(V):.6e}")
```

---

## 不同范数的选择建议

| 应用场景 | 推荐范数 | 理由 |
|---------|---------|------|
| 一般矩阵大小度量 | Frobenius | 计算高效，直观 |
| 重构误差、逼近质量 | Frobenius | 元素级误差 |
| 条件数分析 | Spectral | 对应最大放大因子 |
| 迭代法收敛性 | Spectral | 与谱半径相关 |
| 列空间性质分析 | 1-范数 | 最大列和 |
| 行空间性质分析 | ∞-norm | 最大行和 |
| 低秩约束问题 | Nuclear | 奇异值之和 |
| 稀疏性度量 | 其他 | 取决于具体问题 |
