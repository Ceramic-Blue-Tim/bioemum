# -*- coding: utf-8 -*-
# @title      Geometrical parameters
# @file       Geoparam.py
# @author     Romain Beaubois
# @date       06 Oct 2023
# @copyright
# SPDX-FileCopyrightText: © 2023 Romain Beaubois <refbeaubois@yahoo.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# @brief Class to generates HH neuron parameters
# 
# @details 
# > **06 Oct 2023** : file creation (RB)

class Geoparam:
    def __init__(self):
        """Initialize"""

        self.GID = { 
            "D_const":  0, 
            "nrn_area": 1, 
            "U":        2,
            "ptree":    3
        }
        self.NB_GEOPARAM = len(self.GID)

        pass

    def getNb(self):
        """Get number of parameters"""
        return self.NB_GEOPARAM
    
    def getDict(self):
        """Get dictionnary to handle parameters"""
        return self.GID

    def getParameters(self, nrn_type:str, dt):
        """Get HH parameters for a given neuron type

        :param str nrn_type: type of neuron ("FS","RS",...)
        :param dt float: time step in ms
        :returns: list of parameters, mebrane capacity and area
        """
        hhparam = [0.0]*self.NB_GEOPARAM
        nt = nrn_type.split('_')

        if nt[0] == "three_sec":
            cmem                            = 1.0           # (µF/cm²)
            area_cm2                        = 67e-4*67e-4   # (cm²)
            hhparam[self.PID["D_const"]]    = 0.05          # (S/cm²)
            hhparam[self.PID["nrn_area"]]   = 0.01          # (S/cm²)
            hhparam[self.PID["U"]]          = 0.0           # (S/cm²)
            hhparam[self.PID["ptree"]]      = 0.0           # (S/cm²)

        # hhparam[self.PID["pmul_sigma"]]  = hhparam[self.PID["sigma"]] * sqrt(2* dt * hhparam[self.PID["theta"]])
        hhparam[self.PID["pmul_sigma"]]  = hhparam[self.PID["sigma"]]
        hhparam[self.PID["pmul_theta"]]  = -hhparam[self.PID["theta"]]* dt

        return hhparam