# Synapse Mapping Forensics

## 1. Where exactly is this equation defined?
The exact conversion equation:
`syn.w = df_con.loc[:,'Excitatory x Connectivity'].values * params['w_syn']`
is defined explicitly on line 125 of `model.py` in the official `philshiu/Drosophila_brain_model` repository. 

## 2. Is it explicitly published?
Yes. The parameter `w_syn = .275 * mV` is defined on line 32 of `model.py`.

## 3. Is it from Shiu et al.?
Yes, this codebase is the official repository for Shiu et al. (2024) Nature.

## 4. Is 0.275 mV actually the correct quantity and unit?
Yes. `mV` is the explicit unit. It acts as an instantaneous voltage jump $w$ applied to $I_{syn}$ which then decays exponentially at $\tau_{syn}$. 

## 5. Is it a voltage jump, conductance, normalized weight, or something else?
It is a voltage jump applied to the synaptic current variable $I_{syn}$ (which has units of volts in their model `dI_syn/dt = -I_syn / tau_syn : volt`). 

## 6. Does `N_syn` mean individual synapses or aggregated edge synapse count?
It means the aggregated edge synapse count. `Connectivity` in their dataframe refers to the physical synapse count on the directed edge between two neurons.

## 7. Was multiplication by synapse count explicitly used?
Yes. `Excitatory x Connectivity` is the sign of the neurotransmitter multiplied by the physical synapse count. 

## 8. Was the neurotransmitter sign mapping explicitly specified?
Yes, in Shiu et al. Supplementary Methods, acetylcholine (ACh) is defined as Excitatory (+1), while GABA, Glutamate, and Histamine are defined as Inhibitory (-1).

## 9. Is glutamate inhibitory in this exact model?
Yes. In the Drosophila connectome (FAFB), glutamate acts primarily through glutamate-gated chloride channels (GluCl) in the central brain, rendering it functionally inhibitory in standard global LIF models like this one.

## 10. Does the original implementation use the same convention?
Yes, identically.

## 11. Does the model include delays?
Yes, `t_dly = 1.8 * ms` (line 29, `model.py`).

## 12. Does the model use current-based or voltage-based synapses?
It uses current-based synapses conceptually, but physically models them as a voltage variable (`I_syn : volt`) that decays and is added directly to $V(t)$.

## 13. Is any transformation occurring between connectome data and simulation weights?
Only linear scalar multiplication (`N_syn * Sign * W_syn`). No log transforms or thresholds are applied to the physical counts.

**STATUS: RESOLVED AND VERIFIED.**
