import time
import tracemalloc
import numpy as np
import scipy.sparse as sp
import sys
import os

# Ensure the project root is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from drosophila_connectome.neural.lif import Network, Simulation, LIFParameters

def generate_random_sparse_matrix(N, avg_degree=30):
    if N <= avg_degree:
        num_edges = N * N
    else:
        num_edges = N * avg_degree
        
    rows = np.random.randint(0, N, size=num_edges)
    cols = np.random.randint(0, N, size=num_edges)
    data = np.random.rand(num_edges) * 0.1 # Small random weights
    mat = sp.csr_matrix((data, (rows, cols)), shape=(N, N))
    return mat

def run_benchmark(N, avg_degree=30, num_steps=1000):
    print(f"Benchmarking N={N}...")
    
    # Measure init and memory
    tracemalloc.start()
    init_start = time.time()
    
    weights = generate_random_sparse_matrix(N, avg_degree)
    params = LIFParameters()
    network = Network(N, weights, params)
    simulation = Simulation(network)
    
    init_end = time.time()
    init_time = init_end - init_start
    
    # Measure memory
    current, peak = tracemalloc.get_traced_memory()
    memory_mb = peak / (1024 * 1024)
    tracemalloc.stop()
    
    # Measure simulation
    ext_I = np.zeros(N)
    ext_I[:max(1, N//10)] = 20.0
    inputs = {s: ext_I for s in range(num_steps)}
    
    sim_start = time.time()
    simulation.run(num_steps, inputs=inputs)
    sim_end = time.time()
    sim_time = sim_end - sim_start
    
    return init_time, sim_time, memory_mb

def main():
    sizes = [10, 100, 1000, 10000, 50000, 139255]
    results = []
    
    for N in sizes:
        init_t, sim_t, mem_mb = run_benchmark(N)
        results.append((N, init_t, sim_t, mem_mb))
        
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../reports/c3/benchmarks'))
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, 'scaling.csv')
    
    with open(out_file, 'w') as f:
        f.write("N,init_time,sim_time,memory_mb\n")
        for res in results:
            f.write(f"{res[0]},{res[1]:.4f},{res[2]:.4f},{res[3]:.4f}\n")
            
    print(f"Results saved to {out_file}")

if __name__ == "__main__":
    main()
