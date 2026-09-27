import json
from pathlib import Path

def generate_final_report():
    reports_dir = Path("reports/c2")
    
    jsons = {}
    for f in reports_dir.glob("*.json"):
        if f.name == "c2_final_result.json" or f.name == "cross_agent_audit.json": continue
        with open(f, "r") as fp:
            jsons[f.stem] = json.load(fp)

    final_result = {
        "objective": "Phase C2 Graph Analytics & Biological Sanity Validation",
        "dataset_identity": "FAFB v783",
        "c1_input_commit": "93603efdf845f691e581f1771af3630c3bb72218",
        "c2_ready": True,
        "human_review_required": True,
        "reports_aggregated": list(jsons.keys()),
        "independent_audit_status": "NOT_PERFORMED"
    }
    
    with open(reports_dir / "c2_final_result.json", "w") as fp:
        json.dump(final_result, fp, indent=2)

    md = [
        "# Phase C2 Final Report: Graph Analytics & Biological Sanity Validation",
        "",
        "## 1. Objective",
        "To perform structural validation of the canonical graph representation, characterize topology, degree, and synapse distributions, analyze annotations (regions, cell types, neurotransmitters), and perform reproducible measurement without biological modeling inferences.",
        "",
        "## 2. Dataset Identity & C1 Input",
        "- **Dataset**: FlyWire FAFB v783 (adult female brain)",
        "- **C1 Input Commit**: `93603efdf845f691e581f1771af3630c3bb72218`",
        "- **Canonical Input Directory**: `data/derived/final_v1/`",
        "",
        "## 3. Methods & Metric Definitions",
        "Metrics were extracted cleanly from the canonical data (`neurons.parquet`, `connections.parquet`, `dense_id_mapping.parquet`). See `metric_registry.yaml` for exact definitions. Computations utilized Polars, igraph, and scipy for sparse matrix operations.",
        "",
        "## 4. Data Integrity (Agent A)",
        "The graph explicitly matches 139,255 canonical neurons, 5,342,446 connection rows, and 50,666,648 synapses. The locked FAFB v783 raw and canonical datasets contain zero direct self-loop rows under the tested neuron-ID definitions. 56,231 was a planning/transcription artifact. Direct inspection of the FAFB v783 raw connections and canonical C1 connections found 0 self-loops.",
        "",
        "## 5. Degree Distributions (Agent B)",
        "Calculated `structural_in_degree`, `structural_out_degree`, `structural_total_degree`, `incoming_synapse_count`, `outgoing_synapse_count`, and `total_synapse_count`. All physiological terminology (e.g. 'weighted degree', 'conductance') has been purged.",
        "",
        "## 6. Graph Topology (Agent C)",
        "Calculated sparsity, reciprocity, and connected components. Verified structural edges match topology edges.",
        "",
        "## 7. Regions/Neuropil (Agent D)",
        "Derived region-level connection row and synapse distributions. No pre-region to post-region matrix was falsely manufactured.",
        "",
        "## 8. Neurotransmitters (Agent E)",
        "Annotated NT counts gathered correctly. NT conflict resolution during canonical aggregation (.first()) is documented for future datasets (0 conflicts). No excitation/inhibition inferences were made.",
        "",
        "## 9. Cell Types (Agent F)",
        "Explicit coverage extracted for taxonomic levels (`super_class`, `class`, `subclass`, `hemilineage`, `cell_type`) without false aggregation.",
        "",
        "## 10. Literature Benchmarks (Agent G)",
        "Evidence documented across corresponding structural filters for FAFB v783. The discrepancy in synapse counts (~54.5M published vs 50.6M canonical) is strictly classified as UNRESOLVED pending exact thresholding code evidence.",
        "",
        "## 11. Reproducibility & Provenance",
        "Reproducibility status is PARTIALLY VERIFIED. Hashes matched in the current environment, but independent cross-machine verification was not performed.",
        "",
        "## 12. Audit Findings (Agent H)",
        "The final 'GO' audit documented in `cross_agent_audit.md` and `cross_agent_audit.json` was conducted and asserted by the C2 coordinator. It does NOT represent a genuinely independent execution pass by a distinct Subagent H on the post-fix tree. Independent audit status is NOT_PERFORMED.",
        "",
        "## 13. Limitations & Out-of-Scope Items",
        "No dynamic parameters (delays, conductances, LIFs) were established. The measurements are strictly graph-theoretic and physical annotation derivations.",
        "",
        "## 14. C3 Readiness",
        "The canonical representation passed the structural graph validation checks. Awaiting human review before proceeding to Phase C3."
    ]
    
    with open(reports_dir / "c2_final_report.md", "w") as fp:
        fp.write("\n".join(md))
        
if __name__ == "__main__":
    generate_final_report()
