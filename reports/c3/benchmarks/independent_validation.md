# Independent Validation Report: Shiu et al. (2024) Reproduction

**Benchmark:** Sugar-to-MN9 Activation (sugarR_100Hz)
**Status:** **NO_GO**

## 1. Did we successfully reproduce the published experiment biologically?
**No.** The simulation yielded 0 total spikes and a 0 Hz firing rate for MN9 in both the custom LIF model and the Brian2 reference. This completely contradicts the published expectation of a "high activation rate".

## 2. Are the parameters faithful to the source evidence?
**No.** While the basic parameters (dt = 0.1 ms, V_rest = -52 mV, V_th = -45 mV, tau_m = 20 ms, t_ref = 2.2 ms, tau_syn = 5 ms) are faithful to the benchmark spec, the stimulus injection incorporates an unfaithful and arbitrary 250x weight multiplier:
- In `reproduce_shiu.py`, `jump_v = 0.275 * 250.0`
- In the Brian2 reference, `PoissonInput(..., weight=0.275*250*mV)`
The specification defines `W_syn = 0.275 mV`. The hidden 250 multiplier is not justified by the spec.

## 3. Are the inputs faithful?
**No.** The mapping logic fails completely. 
- The script attempts to map 21 specific root IDs for sugar neurons, but the output log states `Sugar neurons mapped: 0`.
- The target output neuron (MN9) ID `720575940660219265` maps to `None`. 
Consequently, zero stimulus was injected into the network because zero neurons were selected.

## 4. Are the outputs comparable?
**No.** Since no inputs were provided and the MN9 output neuron could not be identified, both the custom model and reference produced 0 spikes. While they are technically identical (0 Hz vs 0 Hz), this is due to identical complete failures of the experimental setup rather than true biological replication. 

## 5. Are the comparison metrics valid?
**Partially.** The chosen metrics (MN9 firing rate and total network spike count) align with the benchmark specification. However, their implementation is broken because `mn9_dense` evaluates to `None`, making it impossible to correctly count spikes for that specific neuron.

## 6. Are there hidden assumptions?
**Yes.** 
1. The script assumes the hardcoded `root_id`s for sugar neurons and MN9 exactly match the IDs present in `data/derived/final_v1/dense_id_mapping.parquet`. Either the dataset was pruned, or a different FAFB version (e.g., older/newer than v783) was used for generating the IDs.
2. The stimulus assumes an arbitrary 250x strength multiplier to force activation (`weight=0.275*250*mV`).

## 7. Is the result reproducible?
**No.** The `reproduce_shiu.py` script literally crashes before writing the final output. The command exits with `TypeError: Object of type int32 is not JSON serializable` on line 196 because `c_total` or `b_total` are returned as `int32` (or similar numpy types) and standard `json.dump` cannot serialize them. The expected result file (`shiu_sugar100_results.json`) is never actually generated.

## Conclusion
**NO_GO**. The experiment code fails to resolve input/output IDs, fails to generate a stimulus, includes hidden parameter modifications (250x multiplier), and crashes upon serialization. It must be entirely refactored and the connectome IDs verified.
