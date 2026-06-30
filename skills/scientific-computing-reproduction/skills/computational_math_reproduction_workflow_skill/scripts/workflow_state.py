"""Workflow state helper (legacy/debug-only).

The default workflow does not require workflow_state.json.
This module is retained for resume scenarios only.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from skills.human_review_skill.scripts.approval_logger import log_approval


DEFAULT_STAGE = "task_understanding"
SCHEMA_VERSION = "0.2"
DEFAULT_PROMPT = "Review the plan and reply approve / revise / reject / skip."
DEFAULT_NEXT_ACTION = "Write plan.md and ask for approve / revise / reject / skip."


def _state_path(run: Path | str) -> Path:
    return Path(run) / "workflow_state.json"


def create_or_load_state(
    run: Path | str,
    run_id: str | None = None,
    source: str | None = None,
) -> dict[str, Any]:
    run = Path(run)
    run.mkdir(parents=True, exist_ok=True)
    path = _state_path(run)
    if path.exists():
        state = json.loads(path.read_text())
        if "next_action_for_agent" not in state and "next_action_for_codex" in state:
            state["next_action_for_agent"] = state["next_action_for_codex"]
            path.write_text(json.dumps(state, indent=2))
        return state
    state: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id or run.name,
        "source": source or "",
        "current_stage": DEFAULT_STAGE,
        "last_completed_stage": None,
        "selected_skills": [],
        "approved_checkpoints": [],
        "pending_checkpoint": "task_understanding",
        "pending_user_decision": True,
        "blocked_actions": [],
        "allowed_next_actions": ["write_plan_md"],
        "evidence_artifacts": [],
        "next_action_for_agent": DEFAULT_NEXT_ACTION,
        "next_action_for_codex": DEFAULT_NEXT_ACTION,
        "next_prompt_to_user": DEFAULT_PROMPT,
    }
    path.write_text(json.dumps(state, indent=2))
    return state


def update_state(run: Path | str, **updates: Any) -> dict[str, Any]:
    run = Path(run)
    state = create_or_load_state(run)
    for key, value in updates.items():
        if value is not None:
            state[key] = value
    if updates.get("next_action_for_agent") is None and updates.get("next_action_for_codex") is not None:
        state["next_action_for_agent"] = state["next_action_for_codex"]
    if updates.get("next_action_for_codex") is None and updates.get("next_action_for_agent") is not None:
        state["next_action_for_codex"] = state["next_action_for_agent"]
    _state_path(run).write_text(json.dumps(state, indent=2))
    return state


def apply_user_decision(
    run: Path | str,
    decision: str,
    reason: str = "",
    operator: str = "human",
) -> dict[str, Any]:
    if decision not in {"approve", "revise", "reject", "skip"}:
        raise ValueError("decision must be approve, revise, reject, or skip")
    run = Path(run)
    state = create_or_load_state(run)
    checkpoint = state.get("pending_checkpoint")
    if not checkpoint:
        raise ValueError("cannot apply a decision without a pending_checkpoint")

    log_approval(run, checkpoint, decision, reason, operator)

    if decision == "approve":
        next_action = f"Proceed after approved {checkpoint}."
        approved = list(state.get("approved_checkpoints", []))
        if checkpoint not in approved:
            approved.append(checkpoint)
        state.update(
            {
                "approved_checkpoints": approved,
                "last_completed_stage": checkpoint,
                "pending_checkpoint": None,
                "pending_user_decision": False,
                "allowed_next_actions": ["proceed_to_next_stage"],
                "next_action_for_agent": next_action,
                "next_action_for_codex": next_action,
                "next_prompt_to_user": "",
            }
        )
    elif decision == "revise":
        next_action = f"Revise {checkpoint} using human feedback: {reason}"
        state.update(
            {
                "pending_checkpoint": checkpoint,
                "pending_user_decision": True,
                "allowed_next_actions": [f"rewrite_{checkpoint}"],
                "next_action_for_agent": next_action,
                "next_action_for_codex": next_action,
                "next_prompt_to_user": f"Review the revised {checkpoint} and reply approve / revise / reject / skip.",
            }
        )
    elif decision == "reject":
        next_action = f"Stop the {checkpoint} path; human rejected it."
        blocked = list(state.get("blocked_actions", []))
        blocked.append(f"{checkpoint}: {reason}")
        state.update(
            {
                "blocked_actions": blocked,
                "pending_checkpoint": None,
                "pending_user_decision": False,
                "allowed_next_actions": [],
                "next_action_for_agent": next_action,
                "next_action_for_codex": next_action,
                "next_prompt_to_user": "",
            }
        )
    else:
        next_action = f"Skip {checkpoint} and continue only if the next stage is optional."
        state.update(
            {
                "pending_checkpoint": None,
                "pending_user_decision": False,
                "allowed_next_actions": ["skip_to_allowed_next_stage"],
                "next_action_for_agent": next_action,
                "next_action_for_codex": next_action,
                "next_prompt_to_user": "",
            }
        )

    _state_path(run).write_text(json.dumps(state, indent=2))
    return state


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    create = subparsers.add_parser("create")
    create.add_argument("--run", required=True)
    create.add_argument("--run-id")
    create.add_argument("--source")
    update = subparsers.add_parser("update")
    update.add_argument("--run", required=True)
    update.add_argument("--current-stage")
    update.add_argument("--selected-skills", default="")
    update.add_argument("--approved-checkpoints", default="")
    update.add_argument("--blocked-actions", default="")
    update.add_argument("--pending-checkpoint")
    update.add_argument("--pending-user-decision", choices=["true", "false"])
    update.add_argument("--allowed-next-actions", default="")
    update.add_argument("--evidence-artifacts", default="")
    update.add_argument("--next-action-for-agent")
    update.add_argument("--next-action-for-codex")
    update.add_argument("--next-prompt-to-user")
    decide = subparsers.add_parser("decide")
    decide.add_argument("--run", required=True)
    decide.add_argument("--decision", required=True)
    decide.add_argument("--reason", default="")
    decide.add_argument("--operator", default="human")
    args = parser.parse_args()
    if args.command == "create":
        state = create_or_load_state(args.run, args.run_id, args.source)
    elif args.command == "decide":
        state = apply_user_decision(args.run, args.decision, args.reason, args.operator)
    else:
        state = update_state(
            args.run,
            current_stage=args.current_stage,
            selected_skills=[item for item in args.selected_skills.split(",") if item],
            approved_checkpoints=[item for item in args.approved_checkpoints.split(",") if item],
            blocked_actions=[item for item in args.blocked_actions.split(",") if item],
            pending_checkpoint=args.pending_checkpoint,
            pending_user_decision={"true": True, "false": False}.get(args.pending_user_decision),
            allowed_next_actions=[item for item in args.allowed_next_actions.split(",") if item],
            evidence_artifacts=[item for item in args.evidence_artifacts.split(",") if item],
            next_action_for_agent=args.next_action_for_agent,
            next_action_for_codex=args.next_action_for_codex,
            next_prompt_to_user=args.next_prompt_to_user,
        )
    print(json.dumps(state, indent=2))


if __name__ == "__main__":
    main()
