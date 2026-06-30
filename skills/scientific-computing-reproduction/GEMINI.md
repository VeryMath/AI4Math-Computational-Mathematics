@./skills/computational_math_reproduction_workflow_skill/SKILL.md
@./skills/registry.yaml

# Gemini Entry Point

This repository is **Skill-first**. The authoritative Skill layer is `skills/`, indexed by `skills/registry.yaml`; the default entrypoint is `computational_math_reproduction_workflow_skill`.

Gemini may act as a coding agent/operator, but it is **not the workflow driver**. The workflow is the Skill layer plus human approvals, compact review artifacts, and evidence under `outputs/{run_id}/`.

## Operating Rules

- Start computational math reproduction work from `skills/computational_math_reproduction_workflow_skill/SKILL.md`.
- Use `skills/registry.yaml` to route to domain, runtime, environment, diagnosis, tuning, visualization, review, and reporting Skills.
- Treat `computational_math_domain_skill` as the broad domain router until a field needs its own specialist Skill.
- Use `matlab_environment_setup_skill` when MATLAB, Octave, or MATLAB MCP access must be verified before execution.
- Treat `matlab_runtime_skill` as an optional runtime backend, not as a controller.
- Ask before consequential execution, source edits, dependency changes, long runs, or tuning.
- Use scripts only as optional helpers, not the workflow driver.
- Keep durable artifacts under `outputs/{run_id}/`.

## Maintainer Boundary

Do not duplicate workflow instructions in this file. Update the shared `skills/` content first, then keep this Gemini entry point thin.
