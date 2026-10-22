"""Resolve public Skill names and existing Python directory names."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent


def load_registry() -> dict:
    """Read the existing registry and check its local routing references."""
    registry = yaml.safe_load((ROOT / "registry.yaml").read_text(encoding="utf-8"))
    aliases = {}
    for entry in registry["skills"]:
        skill_file = ROOT / entry["path"] / "SKILL.md"
        text = skill_file.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            raise ValueError(f"Missing frontmatter: {skill_file}")
        frontmatter = yaml.safe_load(text.split("---", 2)[1])
        if frontmatter["name"] != entry["skill_name"]:
            raise ValueError(f"Skill name differs from frontmatter: {entry['path']}")
        for alias in (entry["name"], entry["skill_name"]):
            if alias in aliases and aliases[alias] is not entry:
                raise ValueError(f"Ambiguous Skill name: {alias}")
            aliases[alias] = entry
    if registry["default_entrypoint"] not in aliases:
        raise ValueError("Unknown default entrypoint")
    for entry in registry["skills"]:
        for dependency in entry.get("requires_skills", []):
            if dependency not in aliases:
                raise ValueError(f"Unknown dependency: {dependency}")
        for dependency in entry.get("requires_external_skills", []):
            if not all(dependency.get(key) for key in ("name", "version", "source")):
                raise ValueError(f"Incomplete external dependency for {entry['skill_name']}")
    return registry


def resolve_skill(name: str) -> dict:
    """Return one entry for either spelling; preserve Python import paths."""
    for entry in load_registry()["skills"]:
        if name in (entry["name"], entry["skill_name"]):
            return dict(entry)
    raise ValueError(f"Unknown Skill: {name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", nargs="?", help="Public name or existing directory name")
    args = parser.parse_args()
    if args.name:
        entry = resolve_skill(args.name)
        print(f"{entry['skill_name']}: skills/{entry['path']}/SKILL.md")
        for name in entry.get("requires_skills", []):
            dependency = resolve_skill(name)
            print(f"  requires {dependency['skill_name']}: skills/{dependency['path']}/SKILL.md")
        for dependency in entry.get("requires_external_skills", []):
            print(f"  requires external {dependency['name']} ({dependency['version']}): {dependency['source']}")
    else:
        registry = load_registry()
        print(f"Checked {len(registry['skills'])} Skill names, paths, and dependency references.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
