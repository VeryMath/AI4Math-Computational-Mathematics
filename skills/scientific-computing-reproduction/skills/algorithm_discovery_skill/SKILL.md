---
name: algorithm-discovery-skill
description: This skill should be used when the user asks to search for external algorithms, find related implementations, discover alternative approaches, or look up papers and code for computational math optimization methods.
---

# Algorithm Discovery Skill

Use this Skill when Codex needs to search external sources such as papers, project pages, and GitHub repositories for algorithm implementations relevant to a computational math task.

For end-to-end computational math research-code reproduction workflows, this Skill should be selected by `computational_math_reproduction_workflow_skill` rather than used as the first entrypoint.

## Codex-Native Workflow

1. Restate the problem type, algorithm family, target metrics, and implementation constraints from the user goal or existing reproduction evidence.
2. Search with Codex-native browser, web, or GitHub tools first.
3. Rank candidates by algorithm match, runnable code availability, license or access risk, likely entrypoints, dependencies, and expected reproduction effort.
4. Write compact candidate notes under the run directory when durable evidence is useful.
5. Present ranked candidates to the human and wait for selection before fetching, cloning, or executing any external source.

## Optional Helper

`skills/algorithm_discovery_skill/scripts/external_search.py` is an optional helper for structured persistence or batch querying. It is not a workflow driver.

The helper can write `algorithm_candidates.json` with ranked candidates when Codex already has a structured task description and wants a repeatable artifact. Prefer native search in conversation unless the helper makes the evidence easier to reproduce.
