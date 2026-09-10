---
name: matlab-runtime-skill
description: Route MATLAB inspection and execution in a computational math reproduction task to the shared matlab-runner skill, then return its evidence to the reproduction workflow.
---

# MATLAB Reproduction Handoff

Use the standalone [matlab-runner](https://github.com/VeryMath/AI4Math-MathTool/tree/main/skills/matlab-runner)
for MATLAB execution. This module connects it to reproduction work and does not
maintain a second set of tool-selection, execution, or recovery instructions.

1. Identify the MATLAB source files, intended entrypoint, data paths, working
   directory, expected outputs, and the user's execution or file-change limits.
   Static repository analysis can use the optional `scripts/matlab_runtime.py`;
   it does not inspect the running MATLAB environment or create execution commands.
2. Locate `matlab-runner` in the current agent's installed skills and read its
   `SKILL.md`. If it is missing, use the linked repository's complete
   `skills/matlab-runner` package, including its references, under the task's
   installation authorization. Do not assume the two repositories are siblings
   or copy the runner's workflow into this package. If it cannot be loaded,
   report the missing dependency and continue only with static repository analysis.
3. Pass the reproduction context and existing user authorization to the runner.
   Let it resolve the actual MATLAB MCP tools and load only the references it
   needs. Follow its execution boundary: no automatic MATLAB or Octave CLI fallback.
   If MCP is unavailable, report that limitation; use `matlab_environment_setup_skill`
   only when the user requests environment configuration.
4. Return the runner's actual outputs, file locations, errors, and execution
   status to the reproduction workflow. Preserve its distinction between static
   inspection and executed MATLAB results. Use existing task artifacts for
   reproduction evidence and `failure_diagnosis_skill` for unresolved failures.

The reproduction workflow remains responsible for the scientific goal, source
interpretation, comparison criteria, and final report. See [context checklist](references/INDEX.md).
