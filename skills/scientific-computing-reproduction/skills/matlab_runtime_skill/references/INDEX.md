# MATLAB Runtime Reference Index

Use this index when MATLAB appears in a computational math reproduction task.

## Signal Routing

| Trigger | Read | Do not |
| --- | --- | --- |
| `.m` script or function | `matlab_runtime_skill/SKILL.md` execution boundary | Do not paste long MATLAB programs into inline evaluation. Prefer file-based execution. |
| `.mlx` Live Script | `matlab_runtime_skill/SKILL.md` execution boundary | Do not assume plain-text execution unless the file has been converted or inspected. |
| MATLAB toolbox name in README or errors | `detect_matlab_toolboxes` capability if available | Do not claim missing toolbox without checking installed products when MCP is available. |
| Existing MATLAB tests | `run_matlab_test_file` capability if available | Do not treat a script run as a test-suite result. |
| MATLAB MCP unavailable, but `matlab` or `octave` exists | CLI run plan from `matlab_runtime.py` / `run_planner.py` | Do not execute before run-plan approval. |
| MATLAB MCP and CLI unavailable | Codex setup reference in `matlab_runtime_skill/SKILL.md` | Do not report MATLAB execution evidence without a tool call or external log. |

## Runtime Decision Table

| Condition | Action |
| --- | --- |
| MATLAB files present, MCP unavailable, CLI available | Create a `matlab -batch` or `octave --eval` run plan and ask for approval. |
| MATLAB files present, MCP and CLI unavailable | Create a runtime plan and ask whether to configure MATLAB MCP, install MATLAB/Octave separately, or proceed with static analysis. |
| MATLAB files present, MCP available | Include exact MATLAB command/tool call in `plan.md`, request approval, then execute. |
| MATLAB code is part of a mixed Python/MATLAB repo | Use `computational_math_domain_skill` for domain routing and this Skill only for MATLAB execution details. |
| MATLAB execution fails | Route to `failure_diagnosis_skill` with logs and toolbox/version evidence. |

## Evidence Checklist

Before running MATLAB code, identify:

- MATLAB entrypoint file;
- required toolbox names;
- expected output files, figures, metrics, or test results;
- working directory;
- timeout;
- whether the command writes outside `outputs/{run_id}/`.

## Preflight Response Pattern

```text
Preflight: matlab_runtime_skill/references/INDEX.md -> MATLAB MCP available/unavailable
```

Then state whether MATLAB will be used for execution or only static analysis.
