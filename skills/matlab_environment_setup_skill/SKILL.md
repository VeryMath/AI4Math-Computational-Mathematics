---
name: matlab-environment-setup-skill
description: Use when MATLAB, Octave, MATLAB MCP, toolboxes, licenses, or coding-agent configuration must be checked or configured before MATLAB code can run.
---

# MATLAB Environment Setup Skill

This Skill is agent-neutral and not Codex-only. Use it to check and prepare MATLAB execution capability for Codex, Claude Code, Gemini, OpenCode, or any generic coding agent before `matlab_runtime_skill` runs repository code.

MATLAB environment setup is a configuration task, not a reproduction run. Always remember: do not modify global configuration without approval.

## When To Use

- The user wants the agent to call MATLAB, Octave, or MATLAB MCP.
- `matlab_runtime_skill` found MATLAB files but no executable or MCP capability is available.
- A run needs MATLAB version, license, root path, toolbox, or MCP status.
- A platform adapter needs to know how to expose MATLAB to a coding agent.

## When Not To Use

- The target repository already has an approved MATLAB run plan. Use `matlab_runtime_skill`.
- The task is only to classify a computational math domain. Use `computational_math_domain_skill`.
- The user asks to install MATLAB itself. Provide setup requirements, but do not automate vendor installer or license changes.

## Setup Targets

| Target | Use When | Notes |
| --- | --- | --- |
| MATLAB CLI | Local `matlab` executable is available or can be added to PATH. | Preferred for direct `matlab -batch` runs. |
| Octave | MATLAB is unavailable and code is likely compatible. | Treat as fallback; toolbox compatibility may differ. |
| MATLAB MCP | The coding agent can call MCP tools or tool connectors. | Best for structured `evaluate_matlab_code`, toolbox checks, and file/test execution. |
| Platform adapter | The agent needs configuration instructions. | Keep platform-specific instructions thin and point back to this Skill. |

## Agent Platforms

- Codex: may use native shell checks, local Skills, and optional MCP registration after approval.
- Claude Code: may use shell checks and project instructions; use its connector/MCP configuration mechanism if available.
- Gemini: may use repository instructions and external tool configuration provided by the host environment.
- OpenCode: may use project-local skills/plugins and host-supported tool configuration.
- generic coding agent: use the same preflight, approval, and verification contract without assuming platform-specific APIs.

## Preflight

1. Read `references/INDEX.md`.
2. Check whether `matlab` or `octave` is on PATH.
3. Check known environment variables such as `MATLAB_ROOT` only if they are visible in the current shell.
4. If a MATLAB executable is available, propose a harmless version/toolbox diagnostic command.
5. If MCP tools are available, propose a harmless `detect_matlab_toolboxes` or short `evaluate_matlab_code` diagnostic.
6. If neither CLI nor MCP is available, produce platform-specific setup guidance and stop.

Use the optional helper for local preflight only:

```bash
conda run -n ai4math python -m skills.matlab_environment_setup_skill.scripts.detect_matlab_environment --out outputs/{run_id}
```

The helper only inspects local PATH and environment signals. It does not install MATLAB, install toolboxes, edit global agent configuration, or run user code.

## Approval Boundary

Ask for approval before:

- editing global agent configuration;
- registering or changing MCP servers;
- changing shell startup files or PATH;
- installing Octave or any dependency;
- installing MATLAB toolboxes;
- running MATLAB code from a user repository.

Approved diagnostics should be low-risk, bounded, and logged under `outputs/{run_id}/`.

## Handoff To Runtime Skill

After setup is verified, hand off to `matlab_runtime_skill` with:

- execution mode: MATLAB CLI, Octave, MATLAB MCP, or static-only;
- executable path or MCP capability list;
- MATLAB version if known;
- toolbox availability if known;
- remaining risks or missing configuration;
- exact approval status for the next run.

Do not run repository code inside this setup Skill unless the user explicitly approved that specific run plan.
