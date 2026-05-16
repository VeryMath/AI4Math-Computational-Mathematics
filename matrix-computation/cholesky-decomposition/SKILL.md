---
name: cholesky-decomposition
description: "Use when you need Cholesky decomposition, symmetric positive definite matrices, triangular factorization, solving SPD systems, covariance matrices, or fast stable Python implementations."
---

# Cholesky Decomposition Skill

## 适用场景
- 对称正定矩阵的分解，写成 $A = L L^T$ 或 $A = R^T R$
- 解决来自最小二乘、协方差矩阵、核矩阵、物理建模的系统
- 在已知矩阵 SPD 时，比一般 LU 更快、更稳定
- 求解需要重复使用同一个 SPD 系数矩阵的线性方程组

## Quick Start
- [ ] 确认矩阵是方阵
- [ ] 检查是否对称，或至少数值上近似对称
- [ ] 判断是否正定；不满足就不要继续套 Cholesky
- [ ] 选择 `numpy.linalg.cholesky` 或 `scipy.linalg.cho_factor` / `cho_solve`
- [ ] 验证 $A \approx L L^T$ 或 $A \approx R^T R$
- [ ] 若失败，说明是对称性问题还是正定性问题

## Selection Rules

- 适用当且仅当矩阵为方阵且数值上对称且正定（SPD）。
- 优先级：若检测到 SPD -> 立即使用 Cholesky（效率和稳定性最佳）。
- 不适用情况：长方形矩阵、秩不足、半正定或非对称矩阵。
- 当 SPD 检查失败但用户强烈要求 Cholesky 时，应提示并建议 LU/SVD 替代方案。

## 执行流程
### 路径 A：用户已给 SPD 矩阵或线性方程组
1. 核对维度，确认 $A$ 是方阵、$b$ 的长度匹配。
2. 检查数值对称性，并确认不是明显的非对称输入。
3. 判断正定性；一旦不成立，明确说明 Cholesky 不适用。
4. 计算下三角 $L$ 或上三角 $R$，再做前代和回代。
5. 报告重构误差或求解残差。

### 路径 B：用户只有问题描述，没有矩阵
1. 先澄清 $A$ 和 $b$，不要补造矩阵。
2. 若用户描述的是协方差、Gram、核矩阵或最小二乘背景，可以说明为什么可能是 SPD。
3. 如果矩阵不满足 SPD，主动切换到 LU、QR 或 SVD 建议。

## 输出模板
```markdown
### 问题重述
...

### 矩阵检查
- shape: ...
- 是否对称: ...
- 是否正定: ...

### 分解结果
- L 或 R: ...

### 验证
- reconstruction error: ...

### 求解结果（如适用）
- x: ...

### 结果解释
...
```

## 歧义与澄清
- 矩阵是否真正对称，而不是只在数值误差内近似对称?
- 是否真的正定，还是只是半正定或不定?
- 需要下三角 $L$ 还是上三角 $R$?
- 只是因子分解，还是还要解方程?
- 若矩阵不是 SPD，不要偷偷改写问题，应改用 LU、QR 或 SVD。

## 范围与边界
- 本 skill 只适用于对称正定矩阵。
- 半正定或不定矩阵不属于 Cholesky 的直接适用范围。
- 数值上轻微不对称可以说明，但不要掩盖原始数据问题。

## Python 技术细节
- 生产场景优先使用 `numpy.linalg.cholesky` 或 `scipy.linalg.cho_factor` / `cho_solve`
- `numpy.linalg.cholesky` 返回下三角矩阵 $L$
- 若想显式使用上三角形式，可在说明中写成 $A = R^T R$
- 对大规模稀疏 SPD 矩阵，可进一步考虑稀疏求解器
- 独立脚本见 [scripts/solve_cholesky.py](./scripts/solve_cholesky.py)

## 示例
需要示例时请阅读 [references/examples.md](./references/examples.md)。

## 病态处理工作流

- 触发条件：在执行 Cholesky 前后发现以下情形之一：
  - 输入矩阵不是数值上对称或存在明显非对称；
  - Cholesky 因异常（如 `LinAlgError`）失败或重构误差异常大；
  - 条件数（condition number）极大或为无穷（奇异/近似奇异）。
- 补救动作（按序）：
  1. 记录问题并尝试矩阵均衡化（row/col scaling）；
  2. 若仍失败，尝试 Tikhonov 正则化（A + alpha I），记录 alpha 并返回正则化解；
  3. 若上述仍失败或不合适，自动回退到 SVD 伪逆（pseudoinverse）并说明原因；
  4. 在所有步骤中生成 `report`（字段示例：`cond_estimate`、`tried`、`final_method`、`residual_norm`）。
