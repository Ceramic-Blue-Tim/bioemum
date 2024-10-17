from os import SEEK_END
from neuron import h as nrn, vec2numpy
from neuron import gui
from matplotlib import pyplot as plt
import numpy

# Neuron units -----------------------------------------------------------
# Category 	                Variable 	    Units
# Time 	                    t 	            [ms]
# Voltage 	                v 	            [mV]
# Current 	                i 	            [mA/cm2] (distributed)
#                                           [nA] (point process)
# Concentration 	        ko, ki, etc. 	[mM]
# Specific capacitance 	    cm 	            [uf/cm2]
# Length 	                diam, L 	    [um]
# Conductance 	            g 	            [S/cm2] (distributed)
#                                           [uS] (point process)
# Cytoplasmic resistivity 	Ra 	            [ohm cm]
# Resistance 	            Ri( ) 	        [Mohm]
# -------------------------------------------------------------------------

def mhh_sim():
    # ### Stimulation ###################################################################
    SAVE_PATH = '../data/'                   # Data relative save path

    nrn.load_file('./mhh_sim_neuron.hoc')     # Load Motor neuron model

    steps_ms            = 32 # dt=2^-6
    dt                  = 1/steps_ms
    t_1ms               = dt*steps_ms

    nrn.steps_per_ms    = steps_ms
    nrn.tstop           = 100*t_1ms          # Simulation time

    # stim                = nrn.IClamp(nrn.somaFS(0))
    # stim.delay          = 0*t_1ms       # ms
    # stim.dur            = 10*t_1ms      # ms
    # stim.amp            = 0.09730       # nA
    # ####################################################################################

    # Init structures --------------------------------------------------------------------------------------------------
    nrn_vects   = []
    nrn_saves   = []
    nrnref      = []

    # Handling ----------------------------------------------------------------------------------------------------------
    ## Labels
    h_names     = ['v', 'icap']         # Name of output dat file
    h_nrnref    = ['v', 'i_cap']        # Name of reference in neuron
    h_sec       = ['somaFS', 'somaFS']                                                  # Name of sections
    h_nodes     = ['0.001', '0.99']                                                      # Index of nodes
    nb_sec      = len(h_sec)
    nb_var      = len(h_names)

    # Set records and output files -----------------------------------------------------------------------------------------
    ## Time stamp
    t_vec   = nrn.Vector()
    t_iax   = nrn.Vector()
    t_save  = nrn.File()

    t_save.wopen(SAVE_PATH+'t.dat')
    t_vec.record(nrn._ref_t)

    ## Variables
    for j in range(nb_sec):
        for i in range(nb_var):
            nrn_vects.append(nrn.Vector())
            nrn_saves.append(nrn.File())
            nrn_saves[i+j*nb_var].wopen(SAVE_PATH+h_sec[j]+'_'+h_names[i]+'.dat')
            exec('nrn_vects[%d].record(nrn.%s(%s)._ref_%s)'%(i+j*nb_var, h_sec[j], h_nodes[j], h_nrnref[i])) # dirty work around but yet working

    # Neuron simulation #########################################################################################
    ## Run neuron simulation
    nrn.run()

    ## Print topology
    print('\nTopology\n')
    nrn.topology()

    ## Print segments
    # for seg in nrn.somaC1.allseg():
    #     print(' x: {}\n ri: {}\n ri_half: {}\n'.format(seg.x, seg.ri(),
    #             0.01 * nrn.somaC1.Ra * nrn.somaC1.L / 2 / nrn.somaC1.nseg / (nrn.PI * (seg.diam / 2) ** 2)))
    # for seg in nrn.somaC2.allseg():
    #     print(' x: {}\n ri: {}\n ri_half: {}\n'.format(seg.x, seg.ri(),
    #             0.01 * nrn.somaC2.Ra * nrn.somaC2.L / 2 / nrn.somaC2.nseg / (nrn.PI * (seg.diam / 2) ** 2)))
    # for seg in nrn.somaC3.allseg():
    #     print(' x: {}\n ri: {}\n ri_half: {}\n'.format(seg.x, seg.ri(),
    #             0.01 * nrn.somaC3.Ra * nrn.somaC3.L / 2 / nrn.somaC3.nseg / (nrn.PI * (seg.diam / 2) ** 2)))
    
    # Generate connection for arbor
    r_diag  = []
    n_area  = []
    ncnt = 0
    for seg in nrn.somaFS.allseg():
        print('{}: ri={} area: {}'.format(ncnt, seg.ri(), seg.area()))
        r_diag.append(seg.ri())
        n_area.append(seg.area())
        ncnt +=1

    for i in range(len(r_diag)):
        print('r_diag[{}] = '.format(i) + str(r_diag[i]))

    for i in range(len(r_diag)):
        print('n_area[{}] = '.format(i) + str(n_area[i]))
    return[t_vec, nrn_vects]
