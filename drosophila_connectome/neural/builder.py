import numpy as np
import scipy.sparse as sp
from .sparse_graph import SparseGraph
from .lif.parameters import LIFParameters
from .lif.network import Network

def build_network_from_graph(graph: SparseGraph, params: LIFParameters = None) -> Network:
    """
    Constructs the LIF network directly from the topological canonical graph data.
    
    This function implements the specific connectivity conversion equations
    from Shiu et al. (2024):
    w_j = W_syn * S_j * N_syn
    
    where:
    W_syn is the global synaptic weight scaling factor (default 0.275 mV).
    S_j is the neurotransmitter polarity sign (+1 for ACh, -1 for GABA/Glut/Hist).
    N_syn is the physical synapse count on the edge.
    """
    if params is None:
        params = LIFParameters()
        
    # Map neurotransmitters to polarity signs (S_j)
    # Shiu et al. mapping: ACh -> +1. GABA, Glutamate, Histamine -> -1
    polarity = np.zeros_like(graph.nt_type, dtype=np.float32)
    polarity[graph.nt_type == 'ACH'] = 1.0
    polarity[graph.nt_type == 'GABA'] = -1.0
    polarity[graph.nt_type == 'GLUT'] = -1.0
    polarity[graph.nt_type == 'SER'] = 0.0 # Not explicitly excitatory/inhibitory in standard LIF without specific receptor mapping
    polarity[graph.nt_type == 'DA'] = 0.0
    polarity[graph.nt_type == 'OCT'] = 0.0
    # Add other NTs if strictly required, but for basic mapping we use the primary ones.
    
    # In Shiu et al:
    # "synaptic polarities S_j were set to 1 for excitatory and -1 for inhibitory neurons based on their predicted principal neurotransmitter"
    
    # Calculate final weights
    # w_j = N_syn * S_j * W_syn
    weights = graph.synapse_count.astype(np.float32) * polarity * params.W_syn
    
    # Construct scipy sparse matrix
    # Format: (data, (row_ind, col_ind))
    # We want weight_matrix[post, pre] = weight for easy vector matrix multiplication (W @ Spikes)
    weight_matrix = sp.csr_matrix(
        (weights, (graph.dense_post, graph.dense_pre)),
        shape=(graph.num_nodes, graph.num_nodes)
    )
    
    return Network(graph.num_nodes, weight_matrix, params)
