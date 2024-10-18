# -*- coding: utf-8 -*-
# @title      Generate configuration files for bioemum
# @file       gen_conf_snn_hh.py
# @author     Romain Beaubois
# @date       06 Oct 2023
# @copyright
# SPDX-FileCopyrightText: © 2022 Romain Beaubois <refbeaubois@yahoo.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# @brief Script to generate configuration file for SNN HH
# 
# @details 
# > **06 Oct 2023** : file creation (RB)

import matplotlib.pyplot as plt
import numpy as np

from configuration.file_managers.SwConfigFile import *
from configuration.file_managers.HwConfigFile import *
from configuration.neurons.Ionrates import *
from configuration.neurons.HHparam import *
from configuration.neurons.Geoparam import *
from configuration.synapses.Synapses import *

def gen_config_bioemum_test_syn(config_name:str, save_path:str):
    # System parameters ####################################################################

    # Software environment version
    sw_ver              = "0.1.1"
    MAX_NB_NRN          = 16
    dt                  = 2**-5 # [ms]

    # Files
    config_fname        = config_name
    local_dirpath_save  = save_path

    # FPGA dev
    GEN_SIM_DEBUG_DATA  = False

    # Application parameters ################################################################
    swconfig_builder                                           = SwConfigFile()
    swconfig_builder.parameters["fpath_hwconfig"]              = "/home/petalinux/bioemum/config/hwconfig_" + config_fname + ".txt"
    swconfig_builder.parameters["emulation_time_s"]            = 0.1
    swconfig_builder.parameters["sel_nrn_vmem_dac"]            = [0, 1, 2, 3, 4, 5, 6, 7]
    swconfig_builder.parameters["sel_nrn_vmem_dma"]            = [x*64 for x in range(16)] + [x+961 for x in range(64-16)]
    swconfig_builder.parameters["save_local_spikes"]           = False
    swconfig_builder.parameters["save_local_vmem"]             = True
    swconfig_builder.parameters["save_path"]                   = "/home/petalinux/bioemum/data/" # target saving director
    swconfig_builder.parameters["en_zmq_spikes"]               = False
    swconfig_builder.parameters["en_zmq_vmem"]                 = False
    swconfig_builder.parameters["en_zmq_stim"]                 = False
    swconfig_builder.parameters["en_wifi_spikes"]              = False
    swconfig_builder.parameters["ip_zmq_spikes"]               = "tcp://*:5557"
    swconfig_builder.parameters["ip_zmq_vmem"]                 = "tcp://*:5558"
    swconfig_builder.parameters["ip_zmq_stim"]                 = "tcp://192.168.137.1:5559"
    swconfig_builder.parameters["nb_tstamp_per_spk_transfer"]  = 100
    swconfig_builder.parameters["nb_tstep_per_vmem_transfer"]  = 190
    swconfig_builder.parameters["en_stim"]                     = True
    swconfig_builder.parameters["stim_delay_ms"]               = 0
    swconfig_builder.parameters["stim_duration_ms"]            = 500

    # Globals & Builders ####################################################################
    tsyn_row, wsyn_row    = ([] for i in range(2))
    tsyn,     wsyn        = ([] for i in range(2))
    tnrn                  = []

    # Custom model #################################################################

    model = "somaFS"

    if model == "test":
        MAX_NB_SEG = 10
        tnrn = ["somaFS"] * MAX_NB_SEG*MAX_NB_NRN
        U_diag  = [0]*MAX_NB_SEG
        D_diag  = [0]*MAX_NB_SEG
        n_area  = [0]*MAX_NB_SEG
        Cmem      = 1.0
        
        #                   0   1   2   3   4   5   6   7   8   9
        pnode           = [-1,  0,  1,  2,  3,  4,  5,  3,  7,  8]
        stim_ins_node   = 0
        virtuals_nodes  = [0, 3, 6, 9]

        U_diag[1] = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.055016523537939135)   # U0 (S)
        U_diag[2] = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.11003304707587827)    # U1 (S)
        U_diag[3] = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.055016523537939135)   # U2 (S)
        U_diag[4] = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.5501652353793913)     # U3 (S)
        U_diag[5] = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.1003304707587827)     # U4 (S)
        U_diag[6] = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.5501652353793913)     # U5 (S)
        U_diag[7] = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.1003304707587827)     # U6 (S)
        U_diag[8] = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/2.2006609415175653)     # U7 (S)
        U_diag[9] = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.1003304707587827)     # U8 (S)

        n_area[0] = 100.0
        n_area[1] = 197.92033717615698
        n_area[2] = 197.92033717615698
        n_area[3] = 100.0
        n_area[4] = 1979.2033717615698
        n_area[5] = 1979.2033717615698
        n_area[6] = 100.0
        n_area[7] = 3958.4067435231395
        n_area[8] = 3958.406
        n_area[9] = 100.0

    elif model == "mne13":
        MAX_NB_SEG      = 64
        
        tnrn            = ["MNE13others"]*MAX_NB_SEG*MAX_NB_NRN
        U_diag          = [0]*MAX_NB_SEG
        D_diag          = [0]*MAX_NB_SEG
        n_area          = [0]*MAX_NB_SEG
        Cmem            = 1.0
        pnode           = [-1, 0, 1, 2, 3, 4, 5, 6, 4, 8, 9, 10, 11, 12, 13, 9, 15, 16, 9, 18, 19, 9, 21, 22, 8, 24, 25, 4, 27, 28, 4, 30, 31, 0, 33, 34, 35, 36, 37, 0, 39, 40, 41, 42, 43, 44, 39, 46, 47, 39, 49, 50, 39, 52, 53, 39, 55, 56, 1, 58, 59, 1, 61, 62]
                           
        stim_ins_node   = 0
        virtuals_nodes  = [0, 7, 14, 17, 20, 23, 26, 29, 32, 34, 36, 38, 45, 48, 51, 54, 57, 60, 63]
        axonactive_nodes= [35,36]
        axon_nodes      = [37,38]

        U_diag[1]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.05943773935485745)
        U_diag[2]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.030640029682480394)
        U_diag[3]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.018271946485155857)
        U_diag[4]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.01588528584429702)
        U_diag[5]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.018271946485155857)
        U_diag[6]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.030640029682480353)
        U_diag[7]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.0594377393548572)
        U_diag[8]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.43518929846260523)
        U_diag[9]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.0307115039034744)
        U_diag[10]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.356650310656043)
        U_diag[11]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.8866184123862657)
        U_diag[12]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/2.433432981725053)
        U_diag[13]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/2.9815916365777033)
        U_diag[14]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.6907108882657491)
        U_diag[15]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.9928330068419752)
        U_diag[16]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/3.858535744674991)
        U_diag[17]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/2.6472386345341046)
        U_diag[18]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.319144893870532)
        U_diag[19]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/4.939434490205624)
        U_diag[20]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/3.425698005013941)
        U_diag[21]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.9928330068419752)
        U_diag[22]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/3.858535744674991)
        U_diag[23]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/2.6472386345341046)
        U_diag[24]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.319144893870532)
        U_diag[25]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/4.939434490205624)
        U_diag[26]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/3.425698005013941)
        U_diag[27]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/3.485402587782814)
        U_diag[28]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/7.139065824148924)
        U_diag[29]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/3.830046804798296)
        U_diag[30]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/2.281152307773597)
        U_diag[31]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/4.690820311345517)
        U_diag[32]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/2.5454240243631183)
        U_diag[33]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.16560716940583312)
        U_diag[34]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.15915494309189535)
        U_diag[35]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/15.915494309189537)
        U_diag[36]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/15.915494309189537)
        U_diag[37]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/15.915494309189537)
        U_diag[38]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/15.915494309189537)
        U_diag[39]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/3.2339140549451537)
        U_diag[40]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/10.058949109581512)
        U_diag[41]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/14.375432585851392)
        U_diag[42]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/16.022313567412358)
        U_diag[43]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/23.30688886817356)
        U_diag[44]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/30.129879914996472)
        U_diag[45]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/16.057856691426725)
        U_diag[46]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/3.0208822586707376)
        U_diag[47]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/6.4437761447348025)
        U_diag[48]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/4.70403220541311)
        U_diag[49]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/3.0208822586707376)
        U_diag[50]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/6.4437761447348025)
        U_diag[51]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/4.70403220541311)
        U_diag[52]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/3.583321159006073)
        U_diag[53]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/7.508965929848454)
        U_diag[54]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/5.326159121305467)
        U_diag[55]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/3.9887041821409954)
        U_diag[56]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/8.27671128857872)
        U_diag[57]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/5.774562831979966)
        U_diag[58]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.5173975049279893)
        U_diag[59]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/3.098836280687496)
        U_diag[60]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.6150688534304205)
        U_diag[61]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.9871681735572647)
        U_diag[62]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/2.0678606759497224)
        U_diag[63]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.3951909750772467)
        
        n_area[0] = 100.0
        n_area[1] = 69.41304762672715
        n_area[2] = 71.0734342703707
        n_area[3] = 70.923054624474
        n_area[4] = 70.92305462447403
        n_area[5] = 71.07343427037065
        n_area[6] = 69.41304762672715
        n_area[7] = 100.0
        n_area[8] = 52.145697691091584
        n_area[9] = 46.31860384389319
        n_area[10] = 39.58140998038023
        n_area[11] = 34.095912729638414
        n_area[12] = 30.31183007410942
        n_area[13] = 27.762145382185285
        n_area[14] = 100.0
        n_area[15] = 59.089900201810366
        n_area[16] = 41.25536919286817
        n_area[17] = 100.0
        n_area[18] = 75.5908692985243
        n_area[19] = 53.76571794854933
        n_area[20] = 100.0
        n_area[21] = 59.089900201810366
        n_area[22] = 41.25536919286817
        n_area[23] = 100.0
        n_area[24] = 75.5908692985243
        n_area[25] = 53.76571794854933
        n_area[26] = 100.0
        n_area[27] = 60.40229589809136
        n_area[28] = 58.31648615402064
        n_area[29] = 100.0
        n_area[30] = 37.992494570103176
        n_area[31] = 36.47370421182964
        n_area[32] = 100.0
        n_area[33] = 6.29084999924438
        n_area[34] = 100.0
        n_area[35] = 628.3185307179587
        n_area[36] = 100.0
        n_area[37] = 628.3185307179587
        n_area[38] = 100.0
        n_area[39] = 72.24576869396755
        n_area[40] = 54.8166124375064
        n_area[41] = 50.8361613499874
        n_area[42] = 45.295322775945564
        n_area[43] = 37.29168619198887
        n_area[44] = 34.91543357506427
        n_area[45] = 100.0
        n_area[46] = 52.5006575858863
        n_area[47] = 46.780852782940265
        n_area[48] = 100.0
        n_area[49] = 52.5006575858863
        n_area[50] = 46.780852782940265
        n_area[51] = 100.0
        n_area[52] = 62.62838512184351
        n_area[53] = 56.34035485992081
        n_area[54] = 100.0
        n_area[55] = 69.8046699720857
        n_area[56] = 63.353822270565495
        n_area[57] = 100.0
        n_area[58] = 30.66348616831567
        n_area[59] = 29.903827589609104
        n_area[60] = 100.0
        n_area[61] = 30.84438369086939
        n_area[62] = 27.801810991684782
        n_area[63] = 100.0

        for n in range(MAX_NB_NRN):
            for s in range(MAX_NB_SEG):
                if s in axon_nodes:
                    tnrn[n*MAX_NB_SEG + s] = "MNE13axon"
                elif s in axonactive_nodes:
                    tnrn[n*MAX_NB_SEG + s] = "MNE13axonactive"
                else:
                    tnrn[n*MAX_NB_SEG + s] = "MNE13others"

    elif model == "mne13_soma_axon":
        MAX_NB_SEG      = 64
        
        tnrn            = ["MNE13others"]*MAX_NB_SEG*MAX_NB_NRN
        U_diag          = [0]*MAX_NB_SEG
        D_diag          = [0]*MAX_NB_SEG
        n_area          = [0]*MAX_NB_SEG
        Cmem            = 1.0
        pnode           = [-1, 0, 1, 2, 3, 4, 5, 0, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62]
                           
        stim_ins_node         = 0
        virtuals_nodes        = [0, 6, 25, 44, 63]
        nodes_soma            = [0, 1, 2, 3, 4, 5, 6]
        nodes_axon_passive    = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
        nodes_axon_active     = [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44]
        nodes_axon            = [45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]

        U_diag[1]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.0639402920749525)
        U_diag[2]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.03217535739961052)
        U_diag[3]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.02017670897007918)
        U_diag[4]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.0201767089700792)
        U_diag[5]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.03217535739961051)
        U_diag[6]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.06394029207495248)
        U_diag[7]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.008841941282883074)
        U_diag[8]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017683882565766147)
        U_diag[9]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017683882565766147)
        U_diag[10]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017683882565766147)
        U_diag[11]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017683882565766147)
        U_diag[12]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017683882565766147)
        U_diag[13]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017683882565766147)
        U_diag[14]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017683882565766147)
        U_diag[15]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017683882565766147)
        U_diag[16]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017683882565766147)
        U_diag[17]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017683882565766147)
        U_diag[18]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017683882565766147)
        U_diag[19]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017683882565766147)
        U_diag[20]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017683882565766147)
        U_diag[21]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017683882565766147)
        U_diag[22]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017683882565766147)
        U_diag[23]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017683882565766147)
        U_diag[24]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017683882565766147)
        U_diag[25]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.008841941282883074)
        U_diag[26]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.8841941282883075)
        U_diag[27]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[28]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[29]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[30]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[31]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[32]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[33]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[34]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[35]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[36]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[37]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[38]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[39]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[40]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[41]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[42]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[43]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[44]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.8841941282883075)
        U_diag[45]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.8841941282883075)
        U_diag[46]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[47]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[48]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[49]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[50]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[51]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[52]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[53]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[54]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[55]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[56]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[57]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[58]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[59]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[60]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[61]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[62]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/1.768388256576615)
        U_diag[63]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.8841941282883075)

        n_area[0]   = 100.0
        n_area[1]   = 83.80215065188017
        n_area[2]   = 85.13632193134131
        n_area[3]   = 84.94212787670081
        n_area[4]   = 85.13632193134136
        n_area[5]   = 83.80215065188013
        n_area[6]   = 100.0
        n_area[7]   = 0.3490658503988659
        n_area[8]   = 0.3490658503988659
        n_area[9]   = 0.3490658503988659
        n_area[10]  = 0.3490658503988659
        n_area[11]  = 0.3490658503988659
        n_area[12]  = 0.3490658503988659
        n_area[13]  = 0.3490658503988659
        n_area[14]  = 0.3490658503988659
        n_area[15]  = 0.3490658503988659
        n_area[16]  = 0.3490658503988659
        n_area[17]  = 0.3490658503988659
        n_area[18]  = 0.3490658503988659
        n_area[19]  = 0.3490658503988659
        n_area[20]  = 0.3490658503988659
        n_area[21]  = 0.3490658503988659
        n_area[22]  = 0.3490658503988659
        n_area[23]  = 0.3490658503988659
        n_area[24]  = 0.3490658503988659
        n_area[25]  = 100.0
        n_area[26]  = 34.906585039886586
        n_area[27]  = 34.906585039886586
        n_area[28]  = 34.906585039886586
        n_area[29]  = 34.906585039886586
        n_area[30]  = 34.906585039886586
        n_area[31]  = 34.906585039886586
        n_area[32]  = 34.906585039886586
        n_area[33]  = 34.906585039886586
        n_area[34]  = 34.906585039886586
        n_area[35]  = 34.906585039886586
        n_area[36]  = 34.906585039886586
        n_area[37]  = 34.906585039886586
        n_area[38]  = 34.906585039886586
        n_area[39]  = 34.906585039886586
        n_area[40]  = 34.906585039886586
        n_area[41]  = 34.906585039886586
        n_area[42]  = 34.906585039886586
        n_area[43]  = 34.906585039886586
        n_area[44]  = 100.0
        n_area[45]  = 34.906585039886586
        n_area[46]  = 34.906585039886586
        n_area[47]  = 34.906585039886586
        n_area[48]  = 34.906585039886586
        n_area[49]  = 34.906585039886586
        n_area[50]  = 34.906585039886586
        n_area[51]  = 34.906585039886586
        n_area[52]  = 34.906585039886586
        n_area[53]  = 34.906585039886586
        n_area[54]  = 34.906585039886586
        n_area[55]  = 34.906585039886586
        n_area[56]  = 34.906585039886586
        n_area[57]  = 34.906585039886586
        n_area[58]  = 34.906585039886586
        n_area[59]  = 34.906585039886586
        n_area[60]  = 34.906585039886586
        n_area[61]  = 34.906585039886586
        n_area[62]  = 34.906585039886586
        n_area[63]  = 100.0

        for n in range(MAX_NB_NRN):
            for s in range(MAX_NB_SEG):
                if s in nodes_soma:
                    tnrn[n*MAX_NB_SEG + s] = "MNE13others"
                elif s in nodes_axon_passive:
                    tnrn[n*MAX_NB_SEG + s] = "MNE13others"
                elif s in nodes_axon_active:
                    tnrn[n*MAX_NB_SEG + s] = "MNE13axonactive"
                elif s in nodes_axon:
                    tnrn[n*MAX_NB_SEG + s] = "MNE13others"
    
    elif model == "somaFS":
        MAX_NB_SEG      = 64
        
        tnrn            = ["somaFS"]*MAX_NB_SEG*MAX_NB_NRN
        U_diag          = [0]*MAX_NB_SEG
        D_diag          = [0]*MAX_NB_SEG
        n_area          = [0]*MAX_NB_SEG
        Cmem            = 1.0
        pnode           = [-1, 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62]

        stim_ins_node   = 0
        virtuals_nodes  = [0, 63]

        U_diag[1]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.008873632828699862)
        U_diag[2]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[3]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[4]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[5]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[6]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[7]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[8]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[9]   = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[10]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[11]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[12]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[13]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[14]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[15]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[16]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[17]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[18]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[19]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[20]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[21]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[22]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[23]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[24]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[25]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[26]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[27]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[28]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[29]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[30]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[31]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[32]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[33]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[34]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[35]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[36]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[37]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[38]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[39]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[40]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[41]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[42]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[43]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[44]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[45]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[46]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[47]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[48]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[49]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[50]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[51]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[52]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[53]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[54]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[55]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[56]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[57]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[58]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[59]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[60]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[61]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[62]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.017747265657399723)
        U_diag[63]  = - (0.5e3*dt/Cmem) * 1e6 * 1e-4 * (1/0.008873632828699862)

        n_area[0]  = 100.0
        n_area[1]  = 31.92263502841242
        n_area[2]  = 31.92263502841242
        n_area[3]  = 31.92263502841242
        n_area[4]  = 31.92263502841242
        n_area[5]  = 31.92263502841242
        n_area[6]  = 31.92263502841242
        n_area[7]  = 31.92263502841242
        n_area[8]  = 31.92263502841242
        n_area[9]  = 31.92263502841242
        n_area[10] = 31.92263502841242
        n_area[11] = 31.92263502841242
        n_area[12] = 31.92263502841242
        n_area[13] = 31.92263502841242
        n_area[14] = 31.92263502841242
        n_area[15] = 31.92263502841242
        n_area[16] = 31.92263502841242
        n_area[17] = 31.92263502841242
        n_area[18] = 31.92263502841242
        n_area[19] = 31.92263502841242
        n_area[20] = 31.92263502841242
        n_area[21] = 31.92263502841242
        n_area[22] = 31.92263502841242
        n_area[23] = 31.92263502841242
        n_area[24] = 31.92263502841242
        n_area[25] = 31.92263502841242
        n_area[26] = 31.92263502841242
        n_area[27] = 31.92263502841242
        n_area[28] = 31.92263502841242
        n_area[29] = 31.92263502841242
        n_area[30] = 31.92263502841242
        n_area[31] = 31.92263502841242
        n_area[32] = 31.92263502841242
        n_area[33] = 31.92263502841242
        n_area[34] = 31.92263502841242
        n_area[35] = 31.92263502841242
        n_area[36] = 31.92263502841242
        n_area[37] = 31.92263502841242
        n_area[38] = 31.92263502841242
        n_area[39] = 31.92263502841242
        n_area[40] = 31.92263502841242
        n_area[41] = 31.92263502841242
        n_area[42] = 31.92263502841242
        n_area[43] = 31.92263502841242
        n_area[44] = 31.92263502841242
        n_area[45] = 31.92263502841242
        n_area[46] = 31.92263502841242
        n_area[47] = 31.92263502841242
        n_area[48] = 31.92263502841242
        n_area[49] = 31.92263502841242
        n_area[50] = 31.92263502841242
        n_area[51] = 31.92263502841242
        n_area[52] = 31.92263502841242
        n_area[53] = 31.92263502841242
        n_area[54] = 31.92263502841242
        n_area[55] = 31.92263502841242
        n_area[56] = 31.92263502841242
        n_area[57] = 31.92263502841242
        n_area[58] = 31.92263502841242
        n_area[59] = 31.92263502841242
        n_area[60] = 31.92263502841242
        n_area[61] = 31.92263502841242
        n_area[62] = 31.92263502841242
        n_area[63] = 100.0

    ### ----------------------------------------------------
    for s in range(MAX_NB_SEG):
        D_diag[s] -= U_diag[s]
        if pnode[s] != -1:
            D_diag[pnode[s]] -= U_diag[s]

    for s in range(MAX_NB_SEG):
        D_diag[s] = D_diag[s] + n_area[s]

    geoparam = []
    for n in range(MAX_NB_NRN):
        for s in range(MAX_NB_SEG):
            if pnode[s] == -1:
                ptree = 0
            else:
                ptree = pnode[s]

            l = []
            l.append(D_diag[s])
            l.append(n_area[s])
            l.append(U_diag[s])
            l.append(ptree)
            geoparam.append(l)

    # Create synaptic conncetions

    # Synaptic types
    #      | source |
    # -----|--------|
    # dest |        |
    tsyn_dict = Synapses().getDict()
    weight = 1.9
    for dest in range(MAX_NB_NRN*MAX_NB_SEG):
        for src in range(MAX_NB_NRN*MAX_NB_SEG):
            if model == "mne13" or model == "mne13_soma_axon":
                tsyn_i = "destexhe_none"
            else:
                # AMPA chaser to check synapses
                if src== 0*MAX_NB_SEG+1 and dest== 1*MAX_NB_SEG+1 or \
                   src== 1*MAX_NB_SEG+1 and dest== 2*MAX_NB_SEG+1 or \
                   src== 2*MAX_NB_SEG+1 and dest== 3*MAX_NB_SEG+1 or \
                   src== 3*MAX_NB_SEG+1 and dest== 4*MAX_NB_SEG+1 or \
                   src== 4*MAX_NB_SEG+1 and dest== 5*MAX_NB_SEG+1 or \
                   src== 5*MAX_NB_SEG+1 and dest== 6*MAX_NB_SEG+1 or \
                   src== 6*MAX_NB_SEG+1 and dest== 7*MAX_NB_SEG+1 or \
                   src== 7*MAX_NB_SEG+1 and dest== 8*MAX_NB_SEG+1 or \
                   src== 8*MAX_NB_SEG+1 and dest== 9*MAX_NB_SEG+1 or \
                   src== 9*MAX_NB_SEG+1 and dest==10*MAX_NB_SEG+1 or \
                   src==10*MAX_NB_SEG+1 and dest==11*MAX_NB_SEG+1 or \
                   src==11*MAX_NB_SEG+1 and dest==12*MAX_NB_SEG+1 or \
                   src==12*MAX_NB_SEG+1 and dest==13*MAX_NB_SEG+1 or \
                   src==13*MAX_NB_SEG+1 and dest==14*MAX_NB_SEG+1 or \
                   src==14*MAX_NB_SEG+1 and dest==15*MAX_NB_SEG+1:
                    tsyn_i = "destexhe_ampa"
                else:
                    tsyn_i = "destexhe_none"

            tsyn_row.append(tsyn_dict[tsyn_i])
            if tsyn_i == "destexhe_none":
                wsyn_row.append(0.0)
            else:
                if tsyn_i == "destexhe_ampa" or tsyn_i == "destexhe_gabaa":
                    wsyn_row.append(1.0)
                else:
                    wsyn_row.append(weight)

        tsyn.append(tsyn_row)
        wsyn.append(wsyn_row)
        tsyn_row = []
        wsyn_row = []

    #   ██████  ██████  ███    ██ ███████ ██  ██████      ███████ ██ ██      ███████ 
    #  ██      ██    ██ ████   ██ ██      ██ ██           ██      ██ ██      ██      
    #  ██      ██    ██ ██ ██  ██ █████   ██ ██   ███     █████   ██ ██      █████   
    #  ██      ██    ██ ██  ██ ██ ██      ██ ██    ██     ██      ██ ██      ██      
    #   ██████  ██████  ██   ████ ██      ██  ██████      ██      ██ ███████ ███████ 
    #                                                                                
    # Config file #################################################################
    hw_cfg_file                 = HwConfigFile(sw_ver, MAX_NB_NRN, MAX_NB_SEG)

    # Parameters
    hw_cfg_file.dt              = dt
    hw_cfg_file.nb_hhparam      = HHparam().getNb()
    hw_cfg_file.nb_ionrate      = Ionrates().getNbIonRates("pospischil")
    hw_cfg_file.depth_ionrate   = Ionrates().getDepthIonRates("pospischil")
    hw_cfg_file.depth_synrate   = Synapses().getDepthSynRates("destexhe")

    # Ionrates
    if model == "mne13" or model == "mne13_soma_axon":
        [hw_cfg_file.m_rates1, hw_cfg_file.m_rates2,
        hw_cfg_file.h_rates1, hw_cfg_file.h_rates2] = Ionrates().getIonRates("MN_E13", dt, GEN_SIM_DEBUG_DATA)
    else:
        [hw_cfg_file.m_rates1, hw_cfg_file.m_rates2,
        hw_cfg_file.h_rates1, hw_cfg_file.h_rates2] = Ionrates().getIonRates("pospischil", dt, GEN_SIM_DEBUG_DATA)

    # Synapse parameters
    hw_cfg_file.psyn     = Synapses().getPsyn("destexhe", dt)

    # Synrates
    hw_cfg_file.synrates = Synapses().getSynRates("destexhe", GEN_SIM_DEBUG_DATA)

    # Neuron types
    for n in range(MAX_NB_NRN):
        for s in range(MAX_NB_SEG):
            hhp = HHparam().getParameters(tnrn[n*MAX_NB_SEG + s], dt)

            # HH currents conductances
            if s in virtuals_nodes:
                hhp[HHparam().PID['G_Na']]   *= 0.0
                hhp[HHparam().PID['G_Kd']]   *= 0.0
                hhp[HHparam().PID['G_M']]    *= 0.0
                hhp[HHparam().PID['G_L']]    *= 0.0
                hhp[HHparam().PID['G_T']]    *= 0.0
                hhp[HHparam().PID['G_Leak']] *= 0.0
            else:
                hhp[HHparam().PID['G_Na']]   *= n_area[s]
                hhp[HHparam().PID['G_Kd']]   *= n_area[s]
                hhp[HHparam().PID['G_M']]    *= n_area[s]
                hhp[HHparam().PID['G_L']]    *= n_area[s]
                hhp[HHparam().PID['G_T']]    *= n_area[s]
                hhp[HHparam().PID['G_Leak']] *= n_area[s]

            # Stimulation current (stimulation current in nA, *100 for unit coherence)
            if s == stim_ins_node and n == 0:
                hhp[HHparam().PID['i_stim']] *= (100/n_area[s]) * n_area[s]
            else:
                hhp[HHparam().PID['i_stim']] *= 0.0

            # Synaptic conductance
            hhp[HHparam().PID['pmul_gsyn']] /= n_area[s]*1e-8 # div by area in cm2 to have S/cm2
            hhp[HHparam().PID['pmul_gsyn']] *= n_area[s]

            hw_cfg_file.HH_param.append(hhp)

    for i in range(len(geoparam)):
        hw_cfg_file.geo_param.append(geoparam[i])

    # Synapses
    hw_cfg_file.tsyn = tsyn
    hw_cfg_file.wsyn = wsyn

    # Write file
    swconfig_builder.write(os.path.join(local_dirpath_save, "swconfig_" + config_fname + ".json"))  # save path of swconfig on local
    hw_cfg_file.write(os.path.join(local_dirpath_save, "hwconfig_" + config_fname + ".txt"))        # save path of hwconfig on local

    return [hw_cfg_file, swconfig_builder]