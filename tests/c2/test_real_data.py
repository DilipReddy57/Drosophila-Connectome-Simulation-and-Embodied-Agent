import polars as pl
from pathlib import Path
from drosophila_connectome.c2.common import load_canonical_data

def test_real_data_invariants():
    neurons, connections = load_canonical_data(verify=True)
    
    # 1. Dataset Accounting
    assert neurons.height == 139255
    assert connections.height == 5342446
    assert connections["synapse_count"].sum() == 50666648
    
    # 2. Endpoints & Uniqueness
    valid_pres = connections.join(neurons, left_on="pre_neuron_id", right_on="neuron_id", how="anti").height == 0
    valid_posts = connections.join(neurons, left_on="post_neuron_id", right_on="neuron_id", how="anti").height == 0
    assert valid_pres and valid_posts
    
    assert neurons.select(["neuron_id"]).is_duplicated().sum() == 0
    assert neurons.select(["dense_index"]).is_duplicated().sum() == 0
    
    # Dense ID contiguity
    assert neurons["dense_index"].min() == 0
    assert neurons["dense_index"].max() == neurons.height - 1
    assert neurons.filter(pl.col("dense_index").is_null()).height == 0
    
    # 3. Canonical duplicate groups
    assert connections.select(["pre_neuron_id", "post_neuron_id", "region"]).is_duplicated().sum() == 0
    
    # 4. Self edges
    assert connections.filter(pl.col("pre_neuron_id") == pl.col("post_neuron_id")).height == 0
    
    # 5. NT Aggregation Robustness
    # Verify directly from raw data to ensure canonical .first() didn't hide conflicts
    raw_path = Path("data/raw/fafb_v783/connections_princeton.csv.gz")
    if raw_path.exists():
        raw_df = pl.read_csv(raw_path)
        nt_conflicts = raw_df.group_by(["pre_root_id", "post_root_id", "neuropil"]).agg(
            pl.col("nt_type").n_unique().alias("unique_nt_count")
        )
        max_nt = nt_conflicts["unique_nt_count"].max()
        conflicting_groups = nt_conflicts.filter(pl.col("unique_nt_count") > 1).height
        assert conflicting_groups == 0
        assert max_nt <= 1

if __name__ == "__main__":
    test_real_data_invariants()
    print("Real-data smoke validation passed.")
