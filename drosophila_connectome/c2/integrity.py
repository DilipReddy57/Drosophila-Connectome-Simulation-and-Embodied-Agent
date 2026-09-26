import polars as pl
from pathlib import Path
from drosophila_connectome.c2.common import load_canonical_data, write_c2_report

def analyze_integrity():
    neurons, connections = load_canonical_data()
    
    metrics = {}
    
    # Neuron count
    metrics['neuron_count'] = neurons.height
    
    # Connection rows
    metrics['connection_rows'] = connections.height
    
    # Total synapse count
    metrics['total_synapse_count'] = int(connections['synapse_count'].sum())
    
    # Self edges
    self_edges = connections.filter(pl.col('pre_neuron_id') == pl.col('post_neuron_id')).height
    metrics['self_edges'] = self_edges
    
    # Missing dense indices
    missing_dense = neurons.filter(pl.col('dense_index').is_null()).height
    metrics['missing_dense_indices'] = missing_dense
    
    # Duplicate root_ids
    duplicate_roots = neurons.filter(pl.col('neuron_id').is_duplicated()).height
    metrics['duplicate_root_ids'] = duplicate_roots
    
    # Duplicate connection rows
    duplicate_conns = connections.filter(
        connections.select(['pre_neuron_id', 'post_neuron_id', 'region']).is_duplicated()
    ).height
    metrics['duplicate_connection_rows'] = duplicate_conns
    
    # Endpoint validity
    valid_pres = connections.join(neurons, left_on='pre_neuron_id', right_on='neuron_id', how='anti').height == 0
    valid_posts = connections.join(neurons, left_on='post_neuron_id', right_on='neuron_id', how='anti').height == 0
    metrics['endpoint_validity'] = bool(valid_pres and valid_posts)
    
    # Create Markdown report
    lines = [
        "# Data Integrity Report",
        "",
        f"- **Neuron Count**: {metrics['neuron_count']}",
        f"- **Connection Rows**: {metrics['connection_rows']}",
        f"- **Total Synapse Count**: {metrics['total_synapse_count']}",
        f"- **Self Edges**: {metrics['self_edges']}",
        f"- **Missing Dense Indices**: {metrics['missing_dense_indices']}",
        f"- **Duplicate Root IDs**: {metrics['duplicate_root_ids']}",
        f"- **Duplicate Connection Rows**: {metrics['duplicate_connection_rows']}",
        f"- **Endpoint Validity**: {'Valid' if metrics['endpoint_validity'] else 'Invalid'}"
    ]
    markdown_str = '\n'.join(lines) + '\n'

    return metrics, markdown_str

if __name__ == '__main__':
    metrics, md = analyze_integrity()
    out_dir = Path(__file__).resolve().parents[2] / 'reports' / 'c2'
    write_c2_report('data_integrity', metrics, md, out_dir)
    print('Integrity report written to reports/c2/data_integrity_report.md')
