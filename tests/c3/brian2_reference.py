import os
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

from brian2 import *
import numpy as np

def run_brian2_reference():
    V_rest = -52 * mV
    V_reset = -52 * mV
    V_th = -45 * mV
    tau_m = 20 * ms
    tau_syn = 5 * ms
    delay = 1.8 * ms
    weight = 10.0 * mV
    t_ref = 2.2 * ms
    dt = 0.1 * ms

    defaultclock.dt = dt
    prefs.codegen.target = "numpy"

    I_ext_arr = np.zeros(500)
    I_ext_arr[:100] = 20.0
    I_ext_stim = TimedArray(I_ext_arr * mV, dt=0.1*ms)

    eqs = """
    dV/dt = (V_rest - V + I_syn + I_ext_stim(t))/tau_m : volt (unless refractory)
    dI_syn/dt = -I_syn/tau_syn : volt
    """

    G = NeuronGroup(2, eqs, threshold="V > V_th", reset="V = V_reset", refractory=t_ref, method="exact")
    G.V = V_rest
    G.I_syn = 0 * mV

    S = Synapses(G, G, "w : volt", on_pre="I_syn += w")
    S.connect(i=0, j=1)
    S.w = weight
    S.delay = delay

    M_V = StateMonitor(G, "V", record=True)
    M_I = StateMonitor(G, "I_syn", record=True)
    M_S = SpikeMonitor(G)

    # We only inject to Neuron 0 by... wait, TimedArray is global in time.
    # We want I_ext_stim for Neuron 0, 0 for Neuron 1.
    # So we can just add I_ext parameter:
    # I_ext : volt
    # and update it at each step? Brian2 allows user-defined operations but TimedArray is easiest if we define an array of shape (time, 2)
    # Yes, TimedArray can be 2D.
    I_ext_2d = np.zeros((500, 2))
    I_ext_2d[:100, 0] = 20.0
    I_ext_stim_2d = TimedArray(I_ext_2d * mV, dt=0.1*ms)
    
    eqs2 = """
    dV/dt = (V_rest - V + I_syn + I_ext_stim_2d(t, i))/tau_m : volt (unless refractory)
    dI_syn/dt = -I_syn/tau_syn : volt
    """
    
    G = NeuronGroup(2, eqs2, threshold="V > V_th", reset="V = V_reset", refractory=t_ref, method="exact")
    G.V = V_rest
    G.I_syn = 0 * mV
    
    S = Synapses(G, G, "w : volt", on_pre="I_syn += w")
    S.connect(i=0, j=1)
    S.w = weight
    S.delay = delay

    M_V = StateMonitor(G, "V", record=True)
    M_I = StateMonitor(G, "I_syn", record=True)
    M_S = SpikeMonitor(G)

    run(50 * ms)
    
    return {
        "t": M_V.t/ms,
        "V": M_V.V/mV,
        "I_syn": M_I.I_syn/mV,
        "spikes_t": M_S.t/ms,
        "spikes_i": M_S.i
    }

if __name__ == "__main__":
    res = run_brian2_reference()
    print("Spikes i:", res["spikes_i"])
    print("Spikes t:", res["spikes_t"])

