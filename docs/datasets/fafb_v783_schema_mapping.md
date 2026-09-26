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
* **Duplicate Behavior**: Summed via aggregation `sum(synapse_count)` grouped by `(pre_root_id, post_root_id, neuropil, source_nt_type)`.

## Missing/Unclassified Handling Rules
* **A. missing biological identifier**: Retain row if it has an ID, reject if strictly missing.
* **B. missing cell-type annotation**: Retain neuron, fill `cell_type` with null.
* **C. missing neurotransmitter prediction**: Retain neuron, fill `neurotransmitter` with null.
* **D. missing proofreading/classification**: Retain neuron (unannotated ≠ invalid).
* **E. missing connection endpoint**: Quarantine connection (record count) because structural topology cannot be mapped.
* **F. malformed row**: Reject (record count).

## Connection Aggregation
* **Source representation**: One row = single-neuropil aggregate of synapses between two proofread neurons.
* **Grouping keys**: `pre_root_id`, `post_root_id`, `neuropil`
* **Aggregation function**: `sum(syn_count)`
* **Biological meaning**: Total structural synapses between a specific presynaptic and postsynaptic neuron within a specific brain region. No weights or model dynamics are inferred during C1.
