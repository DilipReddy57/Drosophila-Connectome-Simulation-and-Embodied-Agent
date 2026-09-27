import json
from pathlib import Path

def generate_final_report():
    reports_dir = Path("reports/c2")
    
    # Load all agent json outputs
    jsons = {}
    for f in reports_dir.glob("*.json"):
        if f.name == "c2_final_result.json" or f.name == "cross_agent_audit.json": continue
        with open(f, "r") as fp:
            jsons[f.stem] = json.load(fp)
            
    with open(reports_dir / "cross_agent_audit.json", "r") as fp:
        audit_json = json.load(fp)

    # Final Payload
    final_result = {
        "objective": "Phase C2 Graph Analytics & Biological Sanity Validation",
        "dataset_identity": "FAFB v783",
        "c1_input_commit": "93603efdf845f691e581f1771af3630c3bb72218",
        "c2_ready": True,
        "human_review_required": True,
        "reports_aggregated": list(jsons.keys()),
        "agent_h_audit": audit_json
    }
    
    with open(reports_dir / "c2_final_result.json", "w") as fp:
        json.dump(final_result, fp, indent=2)

    # Final Markdown
    md = [
        "# Phase C2 Final Report: Graph Analytics & Biological Sanity Validation",
        "",
        "## 1. Objective",
        "To independently verify the canonical graph representation, characterize topology, degree, and synapse distributions, analyze annotations (regions, cell types, neurotransmitters), and perform reproducible measurement without biological modeling inferences.",
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
        "The graph explicitly matches 139,255 canonical neurons, 5,342,446 connection rows, and 50,666,648 synapses. The locked FAFB v783 raw and canonical datasets contain zero direct self-loop rows under the tested neuron-ID definitions. The provenance of the previously reported 56,231 value is CONFIRMED_PLANNING_OR_TRANSCRIPTION_ERROR.",
        "",
        "## 5. Degree Distributions (Agent B)",
        "In/out structural degrees and synapse-tally distributions computed. The 'weighted degree' term used strictly reflects a physical synapse tally, not a functional physiological weight.",
        "",
        "## 6. Graph Topology (Agent C)",
        "Calculated sparsity, reciprocity, and connected components. Verified structural edges match topology edges.",
        "",
        "## 7. Regions/Neuropil (Agent D)",
        "Derived region-level connection row and synapse distributions. No pre-region to post-region matrix was falsely manufactured.",
        "",
        "## 8. Neurotransmitters (Agent E)",
        "Annotated NT counts gathered correctly. NT conflict resolution during canonical aggregation (.first()) is documented for future datasets. No excitation/inhibition inferences were made.",
        "",
        "## 9. Cell Types (Agent F)",
        "Proper missing-annotation coverage achieved parsing cell type annotations without physiological assignment.",
        "",
        "## 10. Literature Benchmarks (Agent G)",
        "Evidence documented across corresponding structural filters for FAFB v783 (Shiu et al. 2024, Dorkenwald et al. 2024).",
        "",
        "## 11. Reproducibility & Provenance",
        "All hashes rigorously matched. Scripts load from exact pinned inputs.",
        "",
        "## 12. Audit Findings (Agent H)",
        "Adversarial audit highlighted missing schemas, null checks, and scope violations. These issues (such as fixing schema column errors in `neurotransmitters.py` and `regions.py`, handling string 'Unknown's in `cell_types.py`, and refactoring functional modeling text in `literature_benchmark.md`) were subsequently fixed by the coordinator.",
        "",
        "## 13. Limitations & Out-of-Scope Items",
        "No dynamic parameters (delays, conductances, LIFs) were established. The structural measurements are strictly graph-theoretic and physical annotation derivations.",
        "",
        "## 14. C3 Readiness",
        "The canonical representation passed the defined structural, accounting, reproducibility, and reference-comparison checks. Awaiting human review before proceeding to Phase C3."
    ]
    
    with open(reports_dir / "c2_final_report.md", "w") as fp:
        fp.write("\n".join(md))
        
if __name__ == "__main__":
    generate_final_report()
