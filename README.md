# AI4Math Reproduction Skills

[中文 README](README.zh-CN.md)

A **Skill-first workflow package** for computational math code reproduction, runtime deployment, auto-tuning, visualization, and reporting with coding agents.

## What This Is

AI4Math Reproduction Skills gives coding agents a reusable workflow layer for computational math research code. The agent reads Skills, inspects a target repository or local path, classifies the computational math domain, writes a compact run plan, waits for human approval, executes only approved steps, diagnoses failures, proposes tuning, generates figures when useful, and writes concise evidence-backed summaries.

This repository is not a CLI-first package, not a fully automatic pipeline, not a benchmark platform, and not a reproduction case library. The normal interface is conversation with a coding agent. Scripts are optional helpers, **not the workflow driver**.

## Who It Is For

The package is designed for agentic coding environments such as Codex, Claude Code, Gemini, and OpenCode. It remains Codex-native in its reference operator profile, but the shared product is the Skill layer under `skills/`, not any one platform wrapper.

Human users remain the decision makers at checkpoints. The agent can inspect, reason, plan, and run approved commands, but consequential execution, source edits, dependency changes, long runs, tuning, and final conclusions require human review.

## Quick Start

Choose the entrypoint for your coding agent:

- Codex: read `.codex/INSTALL.md`.
- Claude Code: read `CLAUDE.md`.
- Gemini: read `GEMINI.md`.
- OpenCode: read `.opencode/INSTALL.md`.

Then start an end-to-end task with the default Skill:

```text
Use computational_math_reproduction_workflow_skill.

Goal:
Inspect this computational math repository, classify the domain,
write plan.md, and wait for approval before executing anything.

Output policy:
- route through skills/registry.yaml;
- keep durable artifacts under outputs/{run_id}/;
- use scripts only as optional helpers, not the workflow driver;
- ask before execution, source edits, dependency changes, or tuning.
```

## Default Workflow

The default entrypoint is `skills/computational_math_reproduction_workflow_skill/SKILL.md`.

At a high level, the agent:

1. Interprets the user goal and target source.
2. Uses `skills/registry.yaml` to route to domain, runtime, environment, diagnosis, tuning, visualization, review, and reporting Skills.
3. Writes a compact `plan.md` under `outputs/{run_id}/`.
4. Asks the human to approve, revise, reject, or skip the next consequential step.
5. Executes only approved steps with bounded commands and saved logs.
6. Writes `repair_plan.md`, `RUN_SUMMARY.md`, tuning artifacts, or figures only when they are useful evidence.

## Skill Architecture

Each Skill is still driven by its `SKILL.md`. The companion `manifest.yaml` files and `skills/registry.yaml` make the Skill layer easier for agents and maintainers to inspect: they declare phase, dependencies, expected artifacts, risk level, and approval boundaries.

- `computational_math_reproduction_workflow_skill`: default workflow entrypoint.
- `computational_math_domain_skill`: broad computational math domain router.
- `continuous_optimization_skill`: mature specialist Skill for ADMM, PPA, proximal, primal-dual, and augmented Lagrangian methods.
- `matlab_environment_setup_skill`: agent-neutral MATLAB, Octave, and MATLAB MCP setup and verification before runtime use.
- `matlab_runtime_skill`: optional MATLAB/Octave runtime backend inspection, planning, toolbox hints, and approved execution boundary.
- `repo_reproduction_skill`: repository analysis, run planning, execution, and evidence collection.
- `environment_deployment_skill`: dependency and runtime setup planning.
- `failure_diagnosis_skill`: failure classification and repair planning.
- `algorithm_discovery_skill`: external algorithm and implementation search.
- `auto_tuning_skill`: tuning plans and bounded search.
- `visualization_skill`: convergence and tuning figures.
- `human_review_skill`: approval checkpoints and optional logs.
- `report_generation_skill`: compact plans, summaries, and reports.

## Supported Scope

Continuous optimization is the first mature domain module, especially ADMM, proximal methods, primal-dual methods, PPA, and augmented Lagrangian workflows.

Other computational math areas are routed through `computational_math_domain_skill` reference cards until they need their own specialist Skills:

- numerical linear algebra;
- differential equations;
- PDE/FEM;
- stochastic simulation;
- inverse problems.

Python is the primary automatic execution target. MATLAB setup is handled by `matlab_environment_setup_skill` in an agent-neutral way for Codex, Claude Code, Gemini, OpenCode, and generic coding agents. MATLAB runtime use is handled by `matlab_runtime_skill`: the agent can inspect `.m`/`.mlx`/`.mat` artifacts, infer entrypoints and toolbox hints, detect local `matlab` or `octave` executables, and generate approved `matlab -batch` or `octave --eval` run plans. MATLAB is not the workflow controller. Julia, C++, and R can be detected and reported, with deeper runtime support added as separate runtime Skills when needed.

## Platform Adapters

Thin platform adapters help other coding agents load the same workflow without copying it:

- `.codex/INSTALL.md`: Codex local Skill installation notes.
- `.opencode/INSTALL.md`: OpenCode loading and plugin-wrapper notes.
- `CLAUDE.md`: Claude Code repository orientation.
- `GEMINI.md`: Gemini entrypoint that includes the default workflow Skill and registry.

All adapters point back to `skills/registry.yaml` and `computational_math_reproduction_workflow_skill`. Platform files should stay small and should not become separate workflow definitions.

## Examples

The repository is not a reproduction case library, but `example/` contains compact reference artifacts that show what a completed Skill-first workflow looks like.

- `example/boyd_admm_lasso_20260513/`: Stanford Boyd ADMM Lasso reproduction in MATLAB, including plan approval, repair for unsaved `grabcode` buffers, convergence figures, and approved `rho` / `alpha` tuning. The baseline run matches the published 15-iteration example, and the tuned setting `rho = 1.0`, `alpha = 1.2` reduces the iteration count to 13 while preserving objective closeness.
- `example/admm_bhushan23_20260511/`: minimal ADMM Lasso objective reproduction for `bhushan23/ADMM` using the current `ai4math` Python environment.

## Outputs

The compact default workflow writes artifacts under `outputs/{run_id}/`:

- `plan.md` before execution;
- `repair_plan.md` only when source or dependency changes are needed;
- `RUN_SUMMARY.md` at the end;
- `tuning/tuning_plan.md` only when tuning is proposed;
- `tuning/tuning_results.csv`, `tuning/best_parameters.json`, `tuning/tuning.log`, `tuning/tuning_figures/`, and `tuning/TUNING_SUMMARY.md` only after tuning is approved.

Checkpoint files under `outputs/{run_id}/checkpoints/` and approval logs under `outputs/{run_id}/approvals/` remain available as optional durable review mechanisms.

## Environment

Use the shared Conda environment `ai4math`.

```bash
conda create -y -n ai4math python=3.13 pip
conda run -n ai4math python -m pip install -e ".[dev]"
```

See `docs/environment.md`.

## Maintainer Notes

Run tests with:

```bash
conda run -n ai4math pytest
```

When adding a Skill, update its `manifest.yaml`, `skills/registry.yaml`, and any routing reference cards. Keep platform adapters thin; improve the shared Skill layer first.
