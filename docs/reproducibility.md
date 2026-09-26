# Reproducibility, evidence, and experiment policy

## Evidence classes

| Class | Use |
| --- | --- |
| A0 | Primary scientific evidence for biological claims |
| A1 | Official dataset/project documentation |
| A2 | Official implementation source code |
| B | Peer-reviewed method |
| C | Technical blog or research communication |
| D | Community implementation reference |
| E | Community discussion or hypothesis; never validation |

## Required experiment fields

Every run uses `templates/experiments/experiment.md` and includes the Git commit, dataset manifest and hash, model and parameter version, seed, environment, hardware, duration, control condition, metrics, artifacts, assumptions, and decision.

## Checkpoints

- **C0:** scope, dataset, hardware, behavior, and validation target are frozen.
- **C1:** raw files are versioned, hashed, licensed, and attributed.
- **C2:** canonical graph statistics reproduce the selected release under a declared filter.
- **C3:** published LIF reference experiment reproduces within declared tolerance.
- **C4:** equivalent runtime backends meet declared numerical-parity criteria.

Do not progress solely because a simulation executes.
