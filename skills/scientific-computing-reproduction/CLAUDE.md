# CLAUDE.md

This file orients Claude Code when working in this repository.

## Project Purpose

This repository is a **Skill-first** computational math reproduction and tuning system for coding agents. The authoritative Skill layer is `skills/`, indexed by `skills/registry.yaml`; the default entrypoint is `skills/computational_math_reproduction_workflow_skill/SKILL.md`.

Claude Code can act as an operator, but it is **not the workflow driver**. The workflow is the Skill layer, human approvals, and compact artifacts under `outputs/{run_id}/`.

## Architecture

- `skills/` is the shared behavior layer for all platforms.
- `skills/registry.yaml` declares the default entrypoint, phases, dependencies, artifacts, risk levels, and approval boundaries.
- `computational_math_reproduction_workflow_skill` orchestrates end-to-end reproduction work.
- `computational_math_domain_skill` routes broad computational math domains such as optimization, numerical linear algebra, differential equations, PDE/FEM, stochastic simulation, and inverse problems.
- `continuous_optimization_skill` is the mature specialist domain Skill.
- `matlab_environment_setup_skill` verifies or configures MATLAB, Octave, and MATLAB MCP access in an agent-neutral way.
- `matlab_runtime_skill` treats MATLAB as an optional runtime backend, not as a controller.
- `outputs/{run_id}/` holds compact review artifacts, logs, summaries, tuning plans, and figures when they are useful.

## Operating Rules

- Start open-source computational math reproduction tasks with `computational_math_reproduction_workflow_skill`.
- Use domain, runtime, environment, diagnosis, tuning, visualization, review, and reporting Skills as routed by `skills/registry.yaml`.
- Prefer native file/search/reasoning/editing tools before optional scripts.
- Use scripts only when they make execution, logging, plotting, or approval records safer to verify; scripts are not the workflow driver.
- Ask before consequential execution, source edits, dependency changes, long runs, tuning, or final conclusions.
- Keep durable artifacts under `outputs/{run_id}/`.

## Common Commands

Use the shared Conda environment:

```bash
conda run -n ai4math pytest
```

If `conda` is not on PATH, locate the local Conda installation and still run tests inside `ai4math`.

## Maintainer Boundary

Keep platform files thin. Do not duplicate workflow logic in `CLAUDE.md`, `GEMINI.md`, `.codex/INSTALL.md`, or `.opencode/INSTALL.md`; update the shared Skills and registry first.
