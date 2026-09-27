import pandas as pd
import numpy as np
from .sparse_graph import SparseGraph

def load_graph(connections_path: str, neurons_path: str, dense_mapping_path: str = None) -> SparseGraph:
    connections = pd.read_parquet(connections_path)
    neurons = pd.read_parquet(neurons_path)
    
    # Filter self-loops
    mask = connections['pre_dense_index'] != connections['post_dense_index']
    connections = connections[mask].copy()
    
    # Deterministic order
    connections.sort_values(by=['pre_dense_index', 'post_dense_index'], inplace=True)
    
    num_nodes = len(neurons)
    
    dense_pre = connections['pre_dense_index'].values.astype(np.int32)
    dense_post = connections['post_dense_index'].values.astype(np.int32)
    synapse_count = connections['synapse_count'].values.astype(np.int32)
    nt_type = connections['source_nt_type'].values if 'source_nt_type' in connections.columns else np.array(['UNKNOWN'] * len(connections))
    
    return SparseGraph(
        num_nodes=num_nodes,
        dense_pre=dense_pre,
        dense_post=dense_post,
        synapse_count=synapse_count,
        nt_type=nt_type
    )
