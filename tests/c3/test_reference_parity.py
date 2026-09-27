import numpy as np
import scipy.sparse as sp
import os

from drosophila_connectome.neural.lif.network import Network, Simulation
from drosophila_connectome.neural.lif.parameters import LIFParameters

def run_custom_sim():
    num_neurons = 2
    weight_matrix = sp.csr_matrix((np.array([10.0]), (np.array([1]), np.array([0]))), shape=(2, 2))
    
    # dt=0.1 ms
    params = LIFParameters(
        V_rest=-52.0,
        V_reset=-52.0,
        V_th=-45.0,
        tau_m=20.0,
        tau_syn=5.0,
        t_ref=2.2,
        delay=1.8,
        dt=0.1,
        W_syn=1.0 # The weight matrix is in mV, so W_syn multiplier is 1.0
    )
    
    net = Network(num_neurons, weight_matrix, params)
    sim = Simulation(net)
    
    num_steps = 500
    
    # Inject current to Neuron 0 for first 100 steps
    inputs = {s: (np.array([20.0, 0.0]) if s < 100 else np.array([0.0, 0.0])) for s in range(num_steps)}
    
    v_trace = np.zeros((num_steps, 2))
    i_trace = np.zeros((num_steps, 2))
    
    for s in range(num_steps):
        v_trace[s, :] = net.state.V.copy()
        i_trace[s, :] = net.state.I_syn.copy()
        sim.step(inputs[s])
        
    return {
        "t": np.arange(num_steps) * 0.1,
        "V": v_trace,
        "I_syn": i_trace,
        "spikes": sim.recorder.spikes
    }

if __name__ == "__main__":
    import brian2_reference
    brian_res = brian2_reference.run_brian2_reference()
    custom_res = run_custom_sim()
    
    import matplotlib.pyplot as plt
    
    os.makedirs("reports/c3/validation", exist_ok=True)
    
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    
    axes[0].plot(brian_res["t"], brian_res["V"][0], label="Brian2 N0", linestyle="--")
    axes[0].plot(custom_res["t"], custom_res["V"][:, 0], label="Custom N0", alpha=0.7)
    axes[0].plot(brian_res["t"], brian_res["V"][1], label="Brian2 N1", linestyle="--")
    axes[0].plot(custom_res["t"], custom_res["V"][:, 1], label="Custom N1", alpha=0.7)
    axes[0].set_ylabel("Membrane Voltage (mV)")
    axes[0].legend()
    axes[0].set_title("Membrane Voltage")
    
    axes[1].plot(brian_res["t"], brian_res["I_syn"][1], label="Brian2 I_syn N1", linestyle="--")
    axes[1].plot(custom_res["t"], custom_res["I_syn"][:, 1], label="Custom I_syn N1", alpha=0.7)
    axes[1].set_xlabel("Time (ms)")
    axes[1].set_ylabel("Synaptic Current (mV)")
    axes[1].legend()
    axes[1].set_title("Synaptic Current")
    
    plt.tight_layout()
    plt.savefig("reports/c3/validation/parity_plot.png")
    
    # Check parity
    brian_v = brian_res["V"].T # (time, neurons)
    custom_v = custom_res["V"]
    
    diff_v = np.abs(brian_v - custom_v)
    max_diff_v = np.max(diff_v)
    
    brian_isyn = brian_res["I_syn"].T
    custom_isyn = custom_res["I_syn"]
    diff_isyn = np.abs(brian_isyn - custom_isyn)
    max_diff_isyn = np.max(diff_isyn)
    
    print("Max Voltage Difference:", max_diff_v)
    print("Max I_syn Difference:", max_diff_isyn)
    print("Custom Spikes:", custom_res["spikes"])
    print("Brian Spikes:", list(zip(brian_res["spikes_t"], brian_res["spikes_i"])))

