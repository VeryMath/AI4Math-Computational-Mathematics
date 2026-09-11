from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = (
    ROOT
    / "skills"
    / "invariant-computation"
    / "schema"
    / "invariant_summary.schema.json"
)
EXAMPLE_PATH = (
    ROOT
    / "skills"
    / "invariant-computation"
    / "examples"
    / "invariant_summary.example.json"
)


class InvariantSummarySchemaTests(unittest.TestCase):
    def load_json(self, path: Path) -> object:
        self.assertTrue(path.is_file(), f"Missing JSON contract artifact: {path}")
        with path.open(encoding="utf-8") as stream:
            return json.load(stream)

    def test_schema_is_valid_draft_2020_12(self) -> None:
        Draft202012Validator.check_schema(self.load_json(SCHEMA_PATH))

    def test_public_example_conforms_to_schema(self) -> None:
        schema = self.load_json(SCHEMA_PATH)
        example = self.load_json(EXAMPLE_PATH)

        Draft202012Validator(schema).validate(example)

    def test_remaining_uncertainty_cannot_be_omitted(self) -> None:
        schema = self.load_json(SCHEMA_PATH)
        example = copy.deepcopy(self.load_json(EXAMPLE_PATH))
        del example["remaining_uncertainty"]

        with self.assertRaises(ValidationError):
            Draft202012Validator(schema).validate(example)

    def test_theorem_backed_classification_may_omit_caveat(self) -> None:
        schema = self.load_json(SCHEMA_PATH)
        example = copy.deepcopy(self.load_json(EXAMPLE_PATH))
        del example["classification_caveat"]
        example["classification_theorem_evidence"] = (
            "validation_report.md records the theorem citation and matched hypotheses."
        )

        Draft202012Validator(schema).validate(example)

    def test_classification_requires_caveat_or_theorem_evidence(self) -> None:
        schema = self.load_json(SCHEMA_PATH)
        example = copy.deepcopy(self.load_json(EXAMPLE_PATH))
        del example["classification_caveat"]

        with self.assertRaises(ValidationError):
            Draft202012Validator(schema).validate(example)

    def test_nonfailed_result_requires_nonnull_value(self) -> None:
        schema = self.load_json(SCHEMA_PATH)
        example = self.load_json(EXAMPLE_PATH)

        for result_quality in (
            "exact",
            "certified_numerical",
            "heuristic",
            "partial",
        ):
            invalid = copy.deepcopy(example)
            invalid["invariant"]["result_quality"] = result_quality
            invalid["invariant"]["value"] = None
            if result_quality in ("heuristic", "partial"):
                invalid["remaining_uncertainty"] = ["The result is not yet conclusive."]
                invalid["next_repair_route"] = "Run a stronger validation route."

            with self.subTest(result_quality=result_quality):
                with self.assertRaises(ValidationError):
                    Draft202012Validator(schema).validate(invalid)

    def test_unsettled_result_requires_remaining_uncertainty(self) -> None:
        schema = self.load_json(SCHEMA_PATH)
        example = self.load_json(EXAMPLE_PATH)

        for result_quality in ("heuristic", "partial", "failed"):
            invalid = copy.deepcopy(example)
            invalid["invariant"]["result_quality"] = result_quality
            invalid["remaining_uncertainty"] = []
            invalid["next_repair_route"] = "Run a stronger validation route."
            if result_quality == "failed":
                invalid["invariant"]["value"] = None

            with self.subTest(result_quality=result_quality):
                with self.assertRaises(ValidationError):
                    Draft202012Validator(schema).validate(invalid)

    def test_unsettled_result_requires_next_repair_route(self) -> None:
        schema = self.load_json(SCHEMA_PATH)
        example = self.load_json(EXAMPLE_PATH)

        for result_quality in ("heuristic", "partial", "failed"):
            invalid = copy.deepcopy(example)
            invalid["invariant"]["result_quality"] = result_quality
            invalid["remaining_uncertainty"] = ["The result is not yet conclusive."]
            invalid["next_repair_route"] = None
            if result_quality == "failed":
                invalid["invariant"]["value"] = None

            with self.subTest(result_quality=result_quality):
                with self.assertRaises(ValidationError):
                    Draft202012Validator(schema).validate(invalid)

    def test_failed_result_may_use_null_value_with_repair_evidence(self) -> None:
        schema = self.load_json(SCHEMA_PATH)
        example = copy.deepcopy(self.load_json(EXAMPLE_PATH))
        example["invariant"]["result_quality"] = "failed"
        example["invariant"]["value"] = None
        example["remaining_uncertainty"] = ["The requested invariant was not computed."]
        example["next_repair_route"] = "Repair the representation and rerun validation."

        Draft202012Validator(schema).validate(example)

    def test_invalid_contract_variants_are_rejected(self) -> None:
        schema = self.load_json(SCHEMA_PATH)
        example = self.load_json(EXAMPLE_PATH)

        unsupported_version = copy.deepcopy(example)
        unsupported_version["schema_version"] = 2
        missing_version = copy.deepcopy(example)
        del missing_version["backend"]["version_evidence"]
        invalid_quality = copy.deepcopy(example)
        invalid_quality["invariant"]["result_quality"] = "proved"
        empty_checks = copy.deepcopy(example)
        empty_checks["validation_checks"] = []
        empty_theorem_evidence = copy.deepcopy(example)
        del empty_theorem_evidence["classification_caveat"]
        empty_theorem_evidence["classification_theorem_evidence"] = ""

        for label, invalid in (
            ("unsupported schema version", unsupported_version),
            ("missing backend version evidence", missing_version),
            ("unsupported result quality", invalid_quality),
            ("empty validation checks", empty_checks),
            ("empty classification theorem evidence", empty_theorem_evidence),
        ):
            with self.subTest(label=label):
                with self.assertRaises(ValidationError):
                    Draft202012Validator(schema).validate(invalid)

    def test_extension_fields_remain_forward_compatible(self) -> None:
        schema = self.load_json(SCHEMA_PATH)
        example = copy.deepcopy(self.load_json(EXAMPLE_PATH))
        example["producer_extension"] = {"name": "downstream-agent"}

        Draft202012Validator(schema).validate(example)


if __name__ == "__main__":
    unittest.main()
