# Shiu et al. (2024) Drosophila Brain Model Specifications

## 1. Leaky Integrate-and-Fire (LIF) Equations

The model utilizes standard leaky integrate-and-fire (LIF) dynamics. The membrane potential $V(t) for a neuron evolves according to:

$$
\tau_m \frac{dV}{dt} = -(V - V_{rest}) + I_{syn}


where:
- $\tau_m$ is the membrane time constant.
- $V_{rest}$ is the resting membrane potential.
- $I_{syn}$ is the aggregate synaptic input (often expressed in terms of voltage units, i.e., $R \cdot I$, in Brian2 simulations).

When $V(t) reaches the spiking threshold $V_{th}$:
1. A spike is emitted.
2. The membrane potential is instantaneously reset to $V_{reset}$.
3. The neuron enters a refractory period of duration $t_{ref}$, during which $V(t)$ is clamped to $V_{reset}$.

## 2. Synapse Equations

The synaptic current $I_{syn}$ decays exponentially over time and increases upon the arrival of presynaptic spikes, incorporating a synaptic transmission delay $d$:

$$
\tau_{syn} \frac{d I_{syn}}{dt} = -I_{syn}


Upon the arrival of a spike from presynaptic neuron $j$ at time $t_{j,k}$, the synaptic variable is updated after the delay $d$:

$$
I_{syn}(t) \leftarrow I_{syn}(t) + w_{j} \quad \text{for} \quad t = t_{j,k} + d


where $w_{j}$ is the synaptic weight.

## 3. Synapse Counts to Weights Conversion

The physical synapse counts provided by the connectome are linearly converted into synaptic weights. The model converts the number of synaptic contacts $N_{syn}$ between neurons into a weight $w_j$ by scaling it by a global synaptic gain parameter ($W_{syn}$) and multiplying by a sign coefficient $S_j$ determined by the neurotransmitter:

$$
w_{j} = W_{syn} \times S_j \times N_{syn}


## 4. Neurotransmitter Handling Conventions

Synaptic polarities ($S_j$) are assigned based on the predicted principal neurotransmitter of the presynaptic neuron:
- **Excitatory ($+1$)**: Acetylcholine (ACh)
- **Inhibitory ($-1$)**: GABA, Glutamate, and Histamine

## 5. Model Parameters

| Parameter | Symbol | Value | Unit |
|---|---|---|---|
| Resting Potential | $V_{rest}$ | -52 | mV |
| Reset Potential | $V_{reset}$ | -52 | mV |
| Spiking Threshold | $V_{th}$ | -45 | mV |
| Refractory Period | $t_{ref}$ | 2.2 | ms |
| Synaptic Decay | $\tau_{syn}$ | 5 | ms |
| Membrane Time Const. | $\tau_{m}$ | 20 | ms |
| Synaptic Delay | $d$ | 1.8 | ms |
| Integration Timestep | $dt$ | 0.1 | ms |
