
# Python code used for the estimation of Tobit model
# Copyright (C) 2014  Chris Strickland

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

import numpy as np
from pymcmc.mcmc import MCMC, CFsampler
from pymcmc.crandom import Crandom
from pymcmc.regtools import LinearModel

class Tobit:
    """Class helps simulated latent variable for Tobit model.
    
    arguments:
        yvec - Is a (n x 1) vector of observations.
        xmat - Is an (n x k) vector of regressors

        nit - An integer that specifies how many iterations to run the
              MCMC scheme for. The default number of iterations is 15000.

        burn - The number of observations from the MCMC sampler that
               should be discarded when doin an MCMC analysis. The default
               number of iterations is 5000. This probably should
               not be reduced.
    """

    def __init__(self, yvec, xmat, nit = 15000, burn = 5000, **kwargs):
        self.yvec = yvec
        self.ystar = yvec.copy()
        self.index = yvec == 0.
        self.num_zero = self.index.sum()
        assert self.num_zero > 0
        self.xmat = xmat[self.index,:]
        self.temp_ystar = np.zeros(self.num_zero)
        if 'prior' in kwargs:
            self.lm = LinearModel(yvec, xmat, prior = kwargs['prior'])
        else:
            self.lm = LinearModel(yvec, xmat)

        self.nit = nit
        self.burn = burn
        self.crandom = Crandom()
        self.LB = np.ones(self.num_zero) * - 1E5

        #blocks for MCMC algorithm
        blocks = []

        #sample ystar
        blocks.append(CFsampler(self.sample_ystar, self.ystar, 'ystar'))

        #sample sigma, beta
        init_sig, init_beta = self.lm.posterior_mean()
        blocks.append(CFsampler(self.sample_sigma_beta,
                                [init_sig, init_beta],
                                ['sigma', 'beta']))

        self.mcmc = MCMC(self.nit, self.burn, {}, blocks,
                         runtime_output = True)

        #An indicator that is True is self.mcmc.sampler() has
        #been called
        self.compute_ind = False

    def output(self):
        """Produces some standard output for the Tobit model.
        """

        if self.compute_ind == False:
            self.mcmc.sampler()
            self.compute_ind = True

        self.mcmc.output(parameters = ['sigma', 'beta'])

    def get_mean_var(self):

        """Returns the posterior mean and 
        posterior variance for sigma, beta."""

        if self.compute_ind == False:
            self.mcmc.sampler()
            self.compute_ind = True

        sigma =  self.mcmc.get_mean_var('sigma')
        beta =  self.mcmc.get_mean_var('beta')

        return sigma, beta

    def get_mean_cov(self):
        """Returns the posterior mean and joint
        posterior covariance for sigma and beta."""

        if self.compute_ind == False:
            self.mcmc.sampler()
            self.compute_ind = True

        return self.mcmc.get_mean_cov(['sigma', 'beta'])


    def sample_ystar(self, store):
        """Function samples augmented data set."""

        mu = np.dot(self.xmat, store['beta'])
        
        self.crandom.randtnorm(self.LB, -mu / store['sigma'],
                   self.temp_ystar)

        self.ystar[self.index] = mu + store['sigma'] * self.temp_ystar

        return self.ystar

                               

    def sample_sigma_beta(self, store):
        """Function samples sigma and beta from linear model."""

        self.lm.update_yvec(self.ystar)
        return self.lm.sample()

