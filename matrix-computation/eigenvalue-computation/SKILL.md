---
name: eigenvalue-computation
description: "Use when you need eigenvalue computations, spectral analysis, or dominant eigenpairs in Python."
---

# 特征值计算 Skill

## 适用场景
- 计算矩阵的全部或部分特征值和特征向量
- 谱分析、模态分解、稳定性分析、主成分的变形
- 求最大特征值或幂法近似

## Quick Start
- 若需要全部特征值，对小/中等密集矩阵使用 `numpy.linalg.eig`
- 若只需前 k 个特征值，或矩阵稀疏，使用 `scipy.sparse.linalg.eigs` 或幂法/反幂法

## Selection Rules
- 对对称实矩阵优先使用 `numpy.linalg.eigh`（更高效、数值稳定）
- 对大型稀疏矩阵使用迭代方法或 `scipy` 的稀疏特征值接口

## 执行流程
1. 澄清是否需要全部特征值、前 k 个或仅最大特征值
2. 根据矩阵类型（对称/非对称、稠密/稀疏）选择方法
3. 返回特征值、特征向量，并提供谱半径、条件数等诊断信息

## Python 技术细节
- `numpy.linalg.eig`、`numpy.linalg.eigh`、及 `scipy.sparse.linalg.eigs` 为常用工具
- 提供简单的 `power_method` 以便教学与快速近似
- 相关脚本见 `scripts/solve_eigen.py`

## 示例
参考 `references/examples.md`。
