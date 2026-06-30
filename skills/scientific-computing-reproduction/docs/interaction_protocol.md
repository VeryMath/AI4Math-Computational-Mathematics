# Interaction Protocol

Use this project through conversation with a coding agent. The agent should summarize evidence and ask for confirmation before running code, changing dependencies, tuning parameters, or accepting final conclusions. Codex is the primary reference operator for this protocol, but any compatible coding agent that can read files, run shell commands, and follow `SKILL.md` instructions can drive the workflow.

## Standard Loop

1. The agent states the Skill it will use.
2. The agent inspects files or searches sources.
3. The agent summarizes evidence and uncertainty.
4. The agent asks one concrete question.
5. The human replies `approve`, `revise`, `reject`, or `skip`.
6. The agent records the decision when a run directory exists.
7. The agent uses an approval gate before execution when a helper supports it.
8. The agent continues with the approved next step.

For repository reproduction, execution helpers should be called with a gate:

```bash
python -m skills.repo_reproduction_skill.scripts.executor \
  --plan outputs/<run_id>/run_plan.json \
  --out outputs/<run_id> \
  --require-approval run_plan
```

Without an `approve` record in `outputs/<run_id>/approvals/approval_log.jsonl`, this command must block instead of running external code.

## Example Questions

Task understanding:

```text
I read this as a Python continuous optimization project using ADMM for LASSO. The key metrics appear to be runtime, primal residual, and dual residual. Is this understanding correct?
```

Run plan:

```text
I found a low-risk demo command with a 300 second timeout. Do you approve running it?
```

Failure fix:

```text
The failure looks like a missing dependency. I can install declared requirements in an isolated environment. Do you approve?
```

Algorithm discovery:

```text
I found these external candidates from papers and GitHub. Candidate 1 has the closest match and available code. Which candidate should I pursue?
```

Tuning:

```text
I propose random search with budget 20 over rho, alpha, tol, and max_iter, minimizing runtime subject to residual thresholds. Do you approve?
```

Final review:

```text
The reproduction status is success based on these logs and metrics. Do you approve this final conclusion?
```
