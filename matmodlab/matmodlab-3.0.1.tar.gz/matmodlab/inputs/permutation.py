#!/usr/bin/env mmd
from matmodlab import *

def func(x, xnames, d, runid, *args):

    mps = MaterialPointSimulator(runid)
    mps.StrainStep(components=(1, 0, 0), increment=1., scale=-.5, frames=10)
    mps.StrainStep(components=(2, 0, 0), increment=1., scale=-.5, frames=10)
    mps.StrainStep(components=(1, 0, 0), increment=1., scale=-.5, frames=10)
    mps.StrainStep(components=(0, 0, 0), increment=1., scale=-.5, frames=10)

    # set up the material
    parameters = dict(zip(xnames, x))
    mps.Material('elastic', parameters)

    # set up and run the model
    mps.run()

    s = mps.get('STRESS_XX')
    return np.amax(s)

def runner():
    N = 15
    K = PermutateVariable('K', 125e9, method='weibull', b=14, N=N)
    G = PermutateVariable('G', 45e9, method='percentage', b=10, N=N)
    xinit = [K, G]
    permutator = Permutator('permutation', func, xinit, method='zip',
                            descriptors=['MAX_PRES'], correlations=True)
    permutator.run()

runner()
