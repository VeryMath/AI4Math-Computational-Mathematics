# Skill Routing

Use `computational_math_reproduction_workflow_skill` as the default entrypoint for end-to-end computational math research-code reproduction workflows. Route to specialist Skills as follows:

| User Intent / Stage | Specialist Skill |
| --- | --- |
| Search papers, project pages, GitHub implementations, or external algorithm candidates | `algorithm_discovery_skill` |
| Classify a broad computational math domain before choosing specialist guidance | `computational_math_domain_skill` |
| Analyze a repository, fetch source, plan commands, run approved reproduction, collect results | `repo_reproduction_skill` |
| Detect ADMM, PPA, proximal gradient, primal-dual, augmented Lagrangian, or related continuous optimization algorithms | `continuous_optimization_skill` |
| Configure or verify MATLAB CLI, Octave, MATLAB MCP, license/toolbox status, or agent tool exposure | `matlab_environment_setup_skill` |
| Handle MATLAB files, toolbox requirements, MATLAB MCP availability, or MATLAB execution plans | `matlab_runtime_skill` |
| Identify dependency files, deployment strategy, Python environment choices, and installation risks | `environment_deployment_skill` |
| Record approval decisions for high-risk operations, or enforce human-in-the-loop pauses | `human_review_skill` |
| Diagnose errors, timeouts, dependency failures, numerical failures, missing data, or unsafe commands | `failure_diagnosis_skill` |
| Design parameter spaces, choose grid/random search, and run approved tuning experiments | `auto_tuning_skill` |
| Plot convergence histories, residuals, tuning runtime, and best-so-far curves | `visualization_skill` |
| Generate compact Markdown reports: plan, run summary, tuning summary | `report_generation_skill` |

## Routing Rules

- Start with `computational_math_reproduction_workflow_skill` when more than one stage is involved.
- Add `computational_math_domain_skill` when the task is computational math but the domain is broader than, or not yet known to be, continuous optimization.
- Add `matlab_environment_setup_skill` when MATLAB execution capability itself is missing, unverified, or needs agent-platform setup.
- Add `matlab_runtime_skill` when `.m`, `.mlx`, MATLAB toolbox names, or MATLAB README commands appear.
- Add `human_review_skill` only when durable approval logs are needed for high-risk operations.
- Add `continuous_optimization_skill` for optimization repositories after domain routing or when the algorithm family is already known.
- Add `failure_diagnosis_skill` immediately after a failed or blocked run.
- Add `report_generation_skill` after reproduction, tuning, or failure diagnosis.

## Artifact Contracts

Default output tree:

```
outputs/{run_id}/
├── plan.md              # required before execution
├── RUN_SUMMARY.md        # required after run
├── logs/run.log         # execution logs
├── results/             # extracted metrics
├── figures/             # convergence/tuning plots
├── patches/             # source patches if repair was needed
├── repair_plan.md       # only if source/dependency/entrypoint/data changes needed
└── tuning/              # only if tuning approved
    ├── tuning_plan.md
    ├── tuning_results.csv
    ├── best_parameters.json
    ├── tuning.log
    ├── tuning_figures/
    └── TUNING_SUMMARY.md
```

| Specialist Skill | Input artifacts | Output artifacts | Failure route |
| --- | --- | --- | --- |
| `algorithm_discovery_skill` | task understanding, algorithm family, problem type, optional query terms | external search results, ranked candidates | `human_review_skill` for candidate selection or `failure_diagnosis_skill` for search failures |
| `computational_math_domain_skill` | source path, README/paper notes, user goal | domain classification and evidence summary | `human_review_skill` when domain evidence is ambiguous |
| `repo_reproduction_skill` | source path or fetched repository | `logs/run.log`, `results/`, `figures/`, analysis summary in `plan.md` | `failure_diagnosis_skill` |
| `continuous_optimization_skill` | repository files, paper notes, README, scripts | algorithm-family evidence in conversation | `human_review_skill` when evidence is ambiguous |
| `matlab_environment_setup_skill` | platform name, optional MATLAB root, optional MCP status | MATLAB environment report, setup plan, capability summary | `human_review_skill` before global configuration changes |
| `matlab_runtime_skill` | MATLAB files, toolbox references, optional MCP status | MATLAB runtime plan, logs, toolbox summary | `failure_diagnosis_skill` for execution failures or `human_review_skill` before MCP/config changes |
| `environment_deployment_skill` | dependency files, repo analysis, runtime constraints | environment findings in conversation | `human_review_skill` before dependency changes |
| `human_review_skill` | approval context | approval log only for high-risk operations | workflow state |
| `failure_diagnosis_skill` | failed command, stdout, stderr, logs, traceback | diagnosis in conversation, `repair_plan.md` only if source/dependency/entrypoint/data changes needed | `human_review_skill` before any fix |
| `auto_tuning_skill` | approved tuning plan, parameter space, execution command, metric | `tuning/tuning_results.csv`, `tuning/best_parameters.json`, `tuning/tuning.log` | `failure_diagnosis_skill` |
| `visualization_skill` | convergence CSV, tuning CSV, result metrics | `figures/` | `report_generation_skill` with a missing-figure note |
| `report_generation_skill` | execution logs, tuning results, figures | `plan.md`, `RUN_SUMMARY.md`, `tuning/TUNING_SUMMARY.md` | `human_review_skill` for final conclusion |

After each specialist Skill finishes, the active coding agent records evidence artifacts in conversation and updates the run directory as needed.
