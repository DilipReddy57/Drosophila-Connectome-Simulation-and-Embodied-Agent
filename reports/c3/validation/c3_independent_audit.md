# Phase C3 Independent Audit: Reference LIF Implementation Parity

## Overview
This report details the comparison between our custom NumPy/SciPy Leaky Integrate-and-Fire (LIF) network (`drosophila_connectome.neural.lif`) and the standard `Brian2` exact integration backend.

A minimal network consisting of two neurons and one excitatory synapse was constructed in both environments:
- **Neuron 0** receives an external constant current of $20$ mV for $10$ ms.
- **Neuron 1** receives a synaptic connection from Neuron 0 with a weight of $10.0$ mV and a delay of $1.8$ ms.
- Network parameters: $V_{rest} = -52$ mV, $V_{reset} = -52$ mV, $V_{th} = -45$ mV, $\tau_m = 20$ ms, $\tau_{syn} = 5$ ms, $t_{ref} = 2.2$ ms, $dt = 0.1$ ms.

## Results
The simulations ran for $50$ ms. 

### Spike Times
- **Custom Simulation Spike Time:** 8.6 ms (step 86)
- **Brian2 Simulation Spike Time:** 8.6 ms
Spike times are **100% identical**.

### Synaptic Current ($I_{syn}$)
- **Max Difference:** $3.55 \times 10^{-15}$ mV.
- The synaptic current decays identically in both implementations (exponential decay step by step). The minute difference is purely attributable to floating-point round-off errors.

### Membrane Voltage ($V$)
- **Max Difference:** $0.0498$ mV
- While visually indistinguishable in the plotted traces, the underlying arrays deviate by approximately $0.05$ mV at the peak of the post-synaptic potential (PSP) in Neuron 1.

## Root Cause Analysis for Voltage Divergence
The discrepancy arises from the numerical integration schemes used for the coupled differential equations.

**Brian2 (Exact Integration)**
Brian2 evaluates linear ODEs analytically. The coupled system:
$$ \tau_m \frac{dV}{dt} = -(V - V_{rest}) + I_{syn} + I_{ext} $$
$$ \tau_{syn} \frac{dI_{syn}}{dt} = -I_{syn} $$
is solved exactly over the time step $\Delta t$, meaning $V(t+\Delta t)$ naturally accounts for the continuous decay of $I_{syn}$ during the step. 

**Custom Implementation (Modified Exponential Euler)**
Our codebase separates the decay updates. In `equations.py`, the membrane voltage uses the formula:
$$ V(t+\Delta t) = V_{rest} + (V(t) - V_{rest})e^{-\Delta t / \tau_m} + I_{syn}(t)(1 - e^{-\Delta t / \tau_m}) $$
This implicitly assumes $I_{syn}(t)$ remains constant over the integration window $\Delta t$, applying the decay to $I_{syn}$ separately. 

Because our step explicitly ignores the intra-step decay of the synaptic current, it slightly overestimates the membrane voltage contribution at each time step compared to the true continuous-time analytical solution.

## Conclusion
The custom implementation accurately matches spike times and tracks synaptic currents with exact parity. The $0.05$ mV deviation in membrane voltage is an expected artifact of the discrete piecewise-constant integration strategy for synaptic currents. For the purposes of the Drosophila connectome scale, this is well within acceptable tolerance, and the implementation is deemed structurally sound.

See `reports/c3/validation/parity_plot.png` for a visual comparison of the voltage and current traces.

