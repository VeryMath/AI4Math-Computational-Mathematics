---
name: conjugate-gradient
description: "Use when you need conjugate gradient method (CG) to solve symmetric positive-definite linear systems, or to compute quadratic-form minimization in Python."
---

# Conjugate Gradient (CG) Method

## 适用场景
- 求解对称正定线性系统 Ax = b（稠密或稀疏）
- 用作二次目标函数的最小化（共轭方向法）
- 在大型系统中做迭代解（不适合直接求逆）

## Quick Start
- 确认矩阵是否对称并尽量满足正定性
- 若是稀疏大矩阵，建议传入线性算子形式以节省内存
- 选择收敛容忍度 `tol`、最大迭代步数 `maxiter` 和预条件器 `M`（若有）

## Selection Rules
- 当 A 为 SPD（symmetric positive definite）且能以矩阵-向量乘积访问时，优先使用 CG
- 若 A 非对称或非 SPD，请考虑 GMRES 或其他通用迭代法

## 执行流程
1. 验证输入：矩阵/算子维度匹配、rhs 维度正确
2. 若用户提供预条件器 `M`，在算法中使用左预条件
3. 运行 CG，监控残差 ||r|| 并按需要返回诊断信息

## 输出模板
```markdown
### 问题重述
...

### 求解结果
- x: 解向量
- info: dict，包含 iterations, residual_norm, converged

### 验证
- residual ||Ax - b||
```

## 范围与边界
- 本 skill 假定线性算子为 SPD。若不满足，应建议用户切换方法。

## Python 技术细节
- 使用纯 `numpy` 实现可重复、易审计
- 对大规模稀疏问题，建议用户使用 `scipy.sparse.linalg.cg`
- 相关脚本见 `scripts/solve_cg.py`

## 示例
参考 `references/examples.md`。
