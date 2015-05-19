# Python code used to aid in the estimation of GLMs
# Copyright (C) 2012  Chris Strickland

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#Helper classes for Probit model


import numpy as np
from pymcmc.mcmc import CFsampler
from pymcmc.regtools import LinearModel, CondRegressionSampler
#from condregconst import CondBetaScale1
from pymcmc.crandom import Crandom
from scipy import stats

class Probit:
    """Helper class for the probit model"""

    def __init__(self, yvec, xmat):
        self.yvec, self.xmat = yvec, xmat
        self.nobs, self.kreg = xmat.shape

        #Used in drawing truncated normal random variables
        self.crandom = Crandom()
        self.ystar = np.zeros(self.nobs)


    def setup_mcmc(self, **kwargs):

        data = {'yvec': self.yvec, 'xmat': self.xmat}
        if 'prior' in kwargs.keys():
            condbeta = CondRegressionSampler(self.yvec, self.xmat, prior = kwargs['prior'])
        else:
            condbeta = CondRegressionSampler(self.yvec, self.xmat)

        data['condbeta'] = condbeta
        bayesreg = LinearModel(self.yvec, self.xmat)
        sig, init_beta = bayesreg.posterior_mean()

        indb = self.yvec == 1
        inda = self. yvec == 0
        self.A = np.zeros(self.nobs)
        self.B = np.zeros(self.nobs)

        self.A[inda] = -10000
        self.B[inda] = 0.
        self.A[indb] = 0.
        self.B[indb] = 10000



        simystar = CFsampler(self.sampleystar,np.zeros(self.nobs),'ystar',store='none')
        simbeta = CFsampler(self.samplebeta, init_beta, 'beta')
        loglike = (self.logl, self.kreg,'yvec')
        blocks = [simystar, simbeta]
        return blocks, data
    
    def sampleystar(self,store):
        """function used to make a candidate draw for ystar"""
        xbeta = np.dot(store['xmat'],store['beta'])
        return self.truncnormc(xbeta)

    def samplebeta(self,store):
        store['condbeta'].update_yvec(store['ystar'])
        return store['condbeta'].sample(1.)


    def truncnormc(self, mu):
        a = self.A - mu
        b = self.B - mu
        self.crandom.randtnorm(a, b, self.ystar)
        return self.ystar + mu



    def logl(self,store):
        """function evaluates the log-likelihood for the log-linear model"""
        return self.loglike(np.dot(store['xmat'], store['beta']), store['beta'])
    
    def log_likelihood(self, xb, theta):
        """returns the log likelihood for the BCM model"""
        
        fbx=self.link(xb)
        return sum(self.yvec*np.log(fbx)+(1.-self.yvec)*np.log(1.0-fbx))

    def link(self,Xb):
        return stats.norm.cdf(Xb)
