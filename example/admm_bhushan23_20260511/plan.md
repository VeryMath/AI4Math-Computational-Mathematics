# ADMM Reproduction Plan

## Task Interpretation

Reproduce a minimal ADMM experiment from `bhushan23/ADMM`, focused on the repository's NumPy implementation in `admm.py`.

Selected source:

- Repository: https://github.com/bhushan23/ADMM
- Local source: `/Users/conanxu/Scientific Computing Reproduction & Auto-Tuning /outputs/admm_bhushan23_20260511/source/ADMM`
- Run directory: `/Users/conanxu/Scientific Computing Reproduction & Auto-Tuning /outputs/admm_bhushan23_20260511`

## Source Inspection Evidence

- README describes ADMM for Lasso and Ridge regression and includes existing result images.
- `admm.py` implements an `ADMM` class with Lasso objective and ADMM update variables `X`, `Z`, `nu`, and `rho`.
- `test.py` is the smallest script but instantiates `ADMM(A, b, parallel=True)`.
- Algorithm detector result: `ADMM`, confidence `0.95`.
- Current `ai4math` environment:
  - Python 3.13.13
  - NumPy 2.4.4
  - joblib 1.5.3
  - scikit-learn available
  - matplotlib available
  - PyTorch not available

## Candidate Command

Run a minimal non-parallel Lasso objective experiment using the repository's `admm.py` without modifying source files:

```bash
conda run -n ai4math python - <<'PY'
import csv
from pathlib import Path
import numpy as np
from admm import ADMM

np.random.seed(0)
num_iterations = 20
N = 100
D = 20

A = np.random.randn(N, D)
b = np.random.randn(N, 1)
admm = ADMM(A, b, parallel=False)

objectives = [float(admm.LassoObjective())]
for _ in range(num_iterations):
    admm.step()
    objectives.append(float(admm.LassoObjective()))

out = Path("/Users/conanxu/Scientific Computing Reproduction & Auto-Tuning /outputs/admm_bhushan23_20260511/results/lasso_objective.csv")
out.parent.mkdir(parents=True, exist_ok=True)
with out.open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["iteration", "objective"])
    for i, value in enumerate(objectives):
        writer.writerow([i, value])

print("initial_objective", objectives[0])
print("final_objective", objectives[-1])
print("min_objective", min(objectives))
print("wrote", out)
PY
```

Working directory:

```text
/Users/conanxu/Scientific Computing Reproduction & Auto-Tuning /outputs/admm_bhushan23_20260511/source/ADMM
```

Execution wrapper will enforce a 120 second timeout and save stdout/stderr to:

```text
/Users/conanxu/Scientific Computing Reproduction & Auto-Tuning /outputs/admm_bhushan23_20260511/logs/run.log
```

## Why This Command

The repository's `test.py` uses `parallel=True`, which reaches `np.asscalar` in `admm.py`. That API is removed in the installed NumPy 2.4.4, and the multiprocessing return values are not written back to parent state. The proposed first run uses the repository's serial ADMM update path, which is the smallest meaningful experiment likely to execute in the current environment without source edits or dependency installs.

`pytorch_test.py` is not selected because it relies on a custom `torch.optim.ADMM` that is not present in the current environment, and PyTorch is not installed in `ai4math`.

## Risk Level

Low.

Reasons:

- Uses a small synthetic random matrix.
- Does not install dependencies.
- Does not modify source files.
- Writes only under the approved run directory in `outputs/`.
- Timeout is 120 seconds.

## Expected Evidence

- `logs/run.log` contains initial, final, and minimum Lasso objective values.
- `results/lasso_objective.csv` contains the objective trace for iterations 0 through 20.
- A successful minimal reproduction should show a finite objective trace and no Python traceback.

## Failure Handling

If the command fails, Codex will inspect `logs/run.log`, write `repair_plan.md` only if a source edit, dependency change, entrypoint change, or adapter is needed, and ask for approval before making any such change.

## Approval Request

Please reply with exactly one of:

- `approve`
- `revise`
- `reject`
- `skip`
