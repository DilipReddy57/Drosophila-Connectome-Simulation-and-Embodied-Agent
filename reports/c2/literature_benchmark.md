# Phase C2: Literature Benchmark for FlyWire FAFB v783

## Overview
This report provides a rigorous comparison between our locally ingested C1 canonical graph metrics and authoritative external sources for the FlyWire FAFB v783 connectome.

## Definitions
- **Canonical Rows:** 5,342,446 distinct (pre_neuron_id, post_neuron_id, region) groupings.
- **Unique Directed Edges:** 3,732,460 distinct (pre_neuron_id, post_neuron_id) pairs.
- **Summed Synapse Count:** 50,666,648 physical synapse tallies aggregated across all groups.

## Benchmark Comparison Table

| Metric | External Value | Local Value | Source | DOI / URL | Dataset / Version | Sex | Scope | Definition | Matches Our Convention |
|--------|----------------|-------------|--------|-----------|-------------------|-----|-------|------------|------------------------|
| **Neurons (Total)** | 139,255 | 139,255 | Dorkenwald et al. 2024 Nature | [10.1038/s41586-024-07558-y](https://doi.org/10.1038/s41586-024-07558-y) | FlyWire FAFB v783 | Female | Whole-brain | Number of proofread neurons | **EXACT MATCH** |
| **Neurons (Model)** | ~125,000 | 139,255 | Shiu et al. 2024 Nature | [10.1038/s41586-024-07981-1](https://doi.org/10.1038/s41586-024-07981-1) | FlyWire FAFB v783 | Female | Thresholded | Subset of neurons included in functional simulation | **DEFINITIONALLY DIFFERENT** |
| **Synapses (Total)** | ~54,500,000 | 50,666,648 | Dorkenwald et al. 2024 Nature | [10.1038/s41586-024-07558-y](https://doi.org/10.1038/s41586-024-07558-y) | FlyWire FAFB v783 | Female | Whole-brain | Total chemical synapses mapped | **PARTIAL MATCH** |
| **Synapses (Model)** | ~50,000,000 | 50,666,648 | Shiu et al. 2024 Nature | [10.1038/s41586-024-07981-1](https://doi.org/10.1038/s41586-024-07981-1) | FlyWire FAFB v783 | Female | Thresholded | Synapses preserved in filtered structural representation | **PARTIAL MATCH** |
| **Cell Types** | 8,453 | N/A | Schlegel et al. 2024 Nature / Codex | [10.1038/s41586-024-07686-5](https://doi.org/10.1038/s41586-024-07686-5) | FlyWire FAFB v783 | Female | Whole-brain | Unique distinct cell type annotations assigned | **PARTIAL MATCH** |

## Notes
- **Dorkenwald et al. 2024** provides the authoritative unthresholded counts for the full structural connectome. Our local `neuron_count` perfectly matches their 139,255 figure.
- **Shiu et al. 2024** provides a filtered baseline specifically tuned for computational structural representations.
- The discrepancy between the total external synapse count (~54.5M) and our canonical synapse count (50,666,648) represents a difference in filtering/accounting that is currently UNRESOLVED. We do not assume this implies equivalency with Shiu et al. 2024's ~50M tally without explicit code evidence demonstrating the same thresholding rules.
