# Numerical Claims Forensics

## Disputed Claim
*"The custom implementation is mathematically perfect."*

## The Underlying Mathematics
- **ODE Being Solved:**
  $$ \tau_m \frac{dV}{dt} = -(V - V_{rest}) + I_{syn} $$
  $$ \tau_{syn} \frac{d I_{syn}}{dt} = -I_{syn} $$
- **Analytical Solution (Coupled):** The true exact solution involves integrating the coupled linear system continuously. Because $I_{syn}$ decays exponentially over $dt$, the exact integral of $I_{syn}$ must be injected into the $V(t)$ integral.
- **Implemented Numerical Update:**
  `delta_V = (V - V_rest) * exp(-dt/tau_m)`
  `I_contribution = I_syn * (1 - exp(-dt/tau_m))`
  `V_next = V_rest + delta_V + I_contribution`
- **Assumptions:** The implementation inherently treats $I_{syn}$ as a *piece-wise constant* across the duration of $dt$, applying the exact exponential decay to $V$ relative to that constant, and then separately decaying $I_{syn}$ via `I_syn *= exp(-dt/tau_syn)`. 
- **Numerical Error Source:** Treating a continuously decaying $I_{syn}$ as a discrete constant over $dt$ introduces a small integration error.
- **Floating-point Behavior:** The calculation is purely float64 numpy arithmetic. 
- **Threshold / Refractory Handling:** Hard-clamped discretely at the step boundaries.

## Conclusion
The previous claim that the implementation is "mathematically perfect" is **scientifically unsupported**.

The implementation is an **exact analytical solution to the uncoupled single-variable ODE**, but it is a **Modified Exponential Euler approximation of the complete coupled network dynamics**. This approximation precisely accounts for the ~0.05 mV deviation when compared to Brian2's `exact` state updater, which computes the fully coupled exact linear matrix exponential. 

The claim must be downgraded from "mathematically perfect" to "a highly accurate Exponential Euler approximation."
