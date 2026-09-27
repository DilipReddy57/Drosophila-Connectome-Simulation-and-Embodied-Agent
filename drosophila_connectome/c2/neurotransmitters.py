import polars as pl
from pathlib import Path
from drosophila_connectome.c2.common import load_canonical_data, write_c2_report

def analyze_neurotransmitters(verify: bool = True):
    neurons, connections = load_canonical_data(verify=verify)
    
    total_synapses = connections["synapse_count"].sum()
    
    metrics_df = connections.group_by("source_nt_type").agg([
        pl.len().alias("connection_count"),
        pl.col("synapse_count").sum().alias("total_synapses"),
        pl.col("pre_neuron_id").n_unique().alias("unique_pre_neurons"),
        pl.col("post_neuron_id").n_unique().alias("unique_post_neurons"),
        pl.col("synapse_count").mean().alias("mean_synapse_count"),
        pl.col("synapse_count").median().alias("median_synapse_count")
    ]).with_columns(
        (pl.col("total_synapses") / total_synapses).alias("synapse_fraction")
    )
    
    metrics = {
        row["source_nt_type"]: {
            "connection_count": row["connection_count"],
            "total_synapses": row["total_synapses"],
            "synapse_fraction": row["synapse_fraction"],
            "unique_pre_neurons": row["unique_pre_neurons"],
            "unique_post_neurons": row["unique_post_neurons"],
            "mean_synapse_count": row["mean_synapse_count"],
            "median_synapse_count": row["median_synapse_count"]
        } for row in metrics_df.to_dicts()
    }
    
    md = [
        "# Neurotransmitter Analysis (Agent E)",
        "",
        "This report analyzes the `source_nt_type` annotations across the connectome.",
        "",
        "## Metrics per NT Type",
        ""
    ]
    
    for nt, m in metrics.items():
        md.append(f"### {nt}")
        for k, v in m.items():
            md.append(f"- {k}: {v}")
        md.append("")
        
    md.extend([
        "## Important Limitations & Methodology",
        "- **Data Aggregation**: The `source_nt_type` is propagated using `.first()` during canonical aggregation. For FAFB v783, this is safe as there are zero duplicate groups, but for future datasets with conflicts, this may introduce loss of resolution.",
        "- **No Inference**: These types are treated strictly as annotations. We explicitly do NOT infer or claim excitation/inhibition mappings from NT types (e.g., we do not claim ACh = excitatory)."
    ])
    
    write_c2_report("neurotransmitters", metrics, "\n".join(md), Path("reports/c2"))
    return metrics

if __name__ == "__main__":
    analyze_neurotransmitters()
