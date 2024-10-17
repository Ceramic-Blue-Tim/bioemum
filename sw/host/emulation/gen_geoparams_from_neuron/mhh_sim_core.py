import mhh_sim_neuron

from matplotlib import pyplot as plt

import numpy as np
import struct

# Simulate dummy neuron to export coefficients
[t_sim_neuron, v_sim_neuron] = mhh_sim_neuron.mhh_sim()

# Plot curves
plt.figure(figsize=(8,4)) # Default figsize is (8,6)
plt.plot(t_sim_neuron, v_sim_neuron[0], '.-')
plt.xlabel('time (ms)')
plt.ylabel('Amp (mV)')    
ax = plt.gca()
ax.legend(['0','1','2','3','4','5','6','7','8','9','ref1','ref2'])
plt.show()
