from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def log_approval(run: Path | str, checkpoint: str, decision: str, reason: str, operator: str = "human") -> Path:
    if decision not in {"approve", "revise", "reject", "skip"}:
        raise ValueError("decision must be approve, revise, reject, or skip")
    run = Path(run)
    directory = run / "approvals"
    directory.mkdir(parents=True, exist_ok=True)
    record = {
        "checkpoint": checkpoint,
        "decision": decision,
        "reason": reason,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "operator": operator,
    }
    path = directory / "approval_log.jsonl"
    with path.open("a") as handle:
        handle.write(json.dumps(record) + "\n")
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--decision", required=True)
    parser.add_argument("--reason", default="")
    parser.add_argument("--operator", default="human")
    args = parser.parse_args()
    print(log_approval(args.run, args.checkpoint, args.decision, args.reason, args.operator))


if __name__ == "__main__":
    main()
