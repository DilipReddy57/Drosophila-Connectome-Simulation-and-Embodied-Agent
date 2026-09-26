import numpy as np
import polars as pl
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
import matplotlib.pyplot as plt
from pathlib import Path
from drosophila_connectome.c2.common import load_canonical_data, write_c2_report

def calculate_topology():
    neurons, connections = load_canonical_data()
    N = len(neurons)
    row = connections['pre_dense_index'].to_numpy()
    col = connections['post_dense_index'].to_numpy()
    data = np.ones(len(row), dtype=np.int8)
    E = len(row)
    adj = coo_matrix((data, (row, col)), shape=(N, N)).tocsr()
    n_wcc, labels_wcc = connected_components(csgraph=adj, directed=False, return_labels=True)
    n_scc, labels_scc = connected_components(csgraph=adj, directed=True, connection='strong', return_labels=True)
    wcc_counts = np.bincount(labels_wcc)
    scc_counts = np.bincount(labels_scc)
    isolated_count = int(np.sum(wcc_counts == 1))
    largest_wcc = int(np.max(wcc_counts))
    largest_scc = int(np.max(scc_counts))
    adj_bool = adj.astype(bool)
    adj_t_bool = adj_bool.transpose()
    reciprocal_adj = adj_bool.multiply(adj_t_bool)
    reciprocal_edges_count = int(reciprocal_adj.nnz)
    total_unique_directed_edges = int(adj_bool.nnz)
    reciprocal_pairs = reciprocal_edges_count // 2
    reciprocity_val = reciprocal_edges_count / total_unique_directed_edges if total_unique_directed_edges > 0 else 0.0
    reciprocity_formula = 'E_recip / E_total (where E_recip is number of directed edges with a counterpart)'
    density = total_unique_directed_edges / (N * N) if N > 0 else 0.0
    metrics = {
        'nodes': int(N),
        'edges': int(E),
        'unique_directed_edges': total_unique_directed_edges,
        'weakly_connected_components': int(n_wcc),
        'strongly_connected_components': int(n_scc),
        'largest_wcc_size': largest_wcc,
        'largest_scc_size': largest_scc,
        'isolated_nodes': isolated_count,
        'reciprocal_pairs': reciprocal_pairs,
        'reciprocity': reciprocity_val,
        'reciprocity_formula': reciprocity_formula,
        'density': density,
        'density_formula': 'observed unique directed edges / (N * N)'
    }
    out_dir = Path('reports/c2')
    fig_dir = out_dir / 'figures'
    fig_dir.mkdir(parents=True, exist_ok=True)
    plt.figure()
    wcc_sizes = np.sort(wcc_counts)[::-1]
    plt.plot(wcc_sizes, marker='o', linestyle='none', markersize=2)
    plt.yscale('log')
    plt.xscale('log')
    plt.title('WCC Size Distribution')
    plt.xlabel('Component Rank')
    plt.ylabel('Size')
    plt.savefig(fig_dir / 'wcc_distribution.png')
    plt.close()
    plt.figure()
    scc_sizes = np.sort(scc_counts)[::-1]
    plt.plot(scc_sizes, marker='o', linestyle='none', markersize=2)
    plt.yscale('log')
    plt.xscale('log')
    plt.title('SCC Size Distribution')
    plt.xlabel('Component Rank')
    plt.ylabel('Size')
    plt.savefig(fig_dir / 'scc_distribution.png')
    plt.close()
    md = f'''# Topology Analysis Report\n\n## Metrics\n- **Nodes**: {N}\n- **Edges (raw)**: {E}\n- **Unique Directed Edges**: {total_unique_directed_edges}\n- **Density**: {density:.6e} ({metrics['density_formula']})\n- **Reciprocity**: {reciprocity_val:.4f} ({reciprocity_formula})\n- **Reciprocal Pairs**: {reciprocal_pairs}\n\n## Components\n- **Weakly Connected Components (WCC)**: {n_wcc}\n- **Largest WCC Size**: {largest_wcc}\n- **Strongly Connected Components (SCC)**: {n_scc}\n- **Largest SCC Size**: {largest_scc}\n- **Isolated Nodes**: {isolated_count}\n\n## Plots\n![WCC Distribution](figures/wcc_distribution.png)\n![SCC Distribution](figures/scc_distribution.png)\n'''
    write_c2_report('topology', metrics, md, out_dir)
    return metrics

if __name__ == '__main__':
    calculate_topology()
