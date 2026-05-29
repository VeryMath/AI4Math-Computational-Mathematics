---
name: choose-decomposition
description: "A lightweight chooser that recommends Cholesky / LU / SVD and optionally runs the chosen solver."
---
# Choose Decomposition Skill

## 用途

- 根据矩阵特性（形状、对称性、SPD 检查、条件数、数值秩）推荐并演示使用 `cholesky`、`lu` 或 `svd` 求解线性系统。

## 接口

- `choose_decomposition(A, b=None) -> dict`：返回决策字典，包含 `method`、`reason`、`info`。
- `demonstrate_choice_and_solve(A, b) -> (x, report, choice)`：执行选择并尝试用对应 skill 求解，返回解、诊断报告与选择。

## 依赖

- 运行示例/脚本需要 `numpy`；若要使用更完善的求解器（SciPy 实现的 cho_factor / lu_factor 等），请安装 `scipy`。
- 推荐使用项目根的 `requirements.txt` 来安装依赖（`pip install -r requirements.txt`）。

## 决策准则（摘要）

- 非方阵 -> `svd`（最稳健的最小二乘/伪逆方案）。
- 方阵且 SPD 且条件数合理 -> `cholesky`。
- 方阵且非 SPD 且条件数合理 -> `lu`。
- 病态矩阵（高 condition number）-> 优先 `svd` 或带正则化的回退方案。

## 示例（使用脚本）

在命令行中运行：

```
python matrix-computation/choose_decomposition/scripts/choose_decomposition.py
```

## 注意

- 本 skill 为自动推荐器，不会在未经用户确认的情况下对矩阵做破坏性修改；若采取正则化或均衡化，会在 `report` 中记录所用参数。
