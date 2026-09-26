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
