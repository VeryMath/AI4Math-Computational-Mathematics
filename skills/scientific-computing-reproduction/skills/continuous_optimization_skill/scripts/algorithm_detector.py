from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ALGORITHM_PATTERNS = {
    "ADMM": [r"\badmm\b", r"alternating direction method", r"rho", r"dual_residual"],
    "PPA": [r"\bppa\b", r"proximal point", r"proximal_parameter"],
    "proximal gradient": [r"proximal gradient", r"ista", r"fista", r"step_size"],
    "primal-dual method": [r"primal[-_ ]dual", r"chambolle", r"dual_step"],
    "augmented Lagrangian": [r"augmented lagrangian", r"alm\b"],
    "gradient descent": [r"gradient descent", r"learning_rate"],
    "coordinate descent": [r"coordinate descent"],
}


def _iter_text_files(source: Path):
    for path in source.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".py", ".md", ".rst", ".txt", ".yaml", ".yml"}:
            yield path


def detect_algorithm(source: Path | str) -> dict:
    source = Path(source)
    evidence: dict[str, list[str]] = {name: [] for name in ALGORITHM_PATTERNS}
    for path in _iter_text_files(source):
        try:
            text = path.read_text(errors="ignore").lower()
        except OSError:
            continue
        haystack = f"{path.name.lower()}\n{text}"
        for name, patterns in ALGORITHM_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, haystack):
                    evidence[name].append(f"{path.relative_to(source)}:{pattern}")

    scored = [(name, len(items)) for name, items in evidence.items()]
    best_name, best_score = max(scored, key=lambda item: item[1], default=("unknown", 0))
    if best_score == 0:
        return {"detected_algorithm": "unknown", "confidence": 0.0, "evidence": []}
    confidence = min(0.95, 0.35 + 0.15 * best_score)
    return {"detected_algorithm": best_name, "confidence": confidence, "evidence": evidence[best_name]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()
    result = detect_algorithm(args.source)
    if args.out:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "algorithm_detection.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
