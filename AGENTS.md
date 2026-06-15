# AGENTS.md

This repository develops a Skill-driven Computational Math Reproduction, Deployment, Auto-Tuning, Visualization, and Reporting System for coding agents.

A coding agent is the operator. Codex is the primary reference operator and implementation profile for this repository, but the workflow artifacts are intended to be usable by other coding agents. Skills are the workflow control layer. Scripts are optional tools that an agent can call during the conversation. The human is the decision maker at checkpoints.

The whole repository is Skill-first and agent-native. Prefer the active coding agent's native abilities to read files, search, reason, edit, inspect outputs, and explain evidence in conversation. Use scripts only as optional tools when they make a local action safer, more reproducible, or easier to log. Do not use or present a CLI pipeline as the workflow driver.

For open-source end-to-end use, start with `skills/computational_math_reproduction_workflow_skill/SKILL.md`. It is the default entrypoint for computational math research-code reproduction workflows.

## Open-source product boundary

What you **ship to users** is the **Skill layer** under `skills/` (plus this contract: conversation, compact review artifacts, `outputs/{run_id}/`, approvals). A user’s **inputs** are natural-language goals plus optional local paths, remote repositories, or archives. Nothing in `tests/` or `tests/fixtures/` is required to *use* the system: those exist only for **maintainers** to verify scripts and gates. The public design goal is: **drive the workflow through Skills** (and the agent reading them), not through a bundled demo tree.

## Design Boundary

This repository is Skill-first and agent-native.

It is not:

- a CLI-first package;
- a fully automatic pipeline;
- a benchmark platform;
- a reproduction case library.

The normal interface is conversation with a coding agent.

This repository does not provide a user-facing CLI pipeline.

## Runtime Environment

Use a project-local or user-provided Python environment for tests and helper
scripts. If a shared Conda environment named `ai4math` exists, it is a
convenient default, but it is not part of the public contract.

Preferred command form:

```bash
conda run -n ai4math python -m <module>
```

Run tests with:

```bash
conda run -n ai4math pytest
```

Do not install this project into the user's global Python environment.

## Scope

- Phase 1 focuses on continuous optimization research code.
- Priority algorithm families: ADMM, PPA, proximal gradient, primal-dual methods, and augmented Lagrangian methods.
- Python projects are supported for automatic environment setup and execution.
- MATLAB environment access is configured or verified with `matlab_environment_setup_skill` in an agent-neutral way.
- MATLAB repositories are inspected with `matlab_runtime_skill` and may be run only after run-plan approval when MATLAB/Octave CLI or MATLAB MCP is available.
- Julia, C++, and R are detected and reported, but are not automatically run in the MVP.

## Conversation-First Workflow

1. Human gives the coding agent a task, repository, archive, or local path.
2. The agent starts with `computational_math_reproduction_workflow_skill` for multi-stage work and states which specialist Skills it will use and why.
3. The agent uses native file/search/reasoning tools to analyze the repository or external sources.
4. The agent writes artifacts under `outputs/{run_id}/` only when durable review or reproducibility is useful.
5. The agent summarizes the checkpoint in conversation.
6. The agent asks the human for `approve`, `revise`, `reject`, or `skip`.
7. The agent records the decision with `approval_logger.py`.
8. The agent executes only the approved next step.
9. The agent reports evidence, failures, and next choices.
10. The agent asks for final review before making final conclusions.

Do not present this system as a fully automatic harness. The normal interface is human-agent dialogue.

## Review Artifacts

The default agent-native workflow keeps review artifacts compact:

- `plan.md`: task interpretation, candidate command, risk, timeout, and expected evidence before execution.
- `repair_plan.md`: only when source edits, dependency changes, adapters, or other repairs are needed.
- `RUN_SUMMARY.md`: reproduction status, evidence, limits, and recommended next steps.
- `tuning/tuning_plan.md`: only after reproduction succeeds or partially succeeds and the human approves tuning.
- `tuning/TUNING_SUMMARY.md`: only after approved tuning runs.

Checkpoint files such as `01_task_understanding.md`, `02_run_plan_review.md`, `03_failure_fix_review.md`, `04_tuning_plan_review.md`, `05_final_review.md`, and `06_algorithm_match_review.md` are debug-only legacy artifacts — they are not the default workflow driver.

For external algorithm discovery, prefer the active agent's native search/browser/GitHub capabilities in conversation. Use scripts only as optional helpers for structured persistence, batch querying, or reproducibility.

For repository analysis, failure diagnosis, report drafting, and tuning-plan design, also prefer agent-native reasoning and file inspection first. Scripts are helpers, not the interface.

## Approval Rules

- Low-risk read-only analysis can run without approval.
- Low-risk demo commands can run after run-plan approval.
- Execution helpers must enforce approval when they support it. `executor.py --require-approval run_plan` may be used for repository reproduction runs after the human approves `plan.md`.
- High-risk commands always require human approval.
- Source modifications require human approval.
- Dependency version changes beyond declared install files require human approval.
- Long experiments and tuning budget expansion require human approval.
- Final conclusions require human review in conversation; `05_final_review.md` is optional durable evidence.

## Output Rules

- All artifacts must be saved under `outputs/`.
- All external command logs must be saved.
- Failed reproduction or tuning must generate `repair_plan.md` if source/dependency/entrypoint/data changes are needed, otherwise diagnose conversationally.
- Tuning must not start until the human approves `tuning/tuning_plan.md` or an equivalent tuning checkpoint.
- Successful reproduction or tuning should generate figures when convergence or tuning data is available.

## Safety Rules

- Do not execute `sudo`.
- Do not execute `rm -rf`.
- Do not execute `curl | bash` or `wget | bash`.
- Do not read sensitive files in the user home directory.
- Do not print tokens, passwords, or API keys.
- Do not modify the user's global Python environment.
- Do not run commands indefinitely.
- All subprocess commands must set `timeout`.
- Risky README commands must be marked `risk_level=high` and must not be executed automatically.
