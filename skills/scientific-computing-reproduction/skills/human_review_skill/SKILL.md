---
name: human-review-skill
description: This skill should be used when the user wants to set up checkpoints, record approval decisions, gate execution pending human confirmation, or manage human-in-the-loop review points in a computational math workflow.
---

# Human Review Skill

Manages lightweight human approval gates for the compact workflow.

For end-to-end computational math research-code reproduction workflows, this Skill should be selected by `computational_math_reproduction_workflow_skill` only when durable approval logs are needed.

## Lightweight Approval Types

Four approval types, all conversation-led:

1. **plan approval** — before executing external code (`plan.md`)
2. **repair approval** — before modifying source, dependencies, entrypoint, or data (`repair_plan.md`)
3. **tuning approval** — before starting or expanding tuning budget (`tuning/tuning_plan.md`)
4. **final acknowledgment** — before accepting conclusions

## Approval Aliases

User replies `approve`, `ok`, `yes`, `可以`, `好的`, `继续`, `同意`, `批准`, `就这个吧`, `选这个`, `没问题` are all treated as approval.

Revise: `revise`, `修改`, `改一下`
Reject: `reject`, `拒绝`, `不行`
Skip: `skip`, `跳过`, `跳过这个`

## Workflow

1. Present the compact artifact (`plan.md`, `repair_plan.md`, `tuning/tuning_plan.md`) to the user.
2. Ask for exactly one decision: `approve`, `revise`, `reject`, or `skip`.
3. Record the decision in conversation.
4. Only write `approvals/approval_log.jsonl` when the operation is high-risk (source changes, dependency installs, budget increases).
5. Do not write numbered checkpoint files (`01_task_understanding.md`, etc.) by default.

## Scripts

### approval_gate
Input: `--run <path>`, `--checkpoint <name>`, `--risk-level <low|high>`
Exits 0 if allowed, exits 2 if blocked.

### approval_logger
Records an approval decision to `approvals/approval_log.jsonl`. Only call when explicitly logging a high-risk approval.

```bash
python -m skills.human_review_skill.scripts.approval_logger --run /path/to/output --checkpoint plan --decision approve --reason "low-risk demo"
```

## Agent Conversation Semantics

- Ask for exactly one decision: `approve`, `revise`, `reject`, or `skip`.
- If the user approves, continue to the next stage.
- If the user asks to revise, keep the same artifact pending and address the requested changes.
- If the user rejects, record the rejection and stop or reroute.
- If the user skips, continue only if the stage is optional.

Do not write numbered checkpoint files by default. Process reasoning stays in conversation.
