"""Data-quality validation for canonical biological records."""
from __future__ import annotations

def validate_records(neurons: list[dict], connections: list[dict], version: str) -> list[str]:
    errors: list[str] = []
    ids = [str(row.get("neuron_id")) for row in neurons]
    indices = [row.get("dense_index") for row in neurons]
    if len(ids) != len(set(ids)): errors.append("duplicate neuron IDs")
    if len(indices) != len(set(indices)): errors.append("duplicate dense indices")
    if sorted(indices) != list(range(len(indices))): errors.append("dense indices are not contiguous")
    known = set(ids)
    for row in neurons:
        if row.get("source_version") != version: errors.append("inconsistent neuron dataset version")
        if not row.get("provenance"): errors.append("missing neuron provenance")
    for row in connections:
        if str(row.get("pre_neuron_id")) not in known or str(row.get("post_neuron_id")) not in known: errors.append("missing connection endpoint")
        if row.get("pre_dense_index") not in indices or row.get("post_dense_index") not in indices: errors.append("dense index out of range")
        if row.get("synapse_count", 0) < 0: errors.append("negative synapse count")
        confidence = row.get("connection_confidence")
        if confidence is not None and not 0 <= confidence <= 1: errors.append("invalid connection confidence")
        if row.get("source_version") != version: errors.append("inconsistent connection dataset version")
        if not row.get("provenance"): errors.append("missing connection provenance")
    return sorted(set(errors))
