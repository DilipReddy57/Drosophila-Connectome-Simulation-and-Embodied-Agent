# Architecture

The importable Python package is organized by responsibility:

- `connectome`: data models, importers, and bundled fixtures.
- `neuroscience`: domain-specific analysis and abstractions.
- `runtime`: simulation execution and scheduling.
- `embodiment`: environment, sensor, and actuator interfaces.
- `behaviors`: policies built on runtime and embodiment components.

Configuration lives in `configs/`; reproducible runnable work lives in
`experiments/`; and tests live in `tests/`.

## Local fixture

`drosophila_connectome.connectome.load_synthetic_connectome()` loads a tiny,
deterministic three-neuron, two-synapse circuit packaged with the project. It is
strictly synthetic and lets contributors develop without downloading biological
connectome datasets.
