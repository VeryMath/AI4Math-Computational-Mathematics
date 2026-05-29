# QR Decomposition - Implementation Reference

> **Note**: This file contains low-level implementation details using numpy/scipy. For usage examples of the `/qr-decomposition` skill, see [examples.md](./examples.md).

---

## 基础示例

### Example 1: 完整 QR 分解

```python
import numpy as np

A = np.array([
    [1.0, 2.0],
    [3.0, 4.0],
    [5.0, 6.0],
])

Q, R = np.linalg.qr(A, mode='complete')
print("Q (complete) =\n", Q)
print("R (complete) =\n", R)
print("Q is orthogonal:", np.allclose(Q.T @ Q, np.eye(Q.shape[1])))
print("Reconstruction error:", np.linalg.norm(A - Q @ R))
```

### Example 2: 经济型 QR 分解

```python
import numpy as np

A = np.array([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
    [7.0, 8.0, 9.0],
])

Q, R = np.linalg.qr(A, mode='reduced')
print("Q (reduced) =\n", Q)
print("R (reduced) =\n", R)
print("Q^T Q =\n", Q.T @ Q)
print("Reconstruction error:", np.linalg.norm(A - Q @ R))
```

### Example 3: 求解最小二乘问题

```python
import numpy as np

# 过定系统：更多方程组
A = np.array([
    [1.0, 1.0],
    [1.0, 2.0],
    [1.0, 3.0],
    [1.0, 4.0],
])
b = np.array([6.0, 9.0, 20.0, 25.0])

Q, R = np.linalg.qr(A, mode='reduced')
x = np.linalg.solve(R, Q.T @ b)
print("Least squares solution x =", x)
print("Residual ||Ax - b|| =", np.linalg.norm(A @ x - b))
```

### Example 4: 带列选主元的 QR（rank-revealing）

```python
import numpy as np
from scipy.linalg import qr

A = np.array([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
    [7.0, 8.0, 9.0],
])

Q, R, P = qr(A, pivoting=True, mode='economic')
print("Q =\n", Q)
print("R =\n", R)
print("Permutation vector P =", P)
print("Diagonal of R:", np.abs(np.diag(R)))
```

---

## 病态矩阵示例

### Example 5: Hilbert 矩阵（极病态）

**Paper Source:**
- Hilbert, D. (1894). "Ein Beitrag zur Theorie des Legendre'schen Polynoms". *Acta Mathematica*, 18, 155-159.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*, 2nd ed. SIAM.

```python
import numpy as np

def hilbert(n: int) -> np.ndarray:
    return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)], dtype=float)

n = 12
A = hilbert(n)
b = np.ones(n)

Q, R = np.linalg.qr(A)
x = np.linalg.solve(R, Q.T @ b)
print("Solution x =", x)
print("Residual ||Ax - b|| =", np.linalg.norm(A @ x - b))
print("Condition number of R:", np.linalg.cond(R))
```

### Example 6: Vandermonde 矩阵

**Paper Source:**
- Vandermonde, A.-T. (1771). "Memoire sur l'élimination".
- Gautschi, W. (1978). "On Inverses of Vandermonde Matrices".

```python
import numpy as np

x = np.linspace(0.1, 5.0, 10)
n = len(x)
V = np.vander(x, N=n, increasing=True)

Q, R = np.linalg.qr(V)
print("Diagonal of R:", np.abs(np.diag(R)))
print("Orthogonality error ||Q^T Q - I|| =", np.linalg.norm(Q.T @ Q - np.eye(Q.shape[1])))

b = np.ones(n)
x_ls = np.linalg.solve(R, Q.T @ b)
print("Residual ||Vx - b|| =", np.linalg.norm(V @ x_ls - b))
```

### Example 7: Cauchy 矩阵

**Paper Source:**
- Cauchy, A. L. (1841). *Exercices d'analyse et de physique mathématique*.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*, 2nd ed. SIAM.

```python
import numpy as np

def cauchy_matrix(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return 1.0 / (x[:, np.newaxis] + y[np.newaxis, :])

x = np.arange(1, 9, dtype=float)
y = np.arange(1, 9, dtype=float)
A = cauchy_matrix(x, y)

Q, R, P = np.linalg.qr(A, pivoting=True, mode='economic')
print("Diagonal of R:", np.abs(np.diag(R)))
print("Condition number:", np.linalg.cond(R))
```

### Example 8: Grcar 矩阵（非正规）

**Paper Source:**
- Grcar, J. F. (1981). "Matrix eigenspace routines". *SIAM*.

```python
import numpy as np

def grcar(n: int, k: int = 3) -> np.ndarray:
    """Return Grcar matrix of order n with subdiagonals -1 and superdiagonals 1."""
    A = np.triu(np.ones((n, n)), 0)
    for i in range(n - 1):
        A[i + 1, i] = -1.0
    for j in range(1, min(k + 1, n)):
        for i in range(n - j):
            A[i, i + j] = 1.0
    return A

n = 20
A = grcar(n)

Q, R = np.linalg.qr(A)
print("Orthogonality error ||Q^T Q - I|| =", np.linalg.norm(Q.T @ Q - np.eye(Q.shape[1])))
print("Diagonal decay of R:", np.abs(np.diag(R)))
```

---

## 秩亏与低秩矩阵示例

### Example 9: 秩亏矩阵（列成比例）

```python
import numpy as np

A = np.array([
    [1.0, 2.0, 3.0],
    [2.0, 4.0, 6.0],
    [3.0, 6.0, 9.0],
])

Q, R = np.linalg.qr(A)
print("Q =\n", Q)
print("R =\n", R)
print("Diagonal of R:", np.abs(np.diag(R)))
print("Numerical rank estimate:", np.sum(np.abs(np.diag(R)) > 1e-10))
```

### Example 10: 随机秩亏矩阵

```python
import numpy as np

np.random.seed(42)
n, m, rank = 10, 8, 3

U, _ = np.linalg.qr(np.random.randn(n, rank))
V, _ = np.linalg.qr(np.random.randn(m, rank))
A = U @ V.T

Q, R = np.linalg.qr(A)
print("True rank:", rank)
print("Diagonal of R:", np.abs(np.diag(R)))
print("Estimated rank:", np.sum(np.abs(np.diag(R)) > 1e-10))
```

---

## 长方形矩阵示例

### Example 11: 过定系统（最小二乘）

```python
import numpy as np

# 多于方程组
A = np.array([
    [1.0, 2.0],
    [3.0, 4.0],
    [5.0, 6.0],
    [7.0, 8.0],
])
b = np.array([5.0, 11.0, 17.0, 23.0])

Q, R = np.linalg.qr(A, mode='reduced')
x = np.linalg.solve(R, Q.T @ b)
print("Least squares solution x =", x)
print("Residual ||Ax - b|| =", np.linalg.norm(A @ x - b))
print("Verification: should be exact (residual near 0)")
```

### Example 12: 欠定系统（最小范数解）

```python
import numpy as np

# 少于方程组
A = np.array([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
])
b = np.array([7.0, 8.0])

# QR doesn't directly give minimum norm solution for underdetermined systems
# Use least squares on A.T instead
Q, R = np.linalg.qr(A.T, mode='reduced')
y = np.linalg.solve(R, Q.T @ b)
x = Q @ y
print("Minimum norm solution x =", x)
print("||x|| =", np.linalg.norm(x))
print("Residual ||Ax - b|| =", np.linalg.norm(A @ x - b))
```

---

## Gram-Schmidt 示例

### Example 13: 经典 Gram-Schmidt（不推荐）

```python
import numpy as np

A = np.array([
    [1.0, 1.0, 0.0],
    [1.0, 0.0, 1.0],
    [0.0, 1.0, 1.0],
], dtype=float)

m, n = A.shape
Q = np.zeros_like(A)
R = np.zeros((n, n))

for j in range(n):
    v = A[:, j].copy()
    for i in range(j):
        R[i, j] = np.dot(Q[:, i], A[:, j])
        v = v - R[i, j] * Q[:, i]
    R[j, j] = np.linalg.norm(v)
    Q[:, j] = v / R[j, j]

print("Q (classical GS) =\n", Q)
print("R (classical GS) =\n", R)
print("Orthogonality error ||Q^T Q - I|| =", np.linalg.norm(Q.T @ Q - np.eye(n)))
```

### Example 14: 修正 Gram-Schmidt（推荐）

```python
import numpy as np

A = np.array([
    [1.0, 1.0, 0.0],
    [1.0, 0.0, 1.0],
    [0.0, 1.0, 1.0],
], dtype=float)

m, n = A.shape
Q = np.zeros_like(A)
R = np.zeros((n, n))

for j in range(n):
    v = A[:, j].copy()
    for i in range(j):
        R[i, j] = np.dot(Q[:, i], v)
        v = v - R[i, j] * Q[:, i]
    R[j, j] = np.linalg.norm(v)
    Q[:, j] = v / R[j, j]

print("Q (modified GS) =\n", Q)
print("R (modified GS) =\n", R)
print("Orthogonality error ||Q^T Q - I|| =", np.linalg.norm(Q.T @ Q - np.eye(n)))
```

---

## Householder 反射示例

### Example 15: 手动实现单个 Householder 变换

```python
import numpy as np

def householder(v: np.ndarray) -> np.ndarray:
    """Return Householder vector for reflection."""
    v = v.astype(float)
    norm_v = np.linalg.norm(v)
    if norm_v == 0:
        return v
    e1 = np.zeros_like(v)
    e1[0] = 1.0
    u = v + np.sign(v[0]) * norm_v * e1
    u = u / np.linalg.norm(u)
    return u

A = np.array([[3.0, 4.0], [0.0, 0.0]], dtype=float)

# Zero out first column below diagonal
u = householder(A[:, 0])
H = np.eye(2) - 2.0 * np.outer(u, u)
print("Householder vector u =", u)
print("H =\n", H)
print("H @ A =\n", H @ A)
```

---

## 病态 QR 求解建议

```python
import numpy as np
from scipy.linalg import qr

def robust_qr_solve(A, b, pivoting=True):
    """Robust QR-based solver with rank detection."""
    if pivoting:
        Q, R, P = qr(A, pivoting=True, mode='economic')
        diag_r = np.abs(np.diag(R))
        tol = max(A.shape) * np.finfo(R.dtype).eps * diag_r[0]
        rank = int(np.sum(diag_r > tol))
        method = "qr_pivoting"
    else:
        Q, R = np.linalg.qr(A, mode='reduced')
        diag_r = np.abs(np.diag(R))
        tol = max(A.shape) * np.finfo(R.dtype).eps * diag_r[0]
        rank = int(np.sum(diag_r > tol))
        method = "qr"

    if rank < min(A.shape):
        # Rank deficient: truncated least squares
        k = rank
        Qk = Q[:, :k]
        Rk = R[:k, :]
        x = np.linalg.solve(Rk, Qk.T @ b)
    else:
        x = np.linalg.solve(R, Q.T @ b)

    report = {
        "method": method,
        "rank_estimate": rank,
        "residual_norm": float(np.linalg.norm(A @ x - b)),
        "orthogonality_error": float(np.linalg.norm(Q.T @ Q - np.eye(Q.shape[1]))),
    }
    return x, report
```
