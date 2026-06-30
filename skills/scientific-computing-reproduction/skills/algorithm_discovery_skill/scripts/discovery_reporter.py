from __future__ import annotations

import argparse
import json
from pathlib import Path


def write_algorithm_match_review(run: Path | str, candidates: list[dict], queries: list[str]) -> Path:
    """Write legacy algorithm match review (debug-only).

    The default workflow does not write numbered checkpoint files.
    Algorithm match results are summarized in conversation and in plan.md.
    This function is retained for debug/legacy use only.
    """
    run = Path(run)
    checkpoint_dir = run / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Algorithm Match Review",
        "",
        "The active coding agent searched external public sources for algorithm candidates. Human confirmation is required before selecting any algorithm for reproduction.",
        "",
        "## Search Queries",
        "",
    ]
    lines.extend(f"- `{query}`" for query in queries)
    lines.extend(["", "## Ranked Candidates", ""])
    for index, candidate in enumerate(candidates, start=1):
        lines.extend(
            [
                f"### {index}. {candidate.get('title', 'untitled')}",
                "",
                f"- source: {candidate.get('source', 'unknown')}",
                f"- score: {candidate.get('match_score', 'not_ranked')}",
                f"- url: {candidate.get('url', '')}",
                f"- evidence: {candidate.get('evidence', [])}",
                f"- summary: {candidate.get('summary', '')[:500]}",
                "",
            ]
        )
    lines.extend(
        [
            "## Human Decision",
            "",
            "- decision: pending",
            "- selected_candidate:",
            "- reason:",
            "",
            "Allowed decisions: approve one candidate, revise search query, reject all candidates, or skip external algorithm discovery.",
        ]
    )
    path = checkpoint_dir / "06_algorithm_match_review.md"
    path.write_text("\n".join(lines))
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    parser.add_argument("--candidates", required=True)
    args = parser.parse_args()
    data = json.loads(Path(args.candidates).read_text())
    candidates = data.get("ranked_candidates") or data.get("candidates", [])
    print(write_algorithm_match_review(args.run, candidates, data.get("queries", [])))


if __name__ == "__main__":
    main()
