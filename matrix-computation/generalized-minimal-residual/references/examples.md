复杂案例
---

- Grcar 矩阵与其他非对称非正规矩阵：测试 GMRES 在非正规系统和伪谱显著时的收敛性。
- 对流-扩散离散化矩阵（非对称、可能具有强对流项）：常见于 PDE 离散化，能展现 GMRES 对非对称项的处理情况。
- 接近奇异或高度不良条件的非对称矩阵：观察重启 GMRES 与无重启 GMRES 的差异。

使用建议
---
- 对比不同重启参数和预处理器（如 ILU、对角预处理）对收敛速度的影响。
- 检查剩余范数随迭代的变化并记录迭代次数与最终残差。

# GMRES 示例

示例：用 GMRES 求解非对称系统

```python
import numpy as np
from scipy.sparse.linalg import gmres as scipy_gmres

A = np.array([[3.0, 2.0], [1.0, 4.0]])
b = np.array([1.0, 2.0])
# 使用 SciPy GMRES 做简单示例；若使用技能内的 gmres 函数，调用方式类似
x, info = scipy_gmres(A, b, rtol=1e-10, restart=5)
print(x)
print(info)
```

提示：生产环境请优先考虑 `scipy.sparse.linalg.gmres`。
