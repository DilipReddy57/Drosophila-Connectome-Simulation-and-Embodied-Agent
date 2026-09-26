# Phase C2: Literature Benchmark for FlyWire FAFB v783

## Overview
This report provides a rigorous comparison between our locally ingested C1 canonical graph metrics and authoritative external sources for the FlyWire FAFB v783 connectome.

The purpose of this benchmark is to ensure that our derived connectome matches expected biological scopes before we lock in the Phase C2 dependencies.

## Benchmark Comparison Table

| Metric | External Value | Local Value | Source | DOI / URL | Dataset / Version | Sex | Scope | Definition | Matches Our Convention |
|--------|----------------|-------------|--------|-----------|-------------------|-----|-------|------------|------------------------|
| **Neurons (Total)** | 139,255 | 139,255 | Dorkenwald et al. 2024 Nature | [10.1038/s41586-024-07558-y](https://doi.org/10.1038/s41586-024-07558-y) | FlyWire FAFB v783 | Female | Whole-brain connectome | Number of proofread neurons | **YES** |
| **Neurons (Model)** | ~125,000 | 139,255 | Shiu et al. 2024 Nature | [10.1038/s41586-024-07981-1](https://doi.org/10.1038/s41586-024-07981-1) | FlyWire FAFB v783 | Female | Structural subset | Filtered subset of neurons used for computational stability | **NO** (We retain the unthresholded graph) |
| **Synapses (Total)** | ~54,500,000 | 50,666,648 | Dorkenwald et al. 2024 Nature | [10.1038/s41586-024-07558-y](https://doi.org/10.1038/s41586-024-07558-y) | FlyWire FAFB v783 | Female | Whole-brain connectome | Total chemical synapses mapped | **PARTIAL** (Our pipeline applies filtering/aggregation rules) |
| **Synapses (Model)** | ~50,000,000 | 50,666,648 | Shiu et al. 2024 Nature | [10.1038/s41586-024-07981-1](https://doi.org/10.1038/s41586-024-07981-1) | FlyWire FAFB v783 | Female | Structural subset | Synapses preserved in filtered structural representation | **PARTIAL** (Very close match, suggesting similar filtration) |
| **Cell Types** | 8,453 | N/A | Schlegel et al. 2024 Nature / Codex | [10.1038/s41586-024-07686-5](https://doi.org/10.1038/s41586-024-07686-5) | FlyWire FAFB v783 | Female | Whole-brain connectome | Unique distinct cell type annotations assigned | **PARTIAL** (Depends on specific snapshot of annotations used locally) |

## Notes
- **Dorkenwald et al. 2024** provides the authoritative unthresholded counts for the full structural connectome. Our local `neuron_count` perfectly matches their 139,255 figure.
- **Shiu et al. 2024** provides a filtered baseline specifically tuned for computational structural representations. They discarded disconnected or problematic fragments, leading to ~125,000 neurons and ~50 million synapses.
- The discrepancy between the total external synapse count (~54.5M) and our canonical synapse count (50,666,648) strongly suggests our data ingestion process applies a specific synapse filtering rule, which closely mirrors the model-ready dataset from Shiu et al. 2024.

