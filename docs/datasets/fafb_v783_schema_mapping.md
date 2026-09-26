# FAFB v783 Source to Canonical Mapping

## Source Schema

### `classification.csv.gz` (role: neuron_metadata)
* **Columns**: `root_id` (String), `flow` (String), `super_class` (String), `class` (String), `sub_class` (String), `hemilineage` (String), `side` (String), `nerve` (String)
* **Identifier**: `root_id`
* **Connectivity**: None
* **Annotation**: `flow`, `super_class`, `class`, `sub_class`, `hemilineage`, `side`
* **Null Behavior**: Blank or "null" strings indicate missing annotations. These neurons are still valid biological objects.
* **Duplicate Behavior**: Should be unique by `root_id`.

### `consolidated_cell_types.csv.gz` (role: annotations)
* **Columns**: `root_id` (String), `primary_type` (String), `additional_type(s)` (String)
* **Identifier**: `root_id`
* **Connectivity**: None
* **Annotation**: `primary_type` -> mapped to `cell_type`
* **Null Behavior**: Missing rows mean no specific cell type annotation.
* **Duplicate Behavior**: Should be unique by `root_id`.

### `neurons.csv.gz` (role: annotations)
* **Columns**: `root_id` (String), `group` (String), `nt_type` (String), `nt_type_score` (Float), (various neurotransmitter averages...)
* **Identifier**: `root_id`
* **Connectivity**: None
* **Annotation**: `nt_type` -> `neurotransmitter`, `nt_type_score` -> `neurotransmitter_confidence`
* **Null Behavior**: Missing rows mean no neurotransmitter prediction.
* **Duplicate Behavior**: Unique by `root_id`.

### `names.csv.gz` (role: annotations)
* **Columns**: `root_id` (String), `name` (String), `group` (String)
* **Identifier**: `root_id`
* **Connectivity**: None
* **Annotation**: (Used for group mapping if needed, generally supplementary).

### `connections_princeton.csv.gz` (role: connectivity)
* **Columns**: `pre_root_id` (String), `post_root_id` (String), `neuropil` (String), `syn_count` (Int64), `nt_type` (String)
* **Identifier**: None (Edge list)
* **Connectivity**: `pre_root_id`, `post_root_id`, `syn_count`
* **Annotation**: `neuropil` (Mapped to `region`), `nt_type` (Mapped to `source_nt_type`)
* **Preserved Annotation**: The `nt_type` from this source edge is preserved strictly as `source_nt_type`, a source-derived annotation. It is **NOT** converted into excitatory/inhibitory sign, conductance, synaptic weight, or delay during Phase C1.
* **Null Behavior**: Edges missing valid integer counts are malformed. Missing endpoints against the master node list are quarantined.
* **Duplicate Behavior**: Grouped by `(pre_root_id, post_root_id, neuropil)` with `sum(synapse_count)`. The `source_nt_type` is preserved via `.first()` as a source-derived annotation on the canonical edge; it is NOT a grouping key.

## Missing/Unclassified Handling Rules
* **A. missing biological identifier**: Retain row if it has an ID, reject if strictly missing.
* **B. missing cell-type annotation**: Retain neuron, fill `cell_type` with null.
* **C. missing neurotransmitter prediction**: Retain neuron, fill `neurotransmitter` with null.
* **D. missing proofreading/classification**: Retain neuron (unannotated ≠ invalid).
* **E. missing connection endpoint**: Quarantine connection (record count) because structural topology cannot be mapped.
* **F. malformed row**: Reject (record count).

## Connection Aggregation

This is a **data-model transformation**, not a biological interpretation.

* **Grouping keys**: `pre_root_id`, `post_root_id`, `region` (canonical name for source `neuropil`)
* **Aggregation function**: `sum(synapse_count)`
* **`source_nt_type` handling**: Preserved via `.first()` as a source-derived annotation on the canonical edge. It is **not** a grouping key. If multiple `nt_type` values existed for the same `(pre, post, region)` tuple, only the first would be retained — but the FAFB v783 export contains zero such duplicate groups (verified by direct duplicate-group validation).
* **Duplicate-group validation**: Before aggregation, the pipeline explicitly counts groups with more than one row. For the FAFB v783 `connections_princeton.csv.gz`, `duplicate_group_count = 0`, confirming that the source file is already structurally unique by `(pre_root_id, post_root_id, neuropil)`.
* **Deterministic ordering**: Canonical output is sorted by `(pre_dense_index, post_dense_index, region)` to guarantee byte-identical Parquet artifacts across repeated executions.
* **What C1 does NOT do**: No synaptic weights, conductances, delays, excitatory/inhibitory signs, or model dynamics are inferred. The `source_nt_type` annotation is strictly passthrough.
