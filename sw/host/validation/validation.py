# -*- coding: utf-8 -*-
# @title      Compare emulation in software and hardware
# @file       validation.py
# @author     Romain Beaubois
# @date       06 Oct 2023
# @copyright
# SPDX-FileCopyrightText: © 2023 Romain Beaubois <refbeaubois@yahoo.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# @brief
# 
# @details
# > **06 Oct 2023** : file creation (RB)

import os, sys
import struct
import numpy as np
import matplotlib.pyplot as plt

# Nodes
NB_SEG       = 64
DEND_NODES   = [8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,58,59,60,61,62,63]
AXON_NODES   = [33,34,35,36,37,38]
SOMA_NODES   = [0,1,2,3,4,5,6,7]
DT           = 2**-5

FPATH_SOFT = "./waves_soft_mne13.csv"
FPATH_HARD = "./waves_hard_mne13.csv"


# Load software emulation
waves_soft = np.loadtxt(FPATH_SOFT, delimiter=";")
t_soft     = np.arange(len(waves_soft[1,:]))*DT

# Load hardware emulation
dtype        = np.dtype(np.float32)
nb_samples   = int(os.path.getsize(FPATH_HARD)/dtype.itemsize)
waves_hard   = np.fromfile(FPATH_HARD, dtype=dtype, count=nb_samples)
nb_lines     = int(len(waves_hard)/(NB_SEG+1))

# Reshape to tstamp, neurons
waves_hard       = waves_hard.reshape(nb_lines, (NB_SEG+1))
# Reconstruct time stamp from float
waves_hard[:,0]  = [int.from_bytes(bytearray(struct.pack("f", waves_hard[x, 0])), "little")*DT for x in range(nb_lines)]
# Crop to range to print
waves_hard = waves_hard[0:len(waves_soft[1,:]), :]
t_hard     = waves_hard[:, 0]

fig, axs = plt.subplots(2,1)
for i in range(NB_SEG):
    if i in SOMA_NODES:
        col = "#fec96c"
    elif i in DEND_NODES:
        col = "#ec6568"
    elif i in AXON_NODES:
        col = "#cccc99"
    axs[0].plot(t_soft, waves_soft[i][:],  color=col)
    axs[0].set_xlabel('Time (ms)')
    axs[0].set_ylabel('Amplitude (mV)')
    axs[0].set_title('Software emulation')
    
    axs[1].plot(t_hard, waves_hard[:,i+1], color=col)
    axs[1].set_xlabel('Time (ms)')
    axs[1].set_ylabel('Amplitude (mV)')
    axs[1].set_title('Hardware emulation')
plt.tight_layout()
plt.show()

ax = plt.axes(projection='3d')
for i in range(NB_SEG):
    if i in SOMA_NODES:
        col = "#fec96c"
    elif i in DEND_NODES:
        col = "#ec6568"
    elif i in AXON_NODES:
        col = "#cccc99"

    x_soft = np.zeros(len(t_soft))
    x_hard = np.zeros(len(t_hard))
    x_soft.fill(i)
    x_hard.fill(i)
    ax.plot3D(x_soft, t_soft, waves_soft[i][:],  linewidth=1.0, color=col)
    ax.plot3D(x_hard, t_hard, waves_hard[:,i+1], linewidth=1.0, color='black')
    ax.set_xlabel('Segment index')
    ax.set_ylabel('Time (ms)')
    ax.set_zlabel('Amlitude (mV)')
plt.show()