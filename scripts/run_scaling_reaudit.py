import time
import tracemalloc
import numpy as np
import scipy.sparse as sp
import pandas as pd
from drosophila_connectome.neural.lif.network import Network, Simulation
from drosophila_connectome.neural.lif.parameters import LIFParameters

def run_benchmark(num_neurons):
    # Sparsity = 30 connections avg
    num_edges = num_neurons * min(30, num_neurons)
    
    # Generate random sparse matrix
    row_ind = np.random.randint(0, num_neurons, size=num_edges)
    col_ind = np.random.randint(0, num_neurons, size=num_edges)
    data = np.random.rand(num_edges) * 0.275 # random weights up to 0.275mV
    
    weight_matrix = sp.csr_matrix((data, (row_ind, col_ind)), shape=(num_neurons, num_neurons))
    
    params = LIFParameters(dt=0.1)
    
    tracemalloc.start()
    t0 = time.time()
    
    net = Network(num_neurons, weight_matrix, params)
    sim = Simulation(net)
    
    t_init = time.time() - t0
    
    t0_sim = time.time()
    
    # Run 100 ms (1000 steps)
    sim.run(1000)
    
    t_sim = time.time() - t0_sim
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    peak_mb = peak / (1024 * 1024)
    
    return {
        "Neuron_Count": num_neurons,
        "Edge_Count": num_edges,
        "Init_Time_s": t_init,
        "Sim_Time_s": t_sim,
        "Peak_Memory_MB": peak_mb,
        "Spike_Count": len(sim.recorder.spikes)
    }

def main():
    sizes = [10, 100, 1000, 10000, 50000, 100000, 139255]
    results = []
    
    print("Running benchmarks...")
    for s in sizes:
        print(f"Benchmarking N={s}...")
        res = run_benchmark(s)
        results.append(res)
        
    df = pd.DataFrame(results)
    
    import os
    os.makedirs("reports/c3/audit", exist_ok=True)
    df.to_csv("reports/c3/audit/scaling_reaudit.csv", index=False)
    
    with open("reports/c3/audit/scaling_reaudit.md", "w") as f:
        f.write("# Scaling Re-Audit\n\n")
        f.write("Machine: Github Actions Runner (or local)\n")
        f.write("OS: Windows\n")
        f.write("Simulation duration: 100 ms\n")
        f.write("dt: 0.1 ms\n\n")
        f.write(df.to_markdown(index=False))
        
    print("Done. Saved to reports/c3/audit/scaling_reaudit.csv")

if __name__ == "__main__":
    main()
