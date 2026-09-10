---
name: matlab-environment-setup-skill
description: Use when the user requests MATLAB or MATLAB MCP environment configuration for reproduction through the shared matlab-runner skill.
---

# MATLAB Environment Setup

Configure MATLAB access only when the user requests setup. Ordinary MATLAB
inspection and execution go through `matlab_runtime_skill` to the shared
[matlab-runner](https://github.com/VeryMath/AI4Math-MathTool/tree/main/skills/matlab-runner).

1. Identify the agent host, requested MATLAB installation, and concrete setup
   problem. Read the installed runner's `references/client-setup.md` for its
   current setup guidance; keep platform-specific commands there.
2. During this requested setup task, inspect only the relevant installation
   paths and visible environment variables. The optional
   `scripts/detect_matlab_environment.py` reports these local signals; it cannot
   establish whether the host exposes MATLAB MCP tools.
3. Configure the requested installation or MCP connection using the host's
   supported method and the user's existing authorization. Do not infer MATLAB
   execution availability from an executable on PATH or substitute Octave.
4. Return to `matlab_runtime_skill` and let `matlab-runner` inspect the host's
   actual MCP capabilities and perform the requested MATLAB work. Report any
   unresolved installation, connection, toolbox, or license issue.

Do not run repository code or duplicate the runner's execution checks in this
setup module. See [setup context](references/INDEX.md).
