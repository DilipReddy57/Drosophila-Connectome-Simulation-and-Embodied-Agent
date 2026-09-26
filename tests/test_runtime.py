from connectome_sim.runtime import Connection, DiscreteNetwork, RuntimeNeuron


def test_synthetic_network_exhibits_excitation_inhibition_delay_and_recording():
    network = DiscreteNetwork(
        [RuntimeNeuron(1), RuntimeNeuron(2), RuntimeNeuron(3)],
        [Connection(1, 2, 1.0, delay_steps=1), Connection(1, 3, -1.0)],
    )
    assert network.step({1: 1.0, 3: 1.0}) == [1, 3]
    assert network.step({3: 1.0}) == []  # inhibitory input cancels tonic drive
    assert network.step() == [2]  # configured delay: source spike at time 0 arrives at time 2
    assert network.spikes == [(0, 1), (0, 3), (2, 2)]


def test_refractory_reset_and_runtime_reset():
    network = DiscreteNetwork([RuntimeNeuron(1, reset_potential=-0.5, refractory_steps=1)], [])
    assert network.step({1: 1.0}) == [1]
    assert network.potential[1] == -0.5
    assert network.step({1: 10.0}) == []  # refractory
    assert network.step({1: 1.5}) == [1]
    network.reset()
    assert (network.time, network.potential, network.spikes) == (0, {1: 0.0}, [])
