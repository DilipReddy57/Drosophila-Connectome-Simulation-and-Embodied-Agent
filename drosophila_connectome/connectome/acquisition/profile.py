"""Reproducible derived graph statistics."""
from __future__ import annotations
from collections import Counter
import json
from pathlib import Path

def _rows(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
def profile(derived_root: Path) -> dict:
    neurons, edges = _rows(derived_root / "canonical_neurons.jsonl"), _rows(derived_root / "canonical_connections.jsonl")
    indegree, outdegree = Counter(), Counter()
    for edge in edges: indegree[edge["post_dense_index"]] += 1; outdegree[edge["pre_dense_index"]] += 1
    values = lambda counter: list(counter.values())
    summary = lambda counter: {"min": min(values(counter), default=0), "max": max(values(counter), default=0), "mean": sum(values(counter), 0) / len(neurons) if neurons else 0}
    field_counts = lambda field: dict(sorted(Counter(str(row[field]) for row in neurons if row.get(field) is not None).items()))
    pairs = [(edge["pre_dense_index"], edge["post_dense_index"], edge.get("region")) for edge in edges]
    return {"source_reported_statistics": {}, "derived_statistics": {"neuron_count": len(neurons), "connection_count": len(edges), "synapse_count": sum(edge["synapse_count"] for edge in edges), "in_degree": summary(indegree), "out_degree": summary(outdegree), "isolated_neurons": sum(not indegree[index] and not outdegree[index] for index in range(len(neurons))), "duplicate_edges": len(pairs) - len(set(pairs)), "self_edges": sum(edge["pre_dense_index"] == edge["post_dense_index"] for edge in edges), "cell_type_counts": field_counts("cell_type"), "super_class_counts": field_counts("super_class"), "class_counts": field_counts("class"), "neuropil_counts": field_counts("neuropil"), "side_counts": field_counts("side"), "neurotransmitter_counts": field_counts("neurotransmitter")}}
