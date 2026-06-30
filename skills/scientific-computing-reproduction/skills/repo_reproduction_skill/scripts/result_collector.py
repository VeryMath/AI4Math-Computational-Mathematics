from __future__ import annotations

import argparse
import json
from pathlib import Path


RESULT_SUFFIXES = {".csv", ".json", ".npy", ".npz", ".mat", ".txt", ".log"}
METRIC_KEYS = {"objective_value", "primal_residual", "dual_residual", "objective_gap", "iterations", "runtime", "convergence_history"}


def collect_results(source: Path | str, out: Path | str) -> dict:
    source = Path(source)
    out = Path(out)
    files = []
    metrics = {}
    for path in source.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in RESULT_SUFFIXES:
            continue
        stat = path.stat()
        rel = str(path.relative_to(source))
        files.append({"path": rel, "size": stat.st_size, "modified_time": stat.st_mtime})
        if path.name == "metrics.json":
            data = json.loads(path.read_text())
            metrics.update({key: data[key] for key in METRIC_KEYS if key in data})
    result = {"files": files, "parsed_metrics": metrics, "parse_note": "No optimization metrics parsed." if not metrics else "Parsed metrics.json."}
    out.mkdir(parents=True, exist_ok=True)
    (out / "collected_results.json").write_text(json.dumps(result, indent=2))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    print(json.dumps(collect_results(args.source, args.out), indent=2))


if __name__ == "__main__":
    main()
