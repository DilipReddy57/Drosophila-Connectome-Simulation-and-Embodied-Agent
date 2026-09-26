# FlyWire FAFB v783 acquisition contract

## Identity and scope

- **Dataset:** FlyWire FAFB adult female brain (`fafb_v783`), version `v783`.
- **Scope:** female adult brain only. This pipeline rejects an unrecorded substitution or mixture with BANC, MANC, or MaleCNS.
- **Primary scientific record:** `PAPER-001` in the source registry.
- **Official data record:** `DATA-001`; exact export URL and license must be captured in the generated manifest.

## Official access limitation

This repository deliberately does **not** invent a static bulk-download URL. The configured files have `source_url: null` because the authorized user must obtain the appropriate official static export or approved FlyWire CAVE/Codex export and record its exact URL, release notes, terms, and license. The manual/API procedure is in `configs/fafb_v783.json`. The `acquire` command fails with this instruction until each configured artifact has an approved official URL.

## Required inputs

| Local name | Role | Required columns / aliases | Why |
| --- | --- | --- | --- |
| `neurons.csv` | neuron metadata | `root_id`/`neuron_id`/`id` | Immutable biological ID population and dense mapping. |
| `connections.csv` | connectivity | `pre_root_id`, `post_root_id`, `synapse_count`; optional `neuropil` | Directed biological connectivity. |
| `annotations.csv` | annotations | `root_id`; optional canonical annotation fields | Joins only source-provided annotations. |

Morphology, meshes, images, and unrelated tables are intentionally excluded because they are unnecessary for C1 and can be substantially larger.

## Commands

```bash
python -m drosophila_connectome.connectome.acquisition validate-config
# After authorized acquisition into data/raw/fafb_v783/:
python -m drosophila_connectome.connectome.acquisition manifest fafb_v783
python -m drosophila_connectome.connectome.acquisition verify fafb_v783
python -m drosophila_connectome.connectome.acquisition normalize fafb_v783
python -m drosophila_connectome.connectome.acquisition profile fafb_v783
```

Create `data/manifests/fafb_v783_manifest.json` with `build_manifest` after downloading the configured raw files. It stores the source, retrieval timestamp, local paths, sizes, formats, roles, and SHA-256 values. Raw data are ignored by Git.

## Normalization and provenance

Neuron IDs are sorted lexicographically as strings and assigned `0..N-1`; the resulting mapping is deterministic for fixed raw inputs and normalization version. Connections are aggregated only as `sum(pre_neuron_id, post_neuron_id, region)`. No weight, sign, or delay is emitted. Missing annotations are null. Each canonical record carries raw artifact/hash, source version, normalization version, and generation time. Upstream source row IDs are `null` unless a stable identifier exists.

## Validation and limitations

`profile` reports derived statistics separately from source-reported statistics (which remain empty unless a verified release statistic is added). The committed fixture exercises acquisition-manifest, verify, normalize, mapping, aggregation, thresholds, provenance, and profiling without biological data. No real FAFB file has been acquired in this repository, so C1 is **BLOCKED on authorized official data access**; C1-A/B/C/D/E/F/G/H/J/K are implemented, while C1-I awaits authorized data.
