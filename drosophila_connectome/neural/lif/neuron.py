class Neuron:
    def __init__(self, neuron_id, param_overrides=None):
        self.neuron_id = neuron_id
        self.param_overrides = param_overrides or {}
