import polars as pl
from pathlib import Path
from drosophila_connectome.c2.regions import analyze_regions

def test_analyze_regions(tmp_path):
    mock_connections = pl.DataFrame({
        "pre_neuron_id": [1, 1, 2, 3],
        "post_neuron_id": [2, 3, 3, 4],
        "synapse_count": [10, 5, 20, 15],
        "region": ["AL", "AL", "MB", "AL"]
    })
    
    mock_neurons = pl.DataFrame() # unused in this analysis
    
    stats = analyze_regions(mock_data=(mock_neurons, mock_connections), output_dir=tmp_path)
    
    assert stats.height == 2
    
    # AL region
    al_stats = stats.filter(pl.col("region") == "AL").row(0, named=True)
    assert al_stats["connection_rows"] == 3
    assert al_stats["total_synapses"] == 30
    assert al_stats["unique_pre_neurons"] == 2  # pre_neuron_id: 1, 3
    assert al_stats["unique_post_neurons"] == 3 # post_neuron_id: 2, 3, 4
    
    # MB region
    mb_stats = stats.filter(pl.col("region") == "MB").row(0, named=True)
    assert mb_stats["connection_rows"] == 1
    assert mb_stats["total_synapses"] == 20
    assert mb_stats["unique_pre_neurons"] == 1  # pre_neuron_id: 2
    assert mb_stats["unique_post_neurons"] == 1 # post_neuron_id: 3
    
    # Check percentages
    assert al_stats["pct_connection_rows"] == 75.0
    assert al_stats["pct_total_synapses"] == 60.0
    assert mb_stats["pct_connection_rows"] == 25.0
    assert mb_stats["pct_total_synapses"] == 40.0
