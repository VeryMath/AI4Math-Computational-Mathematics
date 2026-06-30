from __future__ import annotations

import argparse
import json
from pathlib import Path


APPROVING_DECISIONS = {"approve"}
NON_APPROVING_DECISIONS = {"revise", "reject", "skip"}


def _load_records(run: Path) -> list[dict]:
    path = run / "approvals" / "approval_log.jsonl"
    if not path.exists():
        return []
    records = []
    for line in path.read_text().splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def latest_decision(run: Path | str, checkpoint: str) -> dict | None:
    run = Path(run)
    matches = [record for record in _load_records(run) if record.get("checkpoint") == checkpoint]
    return matches[-1] if matches else None


def check_approval_gate(
    run: Path | str,
    checkpoint: str,
    risk_level: str = "low",
    auto_approve_low_risk: bool = False,
) -> dict:
    record = latest_decision(run, checkpoint)
    if record and record.get("decision") in APPROVING_DECISIONS:
        return {
            "allowed": True,
            "checkpoint": checkpoint,
            "decision": record["decision"],
            "reason": record.get("reason", ""),
            "operator": record.get("operator", ""),
        }
    if record and record.get("decision") in NON_APPROVING_DECISIONS:
        return {
            "allowed": False,
            "checkpoint": checkpoint,
            "decision": record["decision"],
            "reason": f"Latest human decision for {checkpoint} is {record['decision']}.",
            "operator": record.get("operator", ""),
        }
    if risk_level == "low" and auto_approve_low_risk:
        return {
            "allowed": True,
            "checkpoint": checkpoint,
            "decision": "auto_approve_low_risk",
            "reason": "Low-risk action allowed because auto_approve_low_risk was explicitly set.",
            "operator": "agent",
        }
    return {
        "allowed": False,
        "checkpoint": checkpoint,
        "decision": "pending",
        "reason": f"Missing explicit approval for checkpoint {checkpoint}.",
        "operator": "",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--risk-level", default="low")
    parser.add_argument("--auto-approve-low-risk", action="store_true")
    args = parser.parse_args()
    result = check_approval_gate(
        args.run,
        args.checkpoint,
        risk_level=args.risk_level,
        auto_approve_low_risk=args.auto_approve_low_risk,
    )
    print(json.dumps(result, indent=2))
    if not result["allowed"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
