import polars as pl
from pathlib import Path
from drosophila_connectome.c2.neurotransmitters import analyze_neurotransmitters
from unittest.mock import patch

def test_analyze_neurotransmitters(tmp_path):
    neurons = pl.DataFrame({"id": [1, 2]})
    connections = pl.DataFrame({
        "pre_id": [1, 2, 1],
        "post_id": [2, 1, 2],
        "synapse_count": [10, 20, 5],
        "source_nt_type": ["ACH", "GABA", "ACH"]
    })
    
    with patch("drosophila_connectome.c2.neurotransmitters.load_canonical_data", return_value=(neurons, connections)):
        with patch("drosophila_connectome.c2.neurotransmitters.write_c2_report") as mock_write:
            
            metrics = analyze_neurotransmitters(verify=False)
            
            assert "ACH" in metrics
            assert "GABA" in metrics
            
            ach = metrics["ACH"]
            assert ach["connection_count"] == 2
            assert ach["total_synapses"] == 15
            assert ach["unique_pre_neurons"] == 1
            assert ach["unique_post_neurons"] == 1
            assert ach["mean_synapse_count"] == 7.5
            assert ach["median_synapse_count"] == 7.5
            
            gaba = metrics["GABA"]
            assert gaba["connection_count"] == 1
            assert gaba["total_synapses"] == 20
