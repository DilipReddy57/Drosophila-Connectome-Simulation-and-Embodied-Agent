from __future__ import annotations
import json, shutil
from pathlib import Path
import pytest
from drosophila_connectome.connectome.acquisition.manifest import build_manifest, verify_manifest
from drosophila_connectome.connectome.acquisition.normalization import normalize_dataset, threshold_variants
from drosophila_connectome.connectome.acquisition.profile import profile
from drosophila_connectome.connectome.acquisition.validation import validate_records

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/fafb_v783"
def config():
    value = json.loads((ROOT / "configs/fafb_v783.json").read_text())
    for artifact in value["files"]: artifact["source_url"] = "https://flywire.ai/test-fixture"
    return value
def setup_raw(tmp_path):
    raw = tmp_path / "raw"; shutil.copytree(FIXTURE, raw); return raw

def read_jsonl(path): return [json.loads(line) for line in path.read_text().splitlines()]
def test_manifest_hash_and_raw_immutability(tmp_path):
    raw = setup_raw(tmp_path); before = {p.name: p.read_bytes() for p in raw.iterdir()}
    path = tmp_path / "manifest.json"; build_manifest(config(), raw, path)
    assert verify_manifest(path) == []
    (raw / "neurons.csv").write_text("changed")
    assert "hash mismatch" in verify_manifest(path)[0]
    for name, content in before.items():
        if name != "neurons.csv": assert (raw / name).read_bytes() == content

def test_normalization_mapping_aggregation_thresholds_provenance_and_profile(tmp_path):
    raw = setup_raw(tmp_path); derived = tmp_path / "derived"; before = {p.name: p.read_bytes() for p in raw.iterdir()}
    result = normalize_dataset(config(), raw, derived)
    neurons, connections = read_jsonl(derived / "canonical_neurons.jsonl"), read_jsonl(derived / "canonical_connections.jsonl")
    assert [row["neuron_id"] for row in neurons] == ["10", "20", "30"]
    assert [row["dense_index"] for row in neurons] == [0, 1, 2]
    assert connections[0]["synapse_count"] == 5 and connections[0]["pre_neuron_id"] == "10"
    assert all(row["provenance"]["normalization_version"] == result["normalization_version"] for row in neurons + connections)
    assert {key: len(value) for key, value in threshold_variants(connections).items()} == {0: 3, 3: 2, 5: 1, 10: 0}
    assert {p.name: p.read_bytes() for p in raw.iterdir()} == before
    stats = profile(derived)["derived_statistics"]
    assert stats["neuron_count"] == 3 and stats["connection_count"] == 3 and stats["self_edges"] == 1

def test_validation_detects_quality_failures():
    neurons = [{"neuron_id": "1", "dense_index": 0, "source_version": "v", "provenance": {}}, {"neuron_id": "1", "dense_index": 2, "source_version": "wrong", "provenance": None}]
    connections = [{"pre_neuron_id": "1", "post_neuron_id": "2", "pre_dense_index": 0, "post_dense_index": 9, "synapse_count": -1, "connection_confidence": 2, "source_version": "wrong", "provenance": None}]
    errors = validate_records(neurons, connections, "v")
    assert {"duplicate neuron IDs", "dense indices are not contiguous", "missing connection endpoint", "dense index out of range", "negative synapse count", "invalid connection confidence", "missing neuron provenance", "missing connection provenance"}.issubset(errors)
