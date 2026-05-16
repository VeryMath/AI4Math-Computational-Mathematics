# SVD Decomposition Examples

## 基础示例

### Example 1: 完整 SVD 分解

```python
import numpy as np

A = np.array([
    [3.0, 1.0, 1.0],
    [-1.0, 3.0, 1.0],
])

U, s, Vt = np.linalg.svd(A, full_matrices=False)
print("U =\n", U)
print("s =\n", s)
print("Vt =\n", Vt)

Sigma = np.diag(s)
print("reconstruction error =", np.linalg.norm(A - U @ Sigma @ Vt))
```

### Example 2: 秩-k 近似

```python
import numpy as np

A = np.array([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
    [7.0, 8.0, 10.0],
])

U, s, Vt = np.linalg.svd(A, full_matrices=False)
k = 2
Ak = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
print(f"Rank-{k} approximation Ak =\n", Ak)

retained = float(np.sum(s[:k]**2) / np.sum(s**2))
print(f"Retained energy: {retained:.4f} ({retained*100:.2f}%)")
print(f"Approximation error: {np.linalg.norm(A - Ak):.2e}")
```

### Example 3: 伪逆

```python
import numpy as np

A = np.array([
    [1.0, 2.0],
    [2.0, 4.0],
    [3.0, 6.0],
])

A_pinv = np.linalg.pinv(A)
print("A^+ =\n", A_pinv)

# 验证伪逆性质 (A^+ A^+ A = A^+)
print("||A^+ @ A @ A^+ - A^+|| =", np.linalg.norm(A_pinv @ A @ A_pinv - A_pinv))
print("||A @ A^+ @ A - A|| =", np.linalg.norm(A @ A_pinv @ A - A))
```

### Example 4: 最小二乘求解

```python
import numpy as np

A = np.array([
    [1.0, 1.0],
    [1.0, 2.0],
    [1.0, 3.0],
    [1.0, 4.0],
])
b = np.array([6.0, 9.0, 20.0, 25.0])

# 使用伪逆求解最小二乘问题
x = np.linalg.pinv(A) @ b
print("Least squares solution x =", x)
print("Residual ||Ax - b|| =", np.linalg.norm(A @ x - b))
```

---

## 病态矩阵示例

### Example 5: Hilbert 矩阵（极病态）

**Paper Source:**
- Hilbert, D. (1894). "Ein Beitrag zur Theorie des Legendre'schen Polynoms". *Acta Mathematica*, 18, 155-159.
- Kahan, W. (1966). "Four Cholesky Factors of Hilbert Matrices".
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*, 2nd ed. SIAM.

```python
import numpy as np

def hilbert(n: int) -> np.ndarray:
    return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)], dtype=float)

n = 15
A = hilbert(n)
b = np.ones(n)

U, s, Vt = np.linalg.svd(A, full_matrices=False)
cond = float(s[0] / s[-1])
print(f"Condition number: {cond:.2e}")

# 使用截断 SVD 改善稳定性
rcond = 1e-10
s_pinv = np.where(s > rcond * s[0], 1.0 / s, 0.0)
x = Vt.T @ (s_pinv[:, np.newaxis] * U.T) @ b

residual = np.linalg.norm(A @ x - b)
print(f"Residual: {residual:.2e}")
print(f"Solution norm: {np.linalg.norm(x):.2e}")
```

### Example 6: 指数衰减矩阵

**Paper Source:**
- Hansen, P. C. (1998). *Rank-Deficient and Discrete Ill-Posed Problems*. SIAM.
- Tikhonov, A. N., and Arsenin, V. Y. (1977). *Solutions of Ill-Posed Problems*.

```python
import numpy as np

def exponential_decay_matrix(n: int) -> np.ndarray:
    U, _ = np.linalg.qr(np.random.randn(n, n))
    V, _ = np.linalg.qr(np.random.randn(n, n))
    s = 10 ** np.linspace(0, -15, n)
    return U @ np.diag(s) @ V.T

n = 50
A = exponential_decay_matrix(n)
b = np.random.randn(n)

U, s, Vt = np.linalg.svd(A, full_matrices=False)
print(f"Singular values range: [{s[0]:.2e}, {s[-1]:.2e}]")
print(f"Condition number: {s[0]/s[-1]:.2e}")

x = np.linalg.pinv(A, rcond=1e-10) @ b
print(f"Residual: {np.linalg.norm(A @ x - b):.2e}")
```

### Example 7: Cauchy 矩阵

**Paper Source:**
- Cauchy, A. L. (1841). *Exercices d'analyse et de physique mathématique*.
- Tyrtyshnikov, E. E. (1996). "Mosaic-skeleton approximations". *Calcolo*, 33, 47-57.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*, 2nd ed. SIAM.

```python
import numpy as np

def cauchy_matrix(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return 1.0 / (x[:, np.newaxis] + y[np.newaxis, :])

x = np.arange(1, 9, dtype=float)
y = np.arange(1, 9, dtype=float)
A = cauchy_matrix(x, y)

U, s, Vt = np.linalg.svd(A, full_matrices=False)
print(f"Condition number: {s[0]/s[-1]:.2e}")

b = np.ones(len(x))
x = np.linalg.pinv(A) @ b
print(f"Residual: {np.linalg.norm(A @ x - b):.2e}")
```

### Example 8: Vandermonde 矩阵低秩近似

**Paper Source:**
- Vandermonde, A.-T. (1771). "Memoire sur l'élimination".
- Gautschi, W. (1978). "On Inverses of Vandermonde Matrices".

```python
import numpy as np

x = np.geomspace(0.1, 10, 15)
n = len(x)
V = np.vander(x, N=n, increasing=True)

U, s, Vt = np.linalg.svd(V, full_matrices=False)

# 分析奇异值衰减
print("Singular values:", s)

# 不同 k 的能量保留
total_energy = float(np.sum(s**2))
for k in [2, 4, 6, 8]:
    retained = float(np.sum(s[:k]**2) / total_energy)
    print(f"k={k}: retained energy = {retained:.4f} ({retained*100:.2f}%)")
```

---

## 论文引用矩阵示例

### Example 9: Lotkin 矩阵

**Paper Source:**
- Lotkin, M. (1959). "A Set of Test Matrices". *MTAC*, 13(68), 153-161.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*, 2nd ed. SIAM.

```python
import numpy as np

def lotkin(n: int) -> np.ndarray:
    A = np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)], dtype=float)
    A[0, :] = 1.0
    return A

n = 8
A = lotkin(n)

U, s, Vt = np.linalg.svd(A, full_matrices=False)
print(f"Condition number: {s[0]/s[-1]:.2e}")

b = np.ones(n)
x = np.linalg.pinv(A, rcond=1e-12) @ b
print(f"Residual: {np.linalg.norm(A @ x - b):.2e}")
```

### Example 10: Pascal 矩阵

**Paper Source:**
- Call, G. S., and Velleman, D. J. (1993). "Pascal's Matrices". *American Mathematical Monthly*, 100(4), 372-376.

```python
import numpy as np

def pascal_matrix(n: int) -> np.ndarray:
    A = np.ones((n, n), dtype=float)
    for i in range(1, n):
        for j in range(1, n):
            A[i, j] = A[i, j-1] + A[i-1, j]
    return A

n = 10
A = pascal_matrix(n)

U, s, Vt = np.linalg.svd(A, full_matrices=False)
print(f"Condition number: {s[0]/s[-1]:.2e}")

# Pascal 矩阵的逆近似整数
A_pinv = np.linalg.pinv(A)
print(f"A^-1 ≈\n{np.round(A_pinv)}")

b = np.ones(n)
x = A_pinv @ b
print(f"Residual: {np.linalg.norm(A @ x - b):.2e}")
```

---

## 秩亏与低秩矩阵示例

### Example 11: 秩亏矩阵（列成比例）

```python
import numpy as np

A = np.array([
    [1.0, 2.0],
    [2.0, 4.0],
    [3.0, 6.0],
])

U, s, Vt = np.linalg.svd(A, full_matrices=False)
print("Singular values:", s)
print("Numerical rank:", np.sum(s > 1e-10))

# Moore-Penrose 伪逆给出最小范数解
A_pinv = np.linalg.pinv(A)
b = np.array([1.0, 2.0, 3.0])
x = A_pinv @ b

print("Minimum norm solution x:", x)
print("Residual ||Ax - b||:", np.linalg.norm(A @ x - b))
```

### Example 12: 随机奇异值衰减矩阵

```python
import numpy as np

def random_svd_decay(n: int, decay_factor: float = 1e-12) -> np.ndarray:
    U, _ = np.linalg.qr(np.random.randn(n, n))
    V, _ = np.linalg.qr(np.random.randn(n, n))
    s = np.logspace(0, np.log10(decay_factor), num=n)
    return (U * s) @ V.T

n = 12
A = random_svd_decay(n, decay_factor=1e-12)

U, s, Vt = np.linalg.svd(A, full_matrices=False)
print("Singular values:", s)

# 不同 k 的能量保留
total_energy = float(np.sum(s**2))
for k in [2, 4, 6, 8]:
    retained = float(np.sum(s[:k]**2) / total_energy)
    print(f"k={k}: retained energy = {retained:.4f} ({retained*100:.2f}%)")
```

---

## 长方形矩阵示例

### Example 13: 过定系统（最小二乘）

```python
import numpy as np

A = np.array([
    [1.0, 1.0],
    [1.0, 2.0],
    [1.0, 3.0],
    [1.0, 4.0],
])
b = np.array([6.0, 9.0, 20.0])

# SVD 适用于长方形矩阵
U, s, Vt = np.linalg.svd(A, full_matrices=False)

# 最小二乘解
s_pinv = np.where(s > 1e-10 * s[0], 1.0 / s, 0.0)
x = Vt.T @ (s_pinv[:, np.newaxis] * U.T) @ b

residual = np.linalg.norm(A @ x - b)
print(f"Least squares solution x: {x}")
print(f"Residual ||Ax - b||: {residual:.2e}")
```

---

## 输出模板

```markdown
### 问题重述
矩阵 A = [...], 目标: SVD分解/低秩近似/伪逆

### 分解结果
- U: [...]
- singular values: s = [...]
- V^T: [...]

### 秩与截断信息
- 数值秩: rank(A) = ...
- 截断秩 k: ...
- 保留能量: ...

### 验证
- reconstruction error ||A - UΣV^T||: ...
- (如求解) residual ||Ax - b||: ...

### 结果解释
...
```

---

## 病态 SVD 求解建议

```python
import numpy as np

def robust_svd_solve(A, b, rcond=None):
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    cond = float(s[0] / s[-1]) if s[-1] > 0 else float("inf")

    if rcond is None:
        rcond = max(A.shape) * np.finfo(s.dtype).eps

    effective_rcond = rcond * s[0]
    numerical_rank = int(np.sum(s > effective_rcond))

    s_pinv = np.where(s > effective_rcond, 1.0 / s, 0.0)
    x = Vt.T @ (s_pinv[:, np.newaxis] * U.T) @ b

    report = {
        "method": "svd_truncated" if numerical_rank < min(A.shape) else "svd",
        "cond": cond,
        "numerical_rank": numerical_rank,
        "residual_norm": float(np.linalg.norm(A @ x - b)),
    }
    return x, report
```
