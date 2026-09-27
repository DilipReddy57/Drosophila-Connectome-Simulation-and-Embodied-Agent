# Poisson Input Weight Forensics

## 1. Where 250 is defined
In the official Shiu et al. (2024) repository, `model.py` Line 41:
`'f_poi' : 250,  # scaling factor for Poisson synapse; 250 is sufficient to cause spiking`

In the `poi()` function (Line 90):
`weight=params['w_syn']*params['f_poi']`

## 2. Why it exists in the reference implementation
In Brian2, `PoissonInput` directly increases the target variable (in this case, membrane voltage `v`). The distance from resting potential ($V_{rest} = -52$ mV) to spike threshold ($V_{th} = -45$ mV) is 7 mV. 

The baseline synaptic weight $w_{syn}$ is 0.275 mV. A single Poisson event of 0.275 mV would only slightly depolarize the neuron. By multiplying it by 250, the injected voltage jump is:
$0.275 \text{ mV} \times 250 = 68.75 \text{ mV}$

A 68.75 mV instantaneous jump guarantees that the neuron's voltage exceeds the -45 mV threshold regardless of its current sub-threshold state. Furthermore, the script explicitly disables the refractory period for these neurons (`neu[i].rfc = 0 * ms`). 

**Conclusion:** This is an engineering mechanism to force the target neurons to act as perfect spike generators firing at exactly the `r_poi` frequency, without having to remove them from the main `NeuronGroup` integration block.

## 3. Is it a biological parameter?
**NO.** It does not represent a massive biological synapse with 250x multiplicity. It is purely a numerical forcing function.

## 4. What it represents
It represents an **engineering scaling factor** to guarantee deterministic threshold-crossing events.

## 5. Should it be applied to the C3 benchmark?
**YES.** To reproduce the published reference experiment faithfully, our inputs must perfectly mimic the Shiu implementation. Because our custom LIF engine does not natively support `SpikeGeneratorGroup` mixed into the dense state matrices, injecting a massive forcing voltage into $V$ is exactly how we must drive the stimulus to match their network state.

## 6. Does the paper document it?
No. The main text states: *"To simulate sensory input, we provided Poisson spike trains..."* It does not mention the 68.75 mV forcing amplitude.

## 7. Does only the reference repository document it?
Yes. The only evidence for this 250x multiplier exists in the `model.py` code comments. The independent auditor (Agent J) was correct to flag it as an undocumented assumption relative to the main publication text, but we now have provenance proving it is the official intended method.
