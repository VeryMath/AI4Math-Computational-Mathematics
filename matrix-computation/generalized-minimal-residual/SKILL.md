---
name: generalized-minimal-residual
description: "Use when you need GMRES (generalized minimal residual) for general (possibly non-symmetric) linear systems in Python."
---

# GMRES (Generalized Minimal Residual) Method

## 适用场景
- 求解非对称或不可保证正定的线性系统 Ax = b
- 需要稳健迭代求解、可带重启（restarted GMRES）

## Quick Start
- 若 A 非对称或有不良谱结构，优先考虑 GMRES
- 可选择重启参数 `restart` 和最大迭代 `maxiter`
- 若矩阵稀疏，建议使用 `scipy.sparse.linalg.gmres`

## Selection Rules
- 对一般非对称问题使用 GMRES；对对称正定问题优先使用 CG

## 执行流程
1. 验证维度和算子接口
2. 运行 GMRES（可选重启），收集残差历史并返回报告

## Python 技术细节
- 提供纯 `numpy` 的简单实现以便教学与可审计性
- 对生产级大规模问题推荐 `scipy.sparse.linalg.gmres`
- 相关脚本见 `scripts/solve_gmres.py`

## 示例
参考 `references/examples.md`。
