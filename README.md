# Drosophila Connectome Simulation and Embodied Agent

A reproducible research foundation for building a **connectome-constrained computational agent platform**. The project treats structural connectomes, neural dynamics, embodiment, and application-specific behavior as separate, versioned layers.

## Current phase

The repository implements the **Data Acquisition Pack** and governance artifacts required before simulation work:

1. lock a dataset and scientific benchmark;
2. register and classify supporting evidence;
3. acquire immutable raw snapshots with checksums and licenses;
4. normalize into the canonical neuron and connection schemas;
5. validate graph variants before selecting a neural runtime.

No raw biological dataset is committed to this repository. Raw snapshots belong under `data/raw/` and must be referenced by a manifest.

## Start here

- [Project requirements and implementation gate](docs/requirements.md)
- [Data acquisition workflow](docs/data-acquisition.md)
- [Canonical data model](docs/canonical-data-model.md)
- [Reproducibility and evidence policy](docs/reproducibility.md)
- [Research source registry](research/source_registry/sources.csv)
- [Machine-readable schemas](schemas/)
- [Experiment, decision, assumption, and session templates](templates/)

## Repository layout

```text
research/       Evidence registry and source records
data/           Ignored raw data plus normalized and derived artifacts
schemas/        JSON Schemas for manifests and canonical tabular records
templates/      Versioned experimental and governance templates
configs/        Project and future experiment configuration
docs/           Operating procedures and architecture decisions
tests/          Schema and pipeline validation tests
```

## Scientific boundary

The connectome constrains structure; it does not independently establish synaptic conductances, neuron dynamics, learning rules, or an application action mapping. Every value and mapping must be classified as **measured**, **inferred**, or **engineered** and linked to provenance.
