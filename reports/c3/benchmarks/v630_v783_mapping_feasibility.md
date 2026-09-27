# v630 to v783 Mapping Feasibility

FlyWire uses a continuous proofreading graph. "Root IDs" are agglomerations of immutable "Supervoxels". When a neuron is proofread (e.g., a false merge is cleaved, or a missing branch is attached), the old Root ID is immediately retired and two or more new Root IDs are generated. Because v630 was March 2023 and v783 (the publication release) was months later, almost all heavily branched or studied neurons underwent proofreading edits, completely changing their Root IDs.

## Mapping Mechanisms Available

### 1. Root ID Lineage Graph (CAVE API)
- **Method:** Querying the FlyWire CAVE (Chunked Auto-generated Visual Environment) API's `lineage` service to track the exact edit history from the v630 Root ID to its v783 descendants.
- **Classification:** **EXACT**
- **Pros:** Mathematically guaranteed to track the exact same biological mass.
- **Cons:** Requires a live API token and access to the FlyWire CAVE client. One v630 ID might split into multiple v783 IDs (if a false merge was fixed) requiring volumetric logic to pick the "main" neuron.

### 2. Spatial Coordinates (XYZ)
- **Method:** Using the 3D spatial coordinates (usually the nucleus `soma_location`) from the v630 metadata and querying which v783 Root ID occupies that exact voxel space.
- **Classification:** **HIGH-CONFIDENCE BIOLOGICAL MATCH**
- **Pros:** Somatic locations rarely change.
- **Cons:** We need the original v630 XYZ coordinates, which were not provided in `example.ipynb`. We would have to download the v630 completeness CSV from the Shiu supplement to extract the XYZ coordinates.

### 3. Supervoxel ID Mapping
- **Method:** A specific immutable supervoxel ID (e.g., the center of the soma) belonging to the v630 neuron is queried against the v783 dataset to find its new parent Root ID.
- **Classification:** **HIGH-CONFIDENCE BIOLOGICAL MATCH**
- **Pros:** Supervoxels never change IDs.
- **Cons:** Same as coordinates; requires the supervoxel ID from v630 metadata.

### 4. Official Cross-Version Published Tables
- **Method:** Using the official FlyWire mapping table (e.g., `v630_to_v783_crosswalk.csv`) published by Dorkenwald et al. (2024).
- **Classification:** **EXACT**
- **Pros:** Requires no API calls. Pre-computed by the consortium.

### 5. Cell-Type / Label Matching
- **Method:** Searching the v783 `neurons.parquet` for `cell_type == 'MN9'` or `cell_type == 'sugar'`.
- **Classification:** **UNSAFE / HEURISTIC**
- **Why:** The number of neurons assigned to a cell type changes between versions. We cannot guarantee we are stimulating the exact same *biological subgraph* that Shiu simulated if we just regex match names. If Shiu stimulated 21 specific sugar neurons, and v783 classifies 72 neurons as `BM_Taste`, picking a random 21 is scientifically invalid.

## Conclusion
A scientifically valid mapping is entirely feasible. The correct approach is either to use the official CAVE API lineage service, extract the XYZ coordinates from the Shiu v630 supplementary CSV and spatial-query v783, or use an official FlyWire crosswalk table.
