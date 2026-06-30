from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tarfile
import uuid
import zipfile
from pathlib import Path


def fetch_source(source: str, out_root: Path | str = "outputs", run_id: str | None = None) -> dict:
    out_root = Path(out_root)
    run_id = run_id or f"run_{uuid.uuid4().hex[:8]}"
    run = out_root / run_id
    destination = run / "source"
    destination.parent.mkdir(parents=True, exist_ok=True)
    commit_hash = None
    source_type = "unknown"
    status = "success"

    try:
        if source.startswith("https://github.com/") or source.endswith(".git"):
            source_type = "github"
            subprocess.run(["git", "clone", "--depth", "1", source, str(destination)], timeout=300, check=True, capture_output=True, text=True)
            proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=destination, timeout=30, check=False, capture_output=True, text=True)
            commit_hash = proc.stdout.strip() or None
        else:
            path = Path(source)
            if path.is_dir():
                source_type = "local"
                if destination.exists():
                    shutil.rmtree(destination)
                shutil.copytree(path, destination, ignore=shutil.ignore_patterns(".venv", "__pycache__", ".git"))
                git_dir = path / ".git"
                if git_dir.exists():
                    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=path, timeout=30, check=False, capture_output=True, text=True)
                    commit_hash = proc.stdout.strip() or None
            elif zipfile.is_zipfile(path):
                source_type = "zip"
                destination.mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile(path) as archive:
                    archive.extractall(destination)
            elif tarfile.is_tarfile(path):
                source_type = "tar.gz"
                destination.mkdir(parents=True, exist_ok=True)
                with tarfile.open(path) as archive:
                    archive.extractall(destination)
            else:
                status = "failed"
    except Exception as exc:
        status = f"failed: {exc}"

    result = {
        "repo_path": str(destination),
        "source_type": source_type,
        "repo_name": Path(source.rstrip("/")).stem,
        "commit_hash": commit_hash,
        "fetch_status": status,
        "run_id": run_id,
    }
    run.mkdir(parents=True, exist_ok=True)
    (run / "fetch_result.json").write_text(json.dumps(result, indent=2))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--out-root", default="outputs")
    parser.add_argument("--run-id")
    args = parser.parse_args()
    print(json.dumps(fetch_source(args.source, args.out_root, args.run_id), indent=2))


if __name__ == "__main__":
    main()
