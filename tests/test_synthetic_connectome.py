from drosophila_connectome import load_synthetic_connectome


def test_synthetic_connectome_is_available_without_external_data() -> None:
    connectome = load_synthetic_connectome()

    assert [neuron["id"] for neuron in connectome.neurons] == [
        "SENSORY_L",
        "INTERNEURON",
        "MOTOR_R",
    ]
    assert connectome.synapses == (
        {"source": "SENSORY_L", "target": "INTERNEURON", "weight": 0.8},
        {"source": "INTERNEURON", "target": "MOTOR_R", "weight": 0.6},
    )
