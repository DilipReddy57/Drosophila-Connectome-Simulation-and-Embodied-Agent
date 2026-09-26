"""A bundled, deterministic connectome fixture for local development."""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib.resources import files


@dataclass(frozen=True)
class SyntheticConnectome:
    """Small directed neural network used without external biological data."""

    neurons: tuple[dict[str, object], ...]
    synapses: tuple[dict[str, object], ...]


def load_synthetic_connectome() -> SyntheticConnectome:
    """Load the package's tiny synthetic connectome fixture."""

    fixture = files("drosophila_connectome.connectome.data").joinpath(
        "synthetic_connectome.json"
    )
    payload = json.loads(fixture.read_text(encoding="utf-8"))
    return SyntheticConnectome(
        neurons=tuple(payload["neurons"]), synapses=tuple(payload["synapses"])
    )
