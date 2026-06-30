from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
from pathlib import Path


MATLAB_ENV_VARS = ("MATLAB_ROOT", "MATLAB_HOME")


def detect_matlab_environment() -> dict:
    executables = {
        "matlab": shutil.which("matlab"),
        "octave": shutil.which("octave"),
    }
    env_vars = {name: os.environ.get(name) for name in MATLAB_ENV_VARS if os.environ.get(name)}
    execution_mode = "MATLAB CLI" if executables["matlab"] else "Octave" if executables["octave"] else "static-only"

    return {
        "platform": platform.platform(),
        "executables": executables,
        "environment_variables": env_vars,
        "execution_mode": execution_mode,
        "mcp": {
            "status": "not_checked",
            "note": "MCP capabilities must be inspected through the active coding agent host.",
        },
        "next_step": (
            "Create an approved MATLAB runtime plan."
            if execution_mode != "static-only"
            else "Configure MATLAB CLI, Octave, or MATLAB MCP before execution."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out")
    args = parser.parse_args()

    report = detect_matlab_environment()
    print(json.dumps(report, indent=2))
    if args.out:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "matlab_environment_report.json").write_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
