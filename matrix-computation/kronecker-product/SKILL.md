---
name: kronecker-product
description: "Use when you need to compute Kronecker products, Kronecker sum, verify Kronecker properties, or work with tensor product structures in Python."
---
# Kronecker Product Skill

## 适用场景
- 计算两个矩阵的克罗内克积 A ⊗ B
- 验证克罗内克积的代数性质
- 计算克罗内克和 A ⊕ B = A ⊗ I + I ⊗ B
- 求解涉及克罗内克积的线性方程组
- 分析Kronecker积的秩、行列式、迹等性质
- 张量积计算、量子态表示、系统建模

## Quick Start
- [ ] 确认两个矩阵 A 和 B 的维度
- [ ] 判断任务是克罗内克积、克罗内克和，还是性质验证
- [ ] 选择 `numpy.kron` 或自定义实现
- [ ] 验证结果维度：(mp × nq) 对应 A(m×n), B(p×q)
- [ ] 若需求解，考虑Kronecker积的特殊结构

## Selection Rules
- 克罗内克积适用于任意维度的矩阵
- 当计算结果维度较大时，注意内存开销
- 对于Kronecker积线性方程组，使用向量化求解
- 若需验证性质，系统地测试结合律、转置、逆等

## 执行流程

### 路径 A：用户已给矩阵和具体目标
1. 确认输入矩阵 A(m×n) 和 B(p×q) 的维度
2. 计算克罗内克积 A ⊗ B，输出维度为 (mp × nq)
3. 如需验证性质，逐一测试并报告结果
4. 如需求解，使用 vec 算子化简方程

### 路径 B：用户只说"做Kronecker积"但没有明确目标
1. 先确认是需要计算积、和，还是验证性质
2. 说明Kronecker积的定义和结果维度
3. 若矩阵较大，警告内存和计算复杂度
4. 提供常用性质的参考

## 输出模板

```markdown
### 问题重述
...

### 矩阵检查
- A shape: (m, n)
- B shape: (p, q)
- 预期结果 shape: (mp, nq)

### Kronecker积结果
- A ⊗ B 的维度: ...
- (可选) 显示部分结果矩阵

### 性质验证 (如适用)
- 结合律: ...
- 转置: ...
- 秩: ...

### 结果解释
...
```

## 歧义与澄清
- 需要克罗内克积还是克罗内克和(Kronecker sum)？
- 是否需要验证特定的代数性质？
- 是否涉及求解包含Kronecker积的线性方程？
- 矩阵较大时，是否只需要部分结果或性质分析？

## 范围与边界
- 本skill适用于任意维度矩阵的Kronecker积计算
- 对大型矩阵（如总元素超过1e8），需要警告内存问题
- Kronecker积的结果规模增长快，需谨慎处理

## 数学定义与性质

### 定义
对于 A(m×n) 和 B(p×q)，克罗内克积 A ⊗ B 是 (mp × nq) 矩阵：

$$A \otimes B = \begin{bmatrix} a_{11}B & a_{12}B & \cdots & a_{1n}B \\ a_{21}B & a_{22}B & \cdots & a_{2n}B \\ \vdots & \vdots & \ddots & \vdots \\ a_{m1}B & a_{m2}B & \cdots & a_{mn}B \end{bmatrix}$$

### 主要性质
- **结合律**: (A ⊗ B) ⊗ C = A ⊗ (B ⊗ C)
- **分配律**: A ⊗ (B + C) = A ⊗ B + A ⊗ C
- **转置**: (A ⊗ B)^T = A^T ⊗ B^T
- **乘积**: (A ⊗ B)(C ⊗ D) = (AC) ⊗ (BD) (维度匹配时)
- **逆**: (A ⊗ B)^{-1} = A^{-1} ⊗ B^{-1} (A, B可逆时)
- **秩**: rank(A ⊗ B) = rank(A) · rank(B)
- **行列式**: det(A ⊗ B) = det(A)^n · det(B)^m (A是m×m，B是n×n)
- **迹**: tr(A ⊗ B) = tr(A) · tr(B)

### Kronecker和
$$A \oplus B = A \otimes I_n + I_m \otimes B$$

其中 A 是 m×m，B 是 n×n。

## Python 技术细节
- 生产场景优先使用 `numpy.kron(A, B)`
- Scipy提供 `scipy.linalg.kron`，功能相同
- 大矩阵注意使用稀疏格式 `scipy.sparse.kron`
- 独立脚本见 [scripts/solve_kronecker.py](./scripts/solve_kronecker.py)

## 示例
需要示例时请阅读 [references/examples.md](./references/examples.md)。
