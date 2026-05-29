复杂案例
---

- Grcar 矩阵（非对称、非正规）：用于测试特征值求解器在非正规矩阵和强伪谱情形下的稳定性与精度。
- 聚簇特征值的对称矩阵：构造有紧密簇的特征值并加入微小对称扰动，用来测试特征值分辨率。
- 病态对称矩阵（高条件数或接近 Jordan 结构）：用于观察特征向量/特征值的数值不稳定性。

使用建议
---
- 使用 `scipy.linalg.eig` 做稠密参考解，并用 `scipy.sparse.linalg.eigs` 对大维度矩阵抽取部分特征值进行对比。
- 检查残差 ||A v - λ v|| 与特征值间距（gap），以及对小扰动的敏感性。


# 特征值计算示例

示例：密集矩阵的全部特征值和幂法近似最大特征值

```python
import numpy as np

# 稠密对称矩阵的全部特征值（参考）
A = np.array([[2.0, 1.0], [1.0, 3.0]])
vals, vecs = np.linalg.eigh(A)
print(vals)

# 简单幂法示例（近似最大特征值）
def power_method(A, x0=None, tol=1e-8, maxiter=1000):
	n = A.shape[0]
	x = np.random.randn(n) if x0 is None else x0
	x = x / np.linalg.norm(x)
	lambda_old = 0.0
	for _ in range(maxiter):
		y = A @ x
		lambda_new = float(x @ y)
		y_norm = np.linalg.norm(y)
		if y_norm == 0:
			return 0.0, x
		x = y / y_norm
		if abs(lambda_new - lambda_old) <= tol:
			return lambda_new, x
		lambda_old = lambda_new
	return lambda_new, x

lam, v = power_method(A)
print('power method lambda=', lam)
```

提示：对大型稀疏矩阵，使用 `scipy.sparse.linalg.eigs`。
