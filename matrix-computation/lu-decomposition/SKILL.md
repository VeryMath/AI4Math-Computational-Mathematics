---
name: lu-decomposition
description: "Use when you need LU decomposition, partial pivoting, linear solves, determinant estimation, inverse-related workflows, or Gaussian elimination style matrix factorization in Python."
---
# LU Decomposition Skill

## 适用场景

- 对方阵做 $A = P L U$ 分解（SciPy 约定）
- 求解 $A x = b$，尤其是同一系数矩阵的多右端项
- 估计行列式、解释置换矩阵、辅助求逆
- 讲解高斯消元、部分主元和数值稳定性

## Quick Start

- [ ] 确认矩阵是方阵
- [ ] 判断是否需要部分主元，默认启用
- [ ] 区分任务是分解、求解、行列式还是逆
- [ ] 选择 `scipy.linalg.lu` / `lu_factor` / `lu_solve`
- [ ] 验证 $A \approx P L U$ 或残差
- [ ] 若矩阵奇异或病态，明确说明限制

## Selection Rules

- 适用场景：方阵且需要高效求解或重复求解（多右端项）、行列式或逆的估计。
- 优先级：当矩阵为方阵且 condition number 合理（例如 cond < 1e12），LU 为默认首选。
- 不适用或次选：长方形矩阵（考虑 QR 或 SVD）、病态矩阵（推荐 SVD）。
- 当 LU 因奇异或数值不稳定失败时，应切换到 SVD 并报告原因。

## 执行流程

### 路径 A：用户已给矩阵或线性方程组

1. 核对维度：$A$ 是否方阵，$b$ 的长度是否匹配。
2. 默认启用部分主元，避免零主元和不稳定。
3. 计算 $P, L, U$，或直接做分解后前代回代。
4. 报告重构误差、残差或行列式信息。

### 路径 B：需求只给了目标，没有给矩阵

1. 先澄清 $A$ 和 $b$，不要凭空补矩阵。
2. 若问题其实更适合 QR 或 SVD，主动说明并建议替代方案。
3. 如果用户在问教学过程，可以给出 Doolittle + 部分主元的步骤框架。

## 输出模板

```markdown
### 问题重述
...

### 矩阵检查
- shape: ...
- 是否方阵: ...
- 是否需要部分主元: ...

### 分解结果
- P: ...
- L: ...
- U: ...

### 验证
- reconstruction error ||A - PLU||: ...

### 求解结果（如适用）
- x: ...

### 结果解释
...
```

## 歧义与澄清

- 需要 $A = P L U$（SciPy 约定）还是 $P A = L U$（教科书约定）？本 skill 默认使用 SciPy 约定 $A = P L U$。
- 只是分解，还是还要解方程、求行列式或求逆？
- 矩阵是否奇异或近似奇异？
- 是否允许部分主元？默认允许且推荐。
- 若矩阵不是方阵，通常应考虑 QR 或 SVD，而不是强行套 LU。

## 范围与边界

- 本 skill 主要处理方阵的 LU 分解与基于 LU 的求解。
- 对长方形矩阵，LU 不是首选工具。
- 当矩阵秩不足或病态严重时，不要假装分解结果可靠，应明确提示。

## Python 技术细节

- 生产场景优先使用 `scipy.linalg.lu`、`scipy.linalg.lu_factor`、`scipy.linalg.lu_solve`
- `scipy.linalg.lu(A)` 返回 $P, L, U$ 满足 $A = P L U$
- 教学场景可写 Doolittle，并加入部分主元选择
- 行列式可由 $U$ 的对角元和置换符号得到，但前提是矩阵可逆
- 独立脚本见 [scripts/solve_lu.py](./scripts/solve_lu.py)

## 示例

需要示例时请阅读 [references/examples.md](./references/examples.md)。

## 病态处理工作流

- 触发条件：LU 分解过程中出现零主元、奇异矩阵、或条件数过大（病态）。
- 补救动作（按序）：
  1. 启用或确认部分主元（pivoting）并重试；
  2. 若数值仍不稳定，尝试矩阵均衡化（row/col scaling）；
  3. 若仍失败，尝试 Tikhonov 正则化或回退到 SVD 并说明原因；
  4. 为每一步生成 `report`（包含 cond_estimate、tried、final_method、residual_norm 等）。
