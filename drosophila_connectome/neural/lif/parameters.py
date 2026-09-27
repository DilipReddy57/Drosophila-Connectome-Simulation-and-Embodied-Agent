import numpy as np

class LIFParameters:
    def __init__(self, 
                 V_rest=-52.0, 
                 V_reset=-52.0, 
                 V_th=-45.0, 
                 tau_m=20.0, 
                 tau_syn=5.0, 
                 t_ref=2.2, 
                 delay=1.8, 
                 dt=0.1, 
                 W_syn=0.275):
        self.V_rest = V_rest
        self.V_reset = V_reset
        self.V_th = V_th
        self.tau_m = tau_m
        self.tau_syn = tau_syn
        self.t_ref = t_ref
        self.delay = delay
        self.dt = dt
        self.W_syn = W_syn

        self.decay_m = np.exp(-self.dt / self.tau_m)
        self.decay_syn = np.exp(-self.dt / self.tau_syn)
        self.refractory_steps = int(np.round(self.t_ref / self.dt))
        self.delay_steps = int(np.round(self.delay / self.dt))
