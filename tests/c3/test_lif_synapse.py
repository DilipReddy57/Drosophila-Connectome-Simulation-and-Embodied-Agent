import numpy as np
from drosophila_connectome.neural.lif.network import Network, Simulation
from drosophila_connectome.neural.lif.parameters import LIFParameters
import scipy.sparse as sp

def test_e5_synaptic_response():
    params = LIFParameters(dt=0.1, V_rest=-52.0, V_th=-45.0, tau_syn=5.0, delay=1.0)
    W = sp.csr_matrix([[0.0, 0.0], [1.0, 0.0]])
    net = Network(2, W, params=params)
    sim = Simulation(net)
    decay = np.exp(-0.1 / 20.0)
    I_spike = (-45.0 - (-52.0)) / (1 - decay) + 1.0
    sim.step(np.array([I_spike, 0.0]))
    for _ in range(9):
        sim.step(np.array([0.0, 0.0]))
        assert net.state.I_syn[1] == 0.0
    sim.step(np.array([0.0, 0.0]))
    assert net.state.I_syn[1] == 1.0
    sim.step(np.array([0.0, 0.0]))
    expected_decay = 1.0 * np.exp(-0.1 / 5.0)
    assert np.isclose(net.state.I_syn[1], expected_decay)

def test_e6_excitatory_inhibitory_sign():
    params = LIFParameters(dt=0.1, V_rest=-52.0, V_th=-45.0, delay=0.1)
    W = sp.csr_matrix([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]])
    net = Network(3, W, params=params)
    sim = Simulation(net)
    decay = np.exp(-0.1 / 20.0)
    I_spike = (-45.0 - (-52.0)) / (1 - decay) + 1.0
    sim.step(np.array([I_spike, 0.0, 0.0]))
    sim.step(np.array([0.0, 0.0, 0.0]))
    assert net.state.I_syn[1] == 1.0
    assert net.state.I_syn[2] == -1.0
