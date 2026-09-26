"""Deterministic discrete-time spiking network suitable for smoke tests."""

from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeNeuron:
    id: int
    threshold: float = 1.0
    reset_potential: float = 0.0
    refractory_steps: int = 0


@dataclass(frozen=True)
class Connection:
    source_id: int
    target_id: int
    weight: float
    delay_steps: int = 0


class DiscreteNetwork:
    """Integrate external and synaptic current, emitting threshold crossings."""

    def __init__(self, neurons: list[RuntimeNeuron], connections: list[Connection]):
        self.neurons = {neuron.id: neuron for neuron in neurons}
        self.connections = connections
        self.reset()

    def reset(self) -> None:
        self.time = 0
        self.potential = {neuron_id: 0.0 for neuron_id in self.neurons}
        self.refractory_until = {neuron_id: 0 for neuron_id in self.neurons}
        self._scheduled: dict[int, list[tuple[int, float]]] = defaultdict(list)
        self.spikes: list[tuple[int, int]] = []

    def step(self, external_current: dict[int, float] | None = None) -> list[int]:
        external_current = external_current or {}
        current = defaultdict(float)
        for neuron_id, value in self._scheduled.pop(self.time, []):
            current[neuron_id] += value
        for neuron_id, value in external_current.items():
            current[neuron_id] += value

        emitted: list[int] = []
        for neuron_id, neuron in self.neurons.items():
            if self.time < self.refractory_until[neuron_id]:
                continue
            self.potential[neuron_id] += current[neuron_id]
            if self.potential[neuron_id] >= neuron.threshold:
                emitted.append(neuron_id)
                self.spikes.append((self.time, neuron_id))
                self.potential[neuron_id] = neuron.reset_potential
                self.refractory_until[neuron_id] = self.time + neuron.refractory_steps + 1
        for edge in self.connections:
            if edge.source_id in emitted:
                self._scheduled[self.time + edge.delay_steps + 1].append((edge.target_id, edge.weight))
        self.time += 1
        return emitted
