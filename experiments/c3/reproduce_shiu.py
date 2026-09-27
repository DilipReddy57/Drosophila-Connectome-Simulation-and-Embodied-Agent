import pandas as pd
import time
import json
import hashlib
import numpy as np
import scipy.sparse as sp
from pathlib import Path

import os
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
from brian2 import *

from drosophila_connectome.neural.graph_adapter import load_graph
from drosophila_connectome.neural.builder import build_network_from_graph
from drosophila_connectome.neural.lif.network import Simulation
from drosophila_connectome.neural.lif.parameters import LIFParameters

def get_sugar_neurons(sg):
    df_map = pd.read_parquet('data/derived/final_v1/dense_id_mapping.parquet')
    mapping = dict(zip(df_map['root_id'], df_map['dense_index']))
    sugar_ids = [
        720575940624963786, 720575940630233916, 720575940637568838,
        720575940638202345, 720575940617000768, 720575940630797113,
        720575940632889389, 720575940621754367, 720575940621502051,
        720575940640649691, 720575940639332736, 720575940616885538,
        720575940639198653, 720575940620900446, 720575940617937543,
        720575940632425919, 720575940633143833, 720575940612670570,
        720575940628853239, 720575940629176663, 720575940611875570
    ]
    dense_indices = []
    for nid in sugar_ids:
        if nid in mapping:
            dense_indices.append(mapping[nid])
    return dense_indices

def get_mn9_dense(sg):
    df_map = pd.read_parquet('data/derived/final_v1/dense_id_mapping.parquet')
    mapping = dict(zip(df_map['root_id'], df_map['dense_index']))
    mn9_id = 720575940660219265
    return mapping.get(mn9_id, None)

def run_baseline(sg):
    print("=== RUNNING BASELINE (NO STIMULUS) ===")
    net = build_network_from_graph(sg)
    sim = Simulation(net)
    
    t0 = time.time()
    sim.run(10000) # 1000 ms at dt=0.1
    t_run = time.time() - t0
    
    total_spikes = len(sim.recorder.spikes)
    print(f"Baseline total spikes: {total_spikes}")
    print(f"Baseline runtime: {t_run:.2f} s")
    
    out_dir = Path("experiments/c3/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "baseline.json", "w") as f:
        json.dump({
            "experiment": "BASELINE",
            "duration_ms": 1000,
            "total_spikes": total_spikes,
            "runtime_s": t_run
        }, f, indent=2)

def generate_poisson_spikes(dense_indices, rate_hz, duration_ms, dt_ms, seed=42):
    np.random.seed(seed)
    steps = int(duration_ms / dt_ms)
    prob_per_step = (rate_hz / 1000.0) * dt_ms
    
    spikes_by_step = {}
    for step in range(steps):
        mask = np.random.rand(len(dense_indices)) < prob_per_step
        active = np.array(dense_indices)[mask]
        if len(active) > 0:
            spikes_by_step[step] = active
            
    return spikes_by_step

def run_custom_model(sg, sugar_dense, mn9_dense):
    print("=== RUNNING CUSTOM MODEL (100 Hz SUGAR) ===")
    net = build_network_from_graph(sg)
    
    if len(sugar_dense) == 0:
        spikes_by_step = {}
    else:
        spikes_by_step = generate_poisson_spikes(sugar_dense, 100.0, 1000.0, 0.1, seed=42)
    sim = Simulation(net)
    
    jump_v = 0.275 * 250.0
    
    t0 = time.time()
    steps = 10000
    for s in range(steps):
        if s in spikes_by_step:
            active = spikes_by_step[s]
            net.state.V[active] += jump_v
            net.state.refractory_time[active] = 0
        sim.step()
        
    t_run = time.time() - t0
    
    mn9_spikes = 0
    if mn9_dense is not None:
        mn9_spikes = len([1 for step, nid in sim.recorder.spikes if nid == mn9_dense])
    total_spikes = len(sim.recorder.spikes)
    
    print(f"Custom Model Runtime: {t_run:.2f} s")
    print(f"Custom Model Total Spikes: {total_spikes}")
    print(f"Custom Model MN9 Firing Rate: {mn9_spikes} Hz")
    
    return mn9_spikes, total_spikes, t_run

def run_brian2_reference(sg, sugar_dense, mn9_dense):
    print("=== RUNNING BRIAN2 REFERENCE (100 Hz SUGAR) ===")
    prefs.codegen.target = "numpy"
    defaultclock.dt = 0.1 * ms
    
    eqs = """
    dv/dt = (-52*mV - v + g) / (20*ms) : volt (unless refractory)
    dg/dt = -g / (5*ms)                : volt (unless refractory)
    rfc                                : second
    """
    
    num_nodes = sg.num_nodes
    neu = NeuronGroup(num_nodes, eqs, method='linear', threshold='v > -45*mV', reset='v = -52*mV; g=0*mV', refractory='rfc')
    neu.v = -52 * mV
    neu.g = 0 * mV
    neu.rfc = 2.2 * ms
    
    # Create Synapses
    syn = Synapses(neu, neu, 'w : volt', on_pre='g += w', delay=1.8*ms)
    
    # Map weights
    sources = sg.dense_pre
    targets = sg.dense_post
    counts = sg.synapse_count
    
    # Shiu NT rule: ACH=1, GABA/GLUT=-1, else 0
    sign_array = np.zeros_like(counts, dtype=np.float32)
    sign_array[sg.nt_type == 'ACH'] = 1.0
    sign_array[sg.nt_type == 'GABA'] = -1.0
    sign_array[sg.nt_type == 'GLUT'] = -1.0
    
    w_array = counts * sign_array * 0.275
    
    print("Connecting Brian2 Synapses...")
    syn.connect(i=sources, j=targets)
    syn.w = w_array * mV
    
    print("Setting up Poisson Inputs...")
    pois = []
    seed(42)
    for i in sugar_dense:
        p = PoissonInput(target=neu[i], target_var='v', N=1, rate=100*Hz, weight=0.275*250*mV)
        neu.rfc[i] = 0 * ms
        pois.append(p)
        
    spk_mon = SpikeMonitor(neu)
    
    print("Running Brian2 Simulation...")
    t0 = time.time()
    run(1000 * ms)
    t_run = time.time() - t0
    
    mn9_spikes = 0
    if mn9_dense is not None:
        mn9_spikes = list(spk_mon.i).count(mn9_dense)
    total_spikes = spk_mon.num_spikes
    
    print(f"Brian2 Runtime: {t_run:.2f} s")
    print(f"Brian2 Total Spikes: {total_spikes}")
    print(f"Brian2 MN9 Firing Rate: {mn9_spikes} Hz")
    
    return mn9_spikes, total_spikes, t_run

def main():
    print("Loading Graph...")
    sg = load_graph('data/derived/final_v1/connections.parquet', 'data/derived/final_v1/neurons.parquet')
    sugar_dense = get_sugar_neurons(sg)
    mn9_dense = get_mn9_dense(sg)
    
    print(f"Graph loaded. N={sg.num_nodes}, E={len(sg.dense_pre)}")
    print(f"Sugar neurons mapped: {len(sugar_dense)}")
    print(f"MN9 dense ID: {mn9_dense}")
    
    run_baseline(sg)
    
    int(c_mn9), int(float(c_t)otal), float(c_t) = run_custom_model(sg, sugar_dense, mn9_dense)
    int(b_mn9), int(float(b_t)otal), float(b_t) = run_brian2_reference(sg, sugar_dense, mn9_dense)
    
    out_dir = Path("experiments/c3/results")
    
    with open(out_dir / "shiu_sugar100_results.json", "w") as f:
        json.dump({
            "experiment": "sugarR_100Hz",
            "duration_ms": 1000,
            "custom": {
                "mn9_rate": int(c_mn9),
                "total_spikes": int(float(c_t)otal),
                "runtime_s": float(c_t)
            },
            "brian2_reference": {
                "mn9_rate": int(b_mn9),
                "total_spikes": int(float(b_t)otal),
                "runtime_s": float(b_t)
            },
            "diff_mn9_rate": abs(c_mn9 - b_mn9),
            "diff_total_spikes": abs(float(c_t)otal - float(b_t)otal)
        }, f, indent=2)
        
if __name__ == "__main__":
    main()
