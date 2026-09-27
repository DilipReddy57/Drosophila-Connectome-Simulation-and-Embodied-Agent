# Validation Targets for C3 LIF Model

Based on the Shiu et al. (2024) Drosophila brain model, the following validation targets are expected to ensure physiological realism and correct implementation:

## 1. Single Neuron Dynamics
*   **Resting State:** In the absence of synaptic input, neurons should stably rest at -52 mV.
*   **Thresholding and Spiking:** When injected with sufficient depolarizing current, neurons should fire an action potential exactly when $V(t)$ crosses -45 mV.
*   **Refractory Period:** After a spike, the membrane potential must remain clamped at the reset potential (-52 mV) for exactly 2.2 ms before integrating further inputs.
*   **Membrane Time Constant:** The decay of $V(t)$ back to rest (subthreshold) should follow an exponential curve with $\tau_m = 20$ ms.

## 2. Synaptic Dynamics
*   **Synaptic Delay:** Spikes from a presynaptic neuron must not affect the postsynaptic neuron until exactly 1.8 ms later.
*   **Synaptic Decay:** The postsynaptic current or conductance should decay exponentially with a time constant of $\tau_{syn} = 5$ ms.
*   **Sign Implementation:** Acetylcholinergic neurons must strictly exert depolarizing (excitatory) effects. GABAergic, glutamatergic, and histaminergic neurons must strictly exert hyperpolarizing (inhibitory) effects.

## 3. Network Level
*   **Sensorimotor Propagation:** Activity stimulated in sensory pathways (e.g., sugar receptors) must propagate correctly through the network to motor neurons (e.g., proboscis extension), matching the macroscopic behavior reported in Shiu et al. (2024).
