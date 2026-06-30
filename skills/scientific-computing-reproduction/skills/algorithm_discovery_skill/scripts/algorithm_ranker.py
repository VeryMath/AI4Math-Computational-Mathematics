from __future__ import annotations

import argparse
import json
from pathlib import Path


def rank_candidates(candidates: list[dict], keywords: list[str]) -> list[dict]:
    ranked = []
    normalized_keywords = [keyword.lower() for keyword in keywords if keyword]
    for candidate in candidates:
        text = f"{candidate.get('title', '')} {candidate.get('summary', '')}".lower()
        evidence = [keyword for keyword in keywords if keyword and keyword.lower() in text]
        score = len(evidence)
        if candidate.get("source") == "github":
            stars = int(candidate.get("metadata", {}).get("stars", 0) or 0)
            score += min(stars / 1000.0, 2.0)
        if candidate.get("source") == "arxiv":
            score += 0.25
        item = dict(candidate)
        item["match_score"] = round(score, 3)
        item["evidence"] = evidence or [keyword for keyword in normalized_keywords if keyword in text]
        ranked.append(item)
    return sorted(ranked, key=lambda item: item["match_score"], reverse=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--keywords", required=True, help="Comma-separated keywords.")
    parser.add_argument("--out")
    args = parser.parse_args()
    data = json.loads(Path(args.candidates).read_text())
    ranked = rank_candidates(data.get("candidates", data), [item.strip() for item in args.keywords.split(",")])
    if args.out:
        Path(args.out).write_text(json.dumps(ranked, indent=2))
    print(json.dumps(ranked, indent=2))


if __name__ == "__main__":
    main()
