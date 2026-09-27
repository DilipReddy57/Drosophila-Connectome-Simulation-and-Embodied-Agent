import polars as pl
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from drosophila_connectome.c2.common import load_canonical_data, write_c2_report

def compute_degrees(neurons: pl.DataFrame, connections: pl.DataFrame) -> pl.DataFrame:
    unique_edges = connections.group_by(["pre_neuron_id", "post_neuron_id"]).agg(
        pl.col("synapse_count").sum().alias("synapse_count")
    )
    
    out_structural = unique_edges.group_by("pre_neuron_id").agg(pl.len().alias("structural_out_degree"))
    in_structural = unique_edges.group_by("post_neuron_id").agg(pl.len().alias("structural_in_degree"))
    
    out_synapses = unique_edges.group_by("pre_neuron_id").agg(pl.col("synapse_count").sum().alias("outgoing_synapse_count"))
    in_synapses = unique_edges.group_by("post_neuron_id").agg(pl.col("synapse_count").sum().alias("incoming_synapse_count"))
    
    res = neurons.select(["neuron_id"])
    res = res.join(out_structural, left_on="neuron_id", right_on="pre_neuron_id", how="left")
    res = res.join(in_structural, left_on="neuron_id", right_on="post_neuron_id", how="left")
    res = res.join(out_synapses, left_on="neuron_id", right_on="pre_neuron_id", how="left")
    res = res.join(in_synapses, left_on="neuron_id", right_on="post_neuron_id", how="left")
    
    res = res.fill_null(0)
    
    res = res.with_columns(
        (pl.col("structural_in_degree") + pl.col("structural_out_degree")).alias("structural_total_degree"),
        (pl.col("incoming_synapse_count") + pl.col("outgoing_synapse_count")).alias("total_synapse_count")
    )
    return res

def compute_distribution_stats(series: pl.Series) -> dict:
    if len(series) == 0: return {}
    return {
        "min": float(series.min()), "max": float(series.max()),
        "mean": float(series.mean()), "median": float(series.median()),
        "std": float(series.std()) if len(series) > 1 else 0.0,
        "p01": float(series.quantile(0.01)), "p05": float(series.quantile(0.05)),
        "p25": float(series.quantile(0.25)), "p50": float(series.quantile(0.50)),
        "p75": float(series.quantile(0.75)), "p95": float(series.quantile(0.95)),
        "p99": float(series.quantile(0.99)), "p99.9": float(series.quantile(0.999)),
    }

def get_top_50(df: pl.DataFrame, col: str) -> list[str]:
    return df.sort(col, descending=True).head(50)["neuron_id"].to_list()

def plot_histogram(series: pl.Series, title: str, xlabel: str, output_path: Path):
    plt.figure(figsize=(10, 6))
    plt.hist(series.to_numpy(), bins=50, color='skyblue', edgecolor='black')
    plt.title(title); plt.xlabel(xlabel); plt.ylabel("Count")
    plt.yscale("log"); plt.tight_layout(); plt.savefig(output_path); plt.close()

def plot_loglog(series: pl.Series, title: str, xlabel: str, output_path: Path):
    plt.figure(figsize=(10, 6))
    vals, counts = np.unique(series.to_numpy(), return_counts=True)
    mask = vals > 0
    if len(vals[mask]) > 0:
        plt.scatter(vals[mask], counts[mask], alpha=0.5, color='darkblue')
        plt.xscale('log'); plt.yscale('log')
    plt.title(title); plt.xlabel(xlabel); plt.ylabel("Frequency")
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.tight_layout(); plt.savefig(output_path); plt.close()

def run_analysis(output_dir: Path):
    neurons, connections = load_canonical_data()
    degree_df = compute_degrees(neurons, connections)
    
    metrics_cols = ["structural_in_degree", "structural_out_degree", "structural_total_degree", "incoming_synapse_count", "outgoing_synapse_count", "total_synapse_count"]
    metrics = {"distribution_stats": {}, "high_degree_nodes": {}}
    
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    
    report_md = "# Degree and Synapse Distributions Report\n\n"
    report_md += "**Note on Terminology**: `incoming_synapse_count` and `outgoing_synapse_count` strictly denote the physical tally (sum) of `synapse_count`. There is absolutely NO implication that these values represent synaptic weight, conductance, current, efficacy, or physiological strength.\n\n"
    
    for col in metrics_cols:
        series = degree_df[col]
        stats = compute_distribution_stats(series)
        metrics["distribution_stats"][col] = stats
        top50 = get_top_50(degree_df, col)
        metrics["high_degree_nodes"][col] = top50
        
        hist_path = figures_dir / f"{col}_hist.png"
        loglog_path = figures_dir / f"{col}_loglog.png"
        plot_histogram(series, f"Histogram of {col}", col, hist_path)
        plot_loglog(series, f"Log-Log Distribution of {col}", col, loglog_path)
        
        report_md += f"## {col}\n\n### Statistics\n"
        for k, v in stats.items(): report_md += f"- **{k}**: {v:.4f}\n"
        report_md += f"\n### High Degree Nodes (Top 50)\n`{', '.join(top50)}`\n\n"
        report_md += f"### Plots\n![Histogram](figures/{hist_path.name})\n![Log-Log](figures/{loglog_path.name})\n\n"
        
    write_c2_report("degree", metrics, report_md, output_dir)

if __name__ == "__main__":
    run_analysis(Path("reports/c2"))
