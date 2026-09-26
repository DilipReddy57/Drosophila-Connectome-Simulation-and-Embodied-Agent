"""CSV normalization into canonical JSONL artifacts; biological fields are only copied when supplied."""
from __future__ import annotations
import csv, json
from datetime import datetime, timezone
from pathlib import Path
from .checksum import sha256_file
from .validation import validate_records

NORMALIZATION_VERSION = "fafb-v783-normalization-v1"
NULL = {"", "null", "none", "unknown", "na", "n/a"}

def _value(row: dict, *names: str):
    for name in names:
        value = row.get(name)
        if value is not None and str(value).strip().lower() not in NULL: return value
    return None

def _bool(value):
    return None if value is None else str(value).lower() in {"1", "true", "yes"}

def _number(value): return None if value is None else float(value)
def _read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as stream: return list(csv.DictReader(stream))
def _write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as stream:
        for row in rows: stream.write(json.dumps(row, sort_keys=True) + "\n")

def normalize_dataset(config: dict, raw_root: Path, derived_root: Path) -> dict:
    specs = {spec["role"]: spec for spec in config["files"]}
    neuron_spec, connection_spec = specs["neuron_metadata"], specs["connectivity"]
    annotation_spec = specs.get("annotations")
    neuron_path, connection_path = raw_root / neuron_spec["filename"], raw_root / connection_spec["filename"]
    raw_hashes = {str(neuron_path): sha256_file(neuron_path), str(connection_path): sha256_file(connection_path)}
    annotations = {}
    if annotation_spec:
        annotation_path = raw_root / annotation_spec["filename"]
        raw_hashes[str(annotation_path)] = sha256_file(annotation_path)
        annotations = {str(_value(row, "root_id", "neuron_id", "id")): row for row in _read(annotation_path)}
    source_rows = _read(neuron_path)
    raw_ids = [_value(row, "root_id", "neuron_id", "id") for row in source_rows]
    if any(value is None for value in raw_ids) or len(set(raw_ids)) != len(raw_ids):
        raise ValueError("neuron metadata has missing or duplicate biological IDs")
    ordered_ids = sorted(str(value) for value in raw_ids)
    if len(set(ordered_ids)) != len(ordered_ids): raise ValueError("neuron metadata has missing or duplicate biological IDs")
    mapping = {neuron_id: index for index, neuron_id in enumerate(ordered_ids)}
    created = datetime.now(timezone.utc).isoformat()
    neurons = []
    for raw in source_rows:
        neuron_id = str(_value(raw, "root_id", "neuron_id", "id")); ann = annotations.get(neuron_id, {})
        get = lambda *n: _value(ann, *n) if _value(ann, *n) is not None else _value(raw, *n)
        neurons.append({"neuron_id": neuron_id, "dense_index": mapping[neuron_id], "cell_type": get("cell_type", "type"), "super_class": get("super_class", "superclass"), "class": get("class"), "subclass": get("subclass", "sub_class"), "hemilineage": get("hemilineage"), "neuropil": get("neuropil"), "side": get("side", "hemisphere"), "neurotransmitter": get("neurotransmitter", "nt_type"), "neurotransmitter_confidence": _number(get("neurotransmitter_confidence", "nt_confidence")), "is_sensory": _bool(get("is_sensory", "sensory_in")), "is_interneuron": _bool(get("is_interneuron")), "is_motor": _bool(get("is_motor", "effector_out")), "morphology_ref": None, "source_dataset": config["dataset_id"], "source_version": config["version"], "provenance": {"raw_artifact": str(neuron_path), "raw_sha256": raw_hashes[str(neuron_path)], "source_row": None, "normalization_version": NORMALIZATION_VERSION, "generated_at": created}})
    edges = {}
    for raw in _read(connection_path):
        pre, post = str(_value(raw, "pre_root_id", "pre", "source")), str(_value(raw, "post_root_id", "post", "target"))
        if pre not in mapping or post not in mapping: raise ValueError(f"connection endpoint absent from neuron metadata: {pre}->{post}")
        count = int(_value(raw, "synapse_count", "weight", "count") or 0)
        if count < 0: raise ValueError("negative synapse count")
        region = _value(raw, "neuropil", "region")
        key = (pre, post, region)
        edges[key] = edges.get(key, 0) + count
    connections = [{"pre_neuron_id": pre, "post_neuron_id": post, "pre_dense_index": mapping[pre], "post_dense_index": mapping[post], "synapse_count": count, "region": region, "connection_confidence": None, "aggregation_method": "sum(pre_neuron_id,post_neuron_id,region)", "source_version": config["version"], "provenance": {"raw_artifact": str(connection_path), "raw_sha256": raw_hashes[str(connection_path)], "source_row": None, "normalization_version": NORMALIZATION_VERSION, "generated_at": created}} for (pre, post, region), count in sorted(edges.items())]
    if any(sha256_file(Path(path)) != digest for path, digest in raw_hashes.items()):
        raise RuntimeError("raw input changed during normalization; no derived artifact was emitted")
    errors = validate_records(neurons, connections, config["version"])
    if errors: raise ValueError("; ".join(errors))
    derived_root.mkdir(parents=True, exist_ok=True)
    neuron_out, connection_out, mapping_out = (derived_root / "canonical_neurons.jsonl", derived_root / "canonical_connections.jsonl", derived_root / "dense_id_mapping.jsonl")
    _write_jsonl(neuron_out, sorted(neurons, key=lambda row: row["dense_index"])); _write_jsonl(connection_out, connections)
    _write_jsonl(mapping_out, [{"neuron_id": key, "dense_index": value} for key, value in mapping.items()])
    return {"normalization_version": NORMALIZATION_VERSION, "raw_input_hashes": raw_hashes, "outputs": {str(path): sha256_file(path) for path in (neuron_out, connection_out, mapping_out)}, "generated_at": created}

def threshold_variants(connections: list[dict], thresholds=(0, 3, 5, 10)) -> dict[int, list[dict]]:
    return {threshold: [row for row in connections if row["synapse_count"] >= threshold] for threshold in thresholds}
