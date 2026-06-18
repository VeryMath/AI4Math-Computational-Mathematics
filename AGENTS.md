# AGENTS.md

This repository is an AI4Math Skill adapter package for invariant computation across topology, geometry, and algebra.

The shared Skill layer is:

```text
skills/invariant-computation-skill/SKILL.md
```

## Contract

- Use the shared Skill layer as the workflow source of truth.
- Keep platform-specific files thin; do not fork invariant-computation workflow behavior.
- Build a representation and computation checkpoint before executable backend commands.
- Ask before dependency installs, source edits, long runs, API calls, or final mathematical claims.
- Report from saved evidence and distinguish verified invariants, heuristic evidence, and conjectural interpretation.

