# Kronecker Product - Skill Usage Examples

> **Note**: This file demonstrates how to use the `/kronecker-product` skill. For low-level implementation details using numpy/scipy, see [implementation.md](./implementation.md).

---

## Skill 概述

`/kronecker-product` 用于计算克罗内克积、验证其代数性质、求解相关方程。

**定义**: 对于 A(m×n) 和 B(p×q)，克罗内克积 A ⊗ B 是 (mp × nq) 矩阵：

$$A \otimes B = \begin{bmatrix} a_{11}B & a_{12}B & \cdots & a_{1n}B \\ a_{21}B & a_{22}B & \cdots & a_{2n}B \\ \vdots & \vdots & \ddots & \vdots \\ a_{m1}B & a_{m2}B & \cdots & a_{mn}B \end{bmatrix}$$

---

## Example 1: 基础克罗内克积

**问题**: 计算两个矩阵的克罗内克积

$$
A = \begin{bmatrix}
1 & 2 \\
3 & 4
\end{bmatrix}, \quad
B = \begin{bmatrix}
0 & 5 \\
6 & 7
\end{bmatrix}
$$

**调用方式**:

```
计算矩阵 A 和 B 的克罗内克积 A ⊗ B
A = [[1, 2], [3, 4]]
B = [[0, 5], [6, 7]]

使用 /kronecker-product skill
```

**预期输出**:

- skill 计算 A ⊗ B
- 显示结果矩阵（4×4）
- 验证维度：(2×2) ⊗ (2×2) → (4×4)

---

## Example 2: 向量的克罗内克积

**问题**: 计算两个向量的克罗内克积

**调用方式**:

```
计算向量 u 和 v 的克罗内克积 u ⊗ v
u = [1, 2]
v = [3, 4, 5]

使用 /kronecker-product skill
```

**预期输出**:

- skill 计算 u ⊗ v
- 返回 6 维向量
- 解释向量积的应用（如张量积空间）

---

## Example 3: 验证结合律

**问题**: 验证克罗内克积的结合律

**调用方式**:

```
验证克罗内克积的结合律：(A ⊗ B) ⊗ C = A ⊗ (B ⊗ C)

A = [[1, 2], [3, 4]]
B = [[0, 1], [1, 0]]
C = [[1, 1], [0, 1]]

使用 /kronecker-product skill
```

**预期输出**:

- skill 计算两边
- 验证相等性
- 报告最大差异

---

## Example 4: 秩的性质

**问题**: 验证 rank(A ⊗ B) = rank(A) × rank(B)

**调用方式**:

```
验证克罗内克积的秩的性质
A = [[1, 0, 0], [0, 1, 0]]  # rank=2
B = [[1, 1], [1, 1]]        # rank=1

使用 /kronecker-product skill
验证 rank(A ⊗ B) = rank(A) × rank(B)
```

**预期输出**:

- skill 计算各矩阵的秩
- 验证性质
- 解释原理

---

## Example 5: 行列式的性质

**问题**: 验证 det(A ⊗ B) = det(A)^n × det(B)^m

**调用方式**:

```
验证克罗内克积的行列式性质
A = [[2, 1], [1, 2]]  # 2×2, det=3
B 是 3×3 对角矩阵 diag(1, 2, 3)  # det=6

使用 /kronecker-product skill
验证 det(A ⊗ B) = det(A)^n × det(B)^m
```

**预期输出**:

- skill 计算各行列式
- 验证公式
- 解释公式来源

---

## Example 6: 克罗内克和

**问题**: 计算克罗内克和 A ⊕ B = A ⊗ I + I ⊗ B

**调用方式**:

```
计算矩阵 A 和 B 的克罗内克和 A ⊕ B
A = [[1, 2], [3, 4]]
B = [[0, 1], [1, 0]]

使用 /kronecker-product skill
注意: A ⊕ B = A ⊗ I + I ⊗ B
```

**预期输出**:

- skill 构造克罗内克和
- 报告结果维度
- 解释特征值关系（λ_i(A) + μ_j(B)）

---

## Example 7: Lyapunov 方程

**问题**: 使用克罗内克积求解 Lyapunov 方程 AX + XA^T = C

**调用方式**:

```
求解 Lyapunov 方程 AX + XA^T = C
A = [[-1, 0.5], [0.5, -2]]
C = [[2, 1], [1, 2]]

使用 /kronecker-product skill
说明: 使用 vec 算子将方程化为线性系统
```

**预期输出**:

- skill 解释求解方法
- 化为线性系统
- 求解 X
- 验证残差 ||AX + XA^T - C||

---

## Example 8: 特殊矩阵 - Hilbert 矩阵

**问题**: 分析 Hilbert 矩阵克罗内克积的条件数

**调用方式**:

```
分析 Hilbert 矩阵的克罗内克积
A = B = Hilbert(4)  # H[i,j] = 1/(i+j+1)

使用 /kronecker-product skill
分析:
1. 条件数的关系
2. 秩的性质
3. 数值稳定性
```

**预期输出**:

- skill 构造 Hilbert 矩阵
- 计算 A ⊗ A
- 分析条件数增长（呈指数）
- 讨论数值问题

---

## Example 9: 特殊矩阵 - Pascal 矩阵

**问题**: 分析 Pascal 矩阵克罗内克积的整数性质

**调用方式**:

```
分析 Pascal 矩阵的克罗内克积
A = Pascal(3)
B = Pascal(4)

使用 /kronecker-product skill
分析行列式和整数性质
```

**预期输出**:

- skill 构造 Pascal 矩阵
- 计算 A ⊗ B
- 验证行列式性质
- 展示整数结构

---

## Example 10: 2D Laplacian（稀疏矩阵）

**问题**: 使用克罗内克积构造 2D Laplacian

**调用方式**:

```
构造 2D Laplacian 矩阵
使用 1D Laplacian 的克罗内克积
L1 = 三对角矩阵 [2, -1, -1]

使用 /kronecker-product skill
构造 L2D = L1 ⊗ I + I ⊗ L1
分析稀疏性和条件数
```

**预期输出**:

- skill 构造 1D Laplacian
- 计算克罗内克和
- 分析结果矩阵
- 讨论稀疏矩阵优势

---

## Example 11: 循环矩阵

**问题**: 分析循环矩阵克罗内克积的特征值

**调用方式**:

```
分析循环矩阵的克罗内克积
C1 = circulant([1, 2, 3])
C2 = circulant([0.5, 1, 0.5, 1])

使用 /kronecker-product skill
验证特征值关系: eig(C1 ⊗ C2) = eig(C1) × eig(C2)
```

**预期输出**:

- skill 构造循环矩阵
- 计算克罗内克积
- 计算特征值
- 验证关系

---

## Example 12: vec 算子性质

**问题**: 验证 vec(AXB) = (B^T ⊗ A) vec(X)

**调用方式**:

```
验证 vec 算子的性质
A = [[1, 0], [0, 2]]
B = [[1, 1], [0, 1]]
X = [[1, 2], [3, 4]]

使用 /kronecker-product skill
验证 vec(AXB) = (B^T ⊗ A) vec(X)
```

**预期输出**:

- skill 计算两边
- 验证相等
- 解释 vec 算子用途

---

## Example 13: 完整性质验证

**问题**: 系统验证克罗内克积的主要性质

**调用方式**:

```
对以下矩阵系统验证克罗内克积的所有主要性质
A = [[1, 2], [3, 4]]
B = [[0, 1], [1, 0]]

使用 /kronecker-product skill
验证:
1. 结合律
2. 转置性质
3. 乘积规则
4. 秩的关系
5. 迹的关系
```

**预期输出**:

- skill 逐一验证各性质
- 生成完整报告
- 解释每项结果

---

## Example 14: 大规模矩阵性能分析

**问题**: 分析大规模矩阵克罗内克积的性能

**调用方式**:

```
分析大规模矩阵克罗内克积的计算性能
测试规模: 20×20 ⊗ 20×20

使用 /kronecker-product skill
报告:
1. 计算时间
2. 内存使用
3. 结果规模
4. 稀疏性建议
```

**预期输出**:

- skill 执行计算
- 报告性能指标
- 讨论内存和计算复杂度
- 建议稀疏格式

---

## Example 15: 量子态应用

**问题**: 使用克罗内克积表示复合量子系统

**调用方式**:

```
使用克罗内克积表示双量子比特系统
单量子比特状态 |ψ⟩ = [α, β]
计算 |ψ⟩ ⊗ |ψ⟩

使用 /kronecker-product skill
解释量子力学中的应用
```

**预期输出**:

- skill 计算克罗内克积
- 解释复合系统
- 讨论纠缠态

---

## 通用调用模板

**基础积**:

```
计算 A ⊗ B
A = [...]
B = [...]

使用 /kronecker-product skill
```

**克罗内克和**:

```
计算 A ⊕ B = A ⊗ I + I ⊗ B
A = [...]
B = [...]

使用 /kronecker-product skill
```

**性质验证**:

```
验证克罗内克积的 [性质名称]
A = [...]
B = [...]

使用 /kronecker-product skill
```

**方程求解**:

```
求解包含克罗内克积的方程
[描述方程]

使用 /kronecker-product skill
```

**完整分析**:

```
对矩阵 A 和 B 进行完整的克罗内克积分析
A = [...]
B = [...]

使用 /kronecker-product skill
提供完整报告
```

---

## 主要性质速查表

| 性质 | 公式 | 条件 |
|------|------|------|
| 结合律 | (A ⊗ B) ⊗ C = A ⊗ (B ⊗ C) | 维度匹配 |
| 转置 | (A ⊗ B)^T = A^T ⊗ B^T | 无 |
| 乘积 | (A ⊗ B)(C ⊗ D) = (AC) ⊗ (BD) | AC, BD 有效 |
| 逆 | (A ⊗ B)^{-1} = A^{-1} ⊗ B^{-1} | A, B 可逆 |
| 秩 | rank(A ⊗ B) = rank(A)·rank(B) | 无 |
| 行列式 | det(A ⊗ B) = det(A)^n·det(B)^m | 方阵 |
| 迹 | tr(A ⊗ B) = tr(A)·tr(B) | 方阵 |
