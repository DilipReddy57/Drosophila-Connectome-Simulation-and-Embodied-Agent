import numpy as np
from scipy.sparse import csr_matrix

class SparseGraph:
    def __init__(
        self,
        num_nodes: int,
        dense_pre: np.ndarray,
        dense_post: np.ndarray,
        synapse_count: np.ndarray,
        nt_type: np.ndarray
    ):
        self.num_nodes = num_nodes
        self.dense_pre = dense_pre
        self.dense_post = dense_post
        self.synapse_count = synapse_count
        self.nt_type = nt_type
        self.adj_matrix = csr_matrix(
            (self.synapse_count, (self.dense_pre, self.dense_post)),
            shape=(num_nodes, num_nodes)
        )
