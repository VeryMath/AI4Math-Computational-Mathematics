---
name: computational-math-domain-skill
description: Use when classifying a computational math repository or task into a broad domain before choosing specialist Skills, references, runtimes, and validation evidence.
---

# Computational Math Domain Skill

This Skill routes a user goal, paper code repository, or local source tree into a broad computational math domain. It keeps the project from creating one Skill per domain too early: most domains begin as reference cards here, and only become standalone specialist Skills after they need their own workflow, scripts, failure modes, and evals.

For end-to-end reproduction workflows, this Skill is selected by `computational_math_reproduction_workflow_skill` before deeper specialist Skills.

## When To Use

- A repository may be computational math, but the specific domain is unclear.
- The user asks for reproduction beyond continuous optimization.
- The source includes MATLAB, Python, Julia, C++, or mixed-language numerical code.
- A run plan needs domain-specific evidence or validation criteria before execution.

## When Not To Use

- The domain is already known and a mature specialist Skill exists.
- The task is only runtime setup, such as MATLAB MCP configuration. Use `matlab_runtime_skill` for MATLAB execution boundaries.

## Domain Routing

Read `references/INDEX.md` first. It routes observable signals to compact domain cards:

- continuous optimization;
- numerical linear algebra;
- differential equations;
- PDE/FEM;
- stochastic simulation;
- inverse problems.

Continuous optimization is currently the first mature specialist domain. If the index routes to continuous optimization with enough evidence, continue with `continuous_optimization_skill`.

## Workflow

1. Inspect README, paper notes, scripts, dependency files, example commands, and output names.
2. Use `references/INDEX.md` to identify candidate domains.
3. Read only the relevant domain cards.
4. Record evidence, uncertainty, expected validation signals, and likely runtime requirements.
5. Route to mature specialist Skills when available; otherwise keep the domain card as guidance for `repo_reproduction_skill`, `failure_diagnosis_skill`, `visualization_skill`, and `report_generation_skill`.

## Output Contract

In conversation or in `plan.md`, summarize:

- candidate domain;
- source evidence;
- likely runtime backend;
- expected evidence for reproduction;
- domain-specific failure risks;
- whether a mature specialist Skill exists.

If evidence is ambiguous, ask for human review before treating the classification as settled.
