# Neurotransmitter Analysis (Agent E)

This report analyzes the `source_nt_type` annotations across the connectome.

## Metrics per NT Type

### OCT
- connection_count: 28985
- total_synapses: 154441
- synapse_fraction: 0.003048178754592173
- unique_pre_neurons: 106
- unique_post_neurons: 9231
- mean_synapse_count: 5.328307745385544
- median_synapse_count: 3.0

### DA
- connection_count: 63704
- total_synapses: 378682
- synapse_fraction: 0.007473989595680378
- unique_pre_neurons: 786
- unique_post_neurons: 14459
- mean_synapse_count: 5.944399095818159
- median_synapse_count: 3.0

### ACH
- connection_count: 3210049
- total_synapses: 30101369
- synapse_fraction: 0.5941061859864896
- unique_pre_neurons: 94160
- unique_post_neurons: 124421
- mean_synapse_count: 9.377230378726306
- median_synapse_count: 6.0

### GABA
- connection_count: 1172932
- total_synapses: 11902450
- synapse_fraction: 0.23491686286410737
- unique_pre_neurons: 18374
- unique_post_neurons: 116507
- mean_synapse_count: 10.147604464708952
- median_synapse_count: 6.0

### SER
- connection_count: 40396
- total_synapses: 502056
- synapse_fraction: 0.009909003650685555
- unique_pre_neurons: 1435
- unique_post_neurons: 8497
- mean_synapse_count: 12.428359243489455
- median_synapse_count: 6.0

### GLUT
- connection_count: 826380
- total_synapses: 7627650
- synapse_fraction: 0.15054577914844497
- unique_pre_neurons: 22657
- unique_post_neurons: 93431
- mean_synapse_count: 9.230196761780295
- median_synapse_count: 6.0

## Important Limitations & Methodology
- **Data Aggregation**: The `source_nt_type` is propagated using `.first()` during canonical aggregation. For FAFB v783, this is safe as there are zero duplicate groups, but for future datasets with conflicts, this may introduce loss of resolution.
- **No Inference**: These types are treated strictly as annotations. We explicitly do NOT infer or claim excitation/inhibition mappings from NT types (e.g., we do not claim ACh = excitatory).