# Audit of the 250× Input Forcing Mechanism

## 1. Constants in the Reference Code
By direct inspection of the reference `model.py` and simulation setup:
- $w_{syn} = 0.275$ mV (Baseline synaptic weight scalar)
- $f_{poi} = 250$ (Numerical forcing multiplier)
- $V_{rest} = -52$ mV
- $V_{th} = -45$ mV

## 2. Theoretical Effective Jump
The mathematical jump injected into the membrane potential equation upon a Poisson spike is:
$$ \Delta V = w_{syn} \times f_{poi} = 0.275 \times 250 = 68.75 \text{ mV} $$

Given that the threshold distance from rest is $7$ mV ($-45 - (-52)$), an instantaneous jump of $68.75$ mV will deterministically force the target neuron over threshold immediately, rendering it a perfect spike generator at the Poisson rate.

## 3. Empirical Equivalence Validation
We executed a 1-neuron test side-by-side using the official Brian2 backend (with `v += w`) and our Custom LIF backend (with `V += 68.75`).

**Custom Implementation:**
- Voltage at $t=1.0$ ms (Step 10): -52.0 mV
- Injection at $t=1.0$ ms: $+68.75$ mV
- Voltage jumps to $+16.75$ mV.
- Spike registered at step 10.
- Voltage resets to -52.0 mV.

**Brian2 Implementation:**
- Voltage at $t=1.0$ ms: -52.0 mV
- SpikeGeneratorGroup forces $V$ by $+68.75$ mV.
- Voltage jumps to $+16.75$ mV.
- Spike threshold crossed.
- Spike registered at $t=1.1$ ms (Brian2 evaluates spikes at the end of the step interval).
- Voltage resets to -52.0 mV.

**Conclusion:** The two implementations produce identical forcing behavior. We are correctly applying the 250x non-biological scaling factor used by the authors to guarantee deterministic firing in the input population.
