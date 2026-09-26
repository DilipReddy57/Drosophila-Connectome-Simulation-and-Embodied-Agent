import polars as pl
import matplotlib.pyplot as plt
from pathlib import Path
from drosophila_connectome.c2.common import load_canonical_data, write_c2_report

def analyze_cell_types():
    neurons, _ = load_canonical_data(verify=True)

    annotation_cols = ["cell_type", "super_class", "class", "subclass", "hemilineage"]
    
    for col in annotation_cols:
        if col not in neurons.columns:
            neurons = neurons.with_columns(pl.lit(None).alias(col))

    is_annotated = neurons.select(
        pl.any_horizontal([
            pl.col(col).is_not_null() & 
            (pl.col(col) != "unknown") & 
            (pl.col(col) != "Unknown") & 
            (pl.col(col) != "") 
            for col in annotation_cols
        ])
    ).to_series()
    
    num_total = len(neurons)
    num_annotated = is_annotated.sum()
    num_unannotated = num_total - num_annotated

    metrics = {
        "total_neurons": num_total,
        "annotated_neurons": int(num_annotated),
        "unannotated_neurons": int(num_unannotated),
        "categories_distribution": {}
    }

    markdown_lines = [
        "# Cell-Type Analysis Report",
        "",
        f"- **Total Neurons:** {num_total}",
        f"- **Annotated:** {num_annotated}",
        f"- **Unannotated:** {num_unannotated}",
        ""
    ]

    fig_dir = Path("reports/c2/figures")
    fig_dir.mkdir(parents=True, exist_ok=True)

    for col in annotation_cols:
        dist = neurons.select(col).drop_nulls().group_by(col).len().sort("len", descending=True)
        dist_dict = {str(row[col]): int(row["len"]) for row in dist.to_dicts()}
        metrics["categories_distribution"][col] = dist_dict

        markdown_lines.append(f"## {col.capitalize()} Distribution")
        for k, v in list(dist_dict.items())[:10]:
            markdown_lines.append(f"- {k}: {v}")
        markdown_lines.append("")
        
        top_k = dist.head(20)
        
        plt.figure(figsize=(10, 6))
        x_vals = [str(x) for x in top_k[col].to_list()]
        y_vals = top_k["len"].to_list()
        
        plt.bar(x_vals, y_vals)
        plt.xticks(rotation=90)
        plt.title(f"Top 20 {col.capitalize()}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(fig_dir / f"{col}_distribution.png")
        plt.close()

    markdown_str = "\n".join(markdown_lines)
    write_c2_report("cell_types", metrics, markdown_str, Path("reports/c2"))

if __name__ == "__main__":
    analyze_cell_types()
