from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "invariant-computation"


class InvariantComputationSkillShapeTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        path = ROOT / relative_path
        self.assertTrue(path.is_file(), f"Missing file: {path}")
        return path.read_text(encoding="utf-8")

    def test_root_entrypoint_points_to_shared_skill_layer(self) -> None:
        text = self.read("SKILL.md")

        self.assertIn("name: invariant-computation", text)
        self.assertIn("shared Skill layer", text)
        self.assertIn("skills/invariant-computation/SKILL.md", text)

    def test_concrete_skill_frontmatter_and_core_workflow(self) -> None:
        text = self.read("skills/invariant-computation/SKILL.md")

        self.assertIn("name: invariant-computation", text)
        self.assertIn("description: Use when a coding agent must compute", text)
        for required in (
            "homology",
            "persistent homology",
            "knot or manifold invariants",
            "Alexander polynomials",
            "Jones polynomials",
            "HOMFLY-PT",
            "group homology",
            "Hilbert series",
            "primary decompositions",
            "representation_checkpoint.md",
            "Approval Rules",
            "Validation",
            "Failure Modes",
            "classification caveat",
        ):
            self.assertIn(required, text)

    def test_adapter_files_are_thin_and_reference_skill_layer(self) -> None:
        for relative_path in (
            "AGENTS.md",
            "CLAUDE.md",
            "GEMINI.md",
            ".codex/INSTALL.md",
            ".opencode/INSTALL.md",
        ):
            with self.subTest(path=relative_path):
                text = self.read(relative_path)
                self.assertIn("Skill layer", text)
                self.assertIn("skills/invariant-computation/SKILL.md", text)

    def test_readmes_explain_loading_and_interaction(self) -> None:
        english = self.read("README.md")
        chinese = self.read("README.zh-CN.md")

        for required in (
            "Installation / Loading",
            "Quick Start",
            "How To Interact",
            "approve",
            "revise",
            "reject",
            "skip",
        ):
            self.assertIn(required, english)

        for required in (
            "安装 / 加载",
            "如何交互使用",
            "approve",
            "revise",
            "reject",
            "skip",
        ):
            self.assertIn(required, chinese)

    def test_reference_files_cover_route_families_and_tools(self) -> None:
        index = self.read("skills/invariant-computation/references/INDEX.md")
        route_map = self.read("skills/invariant-computation/references/method_route_map.md")
        catalog = self.read("skills/invariant-computation/references/tool_catalog.md")
        checks = self.read("skills/invariant-computation/references/validation_checks.md")
        failures = self.read("skills/invariant-computation/references/failure_modes.md")
        sources = self.read("skills/invariant-computation/references/source_notes.md")

        for filename in (
            "method_route_map.md",
            "tool_catalog.md",
            "validation_checks.md",
            "failure_modes.md",
            "source_notes.md",
        ):
            self.assertIn(filename, index)

        for family in (
            "Finite Complexes",
            "Persistent Homology",
            "Low-Dimensional Topology And Knot Theory",
            "Group And CW Homological Algebra",
            "Algebraic Geometry And Commutative Algebra",
            "Toric, Polyhedral, And Semigroup",
            "Numerical Algebraic Geometry",
        ):
            self.assertIn(family, route_map)

        for tool in (
            "GUDHI",
            "Ripser.py",
            "SageMath",
            "GAP HAP",
            "SnapPy",
            "Spherogram",
            "Regina",
            "Macaulay2",
            "Singular",
            "OSCAR",
            "Normaliz",
        ):
            self.assertIn(tool, catalog + sources)

        for required in ("d_{n-1} d_n = 0", "Euler characteristic", "Poincare duality", "Hopf link"):
            self.assertIn(required, checks)

        for required in ("coefficient", "Groebner", "certification", "polynomial normalization", "Do not infer"):
            self.assertIn(required, failures)

    def test_metadata_files_are_present_and_consistent(self) -> None:
        openai_yaml = self.read("skills/invariant-computation/agents/openai.yaml")
        manifest = self.read("skills/invariant-computation/manifest.yaml")

        self.assertIn('display_name: "Invariant Computation"', openai_yaml)
        self.assertIn("$invariant-computation", openai_yaml)
        self.assertIn("schema_version: 1", manifest)
        self.assertIn("invariant-computation", manifest)
        self.assertIn("approval_policy", manifest)

    def test_no_template_placeholders_remain(self) -> None:
        for path in ROOT.rglob("*"):
            if (
                path.is_file()
                and ".git" not in path.parts
                and "__pycache__" not in path.parts
                and "tests" not in path.parts
            ):
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(
                    re.search(r"TODO|TBD|fill in|replace-with|<skill-name>", text),
                    f"Template placeholder remains in {path}",
                )


if __name__ == "__main__":
    unittest.main()
