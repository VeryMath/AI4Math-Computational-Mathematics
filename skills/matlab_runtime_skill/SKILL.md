---
name: matlab-runtime-skill
description: Use when a computational math repository or task uses MATLAB files, MATLAB README commands, MATLAB toolboxes, or MATLAB MCP execution tools.
---

# MATLAB Runtime Skill

MATLAB is a runtime backend, not the workflow driver. The workflow remains Skill-first and conversation-first: `computational_math_reproduction_workflow_skill` writes plans, records evidence under `outputs/{run_id}/`, and pauses for human approval before consequential execution.

This Skill defines how to inspect, plan, and optionally execute MATLAB code in computational math reproduction tasks. The local helper `scripts/matlab_runtime.py` can summarize MATLAB files, README commands, likely toolboxes, entrypoint candidates, and local `matlab`/`octave` executable availability.

## When To Use

- Source contains `.m`, `.mlx`, `.mat`, MATLAB project files, or MATLAB README commands.
- A repository depends on MATLAB toolboxes.
- The user wants MATLAB execution, tests, static analysis, or toolbox detection.
- MATLAB MCP tools are available or need to be checked.

## When Not To Use

- The task is a pure Python, Julia, C++, or R repository with no MATLAB artifacts.
- The user wants MATLAB Agentic Toolkit installation itself. In that case, use the official MATLAB Agentic Toolkit setup guidance as a reference and ask for approval before changing global Codex configuration.
- MATLAB, Octave, or MATLAB MCP is not configured yet. Use `matlab_environment_setup_skill` first.

## Execution Boundary

- Do static file inspection without approval.
- Before executing MATLAB code, write or update the run plan and ask for approval.
- Use MATLAB MCP tools only when available in the current agent session.
- If MCP tools are unavailable but local `matlab` or `octave` is available, generate a CLI run plan and ask for run-plan approval before execution.
- If neither MCP nor CLI execution is available, produce a MATLAB runtime plan and verification instructions instead of pretending execution happened.
- Save external execution logs to `outputs/{run_id}/logs/run.log`.
- Do not install MATLAB, install toolboxes, or change global MCP configuration without explicit approval.

## Preferred MCP Tools

| Capability | Use |
| --- | --- |
| `detect_matlab_toolboxes` | Confirm MATLAB version and installed toolboxes. |
| `check_matlab_code` | Static Code Analyzer checks for `.m` files. |
| `run_matlab_file` | Run scripts or programs from files. Prefer this over long inline code. |
| `run_matlab_test_file` | Run MATLAB unit tests with structured results. |
| `evaluate_matlab_code` | Short diagnostics and quick variable/toolbox checks only. |

## Local Helper

Use this helper for static preflight and plan evidence:

```bash
conda run -n ai4math python -m skills.matlab_runtime_skill.scripts.matlab_runtime --source <repo> --out outputs/{run_id}
```

The helper writes `matlab_runtime_summary.json` when `--out` is provided. It does not execute MATLAB code. `repo_analyzer.py` and `run_planner.py` use the same helper logic to attach MATLAB runtime summaries and generate approved `matlab -batch` or `octave --eval` candidate plans when a local executable is available.

## Workflow

1. Inspect MATLAB files, README commands, project files, and toolbox references.
2. Read `references/INDEX.md`.
3. Determine whether MATLAB MCP tools, local `matlab`, or local `octave` are available.
4. If unavailable, route to `matlab_environment_setup_skill` for agent-neutral setup.
5. If execution is available, include the exact MATLAB/MCP/Octave action in `plan.md` and wait for approval.
6. Execute only the approved action, capture logs, and summarize evidence.
7. Route failures to `failure_diagnosis_skill`.

## Codex MCP Setup Reference

The official MATLAB Agentic Toolkit recommends registering MATLAB MCP with Codex using:

```bash
codex mcp add matlab -- "<MCP_SERVER_PATH>" --matlab-root "<MATLAB_ROOT>" --matlab-display-mode "<DISPLAY_MODE>"
```

After registration, the MATLAB MCP server should have a longer timeout such as `tool_timeout_sec = 600` in the Codex config. Treat setup as a user-approved environment change, not an automatic reproduction step.
