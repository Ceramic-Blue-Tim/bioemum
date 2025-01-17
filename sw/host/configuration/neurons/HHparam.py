4# -*- coding: utf-8 -*-
# @title      Hodgkin & Huxley parameters
# @file       Hhparam.py
# @author     Romain Beaubois
# @date       05 Dec 2022
# @copyright
# SPDX-FileCopyrightText: © 2022 Romain Beaubois <refbeaubois@yahoo.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# @brief Class to generates HH neuron parameters
# 
# @details 
# > **05 Dec 2022** : file creation (RB)

NB_HHPARAM          = 16
SCALE_FACTOR        = 16 # 16: AMPA stimulation with ~1 spike
PMUL_GSYN_HW_FACTOR = 1e-4

class HHparam:
    PID = { 
        "G_Na":0, 
        "G_Kd":1, 
        "G_M":2,
        "G_L":3,
        "G_T":4,
        "G_Leak":5,
        "E_Na":6,
        "E_K":7,
        "E_Ca":8,
        "E_Leak":9,
        "mu":10,        "noise_offs":10,
        "theta":11,     "pmul_theta":11,
        "sigma":12,     "pmul_sigma":12,
        "i_stim":13,
        "v_init":14,
        "pmul_gsyn":15
    }

    def __init__(self):
        """Initialize"""
        pass

    def getNb(self):
        """Get number of parameters"""
        return NB_HHPARAM
    
    def getDict(self):
        """Get dictionnary to handle parameters"""
        return self.PID

    def getCmem(self, nrn_type):
        """Get membrane capacitiy depending on neuron type

        :param str nrn_type: type of neuron ("FS","RS",...)
        :returns: membrane capacity
        """
        if   nrn_type == "FS":
            cmem = 1.0 # (µF/cm²)
        elif nrn_type == "RS":
            cmem = 1.0 # (µF/cm²)
        else:
            cmem = 1.0 # (µF/cm²)
        
        return cmem

    def getParameters(self, nrn_type:str, dt):
        """Get HH parameters for a given neuron type

        :param str nrn_type: type of neuron ("FS","RS",...)
        :param dt float: time step in ms
        :returns: list of parameters, mebrane capacity and area
        """
        hhparam = [0.0]*NB_HHPARAM
        nt = nrn_type.split('_')

        if nt[0] == "somaFS":
            cmem                             = 1.0           # (µF/cm²)
            area_cm2                         = 67e-4*67e-4   # (cm²)
            hhparam[self.PID["G_Na"]]        = 0.05          # (S/cm²)
            hhparam[self.PID["G_Kd"]]        = 0.01          # (S/cm²)
            hhparam[self.PID["G_M"]]         = 0.0           # (S/cm²)
            hhparam[self.PID["G_L"]]         = 0.0           # (S/cm²)
            hhparam[self.PID["G_T"]]         = 0.0           # (S/cm²)
            hhparam[self.PID["G_Leak"]]      = 0.00015       # (S/cm²)
            hhparam[self.PID["E_Na"]]        = +50.0         # (mV)
            hhparam[self.PID["E_K"]]         = -100.0        # (mV)
            hhparam[self.PID["E_Ca"]]        = 0.0           # (mV)
            hhparam[self.PID["E_Leak"]]      = -70.0         # (mV)
            if not("nonoise" in nt):
                hhparam[self.PID["mu"]]      = 0.048         # 0.05
                hhparam[self.PID["theta"]]   = 8.0           # 8.0
                hhparam[self.PID["sigma"]]   = 0.11          # 0.1
            if not("nostim" in nt):
                hhparam[self.PID["i_stim"]]  = 0.5
            hhparam[self.PID["v_init"]]      = -70.0         # (mV)

        elif nt[0] == "somaRS":
            cmem                             = 1.0           # (µF/cm²)
            area_cm2                         = 97e-4*97e-4   # (cm²)
            hhparam[self.PID["G_Na"]]        = 0.05          # (S/cm²)
            hhparam[self.PID["G_Kd"]]        = 0.005         # (S/cm²)
            hhparam[self.PID["G_M"]]         = 7e-5          # (S/cm²)
            hhparam[self.PID["G_L"]]         = 0.0           # (S/cm²)
            hhparam[self.PID["G_T"]]         = 0.0           # (S/cm²)
            hhparam[self.PID["G_Leak"]]      = 0.0001        # (S/cm²)
            hhparam[self.PID["E_Na"]]        = +50.0         # (mV)
            hhparam[self.PID["E_K"]]         = -100.0        # (mV)
            hhparam[self.PID["E_Ca"]]        = 0.0           # (mV)
            hhparam[self.PID["E_Leak"]]      = -70.0         # (mV)
            if not("nonoise" in nt):
                hhparam[self.PID["mu"]]      = 0.042         # 0.1
                hhparam[self.PID["theta"]]   = 8.0           # 8.0
                hhparam[self.PID["sigma"]]   = 0.09          # 0.12
            if not("nostim" in nt):
                hhparam[self.PID["i_stim"]]  = 0.03         # (mA/cm²)
            hhparam[self.PID["v_init"]]      = -70.0         # (mV)

        elif nt[0] == "somaIB":
            cmem                             = 1.0           # (µF/cm²)
            area_cm2                         = 96e-4*96e-4   # (cm²)
            hhparam[self.PID["G_Na"]]        = 0.05          # (S/cm²)
            hhparam[self.PID["G_Kd"]]        = 0.005         # (S/cm²)
            hhparam[self.PID["G_M"]]         = 3e-5          # (S/cm²)
            hhparam[self.PID["G_L"]]         = 1.0e-4        # (S/cm²)
            hhparam[self.PID["G_T"]]         = 0.0           # (S/cm²)
            hhparam[self.PID["G_Leak"]]      = 1e-5          # (S/cm²)
            hhparam[self.PID["E_Na"]]        = +50.0         # (mV)
            hhparam[self.PID["E_K"]]         = -90.0         # (mV)
            hhparam[self.PID["E_Ca"]]        = 120.0         # (mV)
            hhparam[self.PID["E_Leak"]]      = -70.0         # (mV)
            if not("nonoise" in nt):
                hhparam[self.PID["mu"]]      = 0.042         # 0.1
                hhparam[self.PID["theta"]]   = 8.0           # 8.0
                hhparam[self.PID["sigma"]]   = 0.09          # 0.12
            if not("nostim" in nt):
                hhparam[self.PID["i_stim"]]  = 0.03          # (mA/cm²)
            hhparam[self.PID["v_init"]]      = -70.0         # (mV)

        elif nt[0] == "somaLTS":
            cmem                             = 1.0           # (µF/cm²)
            area_cm2                         = 96e-4*96e-4   # (cm²)
            hhparam[self.PID["G_Na"]]        = 0.05          # (S/cm²)
            hhparam[self.PID["G_Kd"]]        = 0.005         # (S/cm²)
            hhparam[self.PID["G_M"]]         = 3e-5          # (S/cm²)
            hhparam[self.PID["G_L"]]         = 0.0           # (S/cm²)
            hhparam[self.PID["G_T"]]         = 4e-4          # (S/cm²)
            hhparam[self.PID["G_Leak"]]      = 1e-5          # (S/cm²)
            hhparam[self.PID["E_Na"]]        = +50.0         # (mV)
            hhparam[self.PID["E_K"]]         = -100.0        # (mV)
            hhparam[self.PID["E_Ca"]]        = 120.0         # (mV)
            hhparam[self.PID["E_Leak"]]      = -75.0         # (mV)
            if not("nonoise" in nt):
                hhparam[self.PID["mu"]]      = 0.042         # 0.1
                hhparam[self.PID["theta"]]   = 8.0           # 8.0
                hhparam[self.PID["sigma"]]   = 0.09          # 0.12
            if not("nostim" in nt):
                hhparam[self.PID["i_stim"]]  = 0.03         # (mA/cm²)
            hhparam[self.PID["v_init"]]      = -75.0         # (mV)
        
        elif nt[0] == "somaLTS":
            cmem                             = 1.0           # (µF/cm²)
            area_cm2                         = 96e-4*96e-4   # (cm²)
            hhparam[self.PID["G_Na"]]        = 0.05          # (S/cm²)
            hhparam[self.PID["G_Kd"]]        = 0.005         # (S/cm²)
            hhparam[self.PID["G_M"]]         = 3e-5          # (S/cm²)
            hhparam[self.PID["G_L"]]         = 0.0           # (S/cm²)
            hhparam[self.PID["G_T"]]         = 4e-4          # (S/cm²)
            hhparam[self.PID["G_Leak"]]      = 1e-5          # (S/cm²)
            hhparam[self.PID["E_Na"]]        = +50.0         # (mV)
            hhparam[self.PID["E_K"]]         = -100.0        # (mV)
            hhparam[self.PID["E_Ca"]]        = 120.0         # (mV)
            hhparam[self.PID["E_Leak"]]      = -75.0         # (mV)
            if not("nonoise" in nt):
                hhparam[self.PID["mu"]]      = 0.042         # 0.1
                hhparam[self.PID["theta"]]   = 8.0           # 8.0
                hhparam[self.PID["sigma"]]   = 0.09          # 0.12
            if not("nostim" in nt):
                hhparam[self.PID["i_stim"]]  = 0.03         # (mA/cm²)
            hhparam[self.PID["v_init"]]      = -75.0         # (mV)

        elif nt[0] == "MNE13axon":
            cmem                             = 1.0           # (µF/cm²)
            area_cm2                         = 96e-4*96e-4   # (cm²)
            hhparam[self.PID["G_Na"]]        = 0.0059        # (S/cm²)
            hhparam[self.PID["G_Kd"]]        = 0.002         # (S/cm²)
            hhparam[self.PID["G_M"]]         = 0.0           # (S/cm²)
            hhparam[self.PID["G_L"]]         = 0.0           # (S/cm²)
            hhparam[self.PID["G_T"]]         = 0.0           # (S/cm²)
            hhparam[self.PID["G_Leak"]]      = 1/30717       # (S/cm²)
            hhparam[self.PID["E_Na"]]        = +50.0         # (mV)
            hhparam[self.PID["E_K"]]         = -77.0         # (mV)
            hhparam[self.PID["E_Ca"]]        =  0.0          # (mV)
            hhparam[self.PID["E_Leak"]]      = -70.0         # (mV)
            if not("nonoise" in nt):
                hhparam[self.PID["mu"]]      = 0.0         # 0.1
                hhparam[self.PID["theta"]]   = 0.0           # 8.0
                hhparam[self.PID["sigma"]]   = 0.0          # 0.12
            if not("nostim" in nt):
                hhparam[self.PID["i_stim"]]  = 0.09730       # (mA/cm²)
            hhparam[self.PID["v_init"]]      = -65.0         # (mV)

        elif nt[0] == "MNE13axonactive":
            cmem                             = 1.0           # (µF/cm²)
            area_cm2                         = 96e-4*96e-4   # (cm²)
            hhparam[self.PID["G_Na"]]        = 0.0229        # (S/cm²)
            hhparam[self.PID["G_Kd"]]        = 0.048         # (S/cm²)
            hhparam[self.PID["G_M"]]         = 0.0           # (S/cm²)
            hhparam[self.PID["G_L"]]         = 0.0           # (S/cm²)
            hhparam[self.PID["G_T"]]         = 0.0           # (S/cm²)
            hhparam[self.PID["G_Leak"]]      = 1/30717       # (S/cm²)
            hhparam[self.PID["E_Na"]]        = +50.0         # (mV)
            hhparam[self.PID["E_K"]]         = -77.0         # (mV)
            hhparam[self.PID["E_Ca"]]        =  0.0          # (mV)
            hhparam[self.PID["E_Leak"]]      = -70.0         # (mV)
            if not("nonoise" in nt):
                hhparam[self.PID["mu"]]      = 0.0         # 0.1
                hhparam[self.PID["theta"]]   = 0.0           # 8.0
                hhparam[self.PID["sigma"]]   = 0.0          # 0.12
            if not("nostim" in nt):
                hhparam[self.PID["i_stim"]]  = 0.09730       # (mA/cm²)
            hhparam[self.PID["v_init"]]      = -65.0         # (mV)

        elif nt[0] == "MNE13others":
            cmem                             = 1.0           # (µF/cm²)
            area_cm2                         = 96e-4*96e-4   # (cm²)
            hhparam[self.PID["G_Na"]]        = 0.0           # (S/cm²)
            hhparam[self.PID["G_Kd"]]        = 0.002         # (S/cm²)
            hhparam[self.PID["G_M"]]         = 0.0           # (S/cm²)
            hhparam[self.PID["G_L"]]         = 0.0           # (S/cm²)
            hhparam[self.PID["G_T"]]         = 0.0           # (S/cm²)
            hhparam[self.PID["G_Leak"]]      = 1/30717       # (S/cm²)
            hhparam[self.PID["E_Na"]]        = +50.0         # (mV)
            hhparam[self.PID["E_K"]]         = -77.0         # (mV)
            hhparam[self.PID["E_Ca"]]        =  0.0          # (mV)
            hhparam[self.PID["E_Leak"]]      = -70.0         # (mV)
            if not("nonoise" in nt):
                hhparam[self.PID["mu"]]      = 0.0         # 0.1
                hhparam[self.PID["theta"]]   = 0.0           # 8.0
                hhparam[self.PID["sigma"]]   = 0.0          # 0.12
            if not("nostim" in nt):
                hhparam[self.PID["i_stim"]]  = 0.09730       # (mA/cm²)
            hhparam[self.PID["v_init"]]      = -65.0         # (mV)
        
        # Apply pre-mul of conductances/currents
        hhparam[self.PID["G_Na"]]        = hhparam[self.PID["G_Na"]]   * 0.5e3*(dt/cmem)
        hhparam[self.PID["G_Kd"]]        = hhparam[self.PID["G_Kd"]]   * 0.5e3*(dt/cmem)
        hhparam[self.PID["G_M"]]         = hhparam[self.PID["G_M"]]    * 0.5e3*(dt/cmem)
        hhparam[self.PID["G_L"]]         = hhparam[self.PID["G_L"]]    * 0.5e3*(dt/cmem)
        hhparam[self.PID["G_T"]]         = hhparam[self.PID["G_T"]]    * 0.5e3*(dt/cmem)
        hhparam[self.PID["G_Leak"]]      = hhparam[self.PID["G_Leak"]] * 0.5e3*(dt/cmem)
        hhparam[self.PID["i_stim"]]      = hhparam[self.PID["i_stim"]] * 0.5e3*(dt/cmem)
        hhparam[self.PID["noise_offs"]]  = hhparam[self.PID["mu"]]    * hhparam[self.PID["theta"]] * dt
        # hhparam[self.PID["pmul_sigma"]]  = hhparam[self.PID["sigma"]] * (2**-4)
        # hhparam[self.PID["pmul_sigma"]]  = hhparam[self.PID["sigma"]] * sqrt(2* dt * hhparam[self.PID["theta"]])
        hhparam[self.PID["pmul_sigma"]]  = hhparam[self.PID["sigma"]]
        hhparam[self.PID["pmul_theta"]]  = -hhparam[self.PID["theta"]]* dt

        # gsyn is nS so *1e-9 to get S, later divided by cm2 to get same units as gion
        # PMUL_GSYN_HW_FACTOR reduces pmul_gsyn in hw for fixed-point operations
        hhparam[self.PID["pmul_gsyn"]]   = SCALE_FACTOR*PMUL_GSYN_HW_FACTOR*1e-9 *0.5e3*(dt/cmem)

        return hhparam