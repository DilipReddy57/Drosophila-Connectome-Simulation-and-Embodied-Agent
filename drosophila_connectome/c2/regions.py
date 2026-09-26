import polars as pl
import matplotlib.pyplot as plt
from pathlib import Path
from drosophila_connectome.c2.common import load_canonical_data, write_c2_report

def analyze_regions(mock_data=None, output_dir=Path("reports/c2")):
    if mock_data is not None:
        _, connections = mock_data
    else:
        _, connections = load_canonical_data(verify=False)

    region_stats = connections.group_by("region").agg([
        pl.len().alias("connection_rows"),
        pl.col("synapse_count").sum().alias("total_synapses"),
        pl.col("pre_neuron_id").n_unique().alias("unique_pre_neurons"),
        pl.col("post_neuron_id").n_unique().alias("unique_post_neurons")
    ])

    total_rows = connections.height
    total_synapses_all = connections.select(pl.col("synapse_count").sum()).item()

    region_stats = region_stats.with_columns([
        ((pl.col("connection_rows") / total_rows) * 100).alias("pct_connection_rows"),
        ((pl.col("total_synapses") / total_synapses_all) * 100).alias("pct_total_synapses")
    ])

    region_stats = region_stats.sort("total_synapses", descending=True)
    
    metrics = {
        row["region"]: {
            "connection_rows": row["connection_rows"],
            "total_synapses": row["total_synapses"],
            "unique_pre_neurons": row["unique_pre_neurons"],
            "unique_post_neurons": row["unique_post_neurons"],
            "pct_connection_rows": row["pct_connection_rows"],
            "pct_total_synapses": row["pct_total_synapses"]
        }
        for row in region_stats.to_dicts()
    }
    
    markdown_str = "# Region Analysis Report\n\n"
    markdown_str += "## Region Synapse Distribution\n\n"
    markdown_str += "| Region | Rows | Synapses | Unique Pre | Unique Post | % Rows | % Synapses |\n"
    markdown_str += "|---|---|---|---|---|---|---|\n"
    for row in region_stats.to_dicts():
        markdown_str += f"| {row['region']} | {row['connection_rows']} | {row['total_synapses']} | {row['unique_pre_neurons']} | {row['unique_post_neurons']} | {row['pct_connection_rows']:.2f}% | {row['pct_total_synapses']:.2f}% |\n"

    if not mock_data:
        _generate_plots(region_stats, output_dir / "figures")
        write_c2_report("regions", {"regions": metrics}, markdown_str, output_dir)
        
    return region_stats

def _generate_plots(region_stats, figures_dir):
    figures_dir.mkdir(parents=True, exist_ok=True)
    df = region_stats.to_pandas()
    plt.figure(figsize=(12, 6))
    plt.bar(df["region"], df["total_synapses"])
    plt.xticks(rotation=90)
    plt.title("Total Synapses per Region")
    plt.ylabel("Synapses")
    plt.tight_layout()
    plt.savefig(figures_dir / "synapses_per_region.png")
    plt.close()

    plt.figure(figsize=(12, 6))
    x = range(len(df))
    plt.bar([i - 0.2 for i in x], df["unique_pre_neurons"], width=0.4, label="Pre Neurons")
    plt.bar([i + 0.2 for i in x], df["unique_post_neurons"], width=0.4, label="Post Neurons")
    plt.xticks(x, df["region"], rotation=90)
    plt.title("Unique Pre/Post Neurons per Region")
    plt.ylabel("Unique Neurons")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / "unique_neurons_per_region.png")
    plt.close()

if __name__ == '__main__':
    analyze_regions()
