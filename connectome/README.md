# Connectome data contracts

This directory defines JSON Schema Draft 2020-12 contracts for the reproducible data boundary between connectome ingestion and simulation. Validate records against the schema matching their artifact kind.

| Schema | Record | Lifecycle |
| --- | --- | --- |
| `neuron.schema.json` | normalized neuron table | Derived from raw source records; reproducible and provenance-bearing. |
| `connection.schema.json` | aggregated directed connection table | Derived from raw synapse observations; not a raw-synapse format. |
| `simulation-parameters.schema.json` | simulation parameter set | Versioned model configuration, separate from connectome data. |
| `dataset-manifest.schema.json` | release manifest | Inventory linking immutable raw inputs to all derived outputs. |

## Data classes and immutability

**Raw artifacts are immutable.** A raw source file is identified by `artifact_id`, URI, and SHA-256 in `raw_artifacts`. Never overwrite it: an upstream correction or re-download with changed bytes is a new artifact (and normally a new manifest version).

**Normalized neurons and aggregated connections are derived data.** They can be regenerated, but every record must retain `source_dataset`, `source_version`, source artifact checksum(s), transformation/normalization version, and generation time. Connections also require the aggregation method, version, raw synapse count, and raw input identifiers. A manifest’s `derived_artifacts` lists the exact inputs and transformation version for every materialized table.

**Simulation parameters are model parameters, not derived biological truth.** They select model equations, weights/filters, execution engine, seed, and timing. Keep parameter-set versions immutable for recorded runs; create a new `parameter_set_version` for any change and bind the run to `data_manifest_id`.

## Identity and dense-index mapping

`body_id` preserves the source-system identity, while `neuron_id` is the normalized identity. `dense_index` is only a compact simulation lookup key. Within one `dataset_id` and `source_version`, it is zero-based, unique, and contiguous from `0` to `N - 1`. Connection endpoint IDs and indices must agree with the normalized-neuron table. The manifest requires a separately addressable mapping artifact and declares its count, zero base, contiguity, and mapping version; never assume a mapping remains valid across releases.

## Confidence and provenance requirements

`neurotransmitter_confidence` expresses confidence in a transmitter label on a `[0,1]` scale. It is required when a neuron provides a transmitter; edge transmitter confidence may be `null` only when the edge has no transmitter label. `connection_confidence` is required on every aggregated edge and is also normalized to `[0,1]`; it is confidence in the edge’s existence/quality, not its weight.

All records must identify the source dataset and version. Neurons require a source record ID, raw artifact ID/checksum, normalization version, and timestamp. Connections require all raw artifact IDs/checksums plus aggregation metadata and timestamp. Manifests capture the repository revision and generating tool/command. These fields make every derived value traceable to immutable bytes and a named transformation.
