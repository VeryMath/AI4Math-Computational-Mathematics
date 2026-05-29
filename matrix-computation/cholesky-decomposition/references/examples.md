# Cholesky Decomposition - Skill Usage Examples

> **Note**: This file demonstrates how to use the `/cholesky-decomposition` skill. For low-level implementation details using numpy/scipy, see [implementation.md](./implementation.md).

---

## Example 1: 基础 Cholesky 分解

**问题**: 对以下对称正定矩阵进行 Cholesky 分解

$$
A = \begin{bmatrix}
25 & 15 & -5 \\
15 & 18 & 0 \\
-5 & 0 & 11
\end{bmatrix}
$$

**调用方式**:

```
对矩阵 A = [[25, 15, -5], [15, 18, 0], [-5, 0, 11]] 进行 Cholesky 分解

使用 /cholesky-decomposition skill
```

**预期输出**:

- skill 会自动检查矩阵的对称性和正定性
- 返回下三角矩阵 L，满足 A = L @ L.T
- 显示重构误差 ||A - LL^T||

---

## Example 2: 求解 SPD 线性方程组

**问题**: 求解线性方程组 Ax = b，其中

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
求解线性方程组 Ax = b，其中
A = [[4, 1], [1, 3]]
b = [1, 2]

使用 /cholesky-decomposition skill 进行求解
```

**预期输出**:

- skill 会识别这是一个 SPD 系统
- 使用 Cholesky 分解 + 前代/回代求解
- 返回解向量 x 和残差 ||Ax - b||

---

## Example 3: 验证矩阵是否为 SPD

**问题**: 判断以下矩阵是否是对称正定矩阵

$$
A_1 = \begin{bmatrix}
4 & 1 \\
1 & 3
\end{bmatrix}, \quad
A_2 = \begin{bmatrix}
1 & 2 \\
2 & 1
\end{bmatrix}
$$

**调用方式**:

```
判断矩阵 A1 = [[4, 1], [1, 3]] 和 A2 = [[1, 2], [2, 1]] 是否为对称正定矩阵

使用 /cholesky-decomposition skill 进行检查
```

**预期输出**:

- skill 会检查对称性和正定性
- 对于 A1，确认为 SPD，可以进行 Cholesky 分解
- 对于 A2，说明为何不是 SPD（可能不是正定）

---

## Example 4: 病态 Hilbert 矩阵

**问题**: 对 8×8 Hilbert 矩阵进行 Cholesky 分解

$$
H_{ij} = \frac{1}{i + j - 1}, \quad i,j = 1,\ldots,8
$$

**调用方式**:

```
对 8×8 Hilbert 矩阵进行 Cholesky 分解
Hilbert 矩阵定义: H[i,j] = 1/(i + j + 1)

使用 /cholesky-decomposition skill
注意: 这是一个高度病态的矩阵
```

**预期输出**:

- skill 会报告条件数（condition number）
- 尝试进行 Cholesky 分解
- 讨论数值稳定性问题
- 可能建议使用正则化或其他方法

---

## Example 5: 带 Tikhonov 正则化的病态矩阵

**问题**: 求解病态系统 Ax = b，其中 A 是 12×12 Hilbert 矩阵

**调用方式**:

```
求解线性方程组 Ax = b
A 是 12×12 Hilbert 矩阵（定义: H[i,j] = 1/(i+j+1)）
b 是全1向量

由于矩阵高度病态，使用 Tikhonov 正则化
使用 /cholesky-decomposition skill，设置正则化参数 alpha = 1e-8
```

**预期输出**:

- skill 会识别矩阵高度病态
- 使用正则化后的矩阵 A_reg = A + alpha*I
- 报告原始条件数和正则化后的条件数
- 返回正则化解和残差

---

## Example 6: Pascal 矩阵（SPD，整数逆）

**问题**: 对 10×10 Pascal 矩阵进行 Cholesky 分解

Pascal 矩阵定义: P[i,j] = C(i+j, i) = P[i-1,j] + P[i,j-1]

**调用方式**:

```
对 10×10 Pascal 矩阵进行 Cholesky 分解
Pascal 矩阵定义: P[i,j] = P[i-1,j] + P[i,j-1]，边界为1

使用 /cholesky-decomposition skill
```

**预期输出**:

- skill 会构造 Pascal 矩阵
- 验证其 SPD 性质
- 进行 Cholesky 分解
- 可能展示其逆矩阵的整数性质

---

## Example 7: Poisson 1D 离散化矩阵

**问题**: 求解 Poisson 方程离散化系统

对于 n = 50，三对角矩阵:
- 对角线: 2
- 次对角线: -1

**调用方式**:

```
求解 Poisson 1D 问题
矩阵 A 是 50×50 三对角矩阵: 对角线=2, 次对角线=-1
b 是全1向量

使用 /cholesky-decomposition skill 求解 Ax = b
```

**预期输出**:

- skill 会识别这是一个稀疏 SPD 矩阵
- 报告条件数（与 n^2 成正比）
- 使用 Cholesky 求解
- 返回解和残差

---

## Example 8: 反例测试 - 非正定矩阵

**问题**: 验证 Wilkinson 矩阵不是正定矩阵

**调用方式**:

```
验证以下 Wilkinson 矩阵是否可以进行 Cholesky 分解:
Wilkinson 矩阵 W(n) 定义:
  - W[i,i] = |i - n/2| + 1
  - W[i,i-1] = W[i-1,i] = 1
n = 20

使用 /cholesky-decomposition skill 进行检查
```

**预期输出**:

- skill 会检查对称性（满足）
- 尝试 Cholesky 分解（会失败）
- 解释为何失败（矩阵不是正定的）
- 可能建议使用 LU 分解或 SVD

---

## Example 9: Gram 矩阵

**问题**: 从数据矩阵构造 Gram 矩阵并进行 Cholesky 分解

数据矩阵 X: 10×3，从标准正态分布随机采样

**调用方式**:

```
从随机数据构造 Gram 矩阵
数据矩阵 X: 10×3，从 N(0,1) 采样
Gram 矩阵 A = X^T @ X

使用 /cholesky-decomposition skill 对 A 进行分解
```

**预期输出**:

- skill 会构造 Gram 矩阵
- 验证其半正定性
- 检查特征值是否全为正
- 如果是 SPD，进行 Cholesky 分解

---

## Example 10: 完整的病态处理流程

**问题**: 演示完整的鲁棒 Cholesky 求解流程

**调用方式**:

```
演示鲁棒的 Cholesky 求解流程:
1. 对给定矩阵检查条件数
2. 如果条件数 < 1e12，直接 Cholesky
3. 如果条件数很大，使用 Tikhonov 正则化
4. 如果正则化仍失败，回退到 SVD

测试矩阵: 12×12 Hilbert 矩阵

使用 /cholesky-decomposition skill，展示完整的诊断和求解过程
```

**预期输出**:

- skill 会生成详细的诊断报告
- 报告包含:
  - 原始条件数
  - 尝试的方法
  - 使用的正则化参数（如适用）
  - 最终解和残差
- 清晰解释每一步的决策逻辑

---

## 通用调用模板

**基础分解**:

```
对矩阵 A = [...] 进行 Cholesky 分解
使用 /cholesky-decomposition skill
```

**求解方程组**:

```
求解 Ax = b，其中
A = [...]
b = [...]

使用 /cholesky-decomposition skill
```

**检查 SPD**:

```
检查矩阵 A = [...] 是否为对称正定矩阵
使用 /cholesky-decomposition skill 进行验证
```

**病态处理**:

```
对病态矩阵 A = [...] 进行鲁棒求解
b = [...]

使用 /cholesky-decomposition skill
说明: 如果直接 Cholesky 失败，请使用正则化或 SVD 回退
```
