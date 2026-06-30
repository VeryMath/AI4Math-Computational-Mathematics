# Testing

The Codex workflow is not tested as a CLI pipeline. Pytest covers helper tools and the Skill metadata contract. End-to-end reproduction is validated through Codex smoke runs.

Maintainer test command:

```bash
conda run -n ai4math pytest
```

Helper-tool tests may cover approval logging, guarded execution, toy tuning output, report templates, and plotting from toy metrics.

Skill metadata tests verify that every Skill directory has a `manifest.yaml`, that `skills/registry.yaml` covers the available Skills, and that key specialist Skills expose routed reference indexes. These tests keep the repository Skill-first by making discovery, dependencies, outputs, and approval boundaries explicit.
