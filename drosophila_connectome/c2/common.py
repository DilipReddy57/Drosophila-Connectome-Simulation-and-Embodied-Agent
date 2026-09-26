"""Common utilities for C2 Graph Analytics and Validation."""

import json
import hashlib
from pathlib import Path
import polars as pl

ROOT = Path(__file__).resolve().parents[2]
C1_CANONICAL_DIR = ROOT / "data/derived/final_v1"

# Pinned C1 Merge Commit
C1_COMMIT = "93603efdf845f691e581f1771af3630c3bb72218"

# Pinned Canonical Output Hashes (for final_v1 directory)
PINNED_HASHES = {
    "connections.parquet": "653738121089ce697ff489e3d92f82b83c5da2549dacdd9858b16f91c543e853",
    "dense_id_mapping.parquet": "b785ce4aa4fe0857a4cf2b654ff78a73282b66302fa2138a86956d346a550aa3",
    "neurons.parquet": "c132e6d98ab19f501fa5199cf6511184da7943cf06b3d91f5457cb16031e67bf"
}

# Raw input hashes (for provenance)
RAW_HASHES = {
    "classification.csv.gz": "e946b552f4056dfc977707be0674609832c3f64332a22d69dc0d9615e7aae663",
    "connections_princeton.csv.gz": "445f996bf6c4b1803b9ba186189138a3061ff8623aa94c0abcf38af30a5bd48b",
    "consolidated_cell_types.csv.gz": "8aba246d71dc40361677493629972ce3883048c3d02010adc42bda22962a1a2d",
    "names.csv.gz": "e541ef9ef4b9e62d798f165ae76853d15b84174cf1dce95392f313a491055332",
    "neurons.csv.gz": "6a6b3759e635f0f35a677d169052362131ec61d95f55919298b55c43fce4e719"
}

def verify_file_hash(path: Path, expected: str) -> None:
    """Verify the SHA-256 hash of a file."""
    if not path.exists():
        raise FileNotFoundError(f"Missing pinned C1 output: {path}")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError(f"Hash mismatch for {path.name}.\nExpected: {expected}\nActual:   {actual}")

def load_canonical_data(verify: bool = True) -> tuple[pl.DataFrame, pl.DataFrame]:
    """
    Load the canonical C1 output, verifying hashes by default.
    Returns (neurons, connections) DataFrames.
    """
    if verify:
        verify_file_hash(C1_CANONICAL_DIR / "neurons.parquet", PINNED_HASHES["neurons.parquet"])
        verify_file_hash(C1_CANONICAL_DIR / "connections.parquet", PINNED_HASHES["connections.parquet"])
        verify_file_hash(C1_CANONICAL_DIR / "dense_id_mapping.parquet", PINNED_HASHES["dense_id_mapping.parquet"])
        
    neurons = pl.read_parquet(C1_CANONICAL_DIR / "neurons.parquet")
    connections = pl.read_parquet(C1_CANONICAL_DIR / "connections.parquet")
    return neurons, connections

def write_c2_report(
    agent_name: str,
    metrics: dict,
    report_md: str,
    output_dir: Path
) -> None:
    """Write agent-specific output payload and markdown report."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    payload = {
        "agent": agent_name,
        "c1_commit": C1_COMMIT,
        "dataset": "FAFB v783",
        "raw_hashes": RAW_HASHES,
        "pinned_canonical_hashes": PINNED_HASHES,
        "metrics": metrics
    }
    
    with (output_dir / f"{agent_name}.json").open("w") as f:
        json.dump(payload, f, indent=2)
        
    with (output_dir / f"{agent_name}_report.md").open("w") as f:
        f.write(report_md)
