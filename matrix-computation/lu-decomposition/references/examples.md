# LU Decomposition - Skill Usage Examples

> **Note**: This file demonstrates how to use the `/lu-decomposition` skill. For low-level implementation details using numpy/scipy, see [implementation.md](./implementation.md).

---

## Skill 概述

`/lu-decomposition` 用于对方阵进行 LU 分解（A = PLU），求解线性方程组，估计行列式等。

**适用场景**:
- 方阵的 LU 分解
- 求解线性方程组 Ax = b
- 同一系数矩阵的多右端项求解
- 行列式估计

**不适用场景**:
- 非方阵 → 考虑 QR 或 SVD
- SPD 矩阵 → 优先使用 Cholesky
- 高度病态矩阵 → 考虑 SVD

---

## Example 1: 基础 LU 分解

**问题**: 对矩阵进行 LU 分解

$$
A = \begin{bmatrix}
2 & 1 & 1 \\
4 & -6 & 0 \\
-2 & 7 & 2
\end{bmatrix}
$$

**调用方式**:

```
对矩阵 A 进行 LU 分解
A = [[2, 1, 1], [4, -6, 0], [-2, 7, 2]]

使用 /lu-decomposition skill
说明: 使用 SciPy 约定 A = P @ L @ U
```

**预期输出**:

- skill 执行 LU 分解
- 返回置换矩阵 P、下三角矩阵 L、上三角矩阵 U
- 验证重构误差 ||A - PLU||
- 解释部分主元的作用

---

## Example 2: 求解线性方程组

**问题**: 使用 LU 分解求解 Ax = b

$$
A = \begin{bmatrix}
3 & 1 \\
1 & 2
\end{bmatrix}, \quad
b = \begin{bmatrix}
9 \\
8
\end{bmatrix}
$$

**调用方式**:

```
求解线性方程组 Ax = b
A = [[3, 1], [1, 2]]
b = [9, 8]

使用 /lu-decomposition skill
使用 LU 分解求解
```

**预期输出**:

- skill 执行 LU 分解
- 前代和回代求解
- 返回解 x
- 验证残差 ||Ax - b||

---

## Example 3: 多右端项求解

**问题**: 使用同一 LU 分解求解多个右端项

**调用方式**:

```
求解线性方程组组 AX = B
A = [[2, 1], [1, 2]]
B = [[1, 2], [3, 4]]  # 两列，两个右端项

使用 /lu-decomposition skill
说明: 只需分解一次，可高效求解多个右端项
```

**预期输出**:

- skill 执行一次 LU 分解
- 对每个右端项求解
- 返回解矩阵 X
- 讨论 LU 在多右端项时的优势

---

## Example 4: Hilbert 矩阵（病态测试）

**问题**: 对病态的 Hilbert 矩阵进行 LU 分解

**调用方式**:

```
对 8×8 Hilbert 矩阵进行 LU 分解并求解
Hilbert 矩阵定义: H[i,j] = 1/(i + j + 1)
右端项 b 是全1向量

使用 /lu-decomposition skill
分析病态对求解的影响
```

**预期输出**:

- skill 构造 Hilbert 矩阵
- 报告条件数
- 执行 LU 分解和求解
- 讨论数值稳定性问题

---

## Example 5: Vandermonde 矩阵

**问题**: 对 Vandermonde 矩阵进行 LU 分解

**调用方式**:

```
对 Vandermonde 矩阵进行 LU 分解
节点 x = geometric progression from 0.1 to 10, 15 points
右端项 b 是全1向量

使用 /lu-decomposition skill
分析条件数和数值稳定性
```

**预期输出**:

- skill 构造 Vandermonde 矩阵
- 报告条件数（可能很高）
- 执行 LU 分解
- 讨论几何节点的选择

---

## Example 6: Grcar 矩阵（非正规矩阵）

**问题**: 对 Grcar 矩阵进行 LU 分解

**调用方式**:

```
对 20×20 Grcar 矩阵进行 LU 分解
Grcar 矩阵定义: 对角线=1, 下对角线=-1, 上对角线前k个=1
k = 3
右端项 b 是全1向量

使用 /lu-decomposition skill
分析非正规矩阵的 LU 分解
```

**预期输出**:

- skill 构造 Grcar 矩阵
- 报告矩阵特性
- 执行 LU 分解
- 讨论非正规性的影响

---

## Example 7: 行列式估计

**问题**: 使用 LU 分解估计行列式

**调用方式**:

```
计算矩阵 A 的行列式
A = [[2, 1, 1], [4, -6, 0], [-2, 7, 2]]

使用 /lu-decomposition skill
从 LU 分解计算行列式
```

**预期输出**:

- skill 执行 LU 分解
- 从 U 的对角元和置换符号计算行列式
- 返回 det(A)
- 解释计算方法

---

## Example 8: 病态矩阵处理流程

**问题**: 演示完整的病态矩阵处理流程

**调用方式**:

```
对病态矩阵进行鲁棒 LU 求解
A 是条件数约为 10^10 的矩阵
b 是随机向量

使用 /lu-decomposition skill
执行完整诊断:
1. 条件数估计
2. 尝试直接 LU
3. 如失败，尝试矩阵均衡化
4. 如仍失败，回退到 SVD
```

**预期输出**:

- skill 生成结构化报告
  - 条件数估计
  - 尝试的方法
  - 使用的方法
  - 最终解和残差
  - 诊断建议

---

## Example 9: Doolittle 算法演示

**问题**: 演示 Doolittle LU 分解的步骤

**调用方式**:

```
使用 Doolittle 算法对矩阵进行 LU 分解
A = [[2, 1], [1, 2]]

使用 /lu-decomposition skill
展示详细步骤（教学用途）
```

**预期输出**:

- skill 演示 Doolittle 算法
- 展示每步的计算
- 解释 L 和 U 的构造
- 讨论部分主元的必要性

---

## Example 10: 与 Cholesky 比较

**问题**: 在 SPD 矩阵上比较 LU 和 Cholesky

**调用方式**:

```
对 SPD 矩阵比较 LU 分解和 Cholesky 分解
A = [[4, 1], [1, 3]]

使用 /lu-decomposition skill
同时演示 Cholesky 分解
比较两种方法的效率和稳定性
```

**预期输出**:

- skill 执行两种分解
- 比较结果
- 讨论何时使用哪种方法
- 说明 Cholesky 对 SPD 的优势

---

## Example 11: 完整的诊断报告

**问题**: 获取 LU 分解的完整诊断

**调用方式**:

```
对矩阵 A 进行完整的 LU 分解分析
A = [[2, 1, 1], [4, -6, 0], [-2, 7, 2]]

使用 /lu-decomposition skill
提供完整诊断报告:
- 矩阵特性检查
- 分解结果（P, L, U）
- 重构验证
- 行列式
- 置换信息
```

**预期输出**:

- skill 生成结构化报告
  - 矩阵形状和方阵检查
  - 条件数估计
  - P, L, U 矩阵
  - 重构误差 ||A - PLU||
  - det(A) 从 LU 计算
  - 置换向量解释
  - 数值稳定性评估

---

## Example 12: 置换矩阵解释

**问题**: 理解 LU 分解中置换矩阵的作用

**调用方式**:

```
解释 LU 分解中置换矩阵的作用
A = [[0, 1], [1, 0]]  # 需要交换行的矩阵

使用 /lu-decomposition skill
详细解释为何需要置换
```

**预期输出**:

- skill 执行 LU 分解
- 解释零主元问题
- 展示置换矩阵 P
- 说明 A = PLU 的含义

---

## 通用调用模板

**基础分解**:

```
对矩阵 A 进行 LU 分解
A = [...]

使用 /lu-decomposition skill
```

**求解方程组**:

```
求解 Ax = b
A = [...]
b = [...]

使用 /lu-decomposition skill
```

**行列式**:

```
计算矩阵 A 的行列式
A = [...]

使用 /lu-decomposition skill
从 LU 分解计算
```

**病态处理**:

```
对病态矩阵 A 进行鲁棒求解
b = [...]

使用 /lu-decomposition skill
提供完整诊断
```

**完整诊断**:

```
对矩阵 A 进行完整的 LU 分解分析
A = [...]

使用 /lu-decomposition skill
```

---

## 方法选择指南

| 矩阵类型 | 推荐方法 | 理由 |
|---------|---------|------|
| 一般方阵 | LU | 通用、高效 |
| SPD | Cholesky | 更快、更稳定 |
| 非方阵 | QR 或 SVD | LU 不适用 |
| 病态 | SVD + 正则化 | LU 不稳定 |
| 多右端项 | LU | 分解一次，多次求解 |

使用 `/choose_decomposition` skill 可自动选择合适的方法。
