"""Contract checks for the repository's research-foundation artifacts."""
from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FoundationContractTests(unittest.TestCase):
    def test_json_schemas_parse_and_define_required_fields(self) -> None:
        for filename, required in {
            "dataset-manifest.schema.json": {"dataset_id", "files", "source_url"},
            "neuron.schema.json": {"neuron_id", "dense_index", "source_dataset"},
            "connection.schema.json": {"pre_dense_index", "post_dense_index", "synapse_count"},
        }.items():
            with self.subTest(filename=filename):
                schema = json.loads((ROOT / "schemas" / filename).read_text())
                self.assertTrue(required.issubset(schema["required"]))

    def test_source_registry_has_unique_ids_and_valid_tiers(self) -> None:
        with (ROOT / "research" / "source_registry" / "sources.csv").open(newline="") as handle:
            records = list(csv.DictReader(handle))
        ids = [record["source_id"] for record in records]
        self.assertTrue(records)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue({record["tier"] for record in records}.issubset({"A0", "A1", "A2", "B", "C", "D", "E"}))

    def test_manifest_template_has_acquisition_provenance_fields(self) -> None:
        manifest = json.loads((ROOT / "templates" / "dataset_manifest.json").read_text())
        for key in ("dataset_id", "version", "source_url", "license", "retrieved_at", "files"):
            self.assertIn(key, manifest)
        self.assertTrue(manifest["files"])


if __name__ == "__main__":
    unittest.main()
