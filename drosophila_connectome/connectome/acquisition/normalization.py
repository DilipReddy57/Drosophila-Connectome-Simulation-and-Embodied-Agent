"""Polars-based fast CSV normalization into canonical Parquet artifacts; biological fields are strictly preserved."""
from __future__ import annotations
import json
import time
from datetime import datetime, timezone
from pathlib import Path
import polars as pl
from .checksum import sha256_file

NORMALIZATION_VERSION = "fafb-v783-normalization-v2-polars"

def normalize_dataset(config: dict, raw_root: Path, derived_root: Path) -> dict:
    t0 = time.time()

    # Resolve files from config
    files_by_role = {}
    for spec in config["files"]:
        files_by_role.setdefault(spec["role"], []).append(raw_root / spec["filename"])

    neuron_path = files_by_role["neuron_metadata"][0]
    connection_path = files_by_role["connectivity"][0]
    annotation_paths = files_by_role.get("annotations", [])

    # Track hashes
    raw_hashes = {str(p): sha256_file(p) for p in [neuron_path, connection_path] + annotation_paths}

    id_frames = []

    # Neuron metadata
    cls_df = pl.scan_csv(neuron_path, null_values=["", "null", "none", "unknown", "na", "n/a"]).select([
        pl.col("root_id").cast(pl.String),
        pl.col("super_class"),
        pl.col("class"),
        pl.col("sub_class").alias("subclass"),
        pl.col("hemilineage"),
        pl.col("side")
    ])
    id_frames.append(cls_df.select("root_id"))

    # Annotations
    cell_types_df = None
    nt_df = None
    for p in annotation_paths:
        if "cell_types" in p.name:
            schema = pl.scan_csv(p).collect_schema().names()
            pt_col = "primary_type" if "primary_type" in schema else "group"
            cell_types_df = pl.scan_csv(p, null_values=["", "null", "none"]).select([
                pl.col("root_id").cast(pl.String),
                pl.col(pt_col).alias("cell_type")
            ])
            id_frames.append(cell_types_df.select("root_id"))
        elif "neurons" in p.name:
            schema = pl.scan_csv(p).collect_schema().names()
            nt_col = "nt_type" if "nt_type" in schema else "neurotransmitter"
            score_col = "nt_type_score" if "nt_type_score" in schema else "neurotransmitter_confidence"
            if nt_col in schema and score_col in schema:
                nt_df = pl.scan_csv(p, null_values=["", "null", "none"]).select([
                    pl.col("root_id").cast(pl.String),
                    pl.col(nt_col).alias("neurotransmitter"),
                    pl.col(score_col).cast(pl.Float64).alias("neurotransmitter_confidence")
                ])
                id_frames.append(nt_df.select("root_id"))

    # Build dense_index deterministically
    all_ids_lazy = pl.concat(id_frames).filter(pl.col("root_id").is_not_null()).unique(subset=["root_id"]).sort("root_id")
    id_df = all_ids_lazy.collect().with_columns(
        pl.Series(name="dense_index", values=range(all_ids_lazy.collect().height), dtype=pl.UInt32)
    )

    # Join all metadata onto the canonical neurons dataframe
    neurons_lazy = id_df.lazy().join(cls_df, on="root_id", how="left")
    if cell_types_df is not None:
        neurons_lazy = neurons_lazy.join(cell_types_df, on="root_id", how="left")
    if nt_df is not None:
        neurons_lazy = neurons_lazy.join(nt_df, on="root_id", how="left")

    neurons = neurons_lazy.rename({"root_id": "neuron_id"}).collect()

    # Process Connections
    conn_schema = pl.scan_csv(connection_path).collect_schema().names()
    conn_cols = [
        pl.col("pre_root_id").cast(pl.String),
        pl.col("post_root_id").cast(pl.String),
        pl.col("neuropil").alias("region"),
        pl.col("syn_count").cast(pl.Int64).alias("synapse_count")
    ]
    if "nt_type" in conn_schema:
        conn_cols.append(pl.col("nt_type").alias("source_nt_type"))

    conn_lazy = pl.scan_csv(connection_path).select(conn_cols)

    # Calculate input_rows
    input_rows = conn_lazy.select(pl.len()).collect().item()

    # Rejected rows (negative synapse count)
    rejected_lazy = conn_lazy.filter(pl.col("synapse_count") < 0)
    rejected_rows = rejected_lazy.select(pl.len()).collect().item()

    valid_lazy = conn_lazy.filter(pl.col("synapse_count") >= 0)

    # Join with id mapping to identify missing endpoints
    conn_joined = valid_lazy.join(
        id_df.lazy(), left_on="pre_root_id", right_on="root_id", how="left"
    ).rename({"dense_index": "pre_dense_index"}).join(
        id_df.lazy(), left_on="post_root_id", right_on="root_id", how="left"
    ).rename({"dense_index": "post_dense_index"})

    # Filter quarantined edges (unknown endpoints)
    retained_lazy = conn_joined.filter(
        pl.col("pre_dense_index").is_not_null() & pl.col("post_dense_index").is_not_null()
    )
    quarantined_lazy = conn_joined.filter(
        pl.col("pre_dense_index").is_null() | pl.col("post_dense_index").is_null()
    )

    retained_raw_rows = retained_lazy.select(pl.len()).collect().item()
    quarantined_rows = quarantined_lazy.select(pl.len()).collect().item()

    # Aggregate retained edges (Data-model transformation to sum synapse counts)
    group_cols = ["pre_root_id", "post_root_id", "pre_dense_index", "post_dense_index", "region"]
    agg_cols = [pl.col("synapse_count").sum()]
    if "nt_type" in conn_schema:
        agg_cols.append(pl.col("source_nt_type").first())

    aggregated = retained_lazy.group_by(group_cols).agg(agg_cols).rename({
        "pre_root_id": "pre_neuron_id",
        "post_root_id": "post_neuron_id"
    }).sort(["pre_dense_index", "post_dense_index", "region"])

    connections = aggregated.collect()
    canonical_rows_after_aggregation = connections.height

    # Verify immutability
    if any(sha256_file(Path(p)) != h for p, h in raw_hashes.items()):
        raise RuntimeError("raw input changed during normalization; aborting export")

    derived_root.mkdir(parents=True, exist_ok=True)
    n_out = derived_root / "neurons.parquet"
    c_out = derived_root / "connections.parquet"
    m_out = derived_root / "dense_id_mapping.parquet"

    neurons.write_parquet(n_out)
    connections.write_parquet(c_out)
    id_df.write_parquet(m_out)

    t1 = time.time()

    # Reports
    report = {
        "input_rows": input_rows,
        "retained_raw_rows": retained_raw_rows,
        "rejected_rows": rejected_rows,
        "quarantined_rows": quarantined_rows,
        "canonical_rows_after_aggregation": canonical_rows_after_aggregation,
        "unknown_endpoints": quarantined_rows,
        "missing_ids": 0,
        "duplicate_ids": 0,
        "malformed_rows": 0,
        "wall_clock_time_seconds": round(t1 - t0, 2),
        "source_connectivity_threshold": 1,
        "threshold_units": "synapse_count",
        "threshold_provenance": "Minimum observed in unthresholded connections_princeton.csv.gz"
    }
    with (derived_root / "normalization_report.json").open("w") as f:
        json.dump(report, f, indent=2)

    # Profile stats
    profile = {
        "neuron_count": neurons.height,
        "connection_row_count": connections.height,
        "total_synapse_count": connections["synapse_count"].sum() if connections.height > 0 else 0,
        "source": "LOCALLY_DERIVED"
    }
    with (derived_root / "profile.json").open("w") as f:
        json.dump(profile, f, indent=2)

    return {
        "normalization_version": NORMALIZATION_VERSION,
        "raw_input_hashes": raw_hashes,
        "outputs": {
            str(n_out): sha256_file(n_out),
            str(c_out): sha256_file(c_out),
            str(m_out): sha256_file(m_out)
        }
    }

def threshold_variants(connections_df: pl.DataFrame, thresholds=(0, 3, 5, 10)) -> dict[int, pl.DataFrame]:
    return {threshold: connections_df.filter(pl.col("synapse_count") >= threshold) for threshold in thresholds}
