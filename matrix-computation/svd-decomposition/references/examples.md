# SVD Decomposition - Skill Usage Examples

> **Note**: This file demonstrates how to use the `/svd-decomposition` skill. For low-level implementation details using numpy/scipy, see [implementation.md](./implementation.md).

---

## Skill 概述

`/svd-decomposition` 用于对任意矩阵进行奇异值分解（A = UΣV^T），是最通用和稳健的矩阵分解方法。

**适用场景**:
- 任意形状矩阵的分解（方阵或长方形）
- 低秩近似、数据压缩
- 伪逆计算、最小二乘
- 秩分析、条件数估计
- 病态或秩亏矩阵处理
- PCA 等降维技术的前置处理

**优势**:
- 最通用的分解方法
- 数值稳定
- 能处理秩亏和病态矩阵
- 提供清晰的奇异值谱

---

## Example 1: 基础 SVD 分解

**问题**: 对矩阵进行奇异值分解

$$
A = \begin{bmatrix}
3 & 1 & 1 \\
-1 & 3 & 1
\end{bmatrix}
$$

**调用方式**:

```
对矩阵 A 进行奇异值分解
A = [[3, 1, 1], [-1, 3, 1]]

使用 /svd-decomposition skill
```

**预期输出**:

- skill 执行 SVD 分解
- 返回 U, Σ, V^T
- 验证 A ≈ UΣV^T
- 解释奇异值的含义

---

## Example 2: 低秩近似

**问题**: 使用 SVD 进行低秩近似

**调用方式**:

```
对矩阵 A 进行 rank-2 低秩近似
A = [[1, 2, 3], [4, 5, 6], [7, 8, 10]]

使用 /svd-decomposition skill
报告:
- 保留能量比例
- 重构误差
```

**预期输出**:

- skill 执行 SVD 分解
- 计算秩-2 近似
- 报告保留能量
- 展示近似矩阵

---

## Example 3: 秩亏矩阵处理

**问题**: 对秩亏矩阵进行处理

**调用方式**:

```
对秩亏矩阵 A 进行 SVD 分析
A = [[1, 2], [2, 4], [3, 6]]

使用 /svd-decomposition skill
估计数值秩
计算伪逆
```

**预期输出**:

- skill 执行 SVD 分解
- 分析奇异值
- 估计数值秩
- 计算伪逆

---

## Example 4: Hilbert 矩阵（病态）

**问题**: 对高度病态的 Hilbert 矩阵进行分析

**调用方式**:

```
对 15×15 Hilbert 矩阵进行 SVD 分析
Hilbert 矩阵定义: H[i,j] = 1/(i+j+1)

使用 /svd-decomposition skill
分析奇异值衰减
使用截断 SVD 改善稳定性
```

**预期输出**:

- skill 构造 Hilbert 矩阵
- 执行 SVD 分解
- 分析奇异值衰减
- 讨论截断策略

---

## Example 5: 最小二乘求解

**问题**: 使用 SVD 求解过定系统

**调用方式**:

```
求解过定系统的最小二乘解
A = [[1, 1], [1, 2], [1, 3], [1, 4]]
b = [6, 9, 20, 25]

使用 /svd-decomposition skill
使用伪逆求解
```

**预期输出**:

- skill 执行 SVD 分解
- 使用伪逆求解
- 返回最小二乘解
- 报告残差

---

## Example 6: Vandermonde 低秩近似

**问题**: 分析 Vandermonde 矩阵的奇异值衰减

**调用方式**:

```
分析 Vandermonde 矩阵的奇异值衰减
节点: 几何级数 from 0.1 to 10, 15 points

使用 /svd-decomposition skill
分析不同 k 的能量保留
```

**预期输出**:

- skill 构造 Vandermonde 矩阵
- 执行 SVD 分解
- 分析奇异值衰减
- 报告各 k 的能量保留

---

## Example 7: Pascal 矩阵

**问题**: 分析 Pascal 矩阵的 SVD

**调用方式**:

```
对 10×10 Pascal 矩阵进行 SVD 分解
Pascal 矩阵定义: P[i,j] = P[i-1,j] + P[i,j-1]

使用 /svd-decomposition skill
分析条件数和奇异值分布
```

**预期输出**:

- skill 构造 Pascal 矩阵
- 执行 SVD 分解
- 报告条件数
- 讨论数值性质

---

## Example 8: 指数衰减矩阵

**问题**: 分析具有指数衰减奇异值的矩阵

**调用方式**:

```
分析 50×50 指数衰减矩阵的 SVD
奇异值从 1 衰减到 10^-15

使用 /svd-decomposition skill
分析病态性
```

**预期输出**:

- skill 构造测试矩阵
- 执行 SVD 分解
- 分析条件数
- 讨论数值稳定性

---

## Example 9: 截断 SVD 求解

**问题**: 使用截断 SVD 求解病态系统

**调用方式**:

```
求解病态线性系统
A 是条件数约为 10^12 的矩阵
b 是随机向量

使用 /svd-decomposition skill
使用截断 SVD 求解
设置 rcond = 1e-10
```

**预期输出**:

- skill 执行 SVD 分解
- 设置截断阈值
- 求解系统
- 报告残差和截断秩

---

## Example 10: Cauchy 矩阵

**问题**: 分析 Cauchy 矩阵的 SVD

**调用方式**:

```
对 Cauchy 矩阵进行 SVD 分析
Cauchy 矩阵定义: C[i,j] = 1/(x_i + y_j)
x = [1, 2, ..., 8]
y = [1, 2, ..., 8]

使用 /svd-decomposition skill
```

**预期输出**:

- skill 构造 Cauchy 矩阵
- 执行 SVD 分解
- 分析奇异值
- 报告条件数

---

## Example 11: 能量保留分析

**问题**: 分析不同截断秩的能量保留

**调用方式**:

```
对随机矩阵 A (10×10) 进行 SVD 分析
分析不同 k 值的能量保留比例

使用 /svd-decomposition skill
k = 1, 2, ..., 10
```

**预期输出**:

- skill 构造随机矩阵
- 执行 SVD 分解
- 计算各 k 的能量保留
- 可视化衰减曲线

---

## Example 12: 完整诊断报告

**问题**: 获取 SVD 的完整诊断信息

**调用方式**:

```
对矩阵 A 进行完整的 SVD 分析
A = [[1, 2, 3], [4, 5, 6], [7, 8, 10]]

使用 /svd-decomposition skill
提供完整报告:
- 分解结果（U, Σ, V^T）
- 奇异值谱分析
- 数值秩
- 条件数
- 重构验证
- 低秩近似建议
```

**预期输出**:

- skill 生成结构化报告
  - U, Σ, V^T 矩阵
  - 奇异值列表和衰减
  - 数值秩估计
  - 条件数
  - 重构误差 ||A - UΣV^T||
  - 能量保留分析
  - 低秩近似建议

---

## Example 13: 与 QR/LU 比较

**问题**: 比较 SVD 与 QR、LU 在病态问题上的表现

**调用方式**:

```
对病态矩阵比较 SVD、QR 和 LU 的表现
A 是条件数约为 10^10 的矩阵
b 是随机向量

使用 /svd-decomposition skill
同时演示 QR 和 LU 方法
比较稳定性和结果
```

**预期输出**:

- skill 执行三种方法
- 比较各方法的结果
- 讨论数值稳定性
- 建议使用场景

---

## Example 14: PCA 前置处理

**问题**: 使用 SVD 为 PCA 做准备

**调用方式**:

```
对数据矩阵 X 进行 SVD 分析
X 是 100×3 数据矩阵（100个样本，3个特征）

使用 /svd-decomposition skill
说明与 PCA 的关系
```

**预期输出**:

- skill 执行 SVD 分解
- 解释与 PCA 的关系
- 分析主成分
- 讨论降维效果

---

## Example 15: 伪逆性质验证

**问题**: 验证 Moore-Penrose 伪逆的性质

**调用方式**:

```
对矩阵 A 计算 Moore-Penrose 伪逆并验证其性质
A = [[1, 2], [2, 4], [3, 6]]

使用 /svd-decomposition skill
验证:
1. A A^+ A = A
2. A^+ A A^+ = A^+
3. (A A^+)^T = A A^+
4. (A^+ A)^T = A^+ A
```

**预期输出**:

- skill 计算伪逆
- 验证四条 Moore-Penrose 性质
- 报告验证结果
- 解释伪逆的用途

---

## 通用调用模板

**基础分解**:

```
对矩阵 A 进行奇异值分解
A = [...]

使用 /svd-decomposition skill
```

**低秩近似**:

```
对矩阵 A 进行 rank-k 近似
A = [...]
k = 2

使用 /svd-decomposition skill
```

**伪逆**:

```
计算矩阵 A 的伪逆
A = [...]

使用 /svd-decomposition skill
```

**最小二乘**:

```
使用 SVD 求解 Ax = b
A = [...]
b = [...]

使用 /svd-decomposition skill
```

**截断 SVD**:

```
使用截断 SVD 求解病态系统
A = [...]
b = [...]

使用 /svd-decomposition skill
设置 rcond = 1e-10
```

**完整诊断**:

```
对矩阵 A 进行完整 SVD 分析
A = [...]

使用 /svd-decomposition skill
```

---

## 方法选择指南

| 矩阵类型/问题 | 推荐方法 | 理由 |
|---------------|---------|------|
| 任意形状 | SVD | 最通用 |
| 病态/秩亏 | SVD | 最稳定 |
| 一般方阵 | LU | 更快 |
| SPD | Cholesky | 最快最稳定 |
| 长方形/最小二乘 | QR 或 SVD | 自然适合 |
| 低秩近似 | SVD | 直接提供秩信息 |

使用 `/choose_decomposition` skill 可自动选择合适的方法。
