import pytest
from drosophila_connectome.c2.integrity import analyze_integrity

def test_integrity_metrics():
    metrics, md = analyze_integrity()
    
    assert metrics['neuron_count'] == 139255
    assert metrics['connection_rows'] == 5342446
    assert metrics['total_synapse_count'] == 50666648
    assert metrics['self_edges'] == 0
    assert metrics['missing_dense_indices'] == 0
    assert metrics['duplicate_root_ids'] == 0
    assert metrics['duplicate_connection_rows'] == 0
    assert metrics['endpoint_validity'] is True
