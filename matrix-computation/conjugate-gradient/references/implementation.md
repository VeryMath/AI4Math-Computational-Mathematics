# Conjugate Gradient - Implementation Reference

> **Note**: This file contains low-level implementation details using numpy/scipy. For usage examples of the `/conjugate-gradient` skill, see [examples.md](./examples.md).

---

## 复杂案例

- Hilbert 矩阵（对称正定但高度病态）：用于测试共轭梯度在病态 SPD 系统上的收敛行为和数值稳定性。
- 2D Poisson（有限差分离散的 Laplace 算子，稀疏 SPD）：测试在稀疏大系统上的性能与迭代次数增长。
- 带有小特征值的对角缩放矩阵：用来观察 CG 对接近奇异矩阵的敏感性。

## 使用建议

- 对小维度稠密问题用直接方法求参考解（`scipy.linalg.solve`），对较大问题用 `scipy.sparse.linalg.cg` 比较迭代残差与迭代次数趋势。
- 记录相对残差与迭代次数，观察预处理（如对角预处理）对收敛性的影响。

---

## 示例：求解方阵 A x = b

```python
import numpy as np
from scipy.sparse.linalg import cg as scipy_cg

# Hilbert 矩阵定义: H_ij = 1/(i + j - 1)
def hilbert(n: int):
    i = np.arange(1, n + 1)
    return np.array([[1.0 / (ii + jj - 1) for jj in i] for ii in i], dtype=float)

# 小 demo: 对小维度用直接解法作为参考
A = np.array([[4.0, 1.0], [1.0, 3.0]])
b = np.array([1.0, 2.0])
# 若使用自定义 conjugate_gradient: x, info = conjugate_gradient(A, b, tol=1e-10)
# 也可以使用 scipy 的接口:
x, info = scipy_cg(A, b, rtol=1e-10)
print(x)
```

**注意事项**：若 A 不是 SPD，应使用其他迭代器（如 GMRES）。
