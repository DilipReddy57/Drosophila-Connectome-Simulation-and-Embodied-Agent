import polars as pl
from drosophila_connectome.c2.degree import compute_degrees, compute_distribution_stats, get_top_50

def test_compute_degrees():
    neurons = pl.DataFrame({
        "neuron_id": ["A", "B", "C"]
    })
    
    connections = pl.DataFrame({
        "pre_neuron_id": ["A", "A", "B", "B", "B"],
        "post_neuron_id": ["B", "C", "C", "A", "A"],
        "synapse_count": [1, 2, 1, 2, 3] # B->A total 5, B->C total 1
    })
    
    res = compute_degrees(neurons, connections)
    
    assert res.height == 3
    
    # Check A
    a = res.filter(pl.col("neuron_id") == "A").row(0, named=True)
    assert a["structural_out_degree"] == 2 # to B, C
    assert a["structural_in_degree"] == 1 # from B
    assert a["structural_total_degree"] == 3
    assert a["weighted_out_degree"] == 3 # 1+2
    assert a["weighted_in_degree"] == 5 # from B is 2+3
    assert a["weighted_total_degree"] == 8
    
    # Check B
    b = res.filter(pl.col("neuron_id") == "B").row(0, named=True)
    assert b["structural_out_degree"] == 2 # to A, C
    assert b["structural_in_degree"] == 1 # from A
    assert b["structural_total_degree"] == 3
    assert b["weighted_out_degree"] == 6 # 1+2+3
    assert b["weighted_in_degree"] == 1 # from A
    assert b["weighted_total_degree"] == 7
    
    # Check C
    c = res.filter(pl.col("neuron_id") == "C").row(0, named=True)
    assert c["structural_out_degree"] == 0
    assert c["structural_in_degree"] == 2 # from A, B
    assert c["structural_total_degree"] == 2
    assert c["weighted_out_degree"] == 0
    assert c["weighted_in_degree"] == 3 # 2+1
    assert c["weighted_total_degree"] == 3

def test_compute_distribution_stats():
    series = pl.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    stats = compute_distribution_stats(series)
    assert stats["min"] == 1.0
    assert stats["max"] == 5.0
    assert stats["median"] == 3.0
    
def test_get_top_50():
    df = pl.DataFrame({
        "neuron_id": [str(i) for i in range(100)],
        "val": list(range(100))
    })
    top = get_top_50(df, "val")
    assert len(top) == 50
    assert top[0] == "99"
    assert top[-1] == "50"
