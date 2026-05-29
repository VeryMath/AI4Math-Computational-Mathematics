# GMRES - Skill Usage Examples

> **Note**: This file demonstrates how to use the `/generalized-minimal-residual` skill. For low-level implementation details using numpy/scipy, see [implementation.md](./implementation.md).

---

## Skill 概述

`/generalized-minimal-residual` (GMRES) 用于求解**非对称**线性系统的迭代方法，是 CG 方法在非对称情况下的推广。

**适用场景**:
- 非对称线性系统 Ax = b
- 不能保证正定的矩阵
- 需要重启策略的大系统

**不适用场景**:
- 对称正定矩阵 → 优先使用 CG（更高效）

---

## Example 1: 基础非对称系统

**问题**: 求解非对称线性方程组

$$
A = \begin{bmatrix}
3 & 2 \\
1 & 4
\end{bmatrix}, \quad
b = \begin{bmatrix}
1 \\
2
\end{bmatrix}
$$

**调用方式**:

```
求解线性方程组 Ax = b
A = [[3, 2], [1, 4]]
b = [1, 2]

使用 /generalized-minimal-residual skill
设置容差 tol = 1e-10
```

**预期输出**:

- skill 识别为非对称矩阵，使用 GMRES
- 迭代求解返回解向量 x
- 报告迭代次数和残差 ||Ax - b||
- 与直接解法验证

---

## Example 2: 重启 GMRES

**问题**: 比较不同重启参数的效果

**调用方式**:

```
求解线性方程组 Ax = b
A = [[5, 2, 1], [3, 8, 2], [1, 1, 4]]
b = [10, 20, 15]

使用 /generalized-minimal-residual skill
分别测试重启参数: restart=5, restart=10, restart=20
比较收敛行为
```

**预期输出**:

- skill 执行不同重启参数的 GMRES
- 比较各方法的迭代次数
- 讨论重启参数的选择
- 展示内存使用与收敛速度的权衡

---

## Example 3: Grcar 矩阵（非正规矩阵）

**问题**: 使用 GMRES 求解非正规系统

**调用方式**:

```
求解线性方程组 Ax = b
A 是 30×30 Grcar 矩阵
Grcar 定义: 对角线=1, 上对角线前k个=1, 下对角线=-1
k=3
b 是随机向量

使用 /generalized-minimal-residual skill
分析收敛行为
```

**预期输出**:

- skill 构造 Grcar 矩阵
- 执行 GMRES
- 讨论非正规性对收敛的影响
- 可能建议预处理策略

---

## Example 4: 对流-扩散问题

**问题**: 求解对流扩散离散化系统

**调用方式**:

```
求解对流扩散方程离散化系统
网格: 50×50
Pe 数（Peclet）: 10（强对流）
边界条件: Dirichlet

使用 /generalized-minimal-residual skill
注意: 离散化矩阵是非对称的
```

**预期输出**:

- skill 构造对流扩散离散矩阵
- 执行 GMRES
- 报告迭代历史
- 讨论对流项对收敛的影响

---

## Example 5: 预处理 GMRES

**问题**: 使用预处理加速 GMRES 收敛

**调用方式**:

```
求解线性方程组 Ax = b
A 是条件数约为 10^6 的非对称矩阵
b 是随机向量

使用 /generalized-minimal-residual skill
分别尝试:
1. 无预处理 GMRES
2. 对角预处理 GMRES
3. ILU 预处理 GMRES（如可用）

比较收敛速度
```

**预期输出**:

- skill 构造测试矩阵
- 执行不同预处理的 GMRES
- 比较迭代次数和计算时间
- 讨论预处理的效果

---

## Example 6: 比较 GMRES 和 CG

**问题**: 在"对称但非正定"情况下比较 GMRES 和 CG

**调用方式**:

```
求解线性方程组 Ax = b
A = [[1, 2], [2, 1]]（对称但非正定）
b = [3, 4]

使用 /generalized-minimal-residual skill
说明: 如果 A 不是正定的，CG 会失败或收敛很慢
```

**预期输出**:

- skill 检测矩阵对称但非正定
- 说明 CG 的局限性
- 使用 GMRES 求解
- 讨论何时使用 GMRES vs CG

---

## Example 7: 大规模稀疏系统

**问题**: GMRES 在大规模稀疏系统上的性能

**调用方式**:

```
求解大规模稀疏线性系统
A 是 1000×1000 随机稀疏矩阵（非对称）
稀疏度: 95%
b 是随机向量

使用 /generalized-minimal-residual skill
使用稀疏矩阵格式
报告迭代次数和计算时间
```

**预期输出**:

- skill 使用稀疏矩阵存储
- 执行 GMRES
- 报告性能指标
- 讨论稀疏矩阵的优势

---

## Example 8: 收敛停滞诊断

**问题**: 诊断 GMRES 收敛停滞的原因

**调用方式**:

```
以下系统 GMRES 收敛缓慢，请诊断原因
A = [描述一个难解的非对称系统]
b = [...]

使用 /generalized-minimal-residual skill
提供详细诊断:
- 谱分析
- 条件数
- 伪谱分析（如可能）
- 建议改进策略
```

**预期输出**:

- skill 分析矩阵性质
- 识别收敛缓慢原因
- 建议预处理或参数调整
- 可能演示改进效果

---

## Example 9: 与直接法比较

**问题**: 比较迭代法和直接法

**调用方式**:

```
求解线性方程组 Ax = b
A = [[4, 1, 0], [2, 5, 1], [0, 1, 6]]
b = [1, 2, 3]

使用 /generalized-minimal-residual skill
同时尝试:
1. GMRES
2. LU 分解（直接法）

比较:
- 计算时间
- 内存使用
- 解的精度
```

**预期输出**:

- skill 执行两种方法
- 比较各项指标
- 讨论何时用迭代法 vs 直接法

---

## Example 10: 完整的诊断报告

**问题**: 获取 GMRES 求解的完整诊断

**调用方式**:

```
求解线性方程组 Ax = b
A = [[3, 2, 1], [1, 4, 2], [2, 1, 5]]
b = [10, 15, 20]

使用 /generalized-minimal-residual skill
提供完整诊断报告:
- 矩阵特性检查
- 迭代历史
- 收敛分析
- 解的验证
- 与其他方法的比较
```

**预期输出**:

- skill 生成结构化报告
  - 矩阵形状、对称性检查
  - 条件数估计
  - GMRES 参数（重启、容差）
  - 迭代次数、收敛历史
  - 最终解和残差
  - 与直接解法的比较
  - 方法推荐

---

## 通用调用模板

**基础求解**:

```
求解 Ax = b
A = [...]
b = [...]

使用 /generalized-minimal-residual skill
```

**指定重启参数**:

```
求解 Ax = b
A = [...]
b = [...]

使用 /generalized-minimal-residual skill
设置重启参数 restart = 20
容差 tol = 1e-8
```

**预处理**:

```
求解 Ax = b
A = [...]
b = [...]

使用 /generalized-minimal-residual skill
使用对角预处理
```

**稀疏矩阵**:

```
求解稀疏线性系统
A 是 [描述稀疏结构]
b = [...]

使用 /generalized-minimal-residual skill
使用稀疏格式
```

**完整诊断**:

```
求解 Ax = b
A = [...]
b = [...]

使用 /generalized-minimal-residual skill
提供完整诊断报告
```

---

## GMRES 与 CG 比较

| 特性 | CG | GMRES |
|------|-----|-------|
| 适用矩阵 | SPD | 一般方阵 |
| 收敛保证 | 是 | 否 |
| 内存使用 | O(n) | O(n·restart) |
| 重启 | 不需要 | 常用 |
| 预处理 | 简单 | 复杂 |
| 效率 | 高（SPD） | 较低 |

使用 `/choose_decomposition` skill 可自动选择合适的方法：
- SPD → CG
- 非对称 → GMRES
