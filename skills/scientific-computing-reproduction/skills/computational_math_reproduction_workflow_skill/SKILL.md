---
name: computational-math-reproduction-workflow-skill
description: Use when a user starts an end-to-end computational math research-code reproduction, deployment, tuning, visualization, or reporting workflow with a coding agent.
---

# Computational Math Reproduction Workflow Skill

This is the default entrypoint for open-source users of the computational math research-code reproduction system. The repository is Skill-first and Codex-native: Codex reads the relevant Skills, inspects the source, explains evidence in conversation, writes compact review artifacts, and waits for human approval before consequential execution.

Codex is the primary reference operator for this protocol, but the artifact contract is agent-neutral. Other coding agents can follow the same Skill documents, review artifacts, approval records, and evidence rules.

Scripts are tools, not drivers. They may help with local execution, logging, plotting, approval records, or repeatable toy checks, but there is no user-facing CLI pipeline and no command-line orchestrator that defines the workflow.

## When To Use

Use this Skill before any end-to-end task involving:

- computational math code reproduction or repository analysis
- external algorithm discovery
- environment deployment
- experiment execution
- failure diagnosis
- automatic tuning
- convergence or tuning visualization
- final report generation

For a narrow one-off task, Codex may use a specialist Skill directly. For any workflow that crosses stages, return here first.

## Default Flow

The default workflow is compact and conversation-led:

```
user goal
  -> Codex reads relevant Skills
  -> Codex inspects/searches source
  -> Codex writes plan.md
  -> human approves
  -> Codex runs minimal reproduction
  -> repair_plan.md only if needed (source/dependency/entrypoint/data changes)
  -> RUN_SUMMARY.md
  -> optional tuning: human approves tuning_plan.md first
  -> tuning runs under tuning/
  -> tuning/TUNING_SUMMARY.md
```

Process reasoning stays in conversation. Durable files are only for:

- user decisions (`plan.md`, `repair_plan.md`, `tuning/tuning_plan.md`)
- reproducibility evidence (`logs/run.log`, `results/`, `figures/`, `patches/`)
- summaries (`RUN_SUMMARY.md`, `tuning/TUNING_SUMMARY.md`)

No raw context dumps. No checkpoint directory by default.

## Default Output Tree

```
outputs/{run_id}/
├── plan.md
├── RUN_SUMMARY.md
├── logs/
│   └── run.log
├── results/
├── figures/
├── patches/
└── tuning/                    # only when tuning is approved
    ├── tuning_plan.md
    ├── tuning_results.csv
    ├── best_parameters.json
    ├── tuning.log
    ├── tuning_figures/
    └── TUNING_SUMMARY.md
```

`repair_plan.md` is generated only when source edits, dependency changes, adapters, or entrypoint changes are needed.

## Required Start Sequence

1. Understand the user goal: search, reproduce, deploy, tune, report, or a combination.
2. Select domain, runtime, and workflow Skills using `references/skill_routing.md`.
3. Inspect the source or search candidates with Codex-native tools first.
4. Use `computational_math_domain_skill` when the computational math domain is not already known.
5. Use setup Skills such as `matlab_environment_setup_skill` when a runtime is missing or unverified, then runtime Skills such as `matlab_runtime_skill` when the source language or toolchain needs backend-specific handling.
6. Write `outputs/{run_id}/plan.md` with the task interpretation, candidate command, risks, timeout, and expected evidence.
7. Summarize the plan in conversation and wait for `approve / revise / reject / skip`.

## Conversation Playbook

1. Generate a stable `run_id` when the user has not provided one. Prefer a short descriptive name plus date or a numbered `run_###` directory under `outputs/`.
2. Inspect files, dependency manifests, candidate entrypoints, metrics, language/runtime evidence, and domain evidence directly.
3. Route to domain, runtime, and workflow Skills. Record selected Skills in conversation.
4. Write `plan.md` before execution. Include the minimal reproduction command, why it is selected, risk level, timeout, expected outputs, and what will be logged.
5. Ask for exactly one of `approve`, `revise`, `reject`, or `skip`.
6. After approval, execute only the approved minimal reproduction. Log stdout/stderr to `logs/run.log`.
7. If execution fails or repair is needed, write `repair_plan.md`, explain the evidence in conversation, and ask for approval before source edits, dependency changes, adapters, or entrypoint changes.
8. Write `RUN_SUMMARY.md` with reproduction status, logs, metrics, limitations, and next options.
9. Propose tuning only after reproduction succeeds or partially succeeds. Write `tuning/tuning_plan.md`, ask for approval, and only then run tuning under `tuning/`.
10. Write `tuning/TUNING_SUMMARY.md` after approved tuning. Ask for final acknowledgment before accepting conclusions.

## Human Gates

Pause for human confirmation before you:

- execute external code
- install or upgrade dependencies
- create an adapter or wrapper
- modify source
- replace an entrypoint or data
- start tuning
- expand tuning budget
- accept a final conclusion

Logs, metrics, figures, tuning summaries, and best programs are evidence, not
proof. If a reproduction or tuning result creates a theorem claim or proof
obligation, route it to `rethlas-proving` or `lean-formalization`.

## Specialist Routing

- Use `algorithm_discovery_skill` when the user asks Codex to search for external algorithms or implementations.
- Use `computational_math_domain_skill` to classify broad computational math domains before choosing mature specialist Skills.
- Use `continuous_optimization_skill` when the domain card or source evidence points to ADMM, PPA, proximal gradient, primal-dual, augmented Lagrangian, or related methods.
- Use `matlab_environment_setup_skill` when MATLAB CLI, Octave, MATLAB MCP, toolbox/license status, or agent-platform exposure must be configured or verified.
- Use `matlab_runtime_skill` when the source contains MATLAB files, MATLAB toolbox requirements, or MATLAB execution opportunities.
- Use `repo_reproduction_skill` for repository analysis, run planning, execution, and result collection.
- Use `environment_deployment_skill` for dependency and runtime reports.
- Use `failure_diagnosis_skill` when a run fails or repair is needed.
- Use `auto_tuning_skill` only after reproduction succeeds or partially succeeds and the human approves tuning.
- Use `visualization_skill` when convergence or tuning metrics can be plotted.
- Use `report_generation_skill` for `plan.md`, `RUN_SUMMARY.md`, and tuning summaries.
- Use `human_review_skill` only when durable approval logs are needed for risk operations.

## References

- `references/skill_routing.md`: map user intent and stages to specialist Skills.

## Acceptance

A coding agent can start from a natural-language goal, read the Skills, inspect or search the source, write `plan.md`, wait for approval, run a minimal reproduction, produce `RUN_SUMMARY.md`, and optionally run approved tuning under `tuning/` without invoking a user-facing CLI pipeline.
