<div align="center">

# AI4Math · Computational Mathematics

Computational workflows for numerical evidence, symbolic structure, finite
element reasoning, and mathematical invariant computation.

[中文说明](README.zh-CN.md) · [Skill packages](#skill-packages) · [Quick start](#quick-start) · [Security model](#security-and-scope)

![version](https://img.shields.io/badge/version-0.1.0-blue)
![skills](https://img.shields.io/badge/skills-3-2ea44f)
![license](https://img.shields.io/badge/license-MIT-green)

</div>

## What This Repository Is

This repository is the AI4Math home for computational mathematics skills. It
collects packages for turning mathematical objects, equations, data, or paper
excerpts into reviewed computational representations and reproducible evidence.

Use the root page as the public map, then open the package that matches your
task.

## Skill Packages

| Package | Use it for | Start here |
| --- | --- | --- |
| [`finite-element-analysis`](skills/finite-element-analysis/) | Work through finite element modeling prompts, weak forms, element choices, and classroom-scale examples. | [`README`](skills/finite-element-analysis/README.md) · [`SKILL1`](skills/finite-element-analysis/SKILL1.md) · [`SKILL2`](skills/finite-element-analysis/SKILL2.md) · [`SKILL3`](skills/finite-element-analysis/SKILL3.md) |
| [`invariant-computation`](skills/invariant-computation/) | Route and validate algebraic, topological, geometric, TDA, and certified numerical invariant computations. | [`README`](skills/invariant-computation/README.md) · [`SKILL`](skills/invariant-computation/SKILL.md) |
| [`least-squares`](skills/least-squares/) | Fit linear, polynomial, nonlinear, regularized, constrained, and Bayesian least-squares models. | [`README`](skills/least-squares/README.md) · [`SKILL`](skills/least-squares/SKILL.md) |

## Quick Start

Clone the repository and choose a package:

```bash
git clone https://github.com/VeryMath/AI4Math-Computational-Mathematics.git
cd AI4Math-Computational-Mathematics
```

For invariant workflows, start with:

```text
skills/invariant-computation/SKILL.md
```

For finite element analysis, start with:

```text
skills/finite-element-analysis/README.md
```

For least-squares modeling, start with:

```text
skills/least-squares/SKILL.md
```

## Repository Layout

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

Package-local examples are illustrative fixtures. Computation outputs,
environment caches, and large generated artifacts should stay outside git unless
they are intentionally curated examples.

## Validation

There is no root build step. Validate changed standard skill packages with the
local skill validator. For the finite-element package, review `README.md` and
the numbered `SKILL*.md` files directly because it predates the standard
single-`SKILL.md` layout.

## Security and Scope

Do not commit private datasets, unpublished paper excerpts, solver credentials,
API keys, `.env` files, generated caches, or large local outputs. Public
examples should be source-attributed and safe to redistribute.
