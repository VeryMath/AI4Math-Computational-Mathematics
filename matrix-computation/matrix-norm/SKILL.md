---
name: matrix-norm
description: "Use when you need to compute matrix norms (Frobenius, spectral, 1-norm, infinity-norm, nuclear norm, p-norm), condition numbers, or matrix distance metrics in Python."
---
# Matrix Norm Skill

## 适用场景
- 计算矩阵的各种范数：Frobenius、谱范数、1-范数、∞-范数、核范数、p-范数
- 估计矩阵条件数和分析数值稳定性
- 计算矩阵间距离（如 $\|A - B\|_F$）
- 评估近似误差或重构质量
- 比较不同范数的数值大小

## Quick Start
- [ ] 确认矩阵形状和目标范数类型
- [ ] 区分是单个矩阵的范数还是矩阵间距离
- [ ] 选择 `numpy.linalg.norm` 的 `ord` 参数
- [ ] 对条件数计算，报告 $\kappa(A) = \|A\| \cdot \|A^{-1}\|$
- [ ] 验证结果是否符合范数的数学性质

## Selection Rules
- **Frobenius范数** ($\|A\|_F$)：默认选择，适用于一般矩阵大小度量、重构误差
- **谱范数** ($\|A\|_2$)：需要最大奇异值、条件数、算子范数时使用
- **1-范数** ($\|A\|_1$)：列和相关的分析、列空间性质
- **∞-范数** ($\|A\|_\infty$)：行和相关的分析、行空间性质
- **核范数** ($\|A\|_*$)：需要奇异值之和、低秩约束问题时使用
- **p-范数**：一般化范数分析

## 执行流程

### 路径 A：用户已给矩阵和范数类型
1. 确认输入矩阵形状和目标范数
2. 选择合适的 `ord` 参数计算
3. 报告结果和可能的数值性质（如与条件数的关系）
4. 若需比较多种范数，给出对比表

### 路径 B：用户未指定范数类型
1. 先询问具体需求：是度量大小、稳定性、还是距离？
2. 根据应用场景推荐合适的范数
3. 提供多种范数的对比参考
4. 解释不同范数的几何/代数意义

## 输出模板

```markdown
### 问题重述
...

### 矩阵检查
- shape: ...
- 条件数 (如适用): ...

### 范数计算结果
- Frobenius norm: ...
- Spectral norm (2-norm): ...
- 1-norm: ...
- ∞-norm: ...
- Nuclear norm: ...

### 范数关系/解释
...

### 矩阵间距离 (如适用)
- \|A - B\|_F: ...
```

## 歧义与澄清
- 需要哪种范数？若未指定，默认给出 Frobenius 和谱范数
- 是计算单个矩阵范数还是矩阵间距离？
- 是否需要条件数？需要指定使用哪个范数计算条件数
- 对于核范数，确认是否确实需要奇异值之和

## 范数数学定义

| 范数 | 符号 | 定义 | ord参数 |
|------|------|------|---------|
| Frobenius | $\|A\|_F$ | $\sqrt{\sum_{i,j} |a_{ij}|^2}$ | `'fro'` |
| Spectral/2-norm | $\|A\|_2$ | $\sigma_{\max}(A)$ | `2` |
| 1-norm | $\|A\|_1$ | $\max_j \sum_i |a_{ij}|$ | `1` |
| ∞-norm | $\|A\|_\infty$ | $\max_i \sum_j |a_{ij}|$ | `np.inf` |
| Nuclear | $\|A\|_*$ | $\sum_i \sigma_i(A)$ | `'nuc'` |
| p-norm | $\|A\|_p$ | $\max_{\|x\|_p=1} \|Ax\|_p$ | `p` |

## 范数关系性质

- $\|A\|_2 \leq \|A\|_F \leq \sqrt{\min(m,n)} \|A\|_2$
- $\|A\|_2 \leq \sqrt{\|A\|_1 \|A\|_\infty}$
- $\|A\|_* \leq \sqrt{\min(m,n)} \|A\|_F$
- $\|A\|_2 = \|A^T\|_2$, $\|A\|_1 = \|A^T\|_\infty$

## Python 技术细节

- 优先使用 `numpy.linalg.norm(A, ord=...)`
- `scipy.linalg.norm` 也提供相同功能
- 条件数用 `numpy.linalg.cond(A, p=...)`
- 独立脚本见 [scripts/solve_norm.py](./scripts/solve_norm.py)

## 示例
需要示例时请阅读 [references/examples.md](./references/examples.md)。
