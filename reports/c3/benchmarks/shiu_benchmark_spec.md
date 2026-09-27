# Biological Benchmark Specification: Sugar-to-MN9 Activation

## Benchmark Identity
- **Paper:** Shiu et al. 2024 (Nature)
- **Figure / table / experiment:** Example Notebook (`example.ipynb`) - "sugarR_100Hz"
- **Scientific question:** Does activation of sugar-sensing neurons robustly propagate through the central brain to activate downstream motor neurons (MN9)?

## Experimental Setup
- **Stimulus:** Poisson spike injection directly increasing membrane voltage.
- **Input population:** 22 sugar-sensing neurons (`neu_sugar`).
- **Input distribution:** Poisson distribution.
- **Input rate:** 100 Hz.
- **Simulation duration:** 1000 ms (1 second).
- **dt:** 0.1 ms (model.py default).
- **Neuron parameters:** V_rest = -52 mV, V_reset = -52 mV, V_th = -45 mV, tau_m = 20 ms, t_ref = 2.2 ms.
- **Synaptic parameters:** tau_syn = 5 ms, delay = 1.8 ms, W_syn = 0.275 mV.
- **Initial conditions:** V = -52 mV, I_syn = 0.
- **Noise:** None (except Poisson input stochasticity).
- **Random seed:** 42 (Assumed for deterministic verification).
- **Neuron population analyzed:** MN9 (FlyWire ID: 720575940660219265).
- **Output variables:** Mean firing rate (Hz) of MN9 over 1000 ms.

## Published Expected Result
- **Expected result:** High activation rate. In the paper/notebook, sugar neuron activation propagates strongly to motor output. (Exact numerical value was cleared from the notebook, so we will compare against a direct run of the official Brian2 `philshiu` reference model on our v783 connectome).
- **Comparison metric:** MN9 firing rate (Hz) and total network spike count.
- **Acceptance threshold:** Our custom LIF implementation must match the Brian2 reference implementation firing rate within 5% tolerance under identical FAFB v783 conditions.

## Source Evidence
- **Input population:** REFERENCE_CODE (`example.ipynb` cells 1-3).
- **Input rate:** REFERENCE_CODE (`example.ipynb` cell 11).
- **Neuron/Synapse parameters:** PUBLISHED (`model.py` default_params).
- **Output measurement:** REFERENCE_CODE (`example.ipynb` cell 15).
