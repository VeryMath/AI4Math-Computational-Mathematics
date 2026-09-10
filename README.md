<div align="center">

# AI4Math · Computational Mathematics

Computational workflows for numerical evidence, symbolic structure, and
mathematical invariant computation.

[中文说明](README.zh-CN.md) · [Contributors](CONTRIBUTORS.md) · [Skill packages](#skill-packages) · [Installation](#installation) · [Quick start](#quick-start) · [Security model](#security-and-scope)

![version](https://img.shields.io/badge/version-0.1.0-blue)
![skills](https://img.shields.io/badge/skills-3-2ea44f)
![license](https://img.shields.io/badge/license-MIT-green)

</div>

<p align="center">
  If this project helps your work, please consider giving the repository a Star ⭐
  <a href="https://github.com/VeryMath/AI4Math-Computational-Mathematics"><img alt="GitHub stars" src="https://img.shields.io/github/stars/VeryMath/AI4Math-Computational-Mathematics?style=social"></a>
</p>

## What This Repository Is

This repository is the AI4Math home for computational mathematics skills. It
collects packages for turning mathematical objects, equations, data, or paper
excerpts into reviewed computational representations and reproducible evidence.

Use the root page as the public map, then open the package that matches your
task.

## Skill Packages

| Package | Use it for | Start here |
| --- | --- | --- |
| [`invariant-computation`](skills/invariant-computation/) | Route and validate algebraic, topological, geometric, TDA, and certified numerical invariant computations. | [`README`](skills/invariant-computation/README.md) · [`SKILL`](skills/invariant-computation/SKILL.md) |
| [`least-squares`](skills/least-squares/) | Fit linear, polynomial, nonlinear, regularized, constrained, and Bayesian least-squares models. | [`README`](skills/least-squares/README.md) · [`SKILL`](skills/least-squares/SKILL.md) |
| [`scientific-computing-reproduction`](skills/scientific-computing-reproduction/) | Reproduce, diagnose, tune, visualize, and report computational mathematics research code with human approval checkpoints. | [`README`](skills/scientific-computing-reproduction/README.md) · [`SKILL`](skills/scientific-computing-reproduction/SKILL.md) |

## Installation

The recommended path is AI-assisted installation: ask your coding agent to clone or update this repository, read the Skill instructions, install the entrypoints, and verify discovery.

```text
Please install these AI4Math Skills for me.

Repository: https://github.com/VeryMath/AI4Math-Computational-Mathematics.git
Branch: main
Skill paths:
- skills/invariant-computation
- skills/least-squares
- skills/scientific-computing-reproduction

Steps:
1. Clone or update the repository locally.
2. Read README.md, SKILL.md, AGENTS.md if present, and each target Skill entrypoint.
3. If this environment supports local Skill discovery, link each directory that contains SKILL.md into the local skills directory.
4. Keep shared sibling support directories in place when a Skill depends on them.
5. Verify that the installed Skills are discoverable.
6. Tell me the installed paths, whether a restart is needed, and give me one test prompt.
```

Manual fallback for Codex-style local discovery:

```bash
git clone https://github.com/VeryMath/AI4Math-Computational-Mathematics.git
cd AI4Math-Computational-Mathematics
mkdir -p ~/.codex/skills
ln -s "$PWD/skills/invariant-computation" ~/.codex/skills/invariant-computation
ln -s "$PWD/skills/least-squares" ~/.codex/skills/least-squares
ln -s "$PWD/skills/scientific-computing-reproduction" ~/.codex/skills/scientific-computing-reproduction
```

If your agent uses a different local Skill directory, replace `~/.codex/skills` with that configured path.

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

For least-squares modeling, start with:

```text
skills/least-squares/SKILL.md
```

For scientific-computing reproduction and tuning, start with:

```text
skills/scientific-computing-reproduction/SKILL.md
```

## Repository Layout

```text
AI4Math-Computational-Mathematics/
├── README.md
├── README.zh-CN.md
├── SKILL.md
└── skills/
    ├── invariant-computation/
    ├── least-squares/
    └── scientific-computing-reproduction/
```

Package-local examples are illustrative fixtures. Computation outputs,
environment caches, and large generated artifacts should stay outside git unless
they are intentionally curated examples.

## Validation

There is no root build step. Validate changed standard skill packages with the
local skill validator.

## Security and Scope

Do not commit private datasets, unpublished paper excerpts, solver credentials,
API keys, `.env` files, generated caches, or large local outputs. Public
examples should be source-attributed and safe to redistribute.
