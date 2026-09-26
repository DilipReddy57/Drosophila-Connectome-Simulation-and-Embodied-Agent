# Project requirements and implementation gate

## Version 0 decision record

| Field | Status / initial decision |
| --- | --- |
| Project name | Drosophila Connectome Simulation and Embodied Agent |
| Primary dataset | **Proposed:** FlyWire FAFB v783 |
| Dataset version | **Proposed:** v783; must be locked in manifest before ingestion |
| Sex | Female |
| Coverage | Brain |
| Scope | Whole-brain reconstruction, circuit-first execution |
| Scientific fidelity | Medium initially: connectome + transmitter-informed LIF |
| Simulation objective | Reproduce a published sensorimotor whole-brain LIF benchmark |
| Primary behavior | Feeding/taste or grooming benchmark from the selected reference model |
| Learning mode | Frozen connectome for the first reproduction |
| Training allowed | No, until the frozen baseline passes validation |
| Runtime candidate | Brian2 first; alternate backends only through parity benchmarks |
| Initial timestep | Unresolved; record and justify in the model configuration |
| Embodiment target | Deferred; select BANC or MaleCNS only after brain-only validation |
| Real-time requirement | Offline scientific reproduction |
| Application target | Python research API |
| Validation target | Reproduction of the selected published LIF experiment |

## Required decisions before implementation gate C0

The following fields must be changed from **Proposed** or **Unresolved** to a documented decision with evidence IDs:

```text
[PRIMARY_DATASET]
[CONNECTOME_VERSION]
[FIRST_BEHAVIOR]
[HARDWARE_CONSTRAINTS]
[SCIENTIFIC_FIDELITY]
[VALIDATION_TARGET]
[SIMULATION_DT]
```

Record each decision in `decisions/` using `templates/decisions/decision.md` and reference it from the source registry.

## Non-negotiable rules

1. Raw connectome files are immutable and never receive application labels.
2. Every derived artifact records its inputs, transformation, software version, and SHA-256 digest.
3. Female, male, brain-only, and CNS releases are distinct datasets unless an explicit integration procedure says otherwise.
4. Synapse count is not physiological conductance; any conversion is a versioned model assumption.
5. Predicted neurotransmitter identity remains inferred data, with confidence and source retained.
6. Engineered sensor, motor, reward, and game mappings are never presented as biological facts.
7. Every experiment records its random seed, control condition, hardware, and software environment.
# Project Requirements

## Initial Configuration Template

This template is the authoritative starting point for the first implementation
milestone. Values marked **Unresolved** are intentional placeholders and must
be decided through the implementation gate below before work that depends on
them begins.

| Field | Initial configuration | Status |
| --- | --- | --- |
| **Dataset and version** | **Unresolved** — select the source connectome dataset, release/version, licensing terms, and any preprocessing snapshot. | Blocking |
| **Biological scope** | **Unresolved** — define the modeled organism stage, sex, brain regions/cell types, and the intended level of completeness. | Blocking for scientific-fidelity decisions |
| **Simulation objective** | Build an embodied, connectome-informed simulation that can execute and evaluate a defined behavior. | Provisional |
| **Primary behavior** | **Unresolved** — choose one observable first behavior, its stimulus/starting conditions, action space, and success metric. | Blocking |
| **Learning mode** | **Unresolved** — specify whether the initial system is fixed-connectome inference, supervised learning, reinforcement learning, plasticity-driven learning, or a hybrid; document which parameters may change. | Required before learning implementation |
| **Hardware** | **Unresolved** — specify target compute platform, accelerator availability, memory limits, storage budget, operating-system/runtime constraints, and deployment location. | Blocking |
| **Real-time target** | **Unresolved** — specify simulation-time-to-wall-clock ratio, control/update rate, latency budget, and acceptable benchmark hardware. | Required before performance implementation |
| **Neuron model** | **Unresolved** — specify the neuron dynamics model, numerical integration method, timestep, parameter sources, and treatment of cell-type variation. | Required before neural simulation implementation |
| **Synapse model** | **Unresolved** — specify synaptic dynamics, sign/weight initialization, plasticity rules if any, and parameter sources. | Required before neural simulation implementation |
| **Delay model** | **Unresolved** — specify whether connection delays are absent, fixed, distance-derived, or data-derived; include units and discretization. | Required before neural simulation implementation |
| **Environment engine** | **Unresolved** — select the embodied-environment engine and define its physics/sensory interfaces, action interface, determinism controls, and version. | Required before embodiment implementation |
| **Validation target** | **Unresolved** — define the biological and/or behavioral reference data, acceptance metrics, baselines, statistical criteria, and reproducibility protocol. | Blocking for claims of success |

## Implementation Gate

The project **must not begin implementation beyond planning and requirements
work** until all of the following are documented, reviewable, and mutually
consistent:

1. **Dataset:** a named dataset with a pinned version/release, provenance,
   license, and preprocessing plan.
2. **First behavior:** one primary behavior with a testable task definition,
   inputs, outputs, and measurable success criterion.
3. **Hardware constraints:** the target execution hardware and explicit compute,
   memory, storage, and runtime limits.
4. **Scientific fidelity:** an approved biological scope plus neuron, synapse,
   and delay modeling assumptions, each tied to an evidence source or clearly
   labeled simplification; the validation target must test the resulting
   fidelity claim.

Resolving the gate requires recording the selected values in this document and
confirming that the dataset, behavioral task, hardware budget, model choices,
and validation target do not conflict. Any later change to a gate item requires
re-review of affected requirements before implementation resumes.
