# Conjugate Gradient - Skill Usage Examples

> **Note**: This file demonstrates how to use the `/conjugate-gradient` skill. For low-level implementation details using numpy/scipy, see [implementation.md](./implementation.md).

---

## Skill 概述

`/conjugate-gradient` 用于求解**对称正定（SPD）**线性系统的迭代方法，特别适合大型稀疏矩阵。

**适用场景**:
- 对称正定线性系统 Ax = b
- 大规模稀疏矩阵（直接分解内存开销大）
- 二次型最小化问题

**不适用场景**:
- 非对称矩阵 → 使用 GMRES
- 非 SPD 矩阵 → 使用其他迭代法

---

## Example 1: 基础 SPD 系统求解

**问题**: 求解对称正定线性方程组

$$
A = \begin{bmatrix}
4 & 1 \\
1 & 3
\end{bmatrix}, \quad
b = \begin{bmatrix}
1 \\
2
\end{bmatrix}
$$

**调用方式**:

```
求解线性方程组 Ax = b
A = [[4, 1], [1, 3]]
b = [1, 2]

使用 /conjugate-gradient skill
设置容差 tol = 1e-10
```

**预期输出**:

- skill 验证矩阵的 SPD 性质
- 迭代求解并返回解向量 x
- 报告迭代次数和残差 ||Ax - b||
- 可能与直接解法比较验证

---

## Example 2: Hilbert 矩阵（病态 SPD）

**问题**: 使用共轭梯度求解 Hilbert 矩阵系统

**调用方式**:

```
求解线性方程组 Ax = b
A 是 8×8 Hilbert 矩阵: H[i,j] = 1/(i + j + 1)
b 是全1向量

使用 /conjugate-gradient skill
说明: 这是一个高度病态的 SPD 矩阵，观察收敛行为
```

**预期输出**:

- skill 报告条件数
- 进行 CG 迭代
- 展示收敛曲线（残差 vs 迭代次数）
- 讨论病态对收敛性的影响
- 可能建议使用预处理

---

## Example 3: 2D Poisson 问题（稀疏 SPD）

**问题**: 求解 2D Poisson 方程的离散化系统

对于 n×n 网格，离散化后得到稀疏 SPD 矩阵

**调用方式**:

```
求解 2D Poisson 问题
网格大小: 50×50
边界条件: Dirichlet（零边界）
右端项: 全1

使用 /conjugate-gradient skill
注意: 这是稀疏大系统，适合迭代法
```

**预期输出**:

- skill 构造 Poisson 离散化矩阵
- 报告矩阵特性（稀疏度、条件数）
- 进行 CG 迭代
- 报告迭代次数、收敛情况
- 与直接法比较（如适用）

---

## Example 4: 对角预处理 CG

**问题**: 使用对角预处理加速 CG 收敛

**调用方式**:

```
求解线性方程组 Ax = b
A 是 100×100 随机 SPD 矩阵（构造方式: A = X^T @ X + epsilon*I）
b 是随机向量

使用 /conjugate-gradient skill
分别尝试:
1. 无预处理 CG
2. 对角预处理 CG

比较收敛速度
```

**预期输出**:

- skill 构造测试矩阵
- 执行无预处理 CG，记录收敛历史
- 执行对角预处理 CG，记录收敛历史
- 比较两种方法的迭代次数
- 讨论预处理的优劣

---

## Example 5: 收敛容差测试

**问题**: 测试不同容差对 CG 的影响

**调用方式**:

```
求解线性方程组 Ax = b
A = [[4, 1, 0], [1, 4, 1], [0, 1, 4]]
b = [1, 2, 3]

使用 /conjugate-gradient skill
分别测试容差: 1e-4, 1e-6, 1e-8, 1e-10

比较不同容差下的迭代次数和解精度
```

**预期输出**:

- skill 对每个容差运行 CG
- 报告迭代次数 vs 容差的关系
- 展示解精度的变化
- 讨论容差选择的权衡

---

## Example 6: 二次型最小化

**问题**: 使用 CG 最小化二次型

最小化 f(x) = 1/2 x^T A x - b^T x

**调用方式**:

```
最小化二次型 f(x) = 1/2 x^T A x - b^T x
其中 A = [[5, 1], [1, 4]]（SPD）
b = [2, 3]

使用 /conjugate-gradient skill
说明: CG 可以直接用于二次型最小化
```

**预期输出**:

- skill 将问题转化为等价的线性系统
- 求解 Ax = b
- 报告最小值点 x* 和最小值 f(x*)
- 验证梯度为零

---

## Example 7: 反例测试 - 非 SPD 矩阵

**问题**: 验证 CG 对非 SPD 矩阵会失败

**调用方式**:

```
求解线性方程组 Ax = b
A = [[1, 2], [3, 4]]（非对称）
b = [5, 6]

使用 /conjugate-gradient skill
说明: A 不是 SPD，观察会发生什么
```

**预期输出**:

- skill 检测到矩阵非 SPD
- 说明 CG 不适用
- 建议使用 GMRES 或其他方法
- 可能演示失败行为

---

## Example 8: 大规模稀疏系统

**问题**: 测试 CG 在大规模问题上的性能

**调用方式**:

```
求解大规模稀疏线性系统
A 是 1000×1000 Poisson 矩阵（三对角结构）
b 是随机向量

使用 /conjugate-gradient skill
报告:
1. 迭代次数
2. 计算时间
3. 内存使用（如可能）
4. 最终残差
```

**预期输出**:

- skill 构造大规模稀疏矩阵
- 执行 CG 迭代
- 报告性能指标
- 讨论稀疏矩阵的优势

---

## Example 9: 重启动策略

**问题**: 测试重启动 CG 对长迭代的影响

**调用方式**:

```
求解病态线性系统
A 是条件数约为 10^8 的 SPD 矩阵
b 是随机向量

使用 /conjugate-gradient skill
比较:
1. 标准 CG
2. 重启动 CG（每 m 步重启动）

讨论重启动的利弊
```

**预期输出**:

- skill 执行两种 CG 变体
- 比较收敛行为
- 讨论何时重启动有益

---

## Example 10: 完整的诊断报告

**问题**: 获取 CG 求解的完整诊断信息

**调用方式**:

```
求解线性方程组 Ax = b
A = [[4, 1, 0, 0], [1, 4, 1, 0], [0, 1, 4, 1], [0, 0, 1, 4]]
b = [1, 2, 3, 4]

使用 /conjugate-gradient skill
提供完整的诊断报告，包括:
- 矩阵特性检查
- 迭代历史
- 收敛分析
- 解的验证
```

**预期输出**:

- skill 生成结构化报告
  - 矩阵形状、对称性、SPD 检查
  - 条件数估计
  - 迭代次数、收敛容差
  - 每步残差历史
  - 最终解和残差范数
  - 与直接解法的比较

---

## 通用调用模板

**基础求解**:

```
求解 Ax = b
A = [...]
b = [...]

使用 /conjugate-gradient skill
```

**指定容差**:

```
求解 Ax = b
A = [...]
b = [...]

使用 /conjugate-gradient skill
设置容差 tol = 1e-8
最大迭代次数 maxiter = 1000
```

**稀疏矩阵**:

```
求解稀疏线性系统
A 是 [描述稀疏结构，如三对角]
b = [...]

使用 /conjugate-gradient skill
注意利用稀疏性
```

**预处理**:

```
求解 Ax = b
A = [...]
b = [...]

使用 /conjugate-gradient skill
使用对角预处理
```

**诊断报告**:

```
求解 Ax = b
A = [...]
b = [...]

使用 /conjugate-gradient skill
提供完整诊断报告
```

---

## CG 与其他方法的比较

| 方法 | 适用条件 | 优点 | 缺点 |
|------|---------|------|------|
| CG | SPD 矩阵 | 内存少、收敛快 | 仅限 SPD |
| GMRES | 一般方阵 | 通用 | 内存随迭代增长 |
| MINRES | 对称不定 | 对称系统 | 比 CG 慢 |
| Direct (Cholesky/LU) | 一般 | 精确、可靠 | 内存大、慢于大规模 |

使用 `/choose_decomposition` skill 可自动选择合适的方法。
