# Failure Diagnosis Reference Index

Use this index after a command fails, times out, produces unusable output, or produces suspicious numerical results. The purpose is to route diagnosis by observable signal and preserve the approval boundary before repair.

## Signal Routing

| Trigger | Read | Do not |
| --- | --- | --- |
| `ModuleNotFoundError`, `ImportError`, package resolver errors, missing optional dependency | `failure_diagnosis_skill/SKILL.md` dependency workflow | Do not install or upgrade dependencies without human approval. |
| Missing file, missing dataset, bad relative path, failed download, empty input directory | `failure_diagnosis_skill/SKILL.md` missing-data workflow | Do not fabricate data or silently switch datasets. |
| No entrypoint, README command fails, argument parsing error, wrong working directory | `failure_diagnosis_skill/SKILL.md` missing-entrypoint workflow | Do not rewrite the source before checking documented commands and nearby scripts. |
| Timeout, hanging process, long tuning run, no progress output | `failure_diagnosis_skill/SKILL.md` timeout workflow | Do not rerun indefinitely; propose a bounded command and timeout. |
| NaN, Inf, exploding residual, objective divergence, infeasible constraints | `failure_diagnosis_skill/SKILL.md` numerical-failure workflow | Do not report reproduction success just because the script exited. |
| Permission denied, high-risk shell command, write outside run directory | `failure_diagnosis_skill/SKILL.md` safety workflow | Do not bypass permissions or run high-risk commands automatically. |

## Repair Boundary

| Repair type | Required artifact | Approval required |
| --- | --- | --- |
| Source edit | `repair_plan.md` | yes |
| Dependency change | `repair_plan.md` | yes |
| Entrypoint or command change | `repair_plan.md` | yes |
| Data path or adapter change | `repair_plan.md` | yes |
| Pure explanation with existing logs | Conversation summary only | no |

## Evidence Checklist

Before proposing a fix, inspect:

- the approved command and working directory;
- `logs/run.log` or equivalent stdout/stderr capture;
- the first failing stack frame in user or target-repo code;
- dependency files such as `requirements.txt`, `pyproject.toml`, `environment.yml`, or README setup sections;
- whether the failure changes the reproduction status or only blocks optional visualization/tuning.

## Preflight Response Pattern

When this index is used, state a compact line in conversation:

```text
Preflight: failure_diagnosis_skill/references/INDEX.md -> numerical_failure
```

Then report the failure type, concrete signal, and next approved action. Keep raw tracebacks in `logs/run.log`; avoid pasting large logs into `repair_plan.md`.

