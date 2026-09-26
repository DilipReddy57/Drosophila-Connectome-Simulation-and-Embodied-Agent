"""Validation and graph summaries for imported connectome data."""

from dataclasses import dataclass
from typing import Iterable


VALID_NEUROTRANSMITTERS = frozenset({"acetylcholine", "gaba", "glutamate", "dopamine", "serotonin"})


@dataclass(frozen=True)
class Neuron:
    id: int
    neurotransmitter: str


@dataclass(frozen=True)
class SchemaConnection:
    source_id: int
    target_id: int
    weight: float


@dataclass(frozen=True)
class NetworkSchema:
    neurons: tuple[Neuron, ...]
    connections: tuple[SchemaConnection, ...]

    def id_mapping(self) -> dict[int, int]:
        """Map stable dataset IDs to dense simulator indices."""
        return {neuron.id: index for index, neuron in enumerate(self.neurons)}

    def degree_distributions(self) -> tuple[dict[int, int], dict[int, int]]:
        incoming = {neuron.id: 0 for neuron in self.neurons}
        outgoing = {neuron.id: 0 for neuron in self.neurons}
        for edge in self.connections:
            outgoing[edge.source_id] += 1
            incoming[edge.target_id] += 1
        return incoming, outgoing

    def isolated_node_ids(self) -> set[int]:
        incoming, outgoing = self.degree_distributions()
        return {node_id for node_id in incoming if incoming[node_id] == outgoing[node_id] == 0}

    def neurotransmitter_distribution(self) -> dict[str, int]:
        distribution: dict[str, int] = {}
        for neuron in self.neurons:
            distribution[neuron.neurotransmitter] = distribution.get(neuron.neurotransmitter, 0) + 1
        return distribution


def validate_network(network: NetworkSchema) -> None:
    """Raise ``ValueError`` when a network cannot be simulated unambiguously."""
    ids = [neuron.id for neuron in network.neurons]
    if len(ids) != len(set(ids)):
        raise ValueError("neuron IDs must be unique")
    if any(neuron.neurotransmitter not in VALID_NEUROTRANSMITTERS for neuron in network.neurons):
        raise ValueError("neuron has an unsupported neurotransmitter")

    known_ids = set(ids)
    edges = set()
    for edge in network.connections:
        if edge.source_id not in known_ids or edge.target_id not in known_ids:
            raise ValueError("connection references an unknown neuron ID")
        if edge.source_id == edge.target_id:
            raise ValueError("self-connections are not allowed")
        key = (edge.source_id, edge.target_id)
        if key in edges:
            raise ValueError("duplicate directed connection")
        edges.add(key)
