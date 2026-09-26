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
