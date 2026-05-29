# LU Decomposition Examples

## 基础示例

### Example 1: 分解一个方阵

```python
import numpy as np
from scipy.linalg import lu

A = np.array([
    [2.0, 1.0, 1.0],
    [4.0, -6.0, 0.0],
    [-2.0, 7.0, 2.0],
])

P, L, U = lu(A)
print("P =\n", P)
print("L =\n", L)
print("U =\n", U)
# SciPy 约定: A = P @ L @ U
print("reconstruction error =", np.linalg.norm(A - P @ L @ U))
```

### Example 2: 求解 Ax = b

```python
import numpy as np
from scipy.linalg import lu_factor, lu_solve

A = np.array([
    [3.0, 1.0],
    [1.0, 2.0],
])
b = np.array([9.0, 8.0])

lu, piv = lu_factor(A)
x = lu_solve((lu, piv), b)
print(x)
```

### Example 3: Doolittle 算法（教学）

```python
import numpy as np

def lu_doolittle(A):
    A = np.array(A, dtype=float)
    n = A.shape[0]
    L = np.eye(n)
    U = np.zeros_like(A)

    for i in range(n):
        for k in range(i, n):
            U[i, k] = A[i, k] - np.sum(L[i, :i] * U[:i, k])
        for k in range(i + 1, n):
            L[k, i] = (A[k, i] - np.sum(L[k, :i] * U[:i, i])) / U[i, i]
    return L, U
```

---

## 病态矩阵示例

### Example 4: Hilbert 矩阵（极病态）

Hilbert 矩阵 H[i,j] = 1/(i+j+1)，是对称正定的，条件数随 n 指数增长。

**Paper Source:**
- Hilbert, D. (1894). "Ein Beitrag zur Theorie des Legendre'schen Polynoms". *Acta Mathematica*, 18, 155-159.
- Kahan, W. (1966). "Four Cholesky Factors of Hilbert Matrices". University of California, Berkeley.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*, 2nd ed. SIAM, Section 2.8.

```python
import numpy as np
from scipy.linalg import lu_factor, lu_solve

def hilbert(n: int) -> np.ndarray:
    return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)], dtype=float)

n = 8
A = hilbert(n)
b = np.ones(n)

print(f"Condition number: {np.linalg.cond(A):.2e}")

lu, piv = lu_factor(A)
x = lu_solve((lu, piv), b)

residual = np.linalg.norm(A @ x - b)
print(f"Residual: {residual:.2e}")
print(f"Solution norm: {np.linalg.norm(x):.2e}")
```

### Example 5: Lotkin 矩阵（比 Hilbert 更病态）

Lotkin 矩阵类似 Hilbert，但第一行全为 1，非对称且更病态。

**Paper Source:**
- Lotkin, M. (1959). "A Set of Test Matrices". *MTAC*, 13(68), 153-161.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*, 2nd ed. SIAM, Section 26.1.

```python
import numpy as np
from scipy.linalg import lu_factor, lu_solve

def lotkin(n: int) -> np.ndarray:
    A = np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)], dtype=float)
    A[0, :] = 1.0
    return A

n = 8
A = lotkin(n)
b = np.ones(n)

print(f"Condition number: {np.linalg.cond(A):.2e}")

try:
    lu, piv = lu_factor(A)
    x = lu_solve((lu, piv), b)
    residual = np.linalg.norm(A @ x - b)
    print(f"Residual: {residual:.2e}")
except Exception as e:
    print(f"LU failed: {e}")
```

### Example 6: Vandermonde 矩阵（几何节点）

**Paper Source:**
- Vandermonde, A.-T. (1771). "Memoire sur l'elimination". *Histoire de l'Academie Royale des Sciences*, 516-532.
- Gautschi, W. (1978). "On Inverses of Vandermonde and Confluent Vandermonde Matrices". *Numerische Mathematik*, 29, 445-450.

```python
import numpy as np
from scipy.linalg import lu_factor, lu_solve

x = np.geomspace(0.1, 10, 15)
n = len(x)
V = np.vander(x, N=n, increasing=True)
b = np.ones(n)

print(f"Condition number: {np.linalg.cond(V):.2e}")

try:
    lu, piv = lu_factor(V)
    x_sol = lu_solve((lu, piv), b)
    residual = np.linalg.norm(V @ x_sol - b)
    print(f"Residual: {residual:.2e}")
except Exception as e:
    print(f"LU may be unstable: {e}")
```

### Example 7: Toeplitz 指数衰减矩阵

**Paper Source:**
- Toeplitz, O. (1911). "Zur Theorie der unendlichen Matrices". *Rendiconti del Circolo Matematico di Palermo*, 32, 82-86.
- Gray, R. M. (2006). "Toeplitz and Circulant Matrices: A Review". *Foundations and Trends in Communications and Information Theory*, 2(3), 155-239.

```python
import numpy as np

def toeplitz_exponential(n: int, rho: float = 0.99) -> np.ndarray:
    indices = np.arange(n)
    A = rho ** np.abs(indices[:, None] - indices[None, :])
    return A.astype(float)

n = 12
A = toeplitz_exponential(n, rho=0.99)
b = np.ones(n)

print(f"Condition number: {np.linalg.cond(A):.2e}")

from scipy.linalg import lu_factor, lu_solve
lu, piv = lu_factor(A)
x = lu_solve((lu, piv), b)
print(f"Residual: {np.linalg.norm(A @ x - b):.2e}")
```

---

## 论文引用矩阵示例

### Example 8: Pascal 矩阵

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
b = np.ones(n)

from scipy.linalg import lu_factor, lu_solve
lu, piv = lu_factor(A)
x = lu_solve((lu, piv), b)
print(f"Residual: {np.linalg.norm(A @ x - b):.2e}")
```

### Example 9: Kahan 矩阵

**Paper Source:**
- Kahan, W. (1966). "Numerical Linear Algebra". *Canadian Mathematical Bulletin*, 9, 757-801.

```python
import numpy as np
from scipy.linalg import lu_factor, lu_solve

def kahan_matrix(n: int, theta: float = 1.2) -> np.ndarray:
    s = np.sin(theta)
    c = np.cos(theta)
    A = np.eye(n) * s
    for i in range(n):
        for j in range(i+1, n):
            A[i, j] = -c * s**(n - j - 1)
    A[:, -1] = -c * np.ones(n)
    return A

n = 8
A = kahan_matrix(n)
b = np.ones(n)

print(f"Condition number: {np.linalg.cond(A):.2e}")

try:
    lu, piv = lu_factor(A)
    x = lu_solve((lu, piv), b)
    print(f"Residual: {np.linalg.norm(A @ x - b):.2e}")
except Exception as e:
    print(f"LU unstable: {e}")
```

### Example 10: Grcar 矩阵

**Paper Source:**
- Grcar, J. F. (1990). "Operator coefficient matrices for eigenvalue solvers". *SIAM Journal on Scientific and Statistical Computing*, 11(4), 754-763.

```python
import numpy as np
from scipy.linalg import lu_factor, lu_solve

def grcar_matrix(n: int, k: int = 3) -> np.ndarray:
    A = np.zeros((n, n))
    for i in range(n):
        A[i, i] = 1.0
        if i > 0:
            A[i, i-1] = -1.0
        for j in range(1, min(k+1, n-i)):
            A[i, i+j] = 1.0
    return A

n = 20
A = grcar_matrix(n, k=3)
b = np.ones(n)

print(f"Condition number: {np.linalg.cond(A):.2e}")

lu, piv = lu_factor(A)
x = lu_solve((lu, piv), b)
print(f"Residual: {np.linalg.norm(A @ x - b):.2e}")
```

---

## 输出模板

```markdown
### 问题重述
矩阵 A = [...], 目标: 分解/求解

### 矩阵检查
- shape: (n, n)
- 是否方阵: 是
- 条件数: cond(A)

### 分解结果
- P: [...]
- L: [...]
- U: [...]

### 验证
- reconstruction error ||A - PLU||: ...
- (如求解) residual ||Ax - b||: ...

### 结果解释
...
```

---

## 病态矩阵处理建议

当遇到条件数极高的矩阵（cond > 1e12）：

1. 先估计条件数并警告
2. 尝试矩阵均衡化（row/col scaling）
3. 考虑 Tikhonov 正则化（A + αI）
4. 最后回退到 SVD 伪逆

```python
from scipy.linalg import lu_factor, lu_solve
import numpy as np

def robust_lu_solve(A, b):
    cond = np.linalg.cond(A)

    if cond < 1e8:
        lu, piv = lu_factor(A)
        return lu_solve((lu, piv), b), {"method": "direct_lu", "cond": cond}
    elif cond < 1e12:
        row_norms = np.linalg.norm(A, axis=1)
        col_norms = np.linalg.norm(A, axis=0)
        row_scale = np.where(row_norms == 0, 1.0, row_norms)
        col_scale = np.where(col_norms == 0, 1.0, col_norms)

        Dr = np.diag(1.0 / row_scale)
        Dc = np.diag(1.0 / col_scale)
        A_eq = Dr @ A @ Dc

        lu, piv = lu_factor(A_eq)
        x_eq = lu_solve((lu, piv), Dr @ b)
        x = Dc @ x_eq
        return x, {"method": "equilibrated_lu", "cond": cond}
    else:
        x = np.linalg.pinv(A) @ b
        return x, {"method": "svd_fallback", "cond": cond}
```
