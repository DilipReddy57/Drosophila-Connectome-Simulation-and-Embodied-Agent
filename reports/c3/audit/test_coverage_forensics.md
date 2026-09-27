# Test Coverage Forensics

| Test | Classification | Scientifically Validating? | Weaknesses / Hardcoded values |
|---|---|---|---|
| `test_e1_analytical_lif_comparison` | Unit / Math Property | Yes (Math only) | Only tests our specific equation solver, does not test the biology. |
| `test_e2_threshold_check` | Unit Test | No | Only tests `> V_th` python logic. |
| `test_e3_reset_check` | Unit Test | No | Only tests `= V_reset` python logic. |
| `test_e4_refractory_period_check` | Unit Test | No | Only tests clamp logic. |
| `test_e7_timestep_sensitivity` | Unit / Math Property | Yes (Numerical) | Confirms zero error across dt, but only for the uncoupled ODE approximation. |
| `test_e5_synaptic_response` | Unit Test | No | Tests delay queue mechanism, not biological magnitude. |
| `test_e6_excitatory_inhibitory_sign` | Unit Test | No | Tests that + makes V go up and - makes V go down. |
| `test_endpoint_validity` | Integration | Yes (Data) | Tests adapter against dataset. |
| `test_synapse_counts` | Integration | Yes (Data) | Tests adapter against dataset. |
| `test_nt_preservation` | Integration | Yes (Data) | Tests adapter against dataset. |
| `test_no_self_loops` | Integration | Yes (Data) | Tests adapter against dataset. |
| `test_deterministic` | Property | Yes (Code) | Tests sorting logic. |
| `test_reference_parity` | Reference Reproduction | Yes (Math) | Only tests 2 synthetic neurons. Never invokes real connectome. |

## Weaknesses Identified
1. **Missing full-brain reproduction:** No test actually instantiates the 139,255 neuron graph and runs a published biological stimulus (e.g. activating the visual system as Shiu et al. did) and compares the output statistics against the paper.
2. **Missing weight conversion tests:** There are no tests verifying `builder.py` correctly translates NT strings to `+1` / `-1` matrices. 
3. **Tests pass when science fails:** The unit tests (E1-E7) passed when the biological translation layer (synapse to weight) was completely missing from the engine. Unit tests guarantee Python logic, not scientific validity.

**STATUS: INADEQUATE SCIENTIFIC COVERAGE.**
