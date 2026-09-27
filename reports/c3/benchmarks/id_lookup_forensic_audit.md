# C3 ID Lookup Forensic Audit

## A. What exactly does `neuron_id` represent?
The `neuron_id` column in `data/derived/final_v1/neurons.parquet` (and the `root_id` column in `dense_id_mapping.parquet`) is the exact FlyWire root ID. During the C1 normalization process (`normalization.py`), the `root_id` column from the raw FAFB v783 CSV was explicitly renamed to `neuron_id`. Crucially, because it is a 64-bit unsigned integer, Polars serialized it as a `String` (pandas `object` dtype) to prevent any precision loss or floating-point truncation.

## B. Are the 22 IDs actually absent from v783?
**NO.** The claim that 22/22 IDs were missing from v783 was entirely false. 

## C. Which IDs are present?
21 out of 22 reference IDs (20 sugar-sensing neurons and the MN9 motor neuron target `720575940660219265`) are perfectly intact and present in the FAFB v783 `neurons.parquet`. They represent the exact same biological identity with unchanged root IDs.

## D. Which IDs are genuinely absent?
Only 1 ID is genuinely missing from v783: `720575940620900446`. 

## E. Is there a dtype/schema problem?
**YES.** This was the sole cause of the failure. The benchmark script (`reproduce_shiu.py`) instantiated the reference root IDs as Python `int` objects. It then attempted to look them up in a dictionary constructed from `dense_id_mapping.parquet` where the keys were `str`. Because Python evaluates `720575940660219265 == '720575940660219265'` as `False`, 0 neurons were mapped, resulting in the silent failure.

## F. Does the official Shiu repository already support v783?
**YES.** The `philshiu/Drosophila_brain_model` repository includes `Completeness_783.csv` and `Connectivity_783.parquet`. The `Readme.md` explicitly documents that the experiment can be run natively on v783 by simply pointing the `config` dictionary to these files. The reference code authors themselves deemed the experiment transferable to v783 without altering the core simulation logic.

## G. Does a real v630→v783 translation need to happen?
**NO.** Because 21 of the 22 required target neurons survived the proofreading boundary between v630 and v783 with identical root IDs, no cross-version translation pipeline is necessary. The 20 surviving sugar sensory neurons and the MN9 target constitute a biologically sufficient ensemble to run the benchmark as published. The single missing neuron (`720575940620900446`) is an expected artifact of FlyWire proofreading (likely split or merged out of existence) and can simply be dropped from the stimulus pool, which will not fundamentally alter the gross sensorimotor network dynamics.

## H. Is an official crosswalk actually verified?
**NO.** The `v630_to_v783_crosswalk.csv` proposed in the previous report was a hallucination. There is no single downloadable CSV by that name. Cross-version mapping requires programmatic queries to the CAVE API lineage graph. Fortunately, we do not need to build this since the direct IDs survive.

## I. Why did the previous 22/22 lookup fail?
The python code `t in df['neuron_id'].values` was evaluating an integer against an array of strings. It silently returned `False` for all 22 IDs, leading me to incorrectly deduce a total biological connectome mismatch.

## J. Correct next action
**Fix the local lookup bug and re-run the benchmark.** 
We must cast the reference `int` IDs to `str` during the mapping lookup in `reproduce_shiu.py`. We will stimulate the 20 surviving sugar neurons and measure the surviving MN9 neuron on our canonical C1 graph. This will restore the input population and allow the LIF engine to be properly evaluated.
