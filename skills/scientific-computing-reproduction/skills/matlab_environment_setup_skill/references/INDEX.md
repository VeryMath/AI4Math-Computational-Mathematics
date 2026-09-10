# MATLAB Setup Context

Use [the setup entrypoint](../SKILL.md) only for requested environment changes.
The shared [matlab-runner](https://github.com/VeryMath/AI4Math-MathTool/tree/main/skills/matlab-runner)
owns client setup guidance and MATLAB execution rules.

- Read its `references/client-setup.md` for the current host configuration.
- Record the requested MATLAB installation, relevant paths, and actual setup error.
- Inspect the active agent's tool catalog to establish MCP availability; a shell
  PATH check alone cannot establish that connection.
- Reuse the user's existing authorization for the requested configuration.
- Return unresolved setup issues to the user and actual MATLAB work to the runner.

Do not launch MATLAB or Octave through a second execution path in this module.
