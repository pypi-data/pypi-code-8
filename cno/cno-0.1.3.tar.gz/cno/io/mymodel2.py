import pymc
import numpy as np
from cno import cnorbool, cnodata


n = 5*np.ones(4,dtype=int)
x = np.array([-.86,-.3,-.05,.73])



params = {}
for i in range(0,16):
    key = 'X' + str(i+1)
    params[key] = pymc.DiscreteUniform(key, lower=0, upper=1)

c  = cnorbool.CNORbool(cnodata("PKN-ToyMMB.sif"), cnodata("MD-ToyMMB.csv"))


@pymc.deterministic
def obj(**params):
    """theta = logit^{-1}(a+b)"""

    return c.simulate(np.array([X1, X2, X3, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1]))
    #return pymc.invlogit(a+b*x)




"""
import pymc
import mymodel


S = pymc.MCMC(mymodel, db = 'pickle')
S.sample(iter = 10000, burn = 5000, thin = 2)
pymc.Matplot.plot(S)
"""
