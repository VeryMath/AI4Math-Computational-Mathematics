---
name: environment-deployment-skill
description: This skill should be used when the user asks to set up an environment, check dependencies, prepare deployment, or analyze how to run code in a specific computational environment.
---

# Environment Deployment Skill

Analyzes a repository's dependencies and recommends a deployment strategy.

For end-to-end computational math research-code reproduction workflows, this Skill should be selected by `computational_math_reproduction_workflow_skill` rather than used as the first entrypoint.

## Script

### environment_reporter
Input: `--source <path>`, `--out <path>`, `--run-role <controller|reproduction>`
- `controller`: uses shared `ai4math` conda environment
- `reproduction`: uses isolated venv

Output: `deployment_plan.json` and `environment_report.md`

```bash
python -m skills.environment_deployment_skill.scripts.environment_reporter --source /path/to/repo --out /path/to/output --run-role controller
```

## Workflow

1. Run against the source repository
2. Review deployment plan and warnings
3. Ask user to confirm or adjust the deployment strategy
4. Propose installation commands for user approval
