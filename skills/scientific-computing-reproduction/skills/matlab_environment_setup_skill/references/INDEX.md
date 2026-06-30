# MATLAB Environment Setup Reference Index

Use this index when a coding agent needs MATLAB, Octave, or MATLAB MCP access before repository execution.

## Signal Routing

| Trigger | Read | Do not |
| --- | --- | --- |
| User says MATLAB is not configured | `matlab_environment_setup_skill/SKILL.md` | Do not jump directly to repository execution. |
| No `matlab` or `octave` found on PATH | platform setup table below | Do not edit shell startup files without approval. |
| MATLAB MCP unavailable | platform setup table below | Do not assume Codex-only configuration. |
| Toolboxes or license are uncertain | setup Skill preflight | Do not claim toolbox availability without evidence. |
| MATLAB files are ready to run | `matlab_runtime_skill/SKILL.md` | Do not keep runtime execution inside this setup Skill. |

## Platform Setup Table

| Platform | Setup Guidance |
| --- | --- |
| Codex | Use local shell checks first. Register MATLAB MCP only after approval with the Codex MCP command appropriate to the installed toolkit. |
| Claude Code | Use shell checks and host-supported MCP/tool configuration if available; keep repository instructions platform-neutral. |
| Gemini | Use host-provided tool configuration and project instructions; verify capabilities before claiming execution. |
| OpenCode | Use project-local skill/plugin loading and host-supported tool configuration; keep plugin wrappers thin. |
| generic coding agent | Use PATH checks, documented MCP/tool connector setup, and approval gates without assuming a specific config file. |

## Evidence Checklist

Before handing off to `matlab_runtime_skill`, record:

- coding agent platform;
- execution mode: MATLAB CLI, Octave, MATLAB MCP, or static-only;
- executable path or MCP capability names;
- MATLAB version if verified;
- toolbox summary if verified;
- approval status for any global configuration change;
- remaining missing pieces.

## Hard Boundaries

- Do not modify global configuration without approval.
- Do not install MATLAB or toolboxes automatically.
- Do not print license files, tokens, or credentials.
- Do not report MATLAB execution evidence without a CLI command, MCP tool result, or saved external log.
