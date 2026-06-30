# Checkpoint Contract (Debug/legacy only)

The numbered checkpoint file convention (`01_task_understanding.md`, `02_run_plan_review.md`, etc.) is **deprecated**. It is retained only as a debug/legacy reference and must not be used as the default workflow mechanism.

## Current Default

The default workflow uses compact Markdown artifacts instead of numbered checkpoints:

| Purpose | Artifact |
| --- | --- |
| Execution approval | `plan.md` |
| Repair approval | `repair_plan.md` |
| Tuning approval | `tuning/tuning_plan.md` |
| Final acknowledgment | conversation |

## Legacy Checkpoint Names (debug only)

| Stage | Legacy Checkpoint (DO NOT USE BY DEFAULT) |
| --- | --- |
| `task_understanding` | `checkpoints/01_task_understanding.md` |
| `algorithm_discovery` | `checkpoints/06_algorithm_match_review.md` |
| `run_plan` | `checkpoints/02_run_plan_review.md` |
| `failure_fix` | `checkpoints/03_failure_fix_review.md` |
| `tuning_plan` | `checkpoints/04_tuning_plan_review.md` |
| `final_review` | `checkpoints/05_final_review.md` |

These files may only be written when a durable review trail is explicitly needed (not the default).

## Approval Decisions

Ask for exactly one decision: `approve`, `revise`, `reject`, or `skip`.

Record decisions in conversation. Write to `approvals/approval_log.jsonl` only when the operation is high-risk.

## Gates

- Repository reproduction uses `executor.py --require-approval run_plan`.
- Tuning uses `experiment_runner.py --require-approval tuning_plan`.
- If approval is missing, tools must return `blocked` and record the blocked action.
