import numpy as np
import json
import pandas as pd
from pathlib import Path

def get_sugar_neurons():
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
        if str(nid) in mapping:
            dense_indices.append(int(mapping[str(nid)]))
    return dense_indices

def generate_poisson_spikes(dense_indices, rate_hz, duration_ms, dt_ms, seed=42):
    np.random.seed(seed)
    steps = int(duration_ms / dt_ms)
    prob_per_step = (rate_hz / 1000.0) * dt_ms
    
    spikes = []
    for step in range(steps):
        mask = np.random.rand(len(dense_indices)) < prob_per_step
        active = np.array(dense_indices)[mask]
        timestamp_ms = round(step * dt_ms, 4)
        for idx in active:
            spikes.append([timestamp_ms, int(idx)])
            
    return spikes

def main():
    dense_indices = get_sugar_neurons()
    spikes = generate_poisson_spikes(dense_indices, 100.0, 1000.0, 0.1, seed=42)
    out_dir = Path("experiments/c3/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "input_spikes.json", "w") as f:
        json.dump(spikes, f)
    print(f"Generated {len(spikes)} spikes for {len(dense_indices)} neurons.")

if __name__ == '__main__':
    main()
