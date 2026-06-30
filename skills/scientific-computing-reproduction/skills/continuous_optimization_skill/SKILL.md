---
name: continuous-optimization-skill
description: This skill should be used when the user asks to detect what algorithm family a piece of code uses, identify optimization methods, or classify computational math approaches such as ADMM, PPA, proximal gradient, or primal-dual methods.
---

# Continuous Optimization Skill

Detects continuous optimization algorithm families in source code using regex pattern matching.

For end-to-end computational math research-code reproduction workflows, this Skill should be selected by `computational_math_reproduction_workflow_skill` rather than used as the first entrypoint.

## Script

### algorithm_detector
Input: `--source <path>`. Output: `algorithm_detection.json`

Detects: ADMM, PPA, proximal gradient, primal-dual, augmented Lagrangian, gradient descent, coordinate descent.

```bash
python -m skills.continuous_optimization_skill.scripts.algorithm_detector --source /path/to/repo --out /path/to/output
```

## Workflow

1. Run against the target source directory
2. Review detected algorithm and confidence
3. If confidence is low, ask user for clarification about the algorithm family
4. Feed the detected algorithm into repo_reproduction_skill or auto_tuning_skill as context
