# Independent Model Audit: Shiu et al. 2024

## Overview
We independently audited the official codebase for "A Drosophila computational brain model reveals sensorimotor processing" (Shiu et al. 2024), available at `philshiu/Drosophila_brain_model`.

## Findings

### Simulation Backend
The model was implemented using the **Brian2** spiking neural network simulator.

### Hardcoded LIF Parameters
The codebase specifies the following exact default parameters:
- `v_0` (resting potential): `-52 mV`
- `v_rst` (reset potential after spike): `-52 mV`
- `v_th` (threshold for spiking): `-45 mV`
- `t_mbr` (membrane time scale): `20 ms`
- `tau` (time constant for synaptic decay): `5 ms`
- `t_rfc` (refractory period): `2.2 ms`
- `t_dly` (synaptic delay): `1.8 ms`
- `w_syn` (weight per synapse): `0.275 mV`

### Neurotransmitter Signs
Neurotransmitter signs are pre-computed in the connectivity dataframe (`Connectivity_630.parquet` / `Connectivity_783.parquet`) under an `Excitatory` column which maps the neurotransmitter identity to either `1` (excitatory) or `-1` (inhibitory).

### Synaptic Weights
Synapse counts are used directly as a basis for weights without any non-linear transformation. The actual synaptic weight in the model (`syn.w`) is calculated as:
`Synapse Count × Neurotransmitter Sign (1 or -1) × w_syn (0.275 mV)`

### Dataset Version
The paper was based on the **FAFB v630** dataset (default in the codebase), but the code also explicitly provides the ability to run on **FAFB v783** through alternative dataset files (`Completeness_783.csv` and `Connectivity_783.parquet`).
