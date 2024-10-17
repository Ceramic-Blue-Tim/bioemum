# -*- coding: utf-8 -*-
# @title      Emulate configuration file similarly to fpga
# @file       emulate_fpga.py
# @author     Romain Beaubois
# @date       06 Oct 2023
# @copyright
# SPDX-FileCopyrightText: © 2022 Romain Beaubois <refbeaubois@yahoo.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# @brief
# 
# @details 
# > **09 Oct 2023** : file creation (RB)
# > **12 Sep 2024** : fix synapse operation, rprev was forgotten (RB)

NB_IONRATES         = 5
RATE_VMIN           = -76.0
RATE_VMAX           = 52.0
RATE_TABLE_SIZE     = 2048
RATE_STEP           = abs(RATE_VMIN - RATE_VMAX)/RATE_TABLE_SIZE
SPK_THREHSOLD       = 0.0

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from configuration.file_managers.SwConfigFile import *
from configuration.file_managers.HwConfigFile import *
from configuration.neurons.HHparam import *
from configuration.neurons.Geoparam import *
from configuration.synapses.Synapses import *

def hinesSolverArbor(d, u, p, b, nseg, debug):
        # Backward sweep
        for i in range(nseg-1, 0, -1):
            if debug:
                print(i)
                print("Ui : {}".format(u[i]))
                print("Di : {}".format(d[i]))
                print("Bi : {}".format(b[i]))
                print("Dpi : {}".format(d[p[i]]))
                print("Bpi : {}".format(b[p[i]]))
        
            parent      = p[i]
            factor      = u[i] / d[i]
            d[parent]   -= factor * u[i]
            b[parent]   -= factor * b[i]
            
            if debug:
                print("Dpi_new : {}".format(d[parent]))
                print("Bpi_new : {}".format(b[parent]))
        
        # Solve root
        b[0] /= d[0]
        
        if debug:
            print("")
            print("root Bi : {}".format(b[0]))

        # Forward sweep
        for i in range(1, nseg, 1):
            parent  = p[i]
            if debug:
                print(i)
                print("Ui : {}".format(u[i]))
                print("Di : {}".format(d[i]))
                print("Bi : {}".format(b[i]))
                print("Bpi : {}".format(b[p[i]]))
            
            b[i]    -= u[i] * b[parent]
            b[i]    /= d[i]

            if debug:
                print("vmem : {}".format(b[i]))

        return b

def emulate_fpga(hwconfig:HwConfigFile, swconfig:SwConfigFile, nb_nrn:int, nb_seg:int, store_context:bool=False, dtype=np.float32):
    dt          = hwconfig.dt
    to_node     = lambda n,s : (n*nb_seg + s)

    en_stim     = swconfig.parameters['en_stim']
    time_ms     = swconfig.parameters['emulation_time_s']*1e3
    stim_del_ms = swconfig.parameters['stim_delay_ms']
    stim_dur_ms = swconfig.parameters['stim_duration_ms']

    t           = np.linspace(1, time_ms/dt, int(time_ms/dt))

    v              = np.zeros( [nb_nrn*nb_seg, len(t)], dtype=dtype)
    detect         = np.zeros( nb_nrn*nb_seg, dtype=bool)
    spk_tab        = []
        
    mprev_Na       = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    mprev_K        = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    mprev_M        = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    mprev_L        = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    mprev_T        = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    hprev_Na       = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    hprev_L        = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    hprev_T        = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    iprev_noise    = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    geo_D_const    = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    geo_nrn_area   = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    geo_U          = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    geo_ptree      = np.zeros( nb_nrn*nb_seg, dtype=dtype )

    g_Na           = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    g_K            = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    g_M            = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    g_L            = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    g_T            = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    g_Leak         = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    e_Na           = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    e_K            = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    e_Ca           = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    e_Leak         = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    i_stim         = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    v_init         = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    noise_offs     = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    pmul_theta     = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    pmul_sigma     = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    pmul_gsyn      = np.zeros( nb_nrn*nb_seg, dtype=dtype )

    rprev_ampa     = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    rprev_nmda     = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    rprev_gabaa    = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    rprev_gabab    = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    sprev_gabab    = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    
    rnew_ampa      = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    rnew_nmda      = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    rnew_gabaa     = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    rnew_gabab     = np.zeros( nb_nrn*nb_seg, dtype=dtype )
    snew_gabab     = np.zeros( nb_nrn*nb_seg, dtype=dtype )

    Dnew           = np.zeros( nb_seg, dtype=dtype )
    Bnew           = np.zeros( nb_seg, dtype=dtype )
    U_diag         = np.zeros( nb_seg, dtype=dtype )
    p_tree         = np.zeros( nb_seg, dtype=int )

    if store_context:
        mNa        = np.zeros( [nb_nrn*nb_seg, len(t)], dtype=dtype)
        hNa        = np.zeros( [nb_nrn*nb_seg, len(t)], dtype=dtype)
        mK         = np.zeros( [nb_nrn*nb_seg, len(t)], dtype=dtype)
        mM         = np.zeros( [nb_nrn*nb_seg, len(t)], dtype=dtype)
        mL         = np.zeros( [nb_nrn*nb_seg, len(t)], dtype=dtype)
        hL         = np.zeros( [nb_nrn*nb_seg, len(t)], dtype=dtype)
        mT         = np.zeros( [nb_nrn*nb_seg, len(t)], dtype=dtype)
        hT         = np.zeros( [nb_nrn*nb_seg, len(t)], dtype=dtype)

        r_ampa     = np.zeros( [nb_nrn*nb_seg, len(t)], dtype=dtype)
        r_nmda     = np.zeros( [nb_nrn*nb_seg, len(t)], dtype=dtype)
        r_gabaa    = np.zeros( [nb_nrn*nb_seg, len(t)], dtype=dtype)
        r_gabab    = np.zeros( [nb_nrn*nb_seg, len(t)], dtype=dtype)
        s_gabab    = np.zeros( [nb_nrn*nb_seg, len(t)], dtype=dtype)
        Tv_ampa    = np.zeros( [nb_nrn*nb_seg, len(t)], dtype=dtype)
        Bv_nmda    = np.zeros( [nb_nrn*nb_seg, len(t)], dtype=dtype)

        coef_D_syn = np.zeros( [nb_nrn*nb_seg, len(t)], dtype=dtype)
        coef_B_syn = np.zeros( [nb_nrn*nb_seg, len(t)], dtype=dtype)

    pid = HHparam().getDict()
    for nid in range(nb_nrn*nb_seg):
        # Fetch hhparameters for all neurons
        g_Na[nid]        = hwconfig.HH_param[nid][pid["G_Na"]]
        g_K[nid]         = hwconfig.HH_param[nid][pid["G_Kd"]]
        g_M[nid]         = hwconfig.HH_param[nid][pid["G_M"]]
        g_L[nid]         = hwconfig.HH_param[nid][pid["G_L"]]
        g_T[nid]         = hwconfig.HH_param[nid][pid["G_T"]]
        g_Leak[nid]      = hwconfig.HH_param[nid][pid["G_Leak"]]
        e_Na[nid]        = hwconfig.HH_param[nid][pid["E_Na"]]
        e_K[nid]         = hwconfig.HH_param[nid][pid["E_K"]]
        e_Ca[nid]        = hwconfig.HH_param[nid][pid["E_Ca"]]
        e_Leak[nid]      = hwconfig.HH_param[nid][pid["E_Leak"]]
        i_stim[nid]      = hwconfig.HH_param[nid][pid["i_stim"]]
        v_init[nid]      = hwconfig.HH_param[nid][pid["v_init"]]
        noise_offs[nid]  = hwconfig.HH_param[nid][pid["noise_offs"]]
        pmul_theta[nid]  = hwconfig.HH_param[nid][pid["pmul_theta"]]
        pmul_sigma[nid]  = hwconfig.HH_param[nid][pid["pmul_sigma"]]
        pmul_gsyn[nid]   = hwconfig.HH_param[nid][pid["pmul_gsyn"]]

        geo_D_const[nid]    = hwconfig.geo_param[nid][0]
        geo_nrn_area[nid]   = hwconfig.geo_param[nid][1]
        geo_U[nid]          = hwconfig.geo_param[nid][2]
        geo_ptree[nid]      = hwconfig.geo_param[nid][3]
 
        # Initial conditions
        for nid in range(nb_nrn*nb_seg):
            v[nid][0]      = v_init[nid]

            mprev_Na[nid]  = 0.01
            mprev_K[nid]   = 0.01
            mprev_M[nid]   = 0.01
            mprev_L[nid]   = 0.01
            mprev_T[nid]   = 0.01

            hprev_Na[nid]  = 0.99
            hprev_L[nid]   = 0.99
            hprev_T[nid]   = 0.99

        if store_context:
            mNa[nid][0] = mprev_Na[nid]
            mK[nid][0]  = mprev_K[nid]
            mM[nid][0]  = mprev_M[nid]
            mL[nid][0]  = mprev_L[nid]
            mT[nid][0]  = mprev_T[nid]

            hNa[nid][0] = hprev_Na[nid]
            hL[nid][0]  = hprev_L[nid]
            hT[nid][0]  = hprev_T[nid]

    wsyn = hwconfig.wsyn
    tsyn = hwconfig.tsyn

    for i in tqdm(range(len(t)-1)):
            for n in range(nb_nrn):
                for s in range(nb_seg):
                    # Coding vprev/mprev
                    nid = to_node(n,s)
                    vprev = v[nid][i]

                    addr    = round(abs(vprev - RATE_VMIN) / RATE_STEP)
                    if addr < 0:
                        addr = 0
                    elif addr >  RATE_TABLE_SIZE-1:
                        addr =  RATE_TABLE_SIZE-1

                    # Load rate table
                    mNa_r1  = dtype(hwconfig.m_rates1[0][addr])
                    mNa_r2  = dtype(hwconfig.m_rates2[0][addr])
                    hNa_r1  = dtype(hwconfig.h_rates1[0][addr])
                    hNa_r2  = dtype(hwconfig.h_rates2[0][addr])
                    mK_r1   = dtype(hwconfig.m_rates1[1][addr])
                    mK_r2   = dtype(hwconfig.m_rates2[1][addr])
                    mM_r1   = dtype(hwconfig.m_rates1[2][addr])
                    mM_r2   = dtype(hwconfig.m_rates2[2][addr])
                    mL_r1   = dtype(hwconfig.m_rates1[3][addr])
                    mL_r2   = dtype(hwconfig.m_rates2[3][addr])
                    hL_r1   = dtype(hwconfig.h_rates1[3][addr])
                    hL_r2   = dtype(hwconfig.h_rates2[3][addr])
                    mT_r1   = dtype(hwconfig.m_rates1[4][addr])
                    mT_r2   = dtype(hwconfig.m_rates2[4][addr])
                    hT_r1   = dtype(hwconfig.h_rates1[4][addr])
                    hT_r2   = dtype(hwconfig.h_rates2[4][addr])
    
                    mnew_Na = mNa_r1 * mprev_Na[nid]  +  mNa_r2
                    hnew_Na = hNa_r1 * hprev_Na[nid]  +  hNa_r2
                    mnew_K  = mK_r1  * mprev_K[nid]   +  mK_r2
                    mnew_M  = mM_r1  * mprev_M[nid]   +  mM_r2
                    mnew_L  = mL_r1  * mprev_L[nid]   +  mL_r2
                    hnew_L  = hL_r1  * hprev_L[nid]   +  hL_r2
                    mnew_T  = mT_r1  * mprev_T[nid]   +  mT_r2
                    hnew_T  = hT_r1  * hprev_T[nid]   +  hT_r2

                    # Update previous values
                    mprev_Na[nid] = mnew_Na
                    mprev_K[nid]  = mnew_K
                    mprev_M[nid]  = mnew_M
                    mprev_L[nid]  = mnew_L
                    mprev_T[nid]  = mnew_T
                
                    hprev_Na[nid] = hnew_Na
                    hprev_L[nid]  = hnew_L
                    hprev_T[nid]  = hnew_T

                    # Store context
                    if store_context:
                        mNa[nid][i+1] = mnew_Na
                        hNa[nid][i+1] = hnew_Na
                        mK[nid][i+1]  = mnew_K
                        mM[nid][i+1]  = mnew_M
                        mL[nid][i+1]  = mnew_L
                        hL[nid][i+1]  = hnew_L
                        mT[nid][i+1]  = mnew_T
                        hT[nid][i+1]  = hnew_T
                
                    # Calculate currents (from mnew or mprev)
                    gnew_Na    = g_Na[nid]     * (mnew_Na*mnew_Na*mnew_Na) * hnew_Na
                    gnew_K     = g_K[nid]      * (mnew_K*mnew_K*mnew_K*mnew_K)
                    gnew_M     = g_M[nid]      * mnew_M
                    gnew_L     = g_L[nid]      * (mnew_L*mnew_L)  * hnew_L
                    gnew_T     = g_T[nid]      * (mnew_T*mnew_T)  * hnew_T
                    gnew_Leak  = g_Leak[nid]

                    gnewe_Na   =  gnew_Na   * e_Na[nid]
                    gnewe_K    =  gnew_K    * e_K[nid]
                    gnewe_M    =  gnew_M    * e_K[nid]
                    gnewe_L    =  gnew_L    * e_Ca[nid]
                    gnewe_T    =  gnew_T    * e_Ca[nid]
                    gnewe_Leak =  gnew_Leak * e_Leak[nid]

                    # Insert stimulation
                    if (t[i] > (stim_del_ms/dt)) and (t[i] < ((stim_del_ms+stim_dur_ms)/dt)) and en_stim:
                        i_stim_seg = i_stim[nid]
                    else:
                        i_stim_seg = 0

                    # Calculate synaptic current
                    gnew_syn_cumsum   = 0
                    gnewe_syn_cumsum  = 0
                    nodepost     = to_node(n, s) # current node
                    for npre in range(nb_nrn):
                        for spre in range(nb_seg):
                            nodepre  = to_node(npre,spre) # previous node
                            v_npre   = v[nodepre][i]
                            wsyn_i   = wsyn[nodepost][nodepre]
                            
                            match tsyn[nodepost][nodepre]:
                                case"ampa":
                                    [gnew_syn_it, gnewe_syn_it, rnew_ampa[nodepre]]  = Synapses().destexhe.calcISynAmpa( v_npre, vprev, rprev_ampa[nodepre],  wsyn_i, dt)
                                case "gabaa":
                                    [gnew_syn_it, gnewe_syn_it, rnew_gabaa[nodepre]] = Synapses().destexhe.calcISynGabaa(v_npre, vprev, rprev_gabaa[nodepre], wsyn_i, dt)
                                case "nmda":
                                    [gnew_syn_it, gnewe_syn_it, rnew_nmda[nodepre]]  = Synapses().destexhe.calcISynNmda( v_npre, vprev, rprev_nmda[nodepre],  wsyn_i, dt)
                                case "gabab":
                                    [gnew_syn_it, gnewe_syn_it, snew_gabab[nodepre], rnew_gabab[nodepre]] = Synapses().destexhe.calcISynGabab(v_npre, vprev, sprev_gabab[nodepre], rprev_gabab[nodepre], wsyn_i, dt)
                                case _:
                                    gnew_syn_it  = 0
                                    gnewe_syn_it = 0
                            
                            gnew_syn_cumsum  += gnew_syn_it
                            gnewe_syn_cumsum += gnewe_syn_it

                    # Mimic hardware operation
                    gnew_syn_cumsum  *= pmul_gsyn[nodepost]
                    gnewe_syn_cumsum *= pmul_gsyn[nodepost]
                        
                    if store_context:
                        Bv_nmda[nid, i+1] = Synapses().destexhe.B_v(vprev)
                        Tv_ampa[nid, i+1] = Synapses().destexhe.T_v(vprev)
                        
                        coef_D_syn[nid,i+1] = gnew_syn_cumsum
                        coef_B_syn[nid,i+1] = gnewe_syn_cumsum

                    # Calculate current coefficients (HLS IP), also divide by the PMUL_GSYN_HW_FACTOR to get back to correct units
                    Dnew[s]     = gnew_Na + gnew_K + gnew_M + gnew_L + gnew_T + gnew_Leak + geo_D_const[nid] + gnew_syn_cumsum/PMUL_GSYN_HW_FACTOR
                    Bnew[s]     = vprev*geo_nrn_area[nid] + gnewe_Na + gnewe_K + gnewe_M + gnewe_L + gnewe_T + gnewe_Leak + i_stim_seg + gnewe_syn_cumsum/PMUL_GSYN_HW_FACTOR
                    U_diag[s]   = geo_U[nid]
                    p_tree[s]   = int(geo_ptree[nid])

                rnew_ampa     = rprev_ampa
                rnew_nmda     = rprev_nmda
                rnew_gabaa    = rprev_gabaa
                rnew_gabab    = rprev_gabab   
                snew_gabab    = sprev_gabab

                if store_context:
                    r_ampa[:,  i+1]  = rnew_ampa
                    r_nmda[:,  i+1]  = rnew_nmda
                    r_gabaa[:, i+1]  = rnew_gabaa
                    r_gabab[:, i+1]  = rnew_gabab
                    s_gabab[:, i+1]  = snew_gabab

                # Calculate new membrane voltage
                vhalf = hinesSolverArbor(Dnew, U_diag, p_tree, Bnew, nb_seg, debug=False)

                # Forward Euler result at n+1/2 to n+1
                for s in range(nb_seg):
                    v[to_node(n,s)][i+1] = 2*vhalf[s] - v[to_node(n,s)][i]
    return [t, v]