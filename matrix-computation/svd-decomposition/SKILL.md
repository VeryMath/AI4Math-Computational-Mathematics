---
name: svd-decomposition
description: "Use when you need singular value decomposition, rectangular matrices, low-rank approximation, pseudoinverse, PCA preparation, matrix compression, least squares, or rank analysis in Python."
---

# SVD Decomposition Skill

## 适用场景
- 对任意矩阵做奇异值分解，写成 $A = U \Sigma V^T$
- 做低秩近似、压缩、降噪、主成分分析前处理
- 求伪逆、最小二乘解、数值秩、条件数分析
- 处理秩不足、病态矩阵或长方形矩阵

## Quick Start
- [ ] 确认矩阵形状；SVD 对方阵和长方形矩阵都适用
- [ ] 判断任务是 full SVD、rank-$k$ 近似、伪逆还是最小二乘
- [ ] 选择 `numpy.linalg.svd`，必要时再做截断
- [ ] 若截断，说明 $k$、保留能量和重构误差
- [ ] 若做求解，优先说明伪逆或最小二乘方案
- [ ] 对小奇异值或病态矩阵，提示数值稳定性风险

## Selection Rules

- SVD 是通用的后备方案，适用于任意形状矩阵（方阵或长方形）。
- 当矩阵为长方形、秩不足或 condition number 非常大（病态）时，优先使用 SVD。
- 当需要伪逆、最小二乘或秩/能量分析时，SVD 提供最稳健的结果。
- 若矩阵很大且只需要低秩近似，可选择截断 SVD 以节省计算开销。

## 执行流程
### 路径 A：用户已给矩阵和具体目标
1. 先确认输入矩阵的形状和目标类型。
2. 计算 $U, \Sigma, V^T$，默认使用紧凑形式更方便解释。
3. 如果用户只要低秩近似或压缩，就截断到前 $k$ 个奇异值。
4. 如果用户要解线性问题，说明使用伪逆或最小二乘。
5. 报告重构误差、残差、能量保留比例或数值秩。

### 路径 B：用户只说"做 SVD"但没有明确目标
1. 先澄清是完整分解、秩分析、压缩，还是求解问题。
2. 若是教学场景，可以顺带解释奇异值排序和几何意义。
3. 若矩阵太大或稀疏，可以说明是否需要更高效的近似方法。

## 输出模板
```markdown
### 问题重述
...

### 分解结果
- U: ...
- singular values: ...
- V^T: ...

### 截断 / 秩信息
- k: ...
- 保留能量比例: ...

### 验证
- reconstruction error 或 residual: ...

### 结果解释
...
```

## 歧义与澄清
- 需要 full SVD 还是 compact SVD?
- 只要分解，还是要 rank-$k$ 近似、伪逆或最小二乘?
- 截断秩 $k$ 是用户指定，还是需要按阈值自动选取?
- 是否需要解释能量保留比例或条件数?
- 若用户把 SVD 当成"只适合方阵"的方法，要明确纠正：SVD 适用于任意矩阵。

## 范围与边界
- 本 skill 适用于任意形状矩阵。
- 对低秩、病态、秩不足问题，SVD 往往比 LU 和 Cholesky 更合适。
- 若用户需要的是严格的线性方程精确解，SVD 不是唯一工具，但通常是更稳健的分析手段。

## Python 技术细节
- 生产场景优先使用 `numpy.linalg.svd`
- 需要稳健伪逆时可用 `numpy.linalg.pinv`
- 需要最小二乘时可以结合 `numpy.linalg.lstsq` 或 SVD 截断
- 若用户关心压缩效果，要报告保留能量比例和重构误差
- 独立脚本见 [scripts/solve_svd.py](./scripts/solve_svd.py)

## 示例
需要示例时请阅读 [references/examples.md](./references/examples.md)。

## 病态处理工作流

- SVD 通常是处理病态矩阵和秩不足问题的首选稳健工具，但仍建议遵循工作流：
  1. 先估计条件数并报告；
  2. 对需要高效近似的大型矩阵先尝试截断 / 随机 SVD；
  3. 若目标是线性求解且矩阵病态，优先使用截断 SVD 或在伪逆中设置合适的 `rcond`；
  4. 记录每一步并输出 `report`（包含 tried、final_method、residual_norm、retained_energy 等）。
