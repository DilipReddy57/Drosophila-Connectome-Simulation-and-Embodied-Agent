import pytest
import pandas as pd
from drosophila_connectome.neural.graph_adapter import load_graph

CONNECTIONS_PATH = 'data/derived/final_v1/connections.parquet'
NEURONS_PATH = 'data/derived/final_v1/neurons.parquet'
DENSE_MAPPING_PATH = 'data/derived/final_v1/dense_id_mapping.parquet'

@pytest.fixture
def graph():
    return load_graph(CONNECTIONS_PATH, NEURONS_PATH, DENSE_MAPPING_PATH)

def test_endpoint_validity(graph):
    # nodes within bounds
    assert (graph.dense_pre >= 0).all() and (graph.dense_pre < graph.num_nodes).all()
    assert (graph.dense_post >= 0).all() and (graph.dense_post < graph.num_nodes).all()

def test_synapse_counts(graph):
    df = pd.read_parquet(CONNECTIONS_PATH)
    # self loops excluded in graph
    df = df[df['pre_dense_index'] != df['post_dense_index']]
    assert df['synapse_count'].sum() == graph.synapse_count.sum()

def test_nt_preservation(graph):
    df = pd.read_parquet(CONNECTIONS_PATH)
    df = df[df['pre_dense_index'] != df['post_dense_index']]
    df = df.sort_values(by=['pre_dense_index', 'post_dense_index'])
    if 'source_nt_type' in df.columns:
        assert (graph.nt_type == df['source_nt_type'].values).all()

def test_no_self_loops(graph):
    assert not (graph.dense_pre == graph.dense_post).any()

def test_deterministic(graph):
    graph2 = load_graph(CONNECTIONS_PATH, NEURONS_PATH, DENSE_MAPPING_PATH)
    assert (graph.dense_pre == graph2.dense_pre).all()
    assert (graph.dense_post == graph2.dense_post).all()
    assert (graph.synapse_count == graph2.synapse_count).all()
