# MATLAB Reproduction Context

Read [the handoff entrypoint](../SKILL.md), then the installed
[matlab-runner](https://github.com/VeryMath/AI4Math-MathTool/tree/main/skills/matlab-runner).
MATLAB tool selection, execution, environment checks, and recovery belong there.

Pass only the context needed for this reproduction:

- Source and entrypoint paths, including whether the file is a script, function,
  Live Script, or existing MATLAB test.
- Input data, working directory, and required output files or figures.
- Scientific comparison criteria and any toolbox requirements found in the source.
- User constraints, existing execution authorization, and relevant prior errors.

Collect the runner's actual output and saved-file locations for the reproduction
report. Missing runner or MATLAB MCP access permits static analysis only; a local
MATLAB or Octave executable is not a substitute for the runner's execution route.
