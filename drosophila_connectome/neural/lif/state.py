import numpy as np

class State:
    def __init__(self, num_neurons):
        self.num_neurons = num_neurons
        self.V = np.zeros(num_neurons)
        self.I_syn = np.zeros(num_neurons)
        self.refractory_time = np.zeros(num_neurons, dtype=int)
        
    def reset(self, V_rest):
        self.V.fill(V_rest)
        self.I_syn.fill(0.0)
        self.refractory_time.fill(0)
