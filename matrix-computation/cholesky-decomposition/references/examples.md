# Cholesky Decomposition Examples

## 基础示例

### Example 1: 基础 Cholesky 分解

```python
import numpy as np

A = np.array([
    [25.0, 15.0, -5.0],
    [15.0, 18.0, 0.0],
    [-5.0, 0.0, 11.0],
])

L = np.linalg.cholesky(A)
print("L =\n", L)
print("reconstruction error =", np.linalg.norm(A - L @ L.T))
```

### Example 2: 求解 SPD 系统

```python
import numpy as np
from scipy.linalg import cho_factor, cho_solve

A = np.array([
    [4.0, 1.0],
    [1.0, 3.0],
])
b = np.array([1.0, 2.0])

c, lower = cho_factor(A)
x = cho_solve((c, lower), b)
print("Solution x:", x)
print("Residual ||Ax - b|| =", np.linalg.norm(A @ x - b))
```

### Example 3: SPD 检查

```python
import numpy as np

def is_symmetric(A, tol=1e-10):
    return bool(np.allclose(A, A.T, atol=tol, rtol=tol))

def is_spd(A):
    if not is_symmetric(A):
        return False
    try:
        np.linalg.cholesky(A)
        return True
    except np.linalg.LinAlgError:
        return False

# 测试矩阵
A_spd = np.array([[4.0, 1.0], [1.0, 3.0]])
A_non_spd = np.array([[1.0, 2.0], [2.0, 1.0]])

print(f"A is SPD: {is_spd(A_spd)}")
print(f"non-symmetric A is SPD: {is_spd(A_non_spd)}")
```

---

## 病态 SPD 矩阵示例

### Example 4: Hilbert 矩阵（极病态 SPD）

**Paper Source:**
- Hilbert, D. (1894). "Ein Beitrag zur Theorie des Legendre'schen Polynoms". *Acta Mathematica*, 18, 155-159.
- Kahan, W. (1966). "Four Cholesky Factors of Hilbert Matrices".
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*, 2nd ed. SIAM, Section 2.8.

```python
import numpy as np
from scipy.linalg import cho_factor, cho_solve

def hilbert(n: int) -> np.ndarray:
    return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)], dtype=float)

for n in [5, 8, 12]:
    A = hilbert(n)
    cond = np.linalg.cond(A)
    print(f"Hilbert {n}x{n}: cond = {cond:.2e}")

    try:
        L = np.linalg.cholesky(A)
        b = np.ones(n)
        y = np.linalg.solve(L, b)
        x = np.linalg.solve(L.T, y)
        residual = np.linalg.norm(A @ x - b)
        print(f"  Residual: {residual:.2e}")
    except np.linalg.LinAlgError:
        print(f"  Cholesky failed (too ill-conditioned)")
```

### Example 5: Hilbert 矩阵 + Tikhonov 正则化

```python
import numpy as np
from scipy.linalg import cho_factor, cho_solve

def hilbert(n: int) -> np.ndarray:
    return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)], dtype=float)

n = 12
A = hilbert(n)
cond = np.linalg.cond(A)
print(f"Original condition number: {cond:.2e}")

# Tikhonov 正则化
alpha = 1e-8
A_reg = A + alpha * np.eye(n)
cond_reg = np.linalg.cond(A_reg)
print(f"Regularized condition number: {cond_reg:.2e}")

b = np.ones(n)
c, lower = cho_factor(A_reg)
x = cho_solve((c, lower), b)

residual = np.linalg.norm(A_reg @ x - b)
print(f"Residual: {residual:.2e}")
print(f"Regularization alpha: {alpha}")
```

---

## 论文引用 SPD 矩阵示例

### Example 6: Pascal 矩阵（SPD，整数逆）

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

print(f"Condition number: {np.linalg.cond(A):.2e}")

# 检查 SPD 并分解
try:
    L = np.linalg.cholesky(A)
    print("Cholesky successful")

    # Pascal 矩阵的逆近似整数
    A_inv = np.linalg.inv(A)
    print(f"A^-1 ≈\n{np.round(A_inv)}")
except np.linalg.LinAlgError:
    print("Cholesky failed")
```

### Example 7: Poisson 1D 离散化矩阵（三对角 SPD）

**Paper Source:**
- Forsythe, G. E., and Wasow, W. R. (1960). *Finite-Difference Methods for Partial Differential Equations*. Wiley.
- Quarteroni, A., Sacco, R., and Saleri, F. (2007). *Numerical Mathematics*, 2nd ed. Springer, Section 12.2.

```python
import numpy as np

def poisson_1d(n: int) -> np.ndarray:
    A = np.zeros((n, n), dtype=float)
    for i in range(n):
        A[i, i] = 2.0
        if i > 0:
            A[i, i-1] = -1.0
        if i + 1 < n:
            A[i, i+1] = -1.0
    return A

for n in [20, 50, 100]:
    A = poisson_1d(n)
    cond = np.linalg.cond(A)
    print(f"Poisson 1D {n}x{n}: cond = {cond:.2e}")

    # Poisson 矩阵始终是 SPD 的
    L = np.linalg.cholesky(A)
    b = np.ones(n)
    x = np.linalg.solve(A, b)
    residual = np.linalg.norm(A @ x - b)
    print(f"  Residual: {residual:.2e}")
```

### Example 8: Toeplitz 指数相关矩阵（SPD）

```python
import numpy as np

def toeplitz_exponential(n: int, rho: float = 0.9) -> np.ndarray:
    indices = np.arange(n)
    A = rho ** np.abs(indices[:, None] - indices[None, :])
    return A.astype(float)

for rho in [0.5, 0.9, 0.99]:
    n = 20
    A = toeplitz_exponential(n, rho)
    cond = np.linalg.cond(A)
    print(f"Toeplitz exp (rho={rho}): cond = {cond:.2e}")

    if cond < 1e12:
        L = np.linalg.cholesky(A)
        b = np.ones(n)
        x = np.linalg.solve(A, b)
        residual = np.linalg.norm(A @ x - b)
        print(f"  Residual: {residual:.2e}")
    else:
        print(f"  Too ill-conditioned for direct Cholesky")
```



### Example 9: Wilkinson 特征值测试矩阵（反例测试 - 非正定）

**Paper Source:**
- Wilkinson, J. H. (1965). *The Algebraic Eigenvalue Problem*. Clarendon Press.

```python
import numpy as np

def wilkinson_matrix(n: int) -> np.ndarray:
    A = np.zeros((n, n))
    m = n // 2
    for i in range(n):
        A[i, i] = abs(i - m) + 1
        if i > 0:
            A[i, i-1] = 1.0
            A[i-1, i] = 1.0
    return A

n = 20
A = wilkinson_matrix(n)

print(f"Wilkinson {n}x{n}: cond = {np.linalg.cond(A):.2e}")

# 此矩阵虽然对称，但不是正定的，应该触发错误提示
# 预期输出: 矩阵不是正定矩阵，不能用cholesky分解
try:
    L = np.linalg.cholesky(A)
    print("Cholesky successful (unexpected)")
except np.linalg.LinAlgError as e:
    print(f"LinAlgError: {e}")
    print("提示: 此矩阵不是正定矩阵，不能用cholesky分解")
```

**用途**: 这是一个反例测试，用于验证Cholesky skill能否正确识别非正定矩阵并给出适当的错误提示。

### Example 10: 从数据构造 Gram 矩阵

```python
import numpy as np

np.random.seed(42)
m, n = 10, 3
X = np.random.randn(m, n)

# Gram 矩阵 G = X^T @ X
A = X.T @ X

print(f"Data matrix X shape: {X.shape}")
print(f"Gram matrix A = X^T @ X shape: {A.shape}")

# Gram 矩阵总是半正定的
eigenvals = np.linalg.eigvals(A)
print(f"Eigenvalues: min={eigenvals.min():.2e}, max={eigenvals.max():.2e}")

if np.all(eigenvals > 0):
    L = np.linalg.cholesky(A)
    print("Cholesky successful (SPD)")
    b = np.ones(n)
    x = np.linalg.solve(A, b)
    residual = np.linalg.norm(A @ x - b)
    print(f"Residual ||Ax - b||: {residual:.2e}")
else:
    print("Matrix is positive semi-definite, not strictly positive definite")
```

---

## 输出模板

```markdown
### 问题重述
矩阵 A = [...], 目标: Cholesky 分解/求解

### 矩阵检查
- shape: (n, n)
- 对称性: ...
- 正定性: ...
- 条件数: cond(A)

### 分解结果
- L (下三角) = ...

### 验证
- reconstruction error ||A - LL^T||: ...
- (如求解) residual ||Ax - b||: ...

### 结果解释
...
```

---

## 病态 Cholesky 求解建议

```python
import numpy as np
from scipy.linalg import cho_factor, cho_solve

def robust_cholesky_solve(A, b, alpha=None):
    cond = np.linalg.cond(A)
    report = {"cond": cond}

    if cond < 1e12:
        c, lower = cho_factor(A)
        x = cho_solve((c, lower), b)
        report["method"] = "cholesky"
        report["residual_norm"] = float(np.linalg.norm(A @ x - b))
        return x, report

    if alpha is None:
        alpha = 1e-8

    A_reg = A + alpha * np.eye(A.shape[0])
    report["method"] = "tikhonov"
    report["alpha"] = alpha
    report["cond_regularized"] = float(np.linalg.cond(A_reg))

    try:
        c, lower = cho_factor(A_reg)
        x = cho_solve((c, lower), b)
        report["residual_norm"] = float(np.linalg.norm(A_reg @ x - b))
        return x, report
    except np.linalg.LinAlgError:
        x = np.linalg.pinv(A) @ b
        report["method"] = "svd_fallback"
        report["residual_norm"] = float(np.linalg.norm(A @ x - b))
        return x, report
```
