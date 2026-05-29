# Choose Decomposition - Skill Usage Examples

> **Note**: This file demonstrates how to use the `/choose_decomposition` skill to automatically select the appropriate matrix decomposition method.

---

## Skill 概述

`/choose_decomposition` 是一个智能选择器，根据矩阵特性自动推荐最合适的分解方法（Cholesky、LU 或 SVD）。

**决策准则**:
- 非方阵 → SVD（最小二乘/伪逆）
- 方阵 + SPD + 条件数合理 → Cholesky
- 方阵 + 非 SPD + 条件数合理 → LU
- 病态矩阵 → SVD 或带正则化的回退方案

---

## Example 1: SPD 矩阵 - 推荐 Cholesky

**问题**: 求解线性方程组，推荐合适的分解方法

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

使用 /choose_decomposition skill 推荐合适的分解方法
```

**预期输出**:

- skill 分析矩阵: 方阵、对称、正定
- 推荐方法: **Cholesky 分解**
- 原因: 效率高、数值稳定
- 可选: 直接调用 `/cholesky-decomposition` skill 执行求解

---

## Example 2: 非 SPD 方阵 - 推荐 LU

**问题**: 求解非对称线性方程组

$$
A = \begin{bmatrix}
2 & 1 & 3 \\
4 & 5 & 6 \\
7 & 8 & 9
\end{bmatrix}, \quad
b = \begin{bmatrix}
1 \\
2 \\
3
\end{bmatrix}
$$

**调用方式**:

```
求解线性方程组 Ax = b
A = [[2, 1, 3], [4, 5, 6], [7, 8, 9]]
b = [1, 2, 3]

使用 /choose_decomposition skill 推荐合适的分解方法
```

**预期输出**:

- skill 分析矩阵: 方阵、非对称
- 推荐方法: **LU 分解**
- 原因: 通用方阵求解器
- 可选: 直接调用 `/lu-decomposition` skill 执行求解

---

## Example 3: 非方阵 - 推荐 SVD

**问题**: 求解过定系统（最小二乘）

$$
A = \begin{bmatrix}
1 & 1 \\
1 & 2 \\
1 & 3 \\
1 & 4
\end{bmatrix}, \quad
b = \begin{bmatrix}
6 \\
9 \\
20 \\
25
\end{bmatrix}
$$

**调用方式**:

```
求解过定线性方程组 Ax = b（最小二乘问题）
A = [[1, 1], [1, 2], [1, 3], [1, 4]]
b = [6, 9, 20, 25]

使用 /choose_decomposition skill 推荐合适的分解方法
```

**预期输出**:

- skill 分析矩阵: 非方阵（4×2）
- 推荐方法: **SVD 分解**
- 原因: 适合非方阵/秩亏情况
- 可选: 直接调用 `/svd-decomposition` skill 执行求解

---

## Example 4: 病态矩阵 - 推荐 SVD

**问题**: 求解病态系统

$$
A = \begin{bmatrix}
1 & 1 & 1 \\
1 & 1 & 1 \\
1 & 1 & 1
\end{bmatrix}, \quad
b = \begin{bmatrix}
3 \\
3 \\
3
\end{bmatrix}
$$

**调用方式**:

```
求解线性方程组 Ax = b
A = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
b = [3, 3, 3]

使用 /choose_decomposition skill 推荐合适的分解方法
注意: 矩阵可能是秩亏的
```

**预期输出**:

- skill 分析矩阵: 方阵、秩亏（rank=1）
- 推荐方法: **SVD 分解**
- 原因: Cholesky/LU 会失败，SVD 可处理秩亏情况
- 可选: 直接调用 `/svd-decomposition` skill 执行求解

---

## Example 5: Hilbert 矩阵（高条件数）- 推荐 SVD

**问题**: 对高条件数的 Hilbert 矩阵选择合适方法

**调用方式**:

```
求解线性方程组 Ax = b
A 是 8×8 Hilbert 矩阵: H[i,j] = 1/(i + j + 1)
b 是全1向量

使用 /choose_decomposition skill 推荐合适的分解方法
```

**预期输出**:

- skill 分析矩阵: SPD 但条件数极高（~10^10）
- 推荐方法: **SVD 分解** 或 **带正则化的 Cholesky**
- 原因: 直接 Cholesky 数值不稳定
- 说明: 可能建议使用 Tikhonov 正则化

---

## Example 6: 欠定系统 - 推荐 SVD

**问题**: 求解欠定系统

$$
A = \begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6
\end{bmatrix}, \quad
b = \begin{bmatrix}
7 \\
8
\end{bmatrix}
$$

**调用方式**:

```
求解欠定线性方程组 Ax = b（有无穷多解）
A = [[1, 2, 3], [4, 5, 6]]
b = [7, 8]

使用 /choose_decomposition skill 推荐合适的分解方法
```

**预期输出**:

- skill 分析矩阵: 非方阵（2×3），欠定
- 推荐方法: **SVD 分解**（求最小范数解）
- 原因: 可给出最小范数解
- 可选: 直接调用 `/svd-decomposition` skill 执行求解

---

## Example 7: 批量矩阵分析

**问题**: 分析多个矩阵，为每个推荐方法

**调用方式**:

```
为以下矩阵分别推荐最合适的分解方法:

1. A1 = [[4, 1], [1, 3]] (SPD)
2. A2 = [[2, 1], [4, 3]] (非对称方阵)
3. A3 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]] (秩亏)
4. A4 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]] (近似奇异)

使用 /choose_decomposition skill
```

**预期输出**:

- skill 会为每个矩阵生成独立的分析报告
- 报告包含:
  - 矩阵特性（形状、对称性、SPD、条件数、数值秩）
  - 推荐方法
  - 推荐理由
  - 注意事项（如有）

---

## Example 8: 集成工作流 - 选择并执行

**问题**: 自动选择方法并执行求解

**调用方式**:

```
对于以下问题，请自动选择最合适的分解方法并执行求解:

Ax = b，其中
A = [[4, 1, 0], [1, 4, 1], [0, 1, 4]]
b = [1, 2, 3]

使用 /choose_decomposition skill
然后调用推荐的 skill 完成求解
```

**预期输出**:

- `/choose_decomposition` 推荐方法（如 Cholesky）
- 自动调用 `/cholesky-decomposition` skill
- 返回完整解和诊断报告

---

## 通用调用模板

**基础推荐**:

```
对矩阵 A = [...]，推荐最合适的分解方法
使用 /choose_decomposition skill
```

**求解 + 推荐**:

```
求解 Ax = b
A = [...]
b = [...]

使用 /choose_decomposition skill 推荐方法
```

**批量分析**:

```
分析以下矩阵并推荐分解方法:
- A1 = [...]
- A2 = [...]
- ...

使用 /choose_decomposition skill
```

**完整工作流**:

```
对于问题 Ax = b:
A = [...]
b = [...]

1. 使用 /choose_decomposition skill 推荐方法
2. 使用推荐的 skill 执行求解
3. 返回完整报告
```

---

## 决策树总结

```
                    ┌─────────────┐
                    │   给定 A    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
              非方阵?│             │
           ┌─────────┘             │
           │ 是                    │ 否
           ▼                       ▼
    ┌──────────────┐      ┌───────▼────────┐
    │   SVD        │      │  检查对称和 SPD  │
    └──────────────┘      └───────┬────────┘
                                   │
                         ┌─────────┴─────────┐
                    SPD? │                   │
                 ┌───────┘                   │
                 │ 是                        │ 否
                 ▼                           ▼
          ┌──────────────┐          ┌──────────────┐
     条件数合理?│Cholesky    │条件数合理?│  LU          │
    ┌───────────┘           │  ┌───────────┘
    │ 是                    │  │ 是
    ▼                       │  ▼
 ┌─────────┐         ┌─────┴──────┐      ┌─────────┐
 │Cholesky │         │   SVD      │      │   LU    │
 └─────────┘         └────────────┘      └─────────┘
```
