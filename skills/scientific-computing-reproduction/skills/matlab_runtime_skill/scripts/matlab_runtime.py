from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
from pathlib import Path


MATLAB_SOURCE_SUFFIXES = (".m", ".mlx")
MATLAB_DATA_SUFFIXES = (".mat",)
MATLAB_PROJECT_SUFFIXES = (".prj", ".slx")
MATLAB_SUFFIXES = MATLAB_SOURCE_SUFFIXES + MATLAB_DATA_SUFFIXES + MATLAB_PROJECT_SUFFIXES
IGNORED_DIRS = {".git", ".pytest_cache", "__pycache__", "outputs", ".venv", "venv", "env"}

COMMON_ENTRYPOINTS = (
    "main.m",
    "demo.m",
    "run.m",
    "experiment.m",
    "startup.m",
)

TOOLBOX_PATTERNS = {
    "Optimization Toolbox": [
        r"\boptimoptions\b",
        r"\bfmincon\b",
        r"\bquadprog\b",
        r"\blinprog\b",
        r"\blsqlin\b",
        r"\bintlinprog\b",
    ],
    "Statistics and Machine Learning Toolbox": [
        r"\bfitcsvm\b",
        r"\bfitlm\b",
        r"\bkmeans\b",
        r"\bpca\b",
    ],
    "Parallel Computing Toolbox": [
        r"\bparfor\b",
        r"\bspmd\b",
        r"\bgpuArray\b",
        r"\bparpool\b",
    ],
    "PDE Toolbox": [
        r"\bcreatepde\b",
        r"\bpdepe\b",
        r"\bsolvepde\b",
    ],
    "Signal Processing Toolbox": [
        r"\bbutter\b",
        r"\bfiltfilt\b",
        r"\bspectrogram\b",
    ],
    "CVX": [
        r"\bcvx_begin\b",
        r"\bcvx_end\b",
    ],
    "YALMIP": [
        r"\bsdpvar\b",
        r"\boptimize\s*\(",
    ],
}


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _read_text(path: Path) -> str:
    return path.read_text(errors="ignore")


def _matlab_files(source: Path) -> list[Path]:
    def is_in_ignored_dir(path: Path) -> bool:
        relative_parts = path.relative_to(source).parts
        return any(part in IGNORED_DIRS for part in relative_parts[:-1])

    return sorted(
        path
        for path in source.rglob("*")
        if path.is_file() and path.suffix in MATLAB_SUFFIXES and not is_in_ignored_dir(path)
    )


def _readme_text(source: Path) -> str:
    return "\n".join(
        path.read_text(errors="ignore")
        for path in sorted(source.glob("README*"))
        if path.is_file()
    )


def readme_matlab_commands(source: Path | str) -> list[str]:
    source = Path(source)
    commands: list[str] = []
    for line in _readme_text(source).splitlines():
        stripped = line.strip().lstrip("$").strip()
        if re.match(r"^(matlab|octave)\b", stripped, flags=re.IGNORECASE):
            commands.append(stripped)
    return commands


def _is_function_file(path: Path) -> bool:
    for line in _read_text(path).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("%"):
            continue
        return bool(re.match(r"^function\b", stripped, flags=re.IGNORECASE))
    return False


def _is_class_file(path: Path) -> bool:
    return bool(re.search(r"^\s*classdef\b", _read_text(path), flags=re.IGNORECASE | re.MULTILINE))


def _toolbox_requirements(source: Path, files: list[Path]) -> list[str]:
    text_parts = [_readme_text(source)]
    text_parts.extend(_read_text(path) for path in files if path.suffix == ".m")
    text = "\n".join(text_parts)
    found = set()

    for toolbox, patterns in TOOLBOX_PATTERNS.items():
        if toolbox.lower() in text.lower():
            found.add(toolbox)
            continue
        if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns):
            found.add(toolbox)

    return sorted(found)


def _entrypoint_from_batch_expression(expression: str) -> str | None:
    expression = expression.strip().strip('"').strip("'")
    run_match = re.search(r"run\s*\(\s*['\"]([^'\"]+\.m)['\"]\s*\)", expression)
    if run_match:
        return run_match.group(1)
    if re.match(r"^[A-Za-z]\w*$", expression):
        return f"{expression}.m"
    if expression.endswith(".m"):
        return expression
    return None


def _entrypoints_from_readme_commands(commands: list[str]) -> list[str]:
    entrypoints: list[str] = []
    for command in commands:
        try:
            parts = shlex.split(command)
        except ValueError:
            continue
        for index, part in enumerate(parts):
            if part in {"-batch", "--eval"} and index + 1 < len(parts):
                entrypoint = _entrypoint_from_batch_expression(parts[index + 1])
                if entrypoint:
                    entrypoints.append(entrypoint)
    return entrypoints


def _entrypoint_candidates(
    source: Path,
    script_files: list[str],
    readme_commands: list[str],
) -> list[str]:
    candidates: list[str] = []
    candidates.extend(_entrypoints_from_readme_commands(readme_commands))
    for name in COMMON_ENTRYPOINTS:
        if (source / name).exists():
            candidates.append(name)
    candidates.extend(
        path
        for path in script_files
        if Path(path).parent.as_posix() in {".", "examples", "scripts", "tests", "benchmarks"}
    )
    return sorted(dict.fromkeys(candidates))


def matlab_executables() -> dict[str, str | None]:
    return {
        "matlab": shutil.which("matlab"),
        "octave": shutil.which("octave"),
    }


def analyze_matlab_runtime(source: Path | str) -> dict:
    source = Path(source)
    files = _matlab_files(source)
    source_files = [path for path in files if path.suffix in MATLAB_SOURCE_SUFFIXES]
    m_files = [path for path in source_files if path.suffix == ".m"]

    function_files = [_relative(path, source) for path in m_files if _is_function_file(path)]
    class_files = [_relative(path, source) for path in m_files if _is_class_file(path)]
    script_files = [
        _relative(path, source)
        for path in m_files
        if _relative(path, source) not in function_files and _relative(path, source) not in class_files
    ]
    readme_commands = readme_matlab_commands(source)
    executables = matlab_executables()
    execution_available = any(executables.values())

    return {
        "file_counts": {suffix: sum(1 for path in files if path.suffix == suffix) for suffix in MATLAB_SUFFIXES},
        "matlab_files": [_relative(path, source) for path in files],
        "script_files": script_files,
        "function_files": function_files,
        "class_files": class_files,
        "live_scripts": [_relative(path, source) for path in files if path.suffix == ".mlx"],
        "data_files": [_relative(path, source) for path in files if path.suffix == ".mat"],
        "project_files": [_relative(path, source) for path in files if path.suffix in MATLAB_PROJECT_SUFFIXES],
        "entrypoint_candidates": _entrypoint_candidates(source, script_files, readme_commands),
        "readme_commands": readme_commands,
        "toolbox_requirements": _toolbox_requirements(source, files),
        "executables": executables,
        "mcp": {
            "status": "not_checked",
            "capabilities": [
                "detect_matlab_toolboxes",
                "check_matlab_code",
                "run_matlab_file",
                "run_matlab_test_file",
                "evaluate_matlab_code",
            ],
        },
        "execution_available": execution_available,
        "warnings": [] if execution_available else ["No matlab or octave executable detected on PATH."],
    }


def _risk_level_for_matlab_command(command: list[str]) -> str:
    lowered = " ".join(command).lower()
    if any(token in lowered for token in ("sudo", "rm -rf", "curl", "wget", "| bash")):
        return "high"
    return "medium"


def _matlab_batch_for_entrypoint(entrypoint: str) -> str:
    if entrypoint.endswith(".m"):
        return f"run('{entrypoint}')"
    return entrypoint


def make_matlab_run_plans(analysis: dict) -> list[dict]:
    source = Path(analysis["repo_path"])
    summary = analysis.get("matlab") or analyze_matlab_runtime(source)
    executables = summary.get("executables", {})
    plans: list[dict] = []

    for command in summary.get("readme_commands", []):
        parts = shlex.split(command)
        if not parts:
            continue
        tool = parts[0].lower()
        if tool in {"matlab", "octave"} and executables.get(tool):
            plans.append(
                {
                    "command": parts,
                    "working_dir": str(source),
                    "reason": "README provides an explicit MATLAB/Octave run command.",
                    "expected_outputs": ["stdout", "stderr", "logs/run.log", "MATLAB result files"],
                    "timeout_seconds": 600,
                    "risk_level": _risk_level_for_matlab_command(parts),
                    "requires_approval": "run_plan",
                    "runtime": "MATLAB",
                    "skill": "matlab_runtime_skill",
                }
            )

    if plans:
        return plans

    tool = "matlab" if executables.get("matlab") else "octave" if executables.get("octave") else None
    if not tool:
        return []

    for entrypoint in summary.get("entrypoint_candidates", [])[:3]:
        if tool == "matlab":
            command = ["matlab", "-batch", _matlab_batch_for_entrypoint(entrypoint)]
        else:
            command = ["octave", "--quiet", "--eval", _matlab_batch_for_entrypoint(entrypoint)]
        plans.append(
            {
                "command": command,
                "working_dir": str(source),
                "reason": f"Detected MATLAB entrypoint {entrypoint}.",
                "expected_outputs": ["stdout", "stderr", "logs/run.log", "MATLAB result files"],
                "timeout_seconds": 600,
                "risk_level": _risk_level_for_matlab_command(command),
                "requires_approval": "run_plan",
                "runtime": "MATLAB",
                "skill": "matlab_runtime_skill",
            }
        )
    return plans


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()

    summary = analyze_matlab_runtime(args.source)
    print(json.dumps(summary, indent=2))
    if args.out:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "matlab_runtime_summary.json").write_text(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
