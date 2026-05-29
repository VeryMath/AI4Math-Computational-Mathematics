# Eigenvalue Computation - Skill Usage Examples

> **Note**: This file demonstrates how to use the `/eigenvalue-computation` skill. For low-level implementation details using numpy/scipy, see [implementation.md](./implementation.md).

---

## Skill 概述

`/eigenvalue-computation` 用于计算矩阵的特征值和特征向量，进行谱分析、模态分解、稳定性分析等。

**适用场景**:
- 计算全部或部分特征值/特征向量
- 谱分析、模态分解
- 稳定性分析
- 求主特征值（幂法）

**方法选择**:
- 对称矩阵 → `eigh`（高效、稳定）
- 非对称矩阵 → `eig`
- 大型稀疏矩阵 → `eigs`（迭代法）
- 仅最大特征值 → 幂法

---

## Example 1: 对称矩阵特征值

**问题**: 计算对称矩阵的全部特征值和特征向量

$$
A = \begin{bmatrix}
2 & 1 \\
1 & 3
\end{bmatrix}
$$

**调用方式**:

```
计算矩阵 A 的全部特征值和特征向量
A = [[2, 1], [1, 3]]

使用 /eigenvalue-computation skill
```

**预期输出**:

- skill 检测到对称矩阵，使用 `eigh`
- 返回特征值 λ₁, λ₂ 和对应特征向量
- 验证 A v = λ v
- 报告谱半径和条件数

---

## Example 2: 非对称矩阵特征值

**问题**: 计算非对称矩阵的特征值

$$
A = \begin{bmatrix}
1 & 2 \\
3 & 4
\end{bmatrix}
$$

**调用方式**:

```
计算矩阵 A 的特征值
A = [[1, 2], [3, 4]]

使用 /eigenvalue-computation skill
注意: A 是非对称矩阵
```

**预期输出**:

- skill 检测到非对称矩阵，使用 `eig`
- 返回（可能是复数）特征值
- 报告谱性质（实数/复数）
- 可能讨论特征值的几何/代数重数

---

## Example 3: 幂法求主特征值

**问题**: 使用幂法求矩阵的最大特征值

$$
A = \begin{bmatrix}
4 & 1 & 0 \\
1 & 4 & 1 \\
0 & 1 & 4
\end{bmatrix}
$$

**调用方式**:

```
使用幂法求矩阵 A 的最大特征值和对应特征向量
A = [[4, 1, 0], [1, 4, 1], [0, 1, 4]]

使用 /eigenvalue-computation skill
指定使用幂法（power method）
容差 tol = 1e-8
```

**预期输出**:

- skill 使用幂法迭代
- 报告迭代历史
- 返回近似主特征值和特征向量
- 与精确值比较验证

---

## Example 4: 稀疏矩阵的部分特征值

**问题**: 计算大型稀疏矩阵的前 k 个特征值

**调用方式**:

```
计算矩阵 A 的前 5 个最大特征值
A 是 1000×1000 稀疏对称矩阵（三对角: 2在对角线，-1在次对角线）

使用 /eigenvalue-computation skill
使用稀疏方法，仅计算前 5 个
```

**预期输出**:

- skill 使用稀疏特征值求解器
- 返回前 5 个特征值和特征向量
- 报告计算效率和内存使用
- 讨论稀疏矩阵的优势

---

## Example 5: 特征值聚簇测试

**问题**: 测试特征值求解器对聚簇特征值的分辨能力

**调用方式**:

```
计算以下矩阵的特征值
A = Q @ diag([1, 1.01, 1.02, 5, 10]) @ Q.T
其中 Q 是随机正交矩阵

使用 /eigenvalue-computation skill
注意: 前三个特征值非常接近
观察求解器能否正确分辨
```

**预期输出**:

- skill 构造测试矩阵
- 计算特征值
- 分析聚簇特征值的精度
- 讨论数值扰动的影响

---

## Example 6: Grcar 矩阵（非正规矩阵）

**问题**: 计算非正规矩阵的特征值和伪谱

**调用方式**:

```
计算 20×20 Grcar 矩阵的特征值
Grcar 矩阵定义: 对角线=1, 上对角线前k个=1, 下对角线=-1
k = 3

使用 /eigenvalue-computation skill
分析特征值分布和伪谱性质
```

**预期输出**:

- skill 构造 Grcar 矩阵
- 计算特征值（可能在复平面）
- 讨论非正规性
- 可能可视化伪谱

---

## Example 7: 条件数和特征值敏感性

**问题**: 分析特征值对矩阵扰动的敏感性

**调用方式**:

```
分析矩阵特征值的敏感性
A = [[1, 100], [0, 2]]

使用 /eigenvalue-computation skill
1. 计算特征值和特征向量
2. 分析特征值条件数
3. 讨论小扰动的影响
```

**预期输出**:

- skill 计算特征值和特征向量
- 分析特征向量条件数
- 讨论敏感性
- 可能演示扰动实验

---

## Example 8: Rayleigh 商迭代

**问题**: 使用 Rayleigh 商迭代求特定特征值

**调用方式**:

```
使用 Rayleigh 商迭代求矩阵的特征值
A = [[4, 1, 0], [1, 4, 1], [0, 1, 4]]
初始向量: [1, 0, 0]

使用 /eigenvalue-computation skill
方法: Rayleigh 商迭代
```

**预期输出**:

- skill 执行 Rayleigh 商迭代
- 报告收敛历史
- 返回收敛到的特征值
- 与幂法比较

---

## Example 9: 完整的谱分析

**问题**: 对矩阵进行完整的谱分析

**调用方式**:

```
对矩阵 A 进行完整的谱分析
A = [[2, 1, 0], [1, 2, 1], [0, 1, 2]]

使用 /eigenvalue-computation skill
提供完整报告:
- 全部特征值和特征向量
- 谱半径
- 特征值分布
- 特征向量正交性验证
- 条件数分析
```

**预期输出**:

- skill 生成结构化报告
  - 特征值列表（排序）
  - 特征向量矩阵
  - 谱半径 ρ(A)
  - 条件数 κ(A)
  - 特征值分布统计
  - 验证结果

---

## Example 10: Jordan 标准型相关

**问题**: 分析接近 Jordan 结构的矩阵

**调用方式**:

```
分析以下矩阵的特征结构
A = [[2, 1e-6, 0], [0, 2, 1e-6], [0, 0, 2]]

使用 /eigenvalue-computation skill
注意: 这是一个接近 Jordan 块的结构
分析特征向量是否退化
```

**预期输出**:

- skill 计算特征值（三重特征值 2）
- 分析特征向量
- 讨论接近 Jordan 结构的数值问题
- 可能使用广义特征向量

---

## 通用调用模板

**基础特征值**:

```
计算矩阵 A 的特征值和特征向量
A = [...]

使用 /eigenvalue-computation skill
```

**仅特征值**:

```
计算矩阵 A 的特征值（不需要特征向量）
A = [...]

使用 /eigenvalue-computation skill
```

**前 k 个**:

```
计算矩阵 A 的前 k 个最大特征值
A = [...]
k = 5

使用 /eigenvalue-computation skill
```

**幂法**:

```
使用幂法求矩阵 A 的最大特征值
A = [...]

使用 /eigenvalue-computation skill
方法: 幂法
容差: 1e-8
```

**稀疏矩阵**:

```
计算大型稀疏矩阵的部分特征值
A 是 [描述稀疏结构]

使用 /eigenvalue-computation skill
使用稀疏方法
```

**完整谱分析**:

```
对矩阵 A 进行完整谱分析
A = [...]

使用 /eigenvalue-computation skill
提供完整诊断报告
```

---

## 方法选择指南

| 矩阵类型 | 需求 | 推荐方法 |
|---------|------|---------|
| 对称/Hermitian | 全部特征值 | `eigh` |
| 非对称 | 全部特征值 | `eig` |
| 稀疏 | 前 k 个特征值 | `eigs` |
| 任意 | 仅最大特征值 | 幂法 |
| 任意 | 特定范围特征值 | 移位-逆方法 |
| 大型 | 部分谱 | Arnoldi/Lanczos |

使用 `/choose_decomposition` skill 可帮助选择合适的方法。
