# Invariant Computation

Chinese guide: [README.zh-CN.md](README.zh-CN.md)

`invariant-computation` is an AI4Math Skill adapter for computing and validating topological, geometric, and algebraic invariant computations with coding agents.

## What This Skill Does

This standalone skill helps a coding agent compute, route, and validate
invariants for algebraic, topological, geometric, TDA, and certified numerical
questions. It focuses on turning the user's mathematical object into a reviewed
computational representation, choosing an appropriate method/backend, recording
conventions, and validating the result before making claims.

Use it directly when the task names an object plus an invariant, or when the
agent must first determine which invariant computation is appropriate.

## What This Is

Use this Skill when a mathematical task asks an agent to:

- compute or route computations for homology, cohomology, Betti numbers, torsion, Euler characteristic, persistent homology, knot or manifold invariants, Alexander polynomials, Jones polynomials, HOMFLY-PT polynomials, signatures, determinants, linking numbers, group homology, Hilbert series, Betti tables, primary decomposition, dimension, degree, or related invariants;
- turn a prose, LaTeX, code, triangulation, complex, filtration, group presentation, or ideal into a reviewed computational representation;
- choose among exact combinatorial, symbolic algebraic, TDA, low-dimensional topology, or certified numerical methods.

Do not use this Skill when the task is only ordinary numerical optimization, paper triage, or proof formalization without an invariant-computation target.

## What You Install Or Load

The product is the shared Skill layer, not a CLI-first package.

| File | Purpose |
| --- | --- |
| `AGENTS.md` | universal coding-agent contract |
| `SKILL.md` | top-level compatibility entrypoint |
| `skills/invariant-computation/SKILL.md` | concrete workflow Skill |
| `skills/invariant-computation/references/` | method routes, tool catalog, checks, sources |
| `CLAUDE.md` | Claude Code adapter |
| `GEMINI.md` | Gemini adapter |
| `.codex/INSTALL.md` | Codex loading notes |
| `.opencode/INSTALL.md` | OpenCode loading notes |

## Installation / Loading

### One-line Agent Install

Copy this to your coding agent:

```text
Please install the `invariant-computation` skill from https://github.com/VeryMath/AI4Math-Computational-Mathematics.git (branch: codex/ai4math-invariant-computing-skill). Read `.agent.md`, install the declared Skill entrypoint, verify that `$invariant-computation` is discoverable, and tell me whether I need to restart the agent.
```

If you already have this skill repository locally, replace the repository URL
with the local folder path. The coding agent should handle cloning, linking,
configuration, reload/restart checks, and verification.

## Quick Start

```text
Use this repository's invariant-computation workflow.

Read:
- AGENTS.md
- SKILL.md
- skills/invariant-computation/SKILL.md

Goal:
<describe the mathematical object and invariant you want>

Target:
<local path, equations, triangulation, filtration, group presentation, ideal, knot diagram, dataset, or paper excerpt>

Constraints:
- inspect first;
- build a computation checkpoint before execution;
- ask before dependency changes, long runs, source edits, API calls, or final claims.
```

## How To Interact

The normal interface is a checkpoint loop:

```text
object and requested invariant
  -> representation checkpoint
  -> method and backend route
  -> approve / revise / reject / skip
  -> approved computation or command draft
  -> validation and evidence report
```

Use `approve` to run the proposed next step, `revise` to update the route, `reject` to stop the path, `skip` to move past a phase, and `stop` to end the session and summarize state.

## Example Session

```text
User:
Use this Skill to compute the homology of this simplicial complex.
Do not install packages yet. First inspect and propose the route.

Agent:
I will identify the object representation, coefficient ring, and candidate
backends, then write a computation checkpoint before running anything.

User:
approve the read-only route check.

Agent:
[reports closure checks, candidate tools, expected outputs, and next approval]
```

## Workflow And Outputs

Prefer this evidence layout when durable artifacts are useful:

```text
outputs/<run_id>/
├── input_summary.md
├── representation_checkpoint.md
├── route_plan.md
├── commands/
├── logs/
├── results/invariant_summary.json
├── validation_report.md
└── RUN_SUMMARY.md
```

Only create the files that the task needs.

## Safety And Review Rules

- Ask before installing mathematical packages or changing environments.
- Ask before long computations, expensive enumeration, or source edits.
- Record coefficient rings, orientations, grading conventions, variable order, filtration direction, and software versions.
- Prefer exact methods for finite combinatorial or symbolic inputs.
- Use certified or interval-backed routes for numerical geometry when available.
- Do not claim that invariants classify objects unless a cited theorem supports the claim.

## Repository Layout

```text
AGENTS.md
SKILL.md
skills/
  invariant-computation/
    SKILL.md
    agents/openai.yaml
    manifest.yaml
    references/
tests/
```

## Maintainer Checks

Run:

```bash
python <path-to-skill-creator>/scripts/quick_validate.py skills/invariant-computation
python3 -m unittest discover -s tests -v
```

Then check that adapter files point back to the shared Skill layer and that no local absolute paths or private tokens were added.

## License

See [LICENSE](LICENSE).
