# Installing AI4Math Skills for Codex

This repository is **Skill-first**. The authoritative Skill layer is `skills/`, indexed by `skills/registry.yaml`; the default entrypoint is `skills/computational_math_reproduction_workflow_skill/SKILL.md`.

Codex is the reference operator, but Codex is **not the workflow driver**. The workflow is driven by the readable Skills, human approvals, and compact artifacts under `outputs/{run_id}/`.

## Local Install

From this repository root:

```bash
mkdir -p ~/.agents/skills
ln -s "$PWD/skills" ~/.agents/skills/ai4math
```

Restart Codex after creating or updating the link so the local Skill index is refreshed.

If your Codex build discovers skills from `~/.codex/skills` instead, use the same link target there and keep the directory name `ai4math`.

## Verify

```bash
ls ~/.agents/skills/ai4math
```

You should see the same Skill directories as this repository's `skills/` folder, including `computational_math_reproduction_workflow_skill`.

## Usage Prompt

```text
Use computational_math_reproduction_workflow_skill.

Goal:
Reproduce this computational math repository with a minimal approved run.

Output policy:
- route through skills/registry.yaml;
- keep outputs under outputs/{run_id}/;
- use scripts only as optional helpers, not the workflow driver;
- ask before consequential execution, source edits, dependency changes, or tuning.
```

For MATLAB access setup, use `matlab_environment_setup_skill` first; use `matlab_runtime_skill` only after MATLAB, Octave, or MATLAB MCP capability is verified.

## Maintainer Boundary

Do not duplicate the workflow in this adapter. Update `skills/registry.yaml`, the relevant `SKILL.md`, or the domain/runtime reference cards first; this file should remain a thin Codex installation note.
