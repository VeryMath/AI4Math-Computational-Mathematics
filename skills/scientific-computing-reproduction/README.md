# Scientific Computing Reproduction

Chinese guide: [README.zh-CN.md](README.zh-CN.md)

`scientific-computing-reproduction` helps a coding agent reproduce and inspect computational mathematics research code.

## When To Use It

Use this skill when you have:

- a local repository, remote repository, archive, paper-code pointer, or algorithm implementation;
- a need for source inspection before any execution;
- environment, dependency, runtime, failure, tuning, or visualization questions;
- computational claims that should be reported from saved evidence rather than chat memory.

## What It Produces

The agent should produce run plans, command logs, environment notes, metrics, figures, repair or tuning summaries, and `RUN_SUMMARY.md` artifacts under `outputs/{run_id}/`.

## Skill Entry Points

The main Skill entrypoints live under `skills/`.

A Skill is a readable workflow instruction for a coding agent. Each `SKILL.md` tells the agent when to use that workflow, what evidence to inspect, which artifacts to write, what risks require approval, and which optional helper scripts may be called.

The default entrypoint is:

```text
skills/computational_math_reproduction_workflow_skill/SKILL.md
```

The registry is:

```text
skills/registry.yaml
```

The registry routes the default workflow to specialist Skills for domain classification, repository reproduction, environment deployment, MATLAB setup, MATLAB runtime planning, failure diagnosis, tuning, visualization, human review, and report generation.

What users provide:

- a natural-language goal;
- an optional local path, remote repository, archive, or paper-code target;
- checkpoint decisions such as `approve`, `revise`, `reject`, or `skip`.

What the agent produces when useful:

- compact review artifacts under `outputs/{run_id}/`;
- command logs for approved runs;
- figures and tuning summaries when evidence exists;
- concise conversational explanations of what was found and what remains uncertain.

## Installation

Copy this to your coding agent:

```text
Please install the `scientific-computing-reproduction` skill from https://github.com/VeryMath/AI4Math-Computational-Mathematics.git (branch: main, skill path: `skills/scientific-computing-reproduction`). Read `.agent.md`, install the declared Skill entrypoint, verify that `$scientific-computing-reproduction` is discoverable, and tell me whether I need to restart the agent.
```

If you already have this skill repository locally, replace the repository URL
with the local folder path. The coding agent should handle cloning, linking,
configuration, reload/restart checks, and verification.

## Quick Start

After the coding agent can see the Skills, start with a prompt like this:

```text
Use computational_math_reproduction_workflow_skill.

Goal:
Inspect this computational math repository, classify the domain,
write plan.md, and wait for approval before executing anything.

Target:
<local path, repository URL, archive path, or paper-code pointer>

Output policy:
- route through skills/registry.yaml;
- keep durable artifacts under outputs/{run_id}/;
- use scripts only as optional helpers, not the workflow driver;
- ask before execution, source edits, dependency changes, long runs, tuning, or final conclusions.
```

For MATLAB access setup, ask the agent to use `matlab_environment_setup_skill` first. Use `matlab_runtime_skill` only after MATLAB, Octave, or MATLAB MCP capability is verified.

## How To Interact

Use a checkpoint loop:

```text
research-code target -> inspection -> plan -> approve / revise / reject / skip
                     -> approved run, repair, tuning, or report
                     -> evidence summary -> next checkpoint
```

Use `approve` to run a proposed step, `revise` to update the plan, `reject` to
stop the path, and `skip` to move past a phase. The agent should ask before
execution, source edits, dependency changes, long runs, tuning, or final
conclusions.

## Skill Map

- `computational_math_reproduction_workflow_skill`: default end-to-end workflow entrypoint.
- `computational_math_domain_skill`: broad computational math domain router.
- `continuous_optimization_skill`: mature specialist Skill for ADMM, PPA, proximal gradient, primal-dual methods, and augmented Lagrangian methods.
- `matlab_environment_setup_skill`: agent-neutral MATLAB, Octave, and MATLAB MCP setup and verification.
- `matlab_runtime_skill`: optional MATLAB/Octave runtime backend inspection, planning, toolbox hints, and approved execution boundary.
- `repo_reproduction_skill`: repository analysis, run planning, approved execution, and evidence collection.
- `environment_deployment_skill`: dependency and runtime setup planning.
- `failure_diagnosis_skill`: failure classification and repair planning.
- `algorithm_discovery_skill`: external algorithm and implementation discovery.
- `auto_tuning_skill`: approved tuning plans and bounded search.
- `visualization_skill`: convergence and tuning figures.
- `human_review_skill`: approval checkpoints and optional approval logs.
- `report_generation_skill`: compact plans, summaries, and reports.

## Supported Scope

Phase 1 focuses on continuous optimization research code, especially:

- ADMM;
- PPA;
- proximal gradient methods;
- primal-dual methods;
- augmented Lagrangian methods.

Python projects are the primary automatic execution target. MATLAB repositories can be inspected and planned through the MATLAB Skills, then run only after approval when MATLAB, Octave, or MATLAB MCP access is available. Julia, C++, and R are detected and reported in the MVP, but are not automatically run by default.

Other computational math areas are routed through reference cards until they need specialist Skills:

- numerical linear algebra;
- differential equations;
- PDE/FEM;
- stochastic simulation;
- inverse problems.

## Output Contract

The default workflow writes only compact durable artifacts:

- `outputs/{run_id}/plan.md` before execution;
- `outputs/{run_id}/repair_plan.md` only when source, dependency, adapter, entrypoint, or data changes are needed;
- `outputs/{run_id}/RUN_SUMMARY.md` after reproduction work;
- `outputs/{run_id}/tuning/tuning_plan.md` only when tuning is proposed;
- tuning results, tuning logs, tuning figures, and `tuning/TUNING_SUMMARY.md` only after tuning is approved.

Legacy checkpoint files and approval logs remain available as optional durable review mechanisms, but they are not the default workflow driver.

## Examples And Maintainer Material

The repository is not a reproduction case library. The `example/` directory contains compact reference artifacts that help maintainers and readers see what a completed Skill-first workflow looks like.

Tests, fixtures, and helper-script development are maintainer concerns. They are not required for a user to use the Skill layer with a coding agent.

For maintainer work, use the shared Conda environment:

```bash
conda run -n ai4math pytest
```

See `docs/environment.md`, `docs/interaction_protocol.md`, and `docs/testing.md` for maintainer details.

When adding or changing a Skill, update its `manifest.yaml`, `skills/registry.yaml`, and any routing reference cards. Keep platform adapters thin; improve the shared Skill layer first.
