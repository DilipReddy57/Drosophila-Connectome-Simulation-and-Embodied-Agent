import numpy as np

def update_neurons(state, params, external_I=None):
    not_refractory = state.refractory_time == 0
    
    delta_V = (state.V[not_refractory] - params.V_rest) * params.decay_m
    I_contribution = state.I_syn[not_refractory] * (1.0 - params.decay_m)
    
    if external_I is not None:
        I_contribution += external_I[not_refractory] * (1.0 - params.decay_m)
        
    state.V[not_refractory] = params.V_rest + delta_V + I_contribution
    
    spikes = state.V >= params.V_th
    
    state.V[spikes] = params.V_reset
    state.I_syn[spikes] = 0.0
    state.refractory_time[spikes] = params.refractory_steps
    
    in_refractory = state.refractory_time > 0
    state.refractory_time[in_refractory] -= 1
    
    state.V[state.refractory_time > 0] = params.V_reset
    state.I_syn[state.refractory_time > 0] = 0.0
    
    return spikes

def update_synapses(state, delayed_spikes, weight_matrix, params):
    state.I_syn *= params.decay_syn
    
    if delayed_spikes.any():
        state.I_syn += weight_matrix.dot(delayed_spikes)
