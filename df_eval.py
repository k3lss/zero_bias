'''
Script to evaluate the density field of DM at the position of each halo.
'''

import numpy as np
import MAS_library as MASL
import smoothing_library as SL
import pandas as pd

def get_density(sample,matter,Lbox=1000.,Ngrid=512.,R_soft=8.,MAS='CIC',threads=8,Filter='Gaussian'):

    '''
    Function to compute the density field at the position of each halo
    
    sample: array containing the position of halos
    matter: array containing the density field
    Lbox: size of the simulation
    Ngrid: simulation grid
    R_soft: radius of smoothing
    '''

    pos = np.array(sample[['X','Y','Z']],dtype=np.float32) 
    rho_mean = np.mean(matter)
    print(rho_mean)
    delta = matter/rho_mean - 1
    
    W_k = np.zeros((Ngrid,Ngrid,Ngrid),dtype=np.complex64)      # filter for the smoothing
    W_k = SL.FT_filter(Lbox,R_soft,Ngrid,Filter,threads)
    
    delta_smooth = SL.field_smoothing(delta,W_k,threads)    
    Npart = len(pos)
    delta_env = np.zeros(Npart,dtype=np.float32)
    MASL.CIC_interp(delta_smooth,Lbox,pos,delta_env)    
    MASL.CIC_interp(delta,Lbox,pos,delta_env)
    return delta_env


data = pd.read_hdf('/path/to/snapshot.h5', key='rockstar_catalog')
matter = np.load('/path/to/density_mesh.npy')       # For this, the density field has been previously stored as a mesh in an array
sample = data[['X', 'Y', 'Z']]
d_field = get_density(sample, matter, Ngrid =512, R_soft=8.)
np.savetxt('/path/to/save/df_eval.txt', d_field, delimiter=" ")