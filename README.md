# Drosophila Connectome Simulation and Embodied Agent

This repository provides a Python foundation for experiments that link
Drosophila connectome models to embodied-agent behavior.

## Layout

- `drosophila_connectome/connectome/`: connectome models and fixtures.
- `drosophila_connectome/neuroscience/`: neuroscience-domain utilities.
- `drosophila_connectome/runtime/`: simulation runtime primitives.
- `drosophila_connectome/embodiment/`: sensors, actuators, and environments.
- `drosophila_connectome/behaviors/`: behavioral policies.
- `experiments/`, `configs/`, `tests/`, and `docs/`: supporting project areas.

## Quick start

The included synthetic fixture is available offline and is intended for early
development and tests:

```python
from drosophila_connectome import load_synthetic_connectome

connectome = load_synthetic_connectome()
print(len(connectome.neurons))  # 3
```
