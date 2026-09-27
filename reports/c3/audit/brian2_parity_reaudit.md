# Brian2 Parity Re-Audit

| Test                      |   Max_V_Error |   Mean_V_Error |      RMSE_V |   Max_I_syn_Error |   Spike_Count_Diff |
|:--------------------------|--------------:|---------------:|------------:|------------------:|-------------------:|
| Test A (Single, No Input) |   0           |    0           | 0           |       0           |                  0 |
| Test B (Single, Const I)  |   2.06057e-13 |    1.02091e-13 | 1.17367e-13 |       0           |                  0 |
| Test C (2-neuron Exc)     |   0.0498752   |    0.00455613  | 0.0100188   |       3.55271e-15 |                  0 |
| Test D (2-neuron Inh)     |   0.0498752   |    0.00455613  | 0.0100188   |       3.55271e-15 |                  0 |
| Test E (Recurrent)        |   0.00738503  |    0.00230056  | 0.00331506  |       1.77636e-15 |                  0 |
| Test F (Simul Spikes)     |   3.48166e-13 |    1.26107e-13 | 1.78201e-13 |       0           |                  0 |
| Test G (Refractory)       |   3.55271e-14 |    8.2423e-15  | 1.31786e-14 |       0           |                  0 |