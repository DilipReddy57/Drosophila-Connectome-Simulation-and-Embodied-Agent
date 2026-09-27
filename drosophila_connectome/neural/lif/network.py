import numpy as np
import scipy.sparse as sp
from .state import State
from .parameters import LIFParameters
from .equations import update_neurons, update_synapses

class Input:
    def __init__(self, step_indices, values):
        self.step_indices = step_indices
        self.values = values

class Recorder:
    def __init__(self):
        self.spikes = []
        
    def record(self, step, spike_array):
        spiking_neurons = np.where(spike_array)[0]
        for n in spiking_neurons:
            self.spikes.append((step, n))

class Network:
    def __init__(self, num_neurons, weight_matrix, params=None):
        self.num_neurons = num_neurons
        self.weight_matrix = weight_matrix
        self.params = params or LIFParameters()
        self.state = State(num_neurons)
        self.state.reset(self.params.V_rest)
        
        # Buffer for delayed spikes. Rows represent delay steps.
        # Delay steps is how many steps we wait. So a buffer of size delay_steps + 1 
        # is enough to store spikes and retrieve them after delay.
        if self.params.delay_steps > 0:
            self.spike_buffer = np.zeros((self.params.delay_steps + 1, num_neurons), dtype=bool)
        else:
            self.spike_buffer = None
            
        self.step_idx = 0

class Simulation:
    def __init__(self, network, recorder=None):
        self.network = network
        self.recorder = recorder or Recorder()
        
    def step(self, external_I=None):
        # 1. Update synapses using delayed spikes
        delayed_spikes = np.zeros(self.network.num_neurons, dtype=bool)
        if self.network.spike_buffer is not None:
            read_idx = self.network.step_idx % (self.network.params.delay_steps + 1)
            delayed_spikes = self.network.spike_buffer[read_idx]
            
        update_synapses(self.network.state, delayed_spikes, self.network.weight_matrix, self.network.params)
        
        # 2. Update neurons
        spikes = update_neurons(self.network.state, self.network.params, external_I)
        
        # 3. Store new spikes in the buffer for future
        if self.network.spike_buffer is not None:
            write_idx = (self.network.step_idx + self.network.params.delay_steps) % (self.network.params.delay_steps + 1)
            self.network.spike_buffer[write_idx] = spikes
            # Clear current read_idx as we've read it
            self.network.spike_buffer[read_idx] = False
            
        # 4. Record
        self.recorder.record(self.network.step_idx, spikes)
        
        self.network.step_idx += 1
        
    def run(self, num_steps, inputs=None):
        for s in range(num_steps):
            ext_I = inputs[s] if inputs is not None and s in inputs else None
            self.step(ext_I)
