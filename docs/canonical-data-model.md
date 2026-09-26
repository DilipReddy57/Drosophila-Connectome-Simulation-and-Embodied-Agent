# Canonical data model

The simulator consumes canonical records, never a raw vendor table. Raw snapshots remain immutable; normalized graph records and model parameters are separate artifacts.

## Artifact layers

| Layer | Purpose | Mutability |
| --- | --- | --- |
| Raw | Downloaded official source files | Immutable |
| Normalized | Dataset-faithful neuron, annotation, and connection records | Rebuildable from raw manifest |
| Derived | Filtered/aggregated graph variants | Rebuildable and versioned |
| Model | Weights, signs, delays, and neuron parameters | Versioned assumptions/fits |
| Interface | Sensory, motor, reward, and application adapters | Engineered |

## Neurons

`canonical_neurons` uses stable biological IDs and contiguous `dense_index` values for runtime storage. Required fields are defined in [`schemas/neuron.schema.json`](../schemas/neuron.schema.json).

## Connections

`canonical_connections` represents an aggregated directed pre→post relation. It retains raw synapse count, neuropil context, aggregation method, confidence, and source version. Do not overwrite it with derived runtime weight or sign; those belong to a model-parameter artifact. Required fields are defined in [`schemas/connection.schema.json`](../schemas/connection.schema.json).

## Graph variants

Every graph export must name its aggregation and filters, for example:

```text
faFB-v783__aggregate-pre-post-neuropil__min-synapses-5__confidence-none
```

The manifest must retain unfiltered and thresholded edge counts, including thresholds 3, 5, and 10 when supported by the raw product. Multiple rows for one pre/post pair across neuropils are preserved until the explicitly recorded aggregation step.

## Provenance classification

| Classification | Examples |
| --- | --- |
| Measured/annotated | root ID, synapse count, cell type |
| Inferred | predicted neurotransmitter and derived sign |
| Engineered | game action decoder, reward, token encoder |
| Model assumption | LIF threshold, weight rule, delay rule |
| Fitted parameter | value optimized against recordings |
