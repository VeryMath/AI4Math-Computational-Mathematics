from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from skills.continuous_optimization_skill.scripts.algorithm_detector import detect_algorithm
from skills.matlab_runtime_skill.scripts.matlab_runtime import analyze_matlab_runtime, readme_matlab_commands


DEPENDENCY_FILES = [
    "requirements.txt",
    "environment.yml",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "Pipfile",
    "Project.toml",
    "Manifest.toml",
    "Makefile",
]
ENTRYPOINT_FILES = ["main.py", "demo.py", "run.py", "train.py", "experiment.py"]
ENTRYPOINT_DIRS = ["examples", "scripts", "tests", "benchmarks"]
LANGUAGE_SUFFIXES = {
    "Python": [".py"],
    "MATLAB": [".m", ".mlx"],
    "Julia": [".jl"],
    "C++": [".cpp", ".cc", ".hpp", ".h"],
    "R": [".r", ".R"],
}
OPT_KEYWORDS = [
    "ADMM",
    "PPA",
    "proximal",
    "primal-dual",
    "augmented Lagrangian",
    "gradient descent",
    "coordinate descent",
    "LASSO",
    "sparse recovery",
    "matrix completion",
    "convex optimization",
]


def _detect_language(source: Path) -> str:
    counts = {language: 0 for language in LANGUAGE_SUFFIXES}
    for path in source.rglob("*"):
        if path.is_file():
            for language, suffixes in LANGUAGE_SUFFIXES.items():
                if path.suffix in suffixes:
                    counts[language] += 1
    language, count = max(counts.items(), key=lambda item: item[1])
    return language if count else "unknown"


def _readme_commands(source: Path) -> list[str]:
    commands: list[str] = []
    for name in ("README.md", "README.rst", "README.txt"):
        readme = source / name
        if not readme.exists():
            continue
        text = readme.read_text(errors="ignore")
        for line in text.splitlines():
            stripped = line.strip().lstrip("$").strip()
            if re.match(r"^(python|pytest|make|julia|Rscript|matlab|octave)\b", stripped):
                commands.append(stripped)
    return commands


def analyze_repo(source: Path | str) -> dict:
    source = Path(source)
    dependency_files = [name for name in DEPENDENCY_FILES if (source / name).exists()]
    candidate_entrypoints = [name for name in ENTRYPOINT_FILES if (source / name).exists()]
    candidate_entrypoints.extend(name + "/" for name in ENTRYPOINT_DIRS if (source / name).exists())

    readme_commands = _readme_commands(source)
    matlab_summary = analyze_matlab_runtime(source)
    for command in readme_matlab_commands(source):
        if command not in readme_commands:
            readme_commands.append(command)
    detector = detect_algorithm(source)
    detected_algorithms = [] if detector["detected_algorithm"] == "unknown" else [detector["detected_algorithm"]]
    text = " ".join(path.read_text(errors="ignore")[:20000] for path in source.glob("README*") if path.is_file())
    for keyword in OPT_KEYWORDS:
        if keyword.lower() in text.lower() and keyword not in detected_algorithms:
            detected_algorithms.append(keyword)

    warnings = []
    recommended_skills = []
    language = _detect_language(source)
    if matlab_summary["matlab_files"]:
        recommended_skills.append("matlab_runtime_skill")
        candidate_entrypoints.extend(
            entrypoint
            for entrypoint in matlab_summary["entrypoint_candidates"]
            if entrypoint not in candidate_entrypoints
        )
    if language == "MATLAB":
        warnings.append("MATLAB execution requires matlab_runtime_skill, run-plan approval, and MATLAB/Octave or MATLAB MCP availability.")
    elif language != "Python":
        warnings.append(f"{language} is detect-only in the MVP.")
    if not candidate_entrypoints:
        warnings.append("No obvious run entrypoint detected.")
    if not dependency_files:
        warnings.append("No dependency file detected.")

    confidence = detector["confidence"]
    if language == "Python":
        confidence += 0.05
    if dependency_files and candidate_entrypoints:
        confidence += 0.1

    return {
        "repo_path": str(source),
        "language": language,
        "dependency_files": dependency_files,
        "candidate_entrypoints": candidate_entrypoints,
        "readme_commands": readme_commands,
        "detected_algorithms": detected_algorithms,
        "recommended_skills": recommended_skills,
        "matlab": matlab_summary,
        "confidence": min(confidence, 1.0),
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--out")
    parser.add_argument("--no-json", action="store_true", help="Suppress repo_analysis.json output (default)")
    args = parser.parse_args()
    analysis = analyze_repo(args.source)
    print(json.dumps(analysis, indent=2))
    if args.out and not args.no_json:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "repo_analysis.json").write_text(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    main()
