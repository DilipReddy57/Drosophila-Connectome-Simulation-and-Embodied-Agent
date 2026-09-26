from drosophila_connectome.runtime.provenance import ExperimentConfig, MetricCapture


def test_metric_capture_contains_reproducibility_timing_neural_and_behavior_fields():
    config = ExperimentConfig("hemibrain-v1.2", "lif-v0.1", "params-2026-09", 1234, "cpu:test-host")
    capture = MetricCapture(
        config,
        timing={"wall_seconds": 0.25, "simulated_seconds": 1.0},
        neural_metrics={"spike_count": 3, "mean_firing_rate_hz": 2.5},
        behavior_metrics={"distance_m": 1.2, "reward": 0.8},
    )
    assert capture.as_dict() == {
        "config": {"dataset_version": "hemibrain-v1.2", "model_version": "lif-v0.1", "parameter_version": "params-2026-09", "seed": 1234, "hardware": "cpu:test-host"},
        "timing": {"wall_seconds": 0.25, "simulated_seconds": 1.0},
        "neural_metrics": {"spike_count": 3, "mean_firing_rate_hz": 2.5},
        "behavior_metrics": {"distance_m": 1.2, "reward": 0.8},
    }
