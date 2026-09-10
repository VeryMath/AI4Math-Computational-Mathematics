---
name: scientific-computing-reproduction
description: Use when reproducing, deploying, diagnosing, tuning, visualizing, or reporting computational math research code with a coding agent
---

# Scientific Computing Reproduction

This repository is a Skill-first computational math reproduction and tuning skill pack for coding agents. This file is a compatibility entrypoint for the shared Skill layer.

## Entry Point

Start end-to-end work from:

```text
skills/computational_math_reproduction_workflow_skill/SKILL.md
```

Use `skills/registry.yaml` to route to domain, runtime, environment, diagnosis, tuning, visualization, review, and reporting Skills.

This root `SKILL.md` is not the workflow driver. It is a compatibility entrypoint for platforms that expect one top-level Skill file.

## Platform Adapters

| Platform | Adapter |
| --- | --- |
| Codex plugin | `.codex-plugin/plugin.json` |
| Codex local skills | `.codex/INSTALL.md` |
| Claude Code | `.claude-plugin/plugin.json`, `CLAUDE.md` |
| Cursor | `.cursor-plugin/plugin.json` |
| OpenCode | `.opencode/INSTALL.md` |
| Gemini CLI | `GEMINI.md` |
| Agent contract | `AGENTS.md` |

All adapters point back to the shared Skill layer under `skills/`. Do not fork workflow behavior into platform-specific files.

## Operating Boundary

- Keep durable artifacts under `outputs/{run_id}/`.
- Ask before consequential execution, source edits, dependency changes, long runs, tuning, or final conclusions.
- Use `matlab_runtime_skill` to pass MATLAB work to the external `matlab-runner`; keep reproduction decisions and result interpretation in this workflow.
- Use scripts and hooks only as optional helpers; they are not the workflow driver.
