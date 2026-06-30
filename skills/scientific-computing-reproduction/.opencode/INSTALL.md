# Installing AI4Math Skills for OpenCode

This repository is **Skill-first**. The authoritative Skill layer is `skills/`, indexed by `skills/registry.yaml`; the default entrypoint is `skills/computational_math_reproduction_workflow_skill/SKILL.md`.

OpenCode is an operator surface, **not the workflow driver**. The workflow is driven by the Skills, human approvals, and compact artifacts under `outputs/{run_id}/`.

## Project-Local Use

Open this repository as the working project and ask OpenCode to read:

```text
skills/computational_math_reproduction_workflow_skill/SKILL.md
skills/registry.yaml
```

Then give the computational math reproduction task in natural language. The agent should route through the registry, use domain/runtime Skills as needed, and pause before consequential execution.

## Plugin-Style Use

If your OpenCode installation supports Git-backed plugins, keep the plugin wrapper thin and point it at this repository's `skills/` directory. The plugin metadata should not restate the workflow; it should expose the same `skills/registry.yaml` and default `computational_math_reproduction_workflow_skill`.

## Usage Prompt

```text
Use computational_math_reproduction_workflow_skill.

Goal:
Inspect the target repo, classify the computational math domain, write plan.md,
and wait for approval before execution.

Output policy:
- keep durable artifacts under outputs/{run_id}/;
- use scripts only as optional helpers, not the workflow driver;
- treat MATLAB, Python, Julia, C++, and R as runtimes selected by Skills.
```

For MATLAB access setup, use `matlab_environment_setup_skill` first; use `matlab_runtime_skill` only after MATLAB, Octave, or MATLAB MCP capability is verified.

## Maintainer Boundary

Do not fork OpenCode-specific copies of the workflow. Improve the shared Skill layer under `skills/`, then keep this adapter as a compact installation and loading note.
