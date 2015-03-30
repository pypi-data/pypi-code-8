'''
Copyright 2015 by Tobias Houska
This file is part of Statistical Parameter Estimation Tool (SPOTPY).

:author: Tobias Houska

This example implements the Ackley function into SPOT.  
'''

import numpy as np
import spotpy

class spot_setup(object):
    def __init__(self):
        self.dim=30
        
    def parameters(self):
        pars = []   #distribution of random value      #name  #stepsize# optguess
        for i in range(self.dim):        
            pars.append((np.random.uniform(low=-32.768,high=32.768),  str(i),   5.5,  -20.0))        
        dtype=np.dtype([('random', '<f8'), ('name', '|S30'),('step', '<f8'),('optguess', '<f8')])
        return np.array(pars,dtype=dtype)
                
  
    def simulation(self, vector):
        firstSum = 0.0
        secondSum = 0.0
        for c in vector:
            firstSum += c**2.0
            secondSum += np.cos(2.0*np.pi*c)
            n = float(len(vector))
        return [-20.0*np.exp(-0.2*np.sqrt(firstSum/n)) - np.exp(secondSum/n) + 20 + np.e   ]
     
     
     
    def evaluation(self):
        observations=[0]
        return observations
    
    def likelihood(self,simulation,evaluation):
        likelihood= -spotpy.likelihoods.rmse(simulation,evaluation)
        return likelihood