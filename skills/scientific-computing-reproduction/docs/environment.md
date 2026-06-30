# Runtime Environment

This project uses the shared AI4Math maintainer Conda environment:

```text
conda env: ai4math
python: resolved from the active conda installation
```

## Setup

If the environment does not exist, create it:

```bash
conda create -y -n ai4math python=3.13 pip
```

Install this project into the shared environment for maintainer tests and helper-script imports:

```bash
conda run -n ai4math python -m pip install -e ".[dev]"
```

## Agent-Invoked Commands

Prefer `conda run -n ai4math` for agent-invoked helper commands:

```bash
conda run -n ai4math python -m skills.repo_reproduction_skill.scripts.executor \
  --plan outputs/<run_id>/run_plan.json \
  --out outputs/<run_id> \
  --require-approval run_plan
```

This repository does not provide a user-facing CLI pipeline. Scripts are optional tools that Codex or another coding agent may call after reading the relevant Skills and getting any required approval.

For tests:

```bash
conda run -n ai4math pytest
```

## Boundary

The coding-agent Skill controller runs in `ai4math`. Reproduced third-party Python projects may still be placed in isolated environments when dependency installation is explicitly approved, because research repositories can have conflicting dependencies.
