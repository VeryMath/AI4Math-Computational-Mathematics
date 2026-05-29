# QR Decomposition - Skill Usage Examples

> **Note**: This file demonstrates how to use the `/qr-decomposition` skill. For low-level implementation details using numpy/scipy, see [implementation.md](./implementation.md).

---

## Skill 概述

`/qr-decomposition` 用于对任意矩阵进行 QR 分解（A = QR），求解最小二乘问题，计算正交基等。

**适用场景**:
- 任意矩阵的 QR 分解（方阵或长方形）
- 最小二乘问题（过定系统）
- 欠定系统的最小范数解
- 正交基计算、投影
- Gram-Schmidt 正交化

**不适用场景**:
- 明显秩亏或病态 → 推荐 SVD
- SPD 矩阵 → 优先使用 Cholesky

---

## Example 1: 基础 QR 分解

**问题**: 对矩阵进行 QR 分解

$$
A = \begin{bmatrix}
1 & 2 \\
3 & 4 \\
5 & 6
\end{bmatrix}
$$

**调用方式**:

```
对矩阵 A 进行 QR 分解
A = [[1, 2], [3, 4], [5, 6]]

使用 /qr-decomposition skill
说明: 使用经济型 QR
```

**预期输出**:

- skill 执行 QR 分解
- 返回 Q (3×2) 和 R (2×2)
- 验证 A ≈ QR
- 验证 Q 的正交性

---

## Example 2: 求解最小二乘问题

**问题**: 求解过定系统的最小二乘解

$$
\begin{bmatrix}
1 & 1 \\
1 & 2 \\
1 & 3 \\
1 & 4
\end{bmatrix} x = \begin{bmatrix}
6 \\
9 \\
20 \\
25
\end{bmatrix}
$$

**调用方式**:

```
求解过定系统的最小二乘解
A = [[1, 1], [1, 2], [1, 3], [1, 4]]
b = [6, 9, 20, 25]

使用 /qr-decomposition skill
```

**预期输出**:

- skill 执行 QR 分解
- 求解 R x = Q^T b
- 返回最小二乘解 x
- 报告残差 ||Ax - b||

---

## Example 3: 带列选主元的 QR

**问题**: 对近似秩亏矩阵进行 rank-revealing QR

**调用方式**:

```
对矩阵 A 进行 rank-revealing QR 分解
A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

使用 /qr-decomposition skill
使用列选主元（pivoting=True）
估计数值秩
```

**预期输出**:

- skill 执行带列选主元的 QR
- 返回 Q, R, P（置换）
- 分析 R 的对角元
- 估计数值秩

---

## Example 4: Hilbert 矩阵（病态测试）

**问题**: 对病态 Hilbert 矩阵进行 QR 分解

**调用方式**:

```
对 12×12 Hilbert 矩阵进行 QR 分解
Hilbert 矩阵定义: H[i,j] = 1/(i + j + 1)

使用 /qr-decomposition skill
分析数值稳定性
```

**预期输出**:

- skill 构造 Hilbert 矩阵
- 执行 QR 分解
- 报告 R 的条件数
- 讨论病态影响

---

## Example 5: 欠定系统

**问题**: 求解欠定系统的最小范数解

**调用方式**:

```
求解欠定线性系统的最小范数解
A = [[1, 2, 3], [4, 5, 6]]
b = [7, 8]

使用 /qr-decomposition skill
求最小范数解
```

**预期输出**:

- skill 识别为欠定系统
- 使用 A^T 的 QR 分解
- 返回最小范数解 x
- 验证 ||x|| 最小

---

## Example 6: Vandermonde 矩阵

**问题**: 分析 Vandermonde 矩阵的 QR 分解

**调用方式**:

```
对 Vandermonde 矩阵进行 QR 分解
节点 x = linspace(0.1, 5.0, 10)

使用 /qr-decomposition skill
分析 R 的对角元衰减
```

**预期输出**:

- skill 构造 Vandermonde 矩阵
- 执行 QR 分解
- 分析对角元
- 讨论多项式拟合的数值问题

---

## Example 7: Grcar 矩阵（非正规）

**问题**: 对非正规矩阵进行 QR 分解

**调用方式**:

```
对 20×20 Grcar 矩阵进行 QR 分解
Grcar 矩阵定义: 对角线=1, 下对角线=-1, 上对角线前k个=1
k = 3

使用 /qr-decomposition skill
分析正交性误差
```

**预期输出**:

- skill 构造 Grcar 矩阵
- 执行 QR 分解
- 报告正交性误差
- 讨论非正规矩阵

---

## Example 8: Gram-Schmidt 正交化

**问题**: 使用 QR 分解进行 Gram-Schmidt 正交化

**调用方式**:

```
对矩阵 A 的列向量进行 Gram-Schmidt 正交化
A = [[1, 1, 0], [1, 0, 1], [0, 1, 1]]

使用 /qr-decomposition skill
获取正交化的 Q 矩阵
```

**预期输出**:

- skill 执行 QR 分解
- 返回正交矩阵 Q
- 验证正交性
- 解释 Gram-Schmidt 关系

---

## Example 9: 秩亏矩阵检测

**问题**: 检测和处理秩亏矩阵

**调用方式**:

```
检测矩阵的秩并处理秩亏情况
A = [[1, 2, 3], [2, 4, 6], [3, 6, 9]]

使用 /qr-decomposition skill
估计数值秩
处理秩亏情况
```

**预期输出**:

- skill 执行 QR 分解
- 分析 R 对角元
- 估计数值秩
- 讨论处理策略

---

## Example 10: 正交基计算

**问题**: 计算矩阵列空间的正交基

**调用方式**:

```
计算矩阵 A 列空间的正交基
A = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]

使用 /qr-decomposition skill
返回 Q 作为正交基
```

**预期输出**:

- skill 执行经济型 QR
- 返回 Q (4×3)
- 验证正交性
- 解释基的性质

---

## Example 11: 与 SVD 比较

**问题**: 比较 QR 和 SVD 在最小二乘问题上的表现

**调用方式**:

```
对同一最小二乘问题比较 QR 和 SVD 方法
A = [[1, 2], [3, 4], [5, 6]]
b = [7, 8, 9]

使用 /qr-decomposition skill
同时演示 SVD 方法
比较结果和稳定性
```

**预期输出**:

- skill 执行 QR 和 SVD
- 比较解的差异
- 讨论各自优势
- 建议使用场景

---

## Example 12: 完整的诊断报告

**问题**: 获取 QR 分解的完整诊断

**调用方式**:

```
对矩阵 A 进行完整的 QR 分解分析
A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

使用 /qr-decomposition skill
提供完整报告:
- 矩阵特性
- 分解结果（Q, R）
- 正交性验证
- 秩估计
- 数值稳定性评估
```

**预期输出**:

- skill 生成结构化报告
  - 矩阵形状和特性
  - Q, R 矩阵
  - 正交性误差 ||Q^T Q - I||
  - R 的对角元分析
  - 数值秩估计
  - 条件数（如适用）
  - 数值稳定性评估

---

## 通用调用模板

**基础分解**:

```
对矩阵 A 进行 QR 分解
A = [...]

使用 /qr-decomposition skill
```

**最小二乘**:

```
求解 Ax = b 的最小二乘解
A = [...]
b = [...]

使用 /qr-decomposition skill
```

**带选主元**:

```
对矩阵 A 进行 rank-revealing QR 分解
A = [...]

使用 /qr-decomposition skill
使用列选主元
```

**正交基**:

```
计算矩阵 A 列空间的正交基
A = [...]

使用 /qr-decomposition skill
```

**完整诊断**:

```
对矩阵 A 进行完整 QR 分析
A = [...]

使用 /qr-decomposition skill
```

---

## 方法选择指南

| 矩阵类型 | 推荐方法 | 理由 |
|---------|---------|------|
| 一般长方形 | QR | 自然适合最小二乘 |
| 列满秩 | QR | 高效稳定 |
| 秩亏/病态 | SVD | 更可靠 |
| SPD | Cholesky | 更快更稳定 |
| 正交基计算 | QR | 直接得到 Q |

使用 `/choose_decomposition` skill 可自动选择合适的方法。
