import numpy as np
import scipy.sparse as sp
import time
from drosophila_connectome.neural.lif.network import Network as CustomNetwork, Simulation

from brian2 import *
import brian2

def test_custom():
    adj = sp.csr_matrix(np.zeros((1, 1), dtype=np.float32))
    net = CustomNetwork(1, adj)
    sim = Simulation(net)
    
    # Manually inject the jump at step 10
    sim.run(10)
    net.state.V[0] += 0.275 * 250.0
    net.state.refractory_time[0] = 0.0
    sim.step()
    return sim.recorder.spikes

def test_brian2():
    prefs.codegen.target = "numpy"
    defaultclock.dt = 0.1 * ms
    
    eqs = """
    dv/dt = (-52*mV - v + g) / (20*ms) : volt (unless refractory)
    dg/dt = -g / (5*ms)                : volt (unless refractory)
    rfc                                : second
    """
    
    neu = NeuronGroup(1, eqs, method='linear', threshold='v > -45*mV', reset='v = -52*mV; g=0*mV', refractory='rfc')
    neu.v = -52 * mV
    neu.g = 0 * mV
    neu.rfc = 2.2 * ms
    
    # We want to mimic the 250x forcing. Brian2 PoissonInput injects directly into v.
    # We will use SpikeGeneratorGroup feeding into v directly.
    indices = np.array([0])
    times = np.array([1.0]) * ms # step 10
    gen = SpikeGeneratorGroup(1, indices, times)
    
    # Synapse to inject into v (bypassing g)
    syn = Synapses(gen, neu, 'w : volt', on_pre='v += w')
    syn.connect(i=0, j=0)
    syn.w = 0.275 * 250.0 * mV
    
    spk_mon = SpikeMonitor(neu)
    state_mon = StateMonitor(neu, 'v', record=0)
    
    run(2.0 * ms)
    
    return list(spk_mon.t / ms), state_mon.v[0] / mV

if __name__ == "__main__":
    c_spk = test_custom()
    print("Custom Spike Steps:", c_spk)
    
    b_spk, b_v = test_brian2()
    print("Brian2 Spikes (ms):", b_spk)
    print("Brian2 Voltage Trace:", b_v)
