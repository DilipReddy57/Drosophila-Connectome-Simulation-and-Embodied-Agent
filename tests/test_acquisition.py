from __future__ import annotations
import json, shutil
from pathlib import Path
import pytest
import polars as pl
from drosophila_connectome.connectome.acquisition.manifest import build_manifest, verify_manifest
from drosophila_connectome.connectome.acquisition.normalization import normalize_dataset, threshold_variants

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/fafb_v783"

def config():
    value = json.loads((ROOT / "configs/fafb_v783.json").read_text())
    for artifact in value["files"]: artifact["source_url"] = "https://flywire.ai/test-fixture"
    return value

def setup_raw(tmp_path):
    raw = tmp_path / "raw"; shutil.copytree(FIXTURE, raw); return raw

# --- UNIT TESTS ---

def test_manifest_hash_and_raw_immutability(tmp_path):
    raw = setup_raw(tmp_path); before = {p.name: p.read_bytes() for p in raw.iterdir()}
    path = tmp_path / "manifest.json"; build_manifest(config(), raw, path)
    assert verify_manifest(path, override_raw_root=raw) == []
    (raw / "classification.csv.gz").write_text("changed")
    assert "hash mismatch" in verify_manifest(path, override_raw_root=raw)[0]
    for name, content in before.items():
        if name != "classification.csv.gz": assert (raw / name).read_bytes() == content

def test_normalization_mapping_aggregation_thresholds_provenance_and_profile(tmp_path):
    raw = setup_raw(tmp_path); derived = tmp_path / "derived"; before = {p.name: p.read_bytes() for p in raw.iterdir()}
    result = normalize_dataset(config(), raw, derived)

    neurons = pl.read_parquet(derived / "neurons.parquet")
    connections = pl.read_parquet(derived / "connections.parquet")

    assert neurons["neuron_id"].to_list() == ["10", "20", "30"]
    assert neurons["dense_index"].to_list() == [0, 1, 2]

    # Check connection
    conn_list = connections.to_dicts()
    assert conn_list[1]["synapse_count"] == 5 and conn_list[1]["pre_neuron_id"] == "10"

    # threshold variants
    tv = threshold_variants(connections)
    assert {key: df.height for key, df in tv.items()} == {0: 4, 3: 2, 5: 1, 10: 0}

    # provenance and stats report
    report = json.loads((derived / "normalization_report.json").read_text())
    assert "duplicate_group_count" in report
    assert report["minimum_observed_synapse_count"] == 1
    assert report["threshold_units"] == "synapse_count"
    assert "connections_princeton.csv.gz" in report["threshold_provenance"]

    assert {p.name: p.read_bytes() for p in raw.iterdir()} == before

# --- REAL-DATA INTEGRATION TEST ---

def test_real_data_smoke_test(tmp_path):
    # This proves the real pipeline can run locally on gigabytes of data reliably.
    # It reads from data/raw/fafb_v783 (the actual dataset).
    raw_dir = ROOT / "data" / "raw" / "fafb_v783"
    if not raw_dir.exists() or len(list(raw_dir.glob("*.csv.gz"))) < 5:
        pytest.skip("Real data not found locally. Skipping smoke test.")

    derived = tmp_path / "real_derived"

    # Run the actual normalization pipeline
    res = normalize_dataset(json.loads((ROOT / "configs/fafb_v783.json").read_text()), raw_dir, derived)

    # Ensure reports exist
    assert (derived / "normalization_report.json").exists()
    assert (derived / "profile.json").exists()

    # Check that parquet files were generated and have biological scale rows
    assert pl.read_parquet(derived / "neurons.parquet").height > 100_000
    assert pl.read_parquet(derived / "connections.parquet").height > 5_000_000
