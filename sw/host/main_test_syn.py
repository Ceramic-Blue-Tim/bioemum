# -*- coding: utf-8 -*-
# @title      Main
# @file       main.py
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

# Imports #################################################################
from configuration.gen_config_bioemum_test_syn import gen_config_bioemum_test_syn
from emulation.emulate_fpga import emulate_fpga
import numpy as np
import matplotlib.pyplot as plt

# Launch application #################################################################
if __name__ == "__main__":
    [hwconfig, swconfig] = gen_config_bioemum_test_syn(config_name="somaFSwithsyn", save_path="export/")
    
    EMULATE = True
    if EMULATE:
        nb_nrn_emu = 2
        [t, v] = emulate_fpga(hwconfig, swconfig, nb_nrn=nb_nrn_emu, nb_seg=hwconfig.nb_seg, store_context=False)
        
        np.savetxt("./waves-emu.csv", v, delimiter=";")
        
        fig, axs = plt.subplots(nb_nrn_emu, 1)
        for i in range(nb_nrn_emu):
            axs[i].plot(t*hwconfig.dt, v[i*hwconfig.nb_seg][:], color='b')
            axs[i].plot(t*hwconfig.dt, v[i*hwconfig.nb_seg+hwconfig.nb_seg-1][:], linestyle='-.', color='r')
        plt.show()