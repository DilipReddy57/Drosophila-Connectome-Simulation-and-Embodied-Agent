import numpy as np
from drosophila_connectome.neural.lif.network import Network, Simulation
from drosophila_connectome.neural.lif.parameters import LIFParameters
import scipy.sparse as sp

def test_e1_analytical_lif_comparison():
    params = LIFParameters(dt=0.1, tau_m=20.0, V_rest=-52.0)
    net = Network(1, sp.csr_matrix((1, 1)), params=params)
    sim = Simulation(net)
    ext_I = np.array([10.0])
    for _ in range(10):
        sim.step(ext_I)
    t = 1.0
    expected_V = -52.0 + 10.0 * (1 - np.exp(-t/20.0))
    assert np.isclose(net.state.V[0], expected_V, atol=1e-5)

def test_e2_threshold_check():
    params = LIFParameters(dt=0.1, V_rest=-52.0, V_th=-45.0)
    net = Network(1, sp.csr_matrix((1, 1)), params=params)
    sim = Simulation(net)
    decay = np.exp(-0.1 / 20.0)
    I_exact = (-45.0 - (-52.0)) / (1 - decay)
    sim.step(np.array([I_exact - 0.1]))
    assert len(sim.recorder.spikes) == 0
    assert net.state.V[0] < -45.0
    net.state.reset(params.V_rest)
    sim.step(np.array([I_exact + 1.0]))
    assert len(sim.recorder.spikes) == 1

def test_e3_reset_check():
    params = LIFParameters(dt=0.1, V_rest=-52.0, V_th=-45.0, V_reset=-55.0)
    net = Network(1, sp.csr_matrix((1, 1)), params=params)
    sim = Simulation(net)
    decay = np.exp(-0.1 / 20.0)
    I_spike = (-45.0 - (-52.0)) / (1 - decay) + 1.0
    sim.step(np.array([I_spike]))
    assert len(sim.recorder.spikes) == 1
    assert net.state.V[0] == -55.0

def test_e4_refractory_period_check():
    params = LIFParameters(dt=0.1, V_rest=-52.0, V_th=-45.0, V_reset=-55.0, t_ref=2.2)
    net = Network(1, sp.csr_matrix((1, 1)), params=params)
    sim = Simulation(net)
    decay = np.exp(-0.1 / 20.0)
    I_spike = (-45.0 - (-52.0)) / (1 - decay) + 1.0
    sim.step(np.array([I_spike]))
    assert len(sim.recorder.spikes) == 1
    assert net.state.V[0] == -55.0
    for _ in range(21):
        sim.step(np.array([1000.0]))
        assert net.state.V[0] == -55.0
    sim.step(np.array([1000.0]))
    assert net.state.V[0] > -55.0

def test_e7_timestep_sensitivity():
    dts = [0.1, 0.05, 0.01]
    results = []
    for dt in dts:
        params = LIFParameters(dt=dt, tau_m=20.0, V_rest=-52.0)
        net = Network(1, sp.csr_matrix((1, 1)), params=params)
        sim = Simulation(net)
        steps = int(np.round(1.0 / dt))
        for _ in range(steps):
            sim.step(np.array([10.0]))
        results.append(net.state.V[0])
    t = 1.0
    expected_V = -52.0 + 10.0 * (1 - np.exp(-t/20.0))
    for v in results:
        assert np.isclose(v, expected_V, atol=1e-5)
