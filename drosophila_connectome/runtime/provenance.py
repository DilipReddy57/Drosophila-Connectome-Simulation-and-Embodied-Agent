"""Serializable experiment provenance and metric-capture contract."""

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class ExperimentConfig:
    dataset_version: str
    model_version: str
    parameter_version: str
    seed: int
    hardware: str


@dataclass
class MetricCapture:
    config: ExperimentConfig
    timing: dict[str, float] = field(default_factory=dict)
    neural_metrics: dict[str, float] = field(default_factory=dict)
    behavior_metrics: dict[str, float] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "config": asdict(self.config),
            "timing": self.timing,
            "neural_metrics": self.neural_metrics,
            "behavior_metrics": self.behavior_metrics,
        }
