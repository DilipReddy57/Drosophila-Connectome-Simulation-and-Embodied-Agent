# Data acquisition workflow

## Scope

This workflow creates a reproducible input snapshot without downloading or scraping data during normal development. Use official static exports for bulk files; record any database-backed query separately.

## Procedure

1. Add an evidence record to `research/source_registry/sources.csv` and assign a stable `SOURCE_ID`.
2. Create a dataset manifest from `templates/dataset_manifest.json` in `data/manifests/`.
3. Download the file from its official source into a release-specific directory under `data/raw/`.
4. Compute SHA-256 and record the exact URL, retrieval time, license, release, file name, and checksum in the manifest.
5. Validate the manifest against `schemas/dataset-manifest.schema.json`.
6. Preserve the raw file unchanged. Build normalized/derived data as new artifacts with parent checksums.
7. Record all transformations, filters, joins, and aggregation rules in the derived artifact manifest.

## Dataset boundary

FAFB v783, BANC v888, MANC v1.2.1, and MCNS/MaleCNS releases must use separate manifests and raw directories. A name similarity is not evidence of release compatibility.

## Acceptance criteria (C1)

Every raw file has a version, official source URL, license/attribution note, SHA-256, retrieval timestamp, and explicit coverage/sex fields. A missing field blocks normalization.

## FAFB v783 executable workflow

Use the release-specific contract in [`docs/datasets/fafb_v783.md`](datasets/fafb_v783.md) and its configuration in `configs/fafb_v783.json`. The default CLI is intentionally limited to `fafb_v783` and refuses a non-official URL or an overwrite of an unverified raw artifact. It uses streaming I/O and a resumable `.part` file.

```bash
python -m drosophila_connectome.connectome.acquisition validate-config
python -m drosophila_connectome.connectome.acquisition acquire fafb_v783
python -m drosophila_connectome.connectome.acquisition manifest fafb_v783
python -m drosophila_connectome.connectome.acquisition verify fafb_v783
python -m drosophila_connectome.connectome.acquisition normalize fafb_v783
python -m drosophila_connectome.connectome.acquisition profile fafb_v783
```

`acquire` is intentionally blocked until an authorized user enters exact official static-export URLs (and optional expected SHA-256 values) in a reviewed copy of the FAFB configuration. This avoids fabricating an export URL or scraping authenticated interfaces. `normalize` reads CSV exports only, writes JSONL canonical artifacts under `data/derived/fafb_v783/`, and fails when a raw input checksum changes during normalization.
