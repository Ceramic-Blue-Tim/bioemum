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
from configuration.gen_config_bioemum import gen_config_bioemum
from emulation.emulate_fpga import emulate_fpga

# Launch application #################################################################
if __name__ == "__main__":
    [hwconfig, swconfig] = gen_config_bioemum(config_name="multicomp", save_path="export/")
    [t, v] = emulate_fpga(hwconfig, swconfig, nb_nrn=1, nb_seg=hwconfig.nb_seg, store_context=True)


    dend_nodes = [8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,58,59,60,61,62,63]
    axon_nodes = [33,34,35,36,37,38]
    soma_nodes = [0,1,2,3,4,5,6,7]

    import numpy as np
    np.savetxt("./waves-emu.csv", v, delimiter=";")

    import matplotlib.pyplot as plt
    for i in range(hwconfig.nb_seg):
        if i in soma_nodes:
            col = "#fec96c"
        elif i in dend_nodes:
            col = "#ec6568"
        elif i in axon_nodes:
            col = "#cccc99"
        plt.plot(t, v[i][:], color=col)
    plt.show()

    ax = plt.axes(projection='3d')
    for i in range(int(hwconfig.nb_seg)):
        if i in soma_nodes:
            col = "#fec96c"
        elif i in dend_nodes:
            col = "#ec6568"
        elif i in axon_nodes:
            col = "#cccc99"

        x = np.zeros(len(t))
        x.fill(i)
        ax.plot3D(x, t, v[i][:], linewidth=1.0, color=col)
    plt.show()
    