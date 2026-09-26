import pytest
from drosophila_connectome.c2.topology import calculate_topology
from pathlib import Path
import json

def test_calculate_topology():
    metrics = calculate_topology()
    
    assert 'nodes' in metrics
    assert 'edges' in metrics
    assert metrics['nodes'] > 0
    assert metrics['edges'] > 0
    assert 'density' in metrics
    assert 'weakly_connected_components' in metrics
    assert 'strongly_connected_components' in metrics
    assert 'reciprocal_pairs' in metrics
    
    out_dir = Path('reports/c2')
    assert (out_dir / 'topology.json').exists()
    assert (out_dir / 'topology_report.md').exists()
    assert (out_dir / 'figures' / 'wcc_distribution.png').exists()
    assert (out_dir / 'figures' / 'scc_distribution.png').exists()
