<div align="center">

# AI4Math · 计算数学

面向数值证据、符号结构、有限元推理和数学不变量计算的 AI4Math 技能集合。

[English](README.md) · [技能包](#技能包) · [快速开始](#快速开始) · [安全边界](#安全边界)

![version](https://img.shields.io/badge/version-0.1.0-blue)
![skills](https://img.shields.io/badge/skills-3-2ea44f)
![license](https://img.shields.io/badge/license-MIT-green)

</div>

## 这个仓库是什么

这个仓库是 AI4Math 计算数学方向的技能入口，收集用于把数学对象、方程、数据或论文片段转成可复核计算表示和可复现实验证据的技能包。

根 README 负责说明地图；真正执行任务时，请进入对应的 `skills/` 子目录。

## 技能包

| 包 | 适用任务 | 入口 |
| --- | --- | --- |
| [`finite-element-analysis`](skills/finite-element-analysis/) | 有限元建模提示、弱形式推导、单元选择和课堂规模示例。 | [`README`](skills/finite-element-analysis/README.md) · [`SKILL1`](skills/finite-element-analysis/SKILL1.md) · [`SKILL2`](skills/finite-element-analysis/SKILL2.md) · [`SKILL3`](skills/finite-element-analysis/SKILL3.md) |
| [`invariant-computation`](skills/invariant-computation/) | 选择、执行和验证代数、拓扑、几何、TDA 与 certified numerical invariant 计算路线。 | [`README`](skills/invariant-computation/README.md) · [`SKILL`](skills/invariant-computation/SKILL.md) |
| [`least-squares`](skills/least-squares/) | 线性、多项式、非线性、正则化、约束和贝叶斯最小二乘建模。 | [`README`](skills/least-squares/README.md) · [`SKILL`](skills/least-squares/SKILL.md) |

## 快速开始

克隆仓库并选择技能包：

```bash
git clone https://github.com/VeryMath/AI4Math-Computational-Mathematics.git
cd AI4Math-Computational-Mathematics
```

不变量计算从这里开始：

```text
skills/invariant-computation/SKILL.md
```

有限元分析从这里开始：

```text
skills/finite-element-analysis/README.md
```

最小二乘建模从这里开始：

```text
skills/least-squares/SKILL.md
```

## 仓库结构

```text
AI4Math-Computational-Mathematics/
├── README.md
├── README.zh-CN.md
├── SKILL.md
└── skills/
    ├── finite-element-analysis/
    ├── invariant-computation/
    └── least-squares/
```

包内 examples 只作为公开示例。计算输出、环境缓存和大型生成物不要提交，除非已经明确整理成公开示例。

## 验证

这个仓库没有根级构建步骤。标准 `SKILL.md` 技能包请使用本地 skill validator 验证；`finite-element-analysis` 是旧式 numbered skill 包，请直接检查 `README.md` 和 `SKILL*.md`。

## 安全边界

不要提交私有数据集、未公开论文片段、求解器凭证、API key、`.env` 文件、生成缓存或大型本地输出。公开示例应注明来源，并确认可以再分发。
