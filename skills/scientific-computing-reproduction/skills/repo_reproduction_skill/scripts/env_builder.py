from __future__ import annotations

import argparse
import platform
import subprocess
import sys
import venv
from pathlib import Path


def build_python_env(source: Path | str, out: Path | str) -> dict:
    source = Path(source)
    out = Path(out)
    logs = out / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    env_dir = out / ".venv"
    venv.EnvBuilder(with_pip=True, clear=False).create(env_dir)
    python = env_dir / "bin" / "python"
    install_log = logs / "install_log.txt"
    commands = []
    if (source / "requirements.txt").exists():
        commands.append([str(python), "-m", "pip", "install", "-r", str(source / "requirements.txt")])
    elif (source / "pyproject.toml").exists() or (source / "setup.py").exists():
        commands.append([str(python), "-m", "pip", "install", "-e", str(source)])
    status = "no_dependencies"
    with install_log.open("w") as handle:
        for command in commands:
            proc = subprocess.run(command, capture_output=True, text=True, timeout=600, check=False)
            handle.write(f"$ {' '.join(command)}\n{proc.stdout}\n{proc.stderr}\n")
            status = "success" if proc.returncode == 0 else "failed"
            if proc.returncode != 0:
                break
        freeze = subprocess.run([str(python), "-m", "pip", "freeze"], capture_output=True, text=True, timeout=60, check=False)
    report = out / "environment_report.md"
    report.write_text(f"""# Environment Report

- OS: {platform.platform()}
- Python version: {sys.version.split()[0]}
- Virtualenv: {env_dir}
- Installation status: {status}
- Installation log: `{install_log}`

## pip freeze
```text
{freeze.stdout if commands else ''}
```
""")
    return {"venv": str(env_dir), "installation_status": status, "environment_report": str(report)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    print(build_python_env(args.source, args.out))


if __name__ == "__main__":
    main()
