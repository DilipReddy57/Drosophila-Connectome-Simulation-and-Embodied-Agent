# Incomplete Tasks Audit

| TASK | Expected by C3? | Implemented? | Tested? | Scientifically validated? | Evidence? | Remaining work? | Blocking C3 closure? |
|---|---|---|---|---|---|---|---|
| LIF Equation Engine | YES | YES | YES | PARTIAL | `lif/` | Fix exact vs modified Euler approximation if required. | NO |
| Parameters Traced | YES | YES | YES | YES | `parameter_evidence.csv` | None. | NO |
| Adapter to Connectome | YES | YES | YES | YES | `sparse_graph.py` | None. | NO |
| Brian2 Math Parity | YES | YES | YES | YES | `brian2_parity_reaudit.csv` | None. | NO |
| Weight Conversion | YES | YES | NO | YES | `builder.py` | Add unit tests for `builder.py`. | YES |
| **Published Biological Benchmark** | **YES** | **NO** | **NO** | **NO** | None | Must run an actual biological simulation from the paper (e.g. activating specific sensory neurons and measuring network activity) and compare results quantitatively against the published figures. | **YES (BLOCKING)** |

## Conclusion
C3 is blocked from closure because the implementation has only been mathematically verified on synthetic 2-neuron networks, not scientifically validated on the biological connectome against a published outcome.
