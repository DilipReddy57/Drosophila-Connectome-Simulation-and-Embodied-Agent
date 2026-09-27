import os
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import numpy as np
import scipy.sparse as sp
from brian2 import *
from drosophila_connectome.neural.lif.network import Network, Simulation
from drosophila_connectome.neural.lif.parameters import LIFParameters
import pandas as pd

def get_params():
    return LIFParameters(
        V_rest=-52.0, V_reset=-52.0, V_th=-45.0,
        tau_m=20.0, tau_syn=5.0, t_ref=2.2,
        delay=1.8, dt=0.1, W_syn=1.0
    )

def run_brian_test(name, num_neurons, w_matrix_dense, delay_ms, ext_current_func, duration_ms):
    dt_val = 0.1 * ms
    defaultclock.dt = dt_val
    prefs.codegen.target = "numpy"

    eqs = """
    dV/dt = (-52*mV - V + I_syn + I_ext(t, i))/(20*ms) : volt (unless refractory)
    dI_syn/dt = -I_syn/(5*ms) : volt
    """

    G = NeuronGroup(num_neurons, eqs, threshold="V > -45*mV", reset="V = -52*mV", refractory=2.2*ms, method="exact")
    G.V = -52 * mV
    G.I_syn = 0 * mV
    
    steps = int(duration_ms / 0.1)
    I_ext_arr = np.zeros((steps, num_neurons))
    for s in range(steps):
        t_ms = s * 0.1
        for i in range(num_neurons):
            I_ext_arr[s, i] = ext_current_func(t_ms, i)
    I_ext = TimedArray(I_ext_arr * mV, dt=dt_val)

    sources, targets = np.nonzero(w_matrix_dense)
    weights = w_matrix_dense[sources, targets]
    
    # Brian2 requires S.connect() if S is created, else error.
    if len(sources) > 0:
        S = Synapses(G, G, "w : volt", on_pre="I_syn += w")
        S.connect(i=sources, j=targets)
        S.w = weights * mV
        S.delay = delay_ms * ms

    M_V = StateMonitor(G, "V", record=True)
    M_I = StateMonitor(G, "I_syn", record=True)
    M_S = SpikeMonitor(G)

    run(duration_ms * ms)
    
    return {
        "t": M_V.t/ms,
        "V": M_V.V/mV,
        "I_syn": M_I.I_syn/mV,
        "spikes_t": M_S.t/ms,
        "spikes_i": M_S.i
    }

def run_custom_test(name, num_neurons, w_matrix_dense, delay_ms, ext_current_func, duration_ms):
    params = get_params()
    params.delay_steps = int(np.round(delay_ms / params.dt))
    
    w_matrix_dense_T = w_matrix_dense.T
    weight_matrix = sp.csr_matrix(w_matrix_dense_T)
    
    net = Network(num_neurons, weight_matrix, params)
    sim = Simulation(net)
    
    steps = int(duration_ms / params.dt)
    v_trace = np.zeros((steps, num_neurons))
    i_trace = np.zeros((steps, num_neurons))
    
    for s in range(steps):
        t_ms = s * params.dt
        v_trace[s, :] = net.state.V.copy()
        i_trace[s, :] = net.state.I_syn.copy()
        
        ext_I = np.array([ext_current_func(t_ms, i) for i in range(num_neurons)])
        if np.all(ext_I == 0):
            ext_I = None
            
        sim.step(ext_I)
        
    return {
        "t": np.arange(steps) * params.dt,
        "V": v_trace.T,
        "I_syn": i_trace.T,
        "spikes": sim.recorder.spikes
    }

def compare(name, num_neurons, w_matrix_dense, delay_ms, ext_current_func, duration_ms):
    brian = run_brian_test(name, num_neurons, w_matrix_dense, delay_ms, ext_current_func, duration_ms)
    custom = run_custom_test(name, num_neurons, w_matrix_dense, delay_ms, ext_current_func, duration_ms)
    
    diff_v = np.abs(brian["V"] - custom["V"])
    diff_isyn = np.abs(brian["I_syn"] - custom["I_syn"])
    
    max_err_v = np.max(diff_v)
    mean_err_v = np.mean(diff_v)
    rmse_v = np.sqrt(np.mean(diff_v**2))
    max_err_isyn = np.max(diff_isyn)
    
    brian_counts = [len(brian["spikes_i"][brian["spikes_i"] == i]) for i in range(num_neurons)]
    custom_spikes = [(step * 0.1, n) for (step, n) in custom["spikes"]]
    custom_counts = [len([s for s, n in custom_spikes if n == i]) for i in range(num_neurons)]
    spike_diff = np.sum(np.abs(np.array(brian_counts) - np.array(custom_counts)))
    
    return {
        "Test": name,
        "Max_V_Error": max_err_v,
        "Mean_V_Error": mean_err_v,
        "RMSE_V": rmse_v,
        "Max_I_syn_Error": max_err_isyn,
        "Spike_Count_Diff": spike_diff
    }

def run_all():
    results = []
    results.append(compare("Test A (Single, No Input)", 1, np.zeros((1, 1)), 1.8, lambda t, i: 0.0, 50))
    results.append(compare("Test B (Single, Const I)", 1, np.zeros((1, 1)), 1.8, lambda t, i: 10.0, 50))
    
    w = np.zeros((2, 2))
    w[0, 1] = 10.0
    results.append(compare("Test C (2-neuron Exc)", 2, w, 1.8, lambda t, i: 20.0 if i==0 and t<10 else 0.0, 50))
    
    w = np.zeros((2, 2))
    w[0, 1] = -10.0 
    results.append(compare("Test D (2-neuron Inh)", 2, w, 1.8, lambda t, i: 20.0 if i==0 and t<10 else 0.0, 50))
    
    w = np.array([[0, 5.0], [-5.0, 0]])
    results.append(compare("Test E (Recurrent)", 2, w, 1.8, lambda t, i: 15.0 if t<20 else 0.0, 100))
    
    w = np.array([[0, 0, 10.0], [0, 0, 10.0], [0, 0, 0]])
    results.append(compare("Test F (Simul Spikes)", 3, w, 1.8, lambda t, i: 30.0 if (i==0 or i==1) and t<5 else 0.0, 50))
    
    results.append(compare("Test G (Refractory)", 1, np.zeros((1, 1)), 1.8, lambda t, i: 50.0, 50))
    
    df = pd.DataFrame(results)
    import os
    os.makedirs("reports/c3/audit", exist_ok=True)
    df.to_csv("reports/c3/audit/brian2_parity_reaudit.csv", index=False)
    
    with open("reports/c3/audit/brian2_parity_reaudit.md", "w") as f:
        f.write("# Brian2 Parity Re-Audit\n\n")
        f.write(df.to_markdown(index=False))
        
if __name__ == "__main__":
    run_all()
