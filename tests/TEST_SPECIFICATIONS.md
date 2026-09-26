# Initial test specification

## Dataset import and graph integrity

Imported networks must reject duplicate neuron IDs, unsupported neurotransmitters,
unknown endpoints, duplicate directed edges, and self-connections.  Their stable IDs
must map to dense simulator IDs without reordering, and graph reporting must retain
zero-degree (isolated) neurons.  Tests also verify exact in/out-degree and
neurotransmitter distributions.

## Runtime smoke network

A deterministic synthetic network must demonstrate: positive-weight excitation,
negative-weight inhibition, one-step-plus configured propagation delays, refractory
suppression, reset potentials, and timestamped spike recording.  No external data
or nondeterministic random source is allowed in this test.

## Reproducibility and metrics

Every run must record dataset, model, and parameter versions; seed and hardware;
timing measurements; neural metrics; and behavior metrics.  The record must be
serializable to a dictionary suitable for JSON output.
