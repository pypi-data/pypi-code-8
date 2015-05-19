# A Bayesian regression module for PyMCMC. PyMCMC is a Python package for
# Bayesian analysis.
# Copyright (C) 2010  Chris Strickland

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

import types
import os
from os import sys
import numpy as np
from scipy import special
import stochsearch
try:
    import matplotlib.pyplot as plt
    FLAG_PLOT = True
    #able to import matplotlib
except:
    FLAG_PLOT = False
    #unable to import matplotlib

import scipy.stats.distributions as dstn
import reg_helper
from pymcmc.mcmc import MCMC, CFsampler
from pymcmc.sim_distributions import SampleWishart
import wishart
import pdb



class StochasticSearch:
    """
    StochasticSearch is a class that is used in conjunction with regression classes for 
    variable selection in regression.
    
    arguments:
        yvec - (nobs x 1) vector of observations.
        xmat - (nobs x kreg) matrix of regressors.
        prior - list or tuple that defines prior used
                in stochastic search algorithm.
    """


    def __init__(self, yvec, xmat, prior, **kwargs):
        #The number of observations
        self.nobs = yvec.shape[0]
        try:
            assert xmat.ndim == 2
        except:
            raise Exception("xmat must have two dimensions")

        self.kreg = xmat.shape[1]
        try:
            assert self.kreg > 1
        except:
            raise ValueError("The number of regressors must be > 1")

        self.yvec = yvec #Observed variable
        self.xmat = xmat #Regressors

        #calculate quantities used in regression analysis
        self.ypy = np.dot(yvec.T, yvec)
        self.xpy = np.dot(xmat.T, yvec)
        self.xpx = np.asfortranarray(np.dot(xmat.T, xmat))

        #Workspace used in stochastic search algorithms
        self.xgxg = np.zeros((self.kreg, self.kreg), order = 'F' )
        self.work2 = np.zeros((self.kreg, self.kreg), order = 'F' )
        self.xgy = np.zeros(self.kreg)

        #gam is used to store indicator variables for regression analysis
        self.gam = np.zeros(self.kreg, dtype = 'i')
        self.gam[0] = 1 #initialise so first regressors (assumed constant) is included

        #Workspace for stochastic search algorithm
        self.ru = np.zeros(self.kreg)
        self.rn = np.zeros(self.kreg)
        self.work = np.zeros((self.kreg, 6), order = 'F')

        #flag variables used in stochastic search algoriths
        self.ifo = np.array(0, dtype = 'i')
        self.ifo2 = np.array(0, dtype = 'i')

        #Assert that prior is of type tuple or list
        try:
            assert type(prior) in [type(()), type([])]
        except:
            error = "prior must be a list or a tuple"
            raise TypeError(error)

        #Include first regressor in stochastic search
        #default - first regressors is not included

        if 'initial' in kwargs and kwargs['initial'] == True:
            self.ini = 1
        else:
            self.ini = 2


        #Define workspace for each prior
        if prior[0] == 'g_prior':
            #g-prior, spike slab
            self.work[:, 0] = prior[1]
            
            self.g = prior[2]
            self.__samplegam = self.__sim_gamma_gprior
            self.prior_type = 'g_prior'

        elif prior[0] == 'normal_inverted_gamma':
            #Normal inverted gamma prior, not spike spab
            self.nu = prior[1] #prior degrees of freedom
            self.nuo = self.nu + self.nobs #posterior degrees of freedom
            self.nus = prior[2] #scale parameter
            self.R = np.asfortranarray(prior[3]) #correlation matrix
            self.D = np.asfortranarray(prior[4]) #Diagonal scale matrix

            #compute the log determinant of R
            self.logdetR = 2.0 * np.sum(np.diag(np.linalg.cholesky(self.R)))

            #computation and storage for posterior
            self.vxy = self.xgy
            self.vobar = self.xgxg
            self.vubar = self.work2
            self.nuobar = self.nu + self.nobs

            #pointers to functions used for this prior
            self.__samplegam = self.__sim_gamma_nig
            self.__samplegam_cond_beta = self.__sim_gamma_nig_cond_beta
            self.prior_type = 'normal_inverted_gamma'

        elif prior[0] == 'normal_inverted_gamma_spike_slab':
            #normal inverted gamma spike slab prior
            self.nu = prior[1] #prior degrees of freedom
            self.nuo = self.nu + self.nobs #posterior degrees of freedom

            #scale parameter for inverted gamma distribution
            self.nus = prior[2]

            #prior mean
            self.bubar = prior[3]

            #prior precision
            self.vubar = np.asfortranarray(prior[4])
            self.vubarg = np.zeros((self.kreg, self.kreg), order = 'F')

            #vbubar = vubar * bubar 
            self.vbubar = np.dot(self.vubar, self.bubar)

            #posterior precision
            self.vobar = np.asfortranarray(self.xpx + self.vubar)

            #Allocate memory used in algorithm
            #Use memory stored for self.vobarg (relabel)
            self.vobarg = self.xgxg

            #vbobar = vobar * bobar
            self.vbobar = self.xpy.copy()

            #Re-label memory stored
            self.vbobarg = self.xgy

            #work array posterior mean
            self.bobarg = np.zeros(self.kreg)

            self.prior_type = 'normal_inverted_gamma_spike_slab'
            self.__samplegam = self.__sim_gamma_nig_spsl


        else:
            raise NameError("prior incorrectly specified")

        # internal storage for stochastic search
        self.store = [[], []]

    def update_prior(self, prior):
        """Updates priors."""

        if prior[0] == 'g_prior':
            #update spike slab gprior
            self.work[:, 0] = prior[1]
            self.g = prior[2]
            self.__samplegam = self.__sim_gamma_gprior

        elif prior[0] == 'normal_inverted_gamma':
            #Update normal inverted gamma prior
            self.nu = prior[1] #prior degrees of freedom
            self.nuo = self.nu + self.nobs #posterior degrees of freedom
            self.nus = prior[2] #scale parameter

            #correlation matrix
            self.R = np.asfortranarray(prior[3])

            #diagonal scale matrix
            self.D = np.asfortranarray(prior[4])

            #compute log determinant
            self.logdetR = 2.0 * np.sum(np.diag(np.linalg.cholesky(self.R)))

        elif prior[0] == 'normal_inverted_gamma_spike_slab':
            #normal inverted gamma spike slab prior

            self.nu = prior[1] #prior degrees of freedom

            self.nuo = self.nu + self.nobs #posterior degrees of freedom

            #scale parameter for inverted gamma distribution
            self.nus = prior[2]

            #prior precision
            self.vubar = np.asfortranarray(prior[3])

            #posterior precision
            self.vobar = np.asfortranarray(self.xpx + self.vubar)



    def __sim_gamma_gprior(self, *args):

        assert len(args) == 0

        stochsearch.ssreg(self.ini, self.ypy, self.g, self.xpx, self.xpy,
              self.xgxg, self.xgy, self.gam, \
              self.ru, self.work, self.work2,
              self.ifo, self.ifo2, self.nobs)

    def __sim_gamma_nig(self, *args):
        
        assert len(args) == 0
        self.initialise_vubar()
        stochsearch.ssreg_nig(self.ini, self.ypy, self.logdetR, self.nus, self.vxy, self.vobar,
                 self.vubar, self.gam, self.xpx, self.xpy, self.D,
                 self.R, self.nuobar, self.ru)


    def __sim_gamma_nig_cond_beta(self, sig, beta):
        """samples gamma conditional on beta."""
        self.initialise_vubar()
        stochsearch.ssregcbeta_nig(self.ini, beta, sig, self.vxy, self.logdetR, self.vubar,
                       self.gam, self.D, self.R, self.ru)

    def __sim_gamma_nig_spsl(self, *args):
        """Samples gamma based on spike slab prior."""
        if len(args) == 1:
            sig = args[0]
            self.vobar = self.vubar + self.xpx / sig ** 2
            self.vbobar = self.vbubar + self.xpy / sig ** 2
            ypy = 0.0 #goes into constant of proportionality
            fl = 0
        else:
            assert len(args) == 0
            ypy = self.ypy
            fl = 1

        stochsearch.ssreg_sl(self.ini, self.vobarg, self.vobar, self.gam, self.vbobar,
                             self.vbobarg, self.vubar, self.vubarg, self.vbubar,
                             self.bubar, ypy, self.nus, self.bobarg, self.nuo,
                             self.ru, fl)
        
        

    def initialise_vubar(self):
        """Initialise vubar for the case of the normal inverted gamma prior."""
        stochsearch.initialise_vubar(self.vubar, self.gam, self.D, self.R)

    def sample_gamma(self, store, *args):
        """Function samples gamma from posterior distribution."""
        it = store['iteration']
        burn = store['length_of_burnin']
        # self.gam = gamvec.astype('i')
        self.ru = np.random.rand(self.kreg)
        
        self.__samplegam(*args)
        if it >= burn:
            self.update_store()
        return self.gam

    def sample_gamma_cond_beta(self, store, sig, beta):
        """Function samples beta from posterior distribution conditional on
        sigma and beta."""

        it = store['iteration']
        burn = store['length_of_burnin']
        self.ru = np.random.rand(self.kreg)
        self.__samplegam_cond_beta(sig, beta)
        if it >= burn:
            self.update_store()
        return self.gam

    def update_xmat(self, xmat):
        """Function used to update class value for xmat."""

        self.xmat = xmat
        self.xpy = np.dot(xmat.T, self.yvec)
        self.xpx = np.asfortranarray(np.dot(xmat.T, xmat))

        if self.prior_type == 'normal_inverted_gamma_spike_slab':
            #posterior precision
            self.vobar = np.asfortranarray(self.xpx + self.vubar)

            #compute posterior mean
            self.bobar = np.linalg.solve(self.vobar, self.vobar)
            self.bobarg = np.zeros(self.kreg)

    def update_yvec(self, yvec):
        """Function updates class value for yvec."""
        self.yvec = yvec
        self.ypy = np.dot(yvec.T, yvec)
        self.xpy = np.dot(self.xmat.T, yvec)

        if self.prior_type == 'normal_inverted_gamma_spike_slab':
            #vbobar = vobar * bobar
            self.vbobar = self.xpy.copy()

            #compute posterior mean
            self.bobar = np.linalg.solve(self.vobar, self.vobar)
            self.bobarg = np.zeros(self.kreg)

    def update_store(self):
        """function updates internal storage for gamma"""
        gammai = int("".join([str(i) for i in self.gam]))
        if gammai in self.store[0]:
            index = self.store[0].index(gammai)
            self.store[1][index] = self.store[1][index] + 1
        else:
            self.store[0].append(gammai)
            self.store[1].append(1)

    def included_regressors(self, rank):
        """
        list of the rank^th most probable
        model, with rank = 0 indicating the most
        probable.
        Returns a list with each element the
        position of the included regressor,
        e.g.,
          [0,12] means the chosen model includes
          regressors 0 (the intercept) and regressor 12
        """
        arrind = np.array(self.store[1])
        ind = np.argsort(arrind)[::-1]
        modstr = str(self.store[0][ind[rank]])
        included = []
        for i,value in enumerate(modstr):
            if value == '1':
                included.append(i)
        return included
      
    def extract_regressors(self, model_number):
        """returns a design matrix containing just the regressors
        correponding to the specified model_number
        """
        includedregressors = self.included_regressors(model_number)
        tmpxmat = self.xmat[:, includedregressors]
        return tmpxmat

    def extract_prior(self, model_number):
        includedregressors = self.included_regressors(model_number)
        if self.prior_type == 'g_prior':
            prior = ['g_prior', self.work[includedregressors, 0], self.g]

        else:
            assert self.prior_type == 'normal_inverted_gamma'
            index = set(np.arange(self.kreg)) & set(includedregressors)
            D = self.D[:, index]
            DRD = D ** 2 * self.R

            prior = ['normal_inverted_gamma', self.nu, self.nus,
                     np.zeros(self.kreg), np.diag(DRD)]
        return prior




        
    def output(self, destination):
        """
        produce additional output for StochasticSearch
        This is an example of a custom output. The requirement
        is it needs to have a destination which is handled by
        the generic output function.

        """
        
        colwidth = 12
        sigfigs = 7
        arrind = np.array(self.store[1])
        ind = np.argsort(arrind)[::-1]
        total = sum(arrind)
        hline = "-".ljust(5 * colwidth, '-')
        print >>destination
        print >>destination,\
        "Most likely models ordered by decreasing posterior probability"
        print >>destination
        print >>destination, hline        
        print >>destination, """\
{0: <{colwidth}s}| \
{1: <{colwidth}s}""".format("probability", "model", colwidth = colwidth)
        print >>destination, hline
        for i in xrange(min(10, ind.shape[0])):
            incregressors = self.included_regressors(i)
            modstr = ', '.join([str(ireg) for ireg in incregressors])
            print >>destination, """\
{1: <{colwidth}.{sigfigs}g}| \
{0: <{colwidth}s}""".format(modstr,
                float(self.store[1][ind[i]])/total,
                colwidth = colwidth,
                sigfigs = sigfigs)
        print >>destination, hline


class LinearModelBase:
    """
    LinearModelBase is a class used for Bayesian regression. By default this class uses
    Jeffrey's prior. Arguments:

        yvec - Is a one dimensional numpy array containing the dependent
               variable.
        xmat - Is a two dimensional numpy array conting the regressors.
        kwargs - Optional arguments:
            prior - a list containing the name of the prior and the
               corresponding hyperparameters. Examples: 
               prior = ['normal_gamma', nuubar, Subar, betaubar, Vubar]
               prior = ['normal_inverted_gamma', nuubar, Subar, betaubar, Vubar]

               prior = ['g_prior', betaubar, g].
               If none of these options are chosen or they are
               miss - specified then LinearModel will default to
               Jeffreys prior.
        
    """
    def __init__(self, yvec, xmat, **kwargs):
        self.nobs = yvec.shape[0]
        self.yvec = yvec
        if xmat.ndim == 1:
            self.xmat = xmat.reshape(self.nobs, 1)
        else:
            self.xmat = xmat
        self.xpx = np.dot(self.xmat.T, self.xmat)
        self.xpy = np.dot(self.xmat.T, yvec)
        self.kreg = self.xmat.shape[1]
        self.vobar = np.zeros((self.kreg, self.kreg))
        self.betaobar = np.zeros(self.kreg)
        self.updateind_xmat = 0
        self.updateind_yvec = 0
        self.calculated = False
        self.nuobar = 0.0
        self.sobar = 0.0
        self.vbobar = np.zeros(self.kreg)
        self.cholvobar = np.zeros((self.kreg, self.kreg))
        if 'prior' not in kwargs:
            # default: Jeffreys prior
            self.res = np.zeros(self.nobs)
            self.__calculate = self.__calculate_jeffreys
            self.__sample_scale = self.__sample_standard_deviation
            self.__log_cand_prob = self.__log_cand_pr_sig_jeff
            self.prior = ['Jeffreys']
            self.__posterior_variance_scale = self.__posterior_sigma_var
            self.__posterior_mean_scale = self.__posterior_sigma_mean
            self.__log_marginal_likelihood = self.__log_marginal_likelihood_jeff
        else:                   # Normal - gamma prior
            self.prior = kwargs['prior']
            if type(self.prior[0])!= types.StringType:
                print "Warning: Jefferys prior used as prior was \
                    incorectly specified"
                self.res = np.zeros(self.nobs)
                self.__calculate = self.__calculate_jeffreys
                self.__sample_scale = self.__sample_standard_deviation
                self.__log_cand_prob = self.__log_cand_pr_sig
                self.__posterior_variance_scale = self.__posterior_sigma_var
                self.__posterior_mean_scale = self.__posterior_sigma_mean
                self.__log_marginal_likelihood = self.__log_marginal_likelihood_jeff
            else:
                ptype = self.prior[0]
                if ptype not in ['normal_gamma', 'normal_inverted_gamma',
                                 'g_prior']:
                    print "Warning: Jeffery's prior used as prior was \
incorectly specified"
                    self.res = np.zeros(self.nobs)
                    self.__sample_scale = self.__sample_standard_deviation
                    self.__calculate = self.__calculate_jeffreys
                    self.__log_cand_prob = self.__log_cand_pr_sig
                    self.__posterior_variance_scale = \
                                               self.__posterior_sigma_var
                    self.__posterior_mean_scale = \
                                              self.__posterior_sigma_mean
                    self.__log_marginal_likelihood = self.__log_marginal_likelihood_jeff
                else:
                    self.vbubar = np.zeros(self.kreg)
                    if ptype =='normal_gamma':
                        self.__calculate = self.__calculate_normal_gamma
                        self.__sample_scale = self.__sample_precision
                        self.__log_cand_prob = self.__log_cand_pr_kappa
                        self.__posterior_variance_scale = \
                                               self.__posterior_kappa_var
                        self.__posterior_mean_scale = \
                                              self.__posterior_kappa_mean
                        self.__log_marginal_likelihood = \
                                self.__log_marginal_likelihood_nig
                        self.nuubar = self.prior[1]
                        self.subar = self.prior[2]
                        self.betaubar = self.prior[3]
                        self.vubar = np.atleast_2d(self.prior[4])
                        self.lndetvubar = 2.0 * \
                        np.sum(np.log(np.diag(np.linalg.cholesky(self.vubar))))

                    elif ptype =='normal_inverted_gamma':
                        self.__calculate = self.__calculate_normal_gamma
                        self.__sample_scale = \
                                         self.__sample_standard_deviation
                        self.__log_cand_prob = self.__log_cand_pr_sig
                        self.__posterior_variance_scale = \
                                               self.__posterior_sigma_var
                        self.__posterior_mean_scale = \
                                               self.__posterior_sigma_mean
                        self.nuubar = self.prior[1]
                        self.subar = self.prior[2]
                        self.betaubar = self.prior[3]
                        self.vubar = np.atleast_2d(self.prior[4])
                        self.lndetvubar = 2.0 * \
                        np.sum(np.log(np.diag(np.linalg.cholesky(self.vubar))))
                        self.__log_marginal_likelihood = \
                                 self.__log_marginal_likelihood_nig
                        
                    else:
                        # g - prior
                        self.betaubar = self.prior[1]
                        self.g = self.prior[2]
                        self.betahat = np.zeros(self.kreg)
                        self.betadiff = np.zeros(self.kreg)
                        self.res = np.zeros(self.nobs)
                        assert(type(self.g) == types.FloatType)
                        self.gratio = self.g/(self.g + 1.)
                        self.__sample_scale = \
                                        self.__sample_standard_deviation
                        self.__calculate = self.__calculate_g_prior
                        self.__log_cand_prob = self.__log_canc_pr_sig_gprior
                        self.__posterior_variance_scale = \
                                               self.__posterior_sigma_var
                        self.__posterior_mean_scale = \
                                             self.__posterior_sigma_mean
                        self.__log_marginal_likelihood = self.__log_marginal_likelihood_gprior
                        self.vubar = self.xpx / self.g
                        self.lndetvubar = 2.0 * \
                        np.sum(np.log(np.diag(np.linalg.cholesky(self.vubar))))

    def update_prior(self, prior):
        """Updates prior. The specification of the prior must not change.

        arguments:
            prior - a list containing the name of the prior and the
               corresponding hyperparameters. Examples: 
               prior = ['normal_gamma', nuubar, Subar, betaubar, Vubar]
               prior = ['normal_inverted_gamma', nuubar, Subar, betaubar, Vubar]

               prior = ['g_prior', betaubar, g].
               If none of these options are chosen or they are
               miss - specified then LinearModel will default to
               Jeffreys prior.
        """

        if prior[0] == 'normal_inverted_gamma' or prior[0] == 'normal_gamma':
            self.nuubar = self.prior[1]
            self.subar = self.prior[2]
            self.betaubar = self.prior[3]
            self.vubar = self.prior[4]
            self.lndetvubar = 2.0 * \
            np.sum(np.log(np.diag(np.linalg.cholesky(self.vubar))))

        elif prior[0] == 'g_prior':
            self.vubar = self.xpx / self.g
            self.lndetvubar = 2.0 * \
            np.sum(np.log(np.diag(np.linalg.cholesky(self.vubar))))


    def log_posterior_probability(self, scale, beta, **kwargs):
        """Returns the log posterior probability.

        arguments:
            scale - scale parameter
            beta - regression coefficients

        """

        return self.__log_cand_prob(scale, beta, **kwargs)

    def __calculate_jeffreys(self):
        self.calculated = True
        if  self.updateind_xmat == 1 or self.updateind_yvec == 1:
            self.xpy = np.dot(self.xmat.transpose(), self.yvec)
            if self.updateind_xmat == 1: 
                self.xpx = np.dot(self.xmat.transpose(), self.xmat)
            self.updateind_xmat = 0
            self.updateind_yvec = 0

        self.betaobar = np.linalg.solve(self.xpx, self.xpy)
        self.vobar = self.xpx

        self.nuobar = self.nobs - self.kreg
        self.res = self.yvec - np.dot(self.xmat, self.betaobar)
        self.sobar = np.dot(self.res, self.res)

    def __calculate_normal_gamma(self):
        self.calculated = True
        self.vbubar = np.dot(self.vubar, self.betaubar)
        if  self.updateind_xmat == 1 or self.updateind_yvec == 1:
            self.xpy = np.dot(self.xmat.transpose(), self.yvec)
            if self.updateind_xmat == 1: 
                self.xpx = np.dot(self.xmat.transpose(), self.xmat)
            self.updateind_xmat = 0
            self.updateind_yvec = 0
        self.vobar = self.vubar + self.xpx
        self.vbobar = self.xpy + self.vbubar
        self.betaobar = np.linalg.solve(self.vobar, self.vbobar)
        
        self.nuobar = self.nuubar + self.nobs
        self.sobar = self.subar + sum(self.yvec**2)+ \
        np.dot(self.betaubar, self.vbubar)- \
        np.dot(self.betaobar, self.vbobar)

    def __calculate_g_prior(self):
        self.calculated = True
        if  self.updateind_xmat == 1 or self.updateind_yvec == 1:
            self.xpy = np.dot(self.xmat.transpose(), self.yvec)
            if self.updateind_xmat == 1: 
                self.xpx = np.dot(self.xmat.transpose(), self.xmat)
            self.updateind_xmat = 0
            self.updateind_yvec = 0
        self.betahat = np.linalg.solve(self.xpx, self.xpy)
        self.betaobar = self.gratio * (self.betahat +
                                       self.betaubar/self.g)
        self.vobar = 1./self.gratio * self.xpx
        self.nuobar = self.nobs
        self.betadiff = self.betahat - self.betaubar
        self.res = self.yvec - np.dot(self.xmat, self.betahat)
        self.sobar = np.dot(self.res.T, self.res)+ \
        np.dot(self.betadiff.T, np.dot(self.xpx, self.betadiff))/(
            self.g + 1.)


    def sample(self):
        """Returns a sample from the posterior of the linear regression
        model."""

        self.__calculate()
        sig = self.__sample_scale()
        beta = self.betaobar + np.linalg.solve(self.cholvobar.T,
                                               np.random.randn(self.kreg))
        return sig, beta

    def __log_cand_pr_sig(self, sigma, beta, **kwargs):
        """
        calculates the log of the candiate probability given scale = sigma
        """
        loglike = self.loglike(sigma, beta)

        dbeta = beta - self.betaubar
        kern = -self.kreg * np.log(sigma) -0.5 / sigma ** 2 *\
                np.dot(dbeta, np.dot(self.vubar, dbeta))

        kerns = -(self.nuubar + 1) * np.log(sigma) - self.subar/(2.0 * sigma ** 2)
        
        if 'kernel_only' in kwargs and kwargs['kernel_only'] == True:
              return loglike + kern + kerns

        else:
            const = -0.5 * self.kreg * np.log(2 * np.pi) + 0.5 * self.lndetvubar
            consts = np.log(2) - special.gammaln(self.nuubar / 2.) +\
                    self.nuubar / 2. * np.log(self.subar / 2.)
            return loglike + kern + kerns + const + consts


    def __log_cand_pr_sig_jeff(self, sigma, beta, **kwargs):
        
        loglike = self.loglike(sigma, beta)
        return loglike - np.log(sigma)

    def __log_canc_pr_sig_gprior(self, sigma, beta, **kwargs):
        loglike = self.loglike(sigma, beta)
        
        dbeta = beta - self.betaubar
        kern = -self.kreg * np.log(sigma) -0.5 * self.kreg * np.log(self.g) \
                -0.5 / (self.g * sigma ** 2) \
                * np.dot(dbeta, np.dot(self.vubar, dbeta))

        
        if 'kernel_only' in kwargs and kwargs['kernel_only'] == True:
                return kern - np.log(sigma)
        else:
            const = -0.5 * self.kreg * np.log(2 * np.pi) + 0.5 * self.lndetvubar
            return loglike + kern + const - np.log(sigma)


    def __log_cand_pr_kappa(self, kappa, beta, **kwargs):
        loglike = self.loglike(sigma, beta)

        dbeta = beta - betaubar
        kern = 0.5 * self.kreg * np.log(kappa) -0.5 * kappa \
                * np.dot(dbeta, np.dot(self.vubar, dbeta))

        kerns = (nu + 1) / np.log(kappa) - ns * kappa /2.0 
        
        if 'kernel_only' in kwargs and kwargs['kernel_only'] == True:
            return loglike + kern + kerns

        else:
            const = -0.5 * self.kreg * np.log(2 * np.pi) + 0.5 * self.lndetvubar
            consts = np.log(2) - special.gammaln(self.nuubar / 2.) +\
                    self.nuubar / 2. * np.log(self.subar/2.)
            return loglike + kern + kerns + const + consts


    def __sample_standard_deviation(self):
        sig = 1.0/np.sqrt(np.random.gamma(self.nuobar/2., 2./self.sobar, 1))
        # self.cholvobar = 1.0/sig * np.linalg.cholesky(self.vobar)
        self.cholvobar = 1.0/sig * np.linalg.cholesky(self.vobar)
        return sig

    def __sample_precision(self):
        kappa = np.random.gamma(self.nuobar/2., 2./self.sobar, 1)
        self.cholvobar = np.linalg.cholesky(kappa * self.vobar)
        return kappa        

    def loglike(self, scale, beta):
        """Returns the log likelihood for the linear regression model.

        arguments:
            scale - scale pararamter.
            beta - regression coefficients.

        """

        if self.calculated == False:
            self.__calculate()
        if self.prior[0] == 'normal_gamma':
            sig = 1. / np.sqrt(scale)
        else:
            sig = scale
        
        diff = self.yvec - np.dot(self.xmat, np.atleast_1d(beta))
        sigsq = sig**2
        nobs = self.yvec.shape[0]
        return -0.5 * nobs * np.log(2.0 * np.pi * sigsq) - \
               0.5/sigsq * np.dot(diff, diff)

    def log_marginal_likelihood(self):
        """Returns the log marginal likelihood if defined
        else returns nan.
        """

        if self.calculated == False:
            self.__calculate()
        return self.__log_marginal_likelihood()

    def __log_marginal_likelihood_nig(self):
        if self.calculated == False:
            self.__calculate()

        logdet_vubar = 2.0 * sum(np.log(np.diag(np.linalg.cholesky(self.vubar)))) 
        logdet_vobar = 2.0 * sum(np.log(np.diag(np.linalg.cholesky(self.vobar))))
        c1 = -0.5 * self.nobs * np.log(2. * np.pi)
        c2 = 0.5 * (logdet_vubar - logdet_vobar)
        c3 = special.gammaln(self.nuobar / 2.) - special.gammaln(self.nuubar / 2.)
        c4 = 0.5 * (self.nuubar * np.log(self.subar / 2.) - self.nuobar * np.log(self.sobar / 2.))
        return c1 + c2 + c3 + c4

    def __log_marginal_likelihood_jeff(self):
        return np.nan
    
    def __log_marginal_likelihood_gprior(self):
        return np.nan
    
    def posterior_mean(self):
        """Returns the posterior mean for the linear regression
        model.
        """

        if self.calculated == False:
            self.__calculate()
        betamean = self.betaobar
        sigmamean = self.__posterior_mean_scale()

        return sigmamean, betamean

    def __posterior_sigma_mean(self):
        """Zelner (1971), pp 371"""

        S = np.sqrt(self.sobar/self.nuobar)

        return np.exp(special.gammaln((self.nuobar - 1)/2.)-\
                special.gammaln(self.nuobar/2.))*np.sqrt(self.nuobar/2.) * S

    def __posterior_kappa_mean(self):
        # return self.nuubar/self.sobar
        return self.nuobar/self.sobar

    def __posterior_sigma_var(self):
        """function returns the estimate of the posterior variance for
        sigma, Zelner (1971), pp 373"""

        if self.calculated == False:
            self.__calculate()
        sigmamean = self.posterior_mean()[0]
        var = self.sobar/(self.nuobar - 2) - sigmamean**2
        return var

    def __posterior_kappa_var(self):
        if self.calculated == False:
            self.__calculate()
        s2 = self.sobar/self.nuobar
        return 4./(self.nuobar * s2**2)
       

    def get_posterior_covmat(self):
        """
        return the posterior covariance
        matrix for regression coefficients.
        """

        if self.calculated == False:
            self.__calculate()
        s2 = self.sobar/self.nuobar
        Am = np.linalg.inv(self.vobar)
        nuobar = self.nuobar
        covmat = (nuobar/(nuobar - 2)) * s2 * Am
        return covmat

    def bic(self):
        """
        Return BIC
        """

        if self.calculated == False:
            self.__calculate()
        sig,beta = self.posterior_mean()
        loglike = self.loglike(sig,beta)
                               
        return -2 * loglike + (self.kreg + 1) * np.log(self.nobs) 
        
    
    def __thpd(self, nu, bbar, sd):
        """
        Get the hpd interval for the t-dist.
        """

        ## and plot it
        rv = dstn.t(nu, bbar, sd)
        xl = rv.ppf(0.025)
        xu = rv.ppf(0.975)
        return np.array([xl, xu])

    def __plottdist(self, nu, bbar, sd, title):
        """
        Plot t distribution
        """


        ## and plot it
        rv = dstn.t(nu, bbar, sd)
        xmin =  rv.ppf(0.001)
        xmax = rv.ppf(0.999)
        x = np.linspace(xmin, xmax, 100)
        h = plt.plot(x, rv.pdf(x))
        plt.title(title)
        ## add the hpd's
        xl = rv.ppf(0.025)
        xu = rv.ppf(0.975)
        ltx = np.linspace(xmin, xl, 50)
        lty = rv.pdf(ltx)
        plt.fill(np.r_[ltx, ltx[-1]],
                 np.r_[lty, 0], facecolor ="blue", alpha = 0.5)
        utx = np.linspace(xu, xmax, 50)
        uty = rv.pdf(utx)
        plt.fill(np.r_[utx, utx[0]],
                 np.r_[uty, 0], facecolor ="blue", alpha = 0.5)
        ## return rv

        


    def __plotinvertedgamma(self, nu, s2, title):
        """
        plots inverted gamma,
        Zellner 1971 for details
        """


        mode = np.sqrt(s2)*np.sqrt( nu/(nu+1.0) )
        minx = 1E-3
        if minx > 0.01*mode:
            minx = 0.0
            # note this will induce a warning
            # due to divide by zero
        ## centre x on the mode
        x = np.linspace(minx, mode * 2, num = 200)
        d1 = 2.0/special.gamma(nu/2.0)
        d2 = ( (nu * s2)/2.0)**(nu/2.0)
        d3 = 1/(x**(nu + 1.0))
        d4 = (nu * s2)/(2 * (x**2))
        y = d1 * d2 * d3 * np.exp(-d4)
        plt.plot(x, y)
        plt.title(title)

    def __get_plot_dimensions(self, kwargs):
        totalplots = self.kreg + 1
        if kwargs.has_key('individual'):
            cols = 1
            rows = 1
        elif kwargs.has_key('rows') and not kwargs.has_key('cols'):
            ## work out the cols from the rows
            cols = np.ceil(totalplots/float(kwargs['rows']))
            rows = kwargs['rows']
        elif kwargs.has_key('cols') and not kwargs.has_key('rows'):
            rows = np.ceil(totalplots/float(kwargs['cols']))
            cols = kwargs['cols']
        elif not kwargs.has_key('cols') and not kwargs.has_key('rows'):
            cols = np.floor(np.sqrt(totalplots))
            if cols == 0:
                cols = 1
            rows = int(np.ceil(totalplots/cols))
        else:
            rows = kwargs['rows']
            cols = kwargs['cols']

        plotdims = {'totalplots':totalplots,
                    'cols':int(cols),
                    'rows':int(rows),
                    'figsperplot':int(rows * cols)}
        return plotdims


    def plot(self, **kwargs):
        """
        Basic plotting function for regression objects.
        """

        if FLAG_PLOT == False:
            error = """Matplotlib is not installed on this system. You cannot
            use function plot without it."""
            raise Exception(error)

        if not self.calculated:
            self.__calculate()
        s2 = self.sobar/self.nuobar
        betasd = np.sqrt(np.diag(self.get_posterior_covmat()))
        
        plotdims = self.__get_plot_dimensions(kwargs)
        plotcounter = 0
        pagecounter = 0
        for i in range(plotdims['totalplots'] - 1):
            if plotcounter % plotdims['figsperplot'] == 0:
                if plotcounter > 0:
                   pagecounter = pagecounter + 1
                   ## then already plotted something,
                   ## we might want to save it
                   if kwargs.has_key('filename'):
                       (base, suffix) = os.path.splitext(kwargs['filename'])
                       fname = "%s%03d%s" % (base, pagecounter, suffix)
                       plt.savefig(fname) 
                   plotcounter = 0
                   plt.figure()
            plotcounter = plotcounter + 1
            plt.subplot(plotdims['rows'], plotdims['cols'], plotcounter)
            title = r'$\beta_{%d}$' % i
            self.__plottdist(self.nuobar,
                             self.betaobar[i],
                             betasd[i], title)
        ## and the final plot..
        if plotcounter % plotdims['figsperplot'] == 0:
            if plotcounter > 0:
               pagecounter = pagecounter + 1
               ## then already plotted something,
               ## we might want to save it
               if kwargs.has_key('filename'):
                   (base, suffix) = os.path.splitext(kwargs['filename'])
                   fname = "%s%03d%s" % (base, pagecounter, suffix)
                   plt.savefig(fname) 
               plotcounter = 0
               plt.figure()
        plotcounter = plotcounter + 1
        plt.subplot(plotdims['rows'], plotdims['cols'], plotcounter)
        title = r'$\sigma$'
        self.__plotinvertedgamma(self.nuobar, s2, title)
        pagecounter = pagecounter + 1
        ## then already plotted something,
        ## we might want to save it
        if kwargs.has_key('filename'):
            (base, suffix) = os.path.splitext(kwargs['filename'])
            fname = "%s%03d%s" % (base, pagecounter, suffix)
            plt.savefig(fname)
        else:
            plt.show()
        
    
    def update_yvec(self, yvec):
        """Updates the vector of observations.

        argument:
            yvec - vector of observations.
        """

        self.yvec = yvec
        self.updateind_yvec = 1
        self.calculated = False

    def update_xmat(self, xmat):
        """Updates the matrix of regressors.

        arguments:
            xmat - matrix of regressors.
        """

        if xmat.ndim == 1:
            self.xmat = xmat.reshape(xmat.shape[0], 1)
        else:
            self.xmat = xmat
        self.calculated = False
        self.updateind_xmat = 1

    def residuals(self):
        """Returns the vector of residuals"""

        if self.calculated == False:
            self.__calculate()
        sigma,beta=self.posterior_mean()
        return self.yvec-np.dot(self.xmat,beta)
            

    def __print_header(self, destination, colwidth, sigfigs):
        """
        print a generic header for the output:
        """

        print >>destination, ""
        hline =  "{hline: ^{totalwidth}}".format(
            hline ="---------------------------------------------------",
            totalwidth = 6 * colwidth)
        print >>destination, hline
        print >>destination, \
              "{title: ^{totalwidth}}".format(
            title ="Bayesian Linear Regression Summary",
            totalwidth = 6 * colwidth)
        print >>destination, \
              "{priorname: ^{totalwidth}}".format(
            priorname = self.prior[0],
            totalwidth = 6 * colwidth)
        print >>destination, hline
        print >>destination, """\
{0: >{colwidth}.{colwidth}s}\
{1: >{colwidth}.{colwidth}s}\
{2: >{colwidth}.{colwidth}s} \
{3: >{colwidth}.{colwidth}s}\
{4: >{colwidth}.{colwidth}s}""".format(" ", "mean", "sd", "2.5%", "97.5%",
                                           colwidth = colwidth,
                                           sigfigs = sigfigs)

    def __print_summary(self, destination, paramname, meanval, sdval,
                      hpdintervals, hpd05, colwidth, sigfigs):
        """
        format the output for a single line.
        Arguments are the name of the parameter, its
        mean value, the standard deviation and the hpd (if present).
        Presumably only for a vector.
        """

        name = paramname
        print >>destination, """\
{name: >{colwidth}.{colwidth}}\
{val1: >0{colwidth}.{sigfigs}g}\
{val2: >0{colwidth}.{sigfigs}g}""".format(
            name = name,
            val1 = meanval,
            val2 = sdval,
            colwidth = colwidth, sigfigs = sigfigs),
        if hpdintervals:
            ## now for the hpd's
            print  >>destination, """\
{val1: >0{colwidth}.{sigfigs}g}\
{val5: >0{colwidth}.{sigfigs}g}""".format(
                val1 = hpd05[0],
                val5 = hpd05[1],
                colwidth = colwidth,
                sigfigs = sigfigs)
        else:
            print  >>destination, """\
{0: >0{colwidth}.{colwidth}s}\
{0: >0{colwidth}.{colwidth}s}""".format("NA", colwidth = colwidth - 1)


    def output(self, **kwargs):
        """
        Output for the regression summary.
        """

        colwidth = 12
        sigfigs = 4
        if not self.calculated:
            self.__calculate()
        if kwargs.has_key("filename"):
            destination = open(kwargs['filename'], 'w')
        else:
            destination = sys.stdout
        self.__print_header(destination, colwidth, sigfigs)
        sigmean, betamean = self.posterior_mean()
        betasd = np.sqrt(np.diag(self.get_posterior_covmat()))
        for i in range(len(betamean)):
            paramname = "beta[%d]" % i
            hpd = self.__thpd(self.nuobar,
                              betamean[i],
                              betasd[i])
            
            self.__print_summary(destination, paramname,
                          betamean[i],
                          betasd[i],
                          True, hpd, colwidth, sigfigs)

        
        ## and now for sigma
        if self.prior[0] =="normal_gamma":
            scale_name = "kappa"
        else:
            scale_name = "sigma"
        sigsd = np.sqrt(self.__posterior_variance_scale())
        self.__print_summary(destination, scale_name,
                      sigmean,
                      sigsd,
                      False, None, colwidth, sigfigs) 
        ## and print loglikelihood:
        print >>destination
        print >>destination, \
        "loglikelihood = {loglik: <0{colwidth}.{sigfigs}g}".format(
            loglik=self.loglike(sigmean,betamean),
            colwidth=colwidth,
            sigfigs=sigfigs)
        print >>destination,\
        "log marginal likelihood = {marglik: <0{colwidth}.{sigfigs}g}".format(
            marglik = self.log_marginal_likelihood(),
            colwidth = colwidth,
            sigfigs = sigfigs)

        print >>destination, \
        "BIC  = {bic: <0{colwidth}.{sigfigs}g}".format(
            bic = self.bic(),
            colwidth = colwidth,
            sigfigs = sigfigs)


class LinearModel:
    """A class for the Bayesian analysis of the linear regression
    model. Arguments:
        yvec - Vector of observations
        xmat - Matrix of regressors
        nit - number of interations (in case MCMC is being used).
        burn - length of burnin (in case MCMC is being used).
    """
    def __init__(self, yvec, xmat, nit = 20000, burn = 5000, **kwargs):

        #default number of iterations
        self.nit = nit

        #default burnin length
        self.burn = burn

        #number of regressors
        if xmat.ndim == 2:
            kreg = xmat.shape[1]
        else:
            kreg = 1

        #indicator for for cases that use MCMC
        self.mcmc_sampler_ind = False

        if 'prior' in kwargs:
            self.prior = kwargs['prior']
        else:
            self.prior = ['default']

        if self.prior[0] in ['normal_inverted_gamma_SS', 'normal_inverted_gamma_SS_spike_slab']:
            #lm_prior = ['normal_inverted_gamma', self.prior[1], self.prior[2]]
            #kwargs['prior'] = lm_prior
            if self.prior[0] == 'normal_inverted_gamma_SS':
                self.spike_slab = False
                self.prior[0] = 'normal_inverted_gamma'
            else:
                self.spike_slab = True
                self.prior[0] = 'normal_inverted_gamma_spike_slab'

            
            self.SS = StochasticSearch(yvec, xmat, self.prior)
            data = {}
            self.__sample = self.__SS_sample
            self.__output = self.__SS_output

            init_gamma = np.zeros(kreg, dtype = 'i')
            init_gamma[0] = 1
            simgam = CFsampler(self.__sample_gamma, init_gamma, 'gamma',
                               store = 'none')
            self.mcmc = MCMC(self.nit, self.burn, data, [simgam])
            self.ind_SS = True
            self.yvec = yvec

            



        elif self.prior[0] == 'g_prior_SS':
            self.prior[0] = 'g_prior'
            self.SS = StochasticSearch(yvec, xmat, self.prior)
            self.__sample = self.__SS_sample
            self.__output = self.__SS_output
            init_gamma = np.zeros(kreg, dtype = 'i')
            init_gamma[0] = 1
            data = {'SS': StochasticSearch(yvec, xmat, self.prior)}
            simgam = CFsampler(self.__sample_gamma, init_gamma, 'gamma',
                               store = 'none')
            self.mcmc = MCMC(self.nit, self.burn, data, [simgam])
            self.ind_SS = True
            self.yvec = yvec

        else:
            self.LM = LinearModelBase(yvec, xmat, **kwargs)
            self.__sample = self.__std_sample
            self.__output = self.__std_output
            self.ind_SS = False


    def update_number_of_iterations(self, nit):
        """Changes the number of iterations if MCMC is used for estimation""" 
        self.nit = nit

    def update_length_of_burnin(self, burn):
        """Changes the length of the burnin that is discarded
        if MCMC is used for estimation"""

        self.burn = burn

    def sample(self):
        """Draws a sample from the posterior distribution of the linear
        regression model"""

        return self.__sample()

    def __SS_sample(self, store):

        gamma = self.__sample_gamma(store)
        return gamma

    def __SS_output(self, **kwargs):
        if self.mcmc_sampler_ind == False:
            self.mcmc.sampler()
            self.mcmc_sampler_ind = True
            
        self.mcmc.output(custom = self.SS.output, **kwargs)
        #Extract regressors from most probable model
        txmat = self.SS.extract_regressors(0)

        #Extract index of included regressors
        inc = np.array(self.SS.included_regressors(0))

        if self.spike_slab == False:
            #Construct prior corresponding to most probable model
            D = self.prior[4][inc, 1]
            R = self.prior[3][inc][:, inc]

            #Construct vubar
            vubar = D[:, np.newaxis] * (R * D)
            prior = [self.prior[0], self.prior[1], self.prior[2],
                     np.zeros(inc.shape[0]), vubar]

        else:
            #Prior in spike slab case

            prior = self.prior
            prior[0] = 'normal_inverted_gamma'
            prior[3] = prior[3][inc]
            prior[4] = prior[4][inc][:, inc]
            
        
        breg = LinearModel(self.yvec, txmat, prior = prior)
        breg.output(**kwargs)


    def __sample_gamma(self, store):
        return self.SS.sample_gamma(store)


    def __std_sample(self):
        return self.LM.sample()

    def __std_output(self, **kwargs):
        self.LM.output(**kwargs)

    def output(self, **kwargs):
        """Produces a standard output for the linear
        regression model"""

        self.__output(**kwargs)

    def __check_SS(self):

        if self.ind_SS == True:
            if self.mcmc_sampler_ind == False:
                self.mcmc.sampler()
                self.mcmc_sampler_ind = True
            txmat = self.SS.extract_regressors(0)
            prior = self.SS.extract_prior(0)
            breg = LinearModel(self.yvec, txmat, prior = prior)
            return breg
        else:
            return self.LM
    
    def update_prior(self, prior):
        """Updates the prior for the linear regresssion model"""

        if prior[0] in ['normal_inverted_gamma', 'normal_gamma', 'g_prior']:
            self.LM.update_prior(prior)

        else:
            if prior[0] == 'normal_inverted_gamma_SS':
                prior[0] == 'normal_inverted_gamma'

            else:
                assert prior[0] == 'g_prior_SS'
                prior[0] == 'g_prior'

            self.SS.update_prior(prior)

    def log_posterior_probability(self, scale, beta, **kwargs):
        """Returns the log posterior probability of the linear
        regression model.

        arguments:
            scale - scale parameter
            beta - regression coefficients
        """
            
        breg = self.__check_SS()
        return breg.log_posterior_probability(scale, beta,
                                                 **kwargs)

    def loglike(self, scale, beta):
        """Returns the log likelihood for the linear regression model

        arguments:
            scale - scale parameter
            beta - regression coefficients
        """

        breg = self.__check_SS()
        return breg.loglike(scale, beta)

    def log_marginal_likelihood(self):
        """Returns the log marginal likelihood if defined; else 
        returns nan."""

        breg = self.__check_SS()
        return breg.log_marginal_likelihood()

    def posterior_mean(self):
        """Returns the posterior mean estimates for the scale parameter
        and regression coefficients, respectively."""

        breg = self.__check_SS()
        return breg.posterior_mean()

    def get_posterior_covmat(self):
        """Returns the posterior covariance for the regression coefficients """
        breg = self.__check_SS()
        return breg.get_posterior_covmat()

    def bic(self):
        """Returns the Bayesian Information Criterion for the
        linear regression model."""

        breg = self.__check_SS()
        return breg.bic()

    def plot(self, **kwargs):
        """Produces a standard set of plots for the linear regression model."""

        if FLAG_PLOT == False:
            error = """Matplotlib is not installed on this system. You cannot
            use function plot without it."""
            raise Exception(error)

        breg = self.__check_SS()
        breg.plot(**kwargs)

    def update_yvec(self, yvec):
        """Updates the vector of observations.

        arguments:
            yvec - vector of observations.
        """

        self.LM.update_yvec(yvec)
        if self.ind_SS == True:
            self.SS.update_yvec(yvec)

    def update_xmat(self, xmat):
        """Function updates the (N x k) matrix of regressors.
        
        arguments:
            xmat - (N x k) matrix of regressors."""

        self.LM.update_xmat(xmat)
        if self.ind_SS == True:
            self.SS.update_xmat(xmat)

    def residuals(self):
        """Returns the residuals from the linear regressions model."""

        breg = self.__check_SS()
        return breg.residuals()
            

class CondRegressionSampler:

    """

    This class samples beta assuming it is generated from a linear
    regression model where the scale parameter is known. This class is
    initialised with the following arguments:
      yvec - a one dimensional numpy array containing the data.
      xmat - a two dimensional numpy array containing the regressors.
      kwargs - optional arguments:

          prior - a list containing the name of the prior and the
            corresponding  hyperparameters.
            Examples:
              prior = ['normal', betaubar, Vubar] or
              prior = ['g_prior', betaubar, g].
            If none of these options are chosen or they are miss-specified
            then CondRegressionSampler will default to Jeffrey's prior.

          algorithm - SVD is an optional argument if you want to use
          the singular value decomposition. The default is to use the
          Cholesky decomposition. 
    """

    def __init__(self, yvec, xmat, **kwargs):
        self.nobs = yvec.shape[0] #number of observations
        if xmat.ndim == 1:
            xmat = np.asfortranarray(xmat.reshape(xmat.shape[0], 1))
        self.kreg = xmat.shape[1] #numboer of regressors
        self.yvec = yvec
        self.xmat = np.asfortranarray(xmat)
        #self.xpx = np.dot(xmat.T, xmat)
        #self.xpy = np.dot(xmat.T, yvec)
        self.xpx = np.zeros((self.kreg, self.kreg), order = 'F')
        self.xpy = np.zeros(self.kreg)
        self.updateind_xmat = 1
        self.updateind_yvec = 1
        self.updateind_prior = 1
        self.betaobar = np.zeros(self.kreg)
        self.vobar = np.zeros((self.kreg, self.kreg))
        self.vbobar = np.zeros(self.kreg)


        #Default Algorithm
        self.algorithm = 'Cholesky'
        if 'algorithm' in kwargs and kwargs['algorithm'] == 'Cholesky':
            self.algorithm = 'Cholesky'
        elif 'algorithm' in kwargs and kwargs['algorithm'] == 'SVD':
            self.algorithm = 'SVD'
            #placeholders for SVD
            self.S = None
            self.V = None
            self.U = None
        else:
            self.algorithm = 'Cholesky'

        if self.algorithm == 'Cholesky':
            self.cholvobar = np.zeros((self.kreg, self.kreg))
        if 'prior' not in kwargs:      # default: Jeffrey's prior
            self.__calculate = self.__calculate_jeffreys
            self.__sample = self.__sample_jeffreys
        
        else:                   # Normal - gamma prior
            self.prior = kwargs['prior']
            if type(self.prior[0])!= types.StringType:
                print "Warning: Jeffery's prior used as prior was \
incorectly specified"
                self.__calculate = self.__calculate_jeffreys
                self.__sample = self.__sample_jeffreys

            else:
                ptype = self.prior[0]
                if ptype not in['normal', 'g_prior']:
                    print "Warning: Jeffery's prior used as prior was \
incorectly specified"
                    self.__calculate = self.__calculate_jeffreys
                    self.__sample = self.__sample_jeffreys
                elif ptype =='normal': 
                    assert(len(self.prior) == 3)
                    self.betaubar = self.prior[1]
                    self.vubar = self.prior[2]
                    self.__calculate = self.__calculate_normal
                    self.__sample = self.__sample_gen
                    self.vbubar = np.dot(self.vubar, self.betaubar)
                    if self.algorithm == 'SVD':
                        E, V = np.linalg.eig(self.vubar)
                        sqrt_vubar = np.dot(V,
                               (E ** 0.5).reshape(self.kreg,1) * V.T)
                        self.Amat = np.vstack([self.xmat, sqrt_vubar])
                        self.rhs = np.hstack([self.yvec, self.vbubar])
                else:
                    # g_prior
                    assert(len(self.prior) == 3)
                    self.betaubar = self.prior[1]
                    self.g = float(self.prior[2])
                    self.gratio = self.g/(1.+self.g)
                    self.betahat = np.zeros(self.kreg)
                    self.__calculate = self.__calculate_g_prior
                    self.__sample = self.__sample_gen
                    

    def calculate(self, sigma, **kwargs):
        """Calculations that are necessary for estimation."""

        self.__calculate(**kwargs)
    def __calculate_jeffreys(self, **kwargs):
        if self.algorithm == 'SVD':
            if 'index' in kwargs:
                index = kwargs['index']
                #if index always recalculate
                self.U, self.S, self.V = np.linalg.svd(self.xmat[:, index],
                                                      full_matrices = False)
            else:
                if self.updateind_xmat == 1:
                    self.U, self.S, self.V = np.linalg.svd(self.xmat,
                                               full_matrices = False)

            pinv = np.dot(self.V.T, 1. / self.S.reshape(self.kreg, 1) * \
                              self.U.T)
            if 'index' in kwargs:
                self.betaobar[index] = np.dot(pinv, self.yvec)

            else:
                self.betaobar = np.dot(pinv, self.yvec)

        else:
            if  self.updateind_xmat == 1 or self.updateind_yvec == 1:
                #self.xpy = np.dot(self.xmat.transpose(), self.yvec)
                reg_helper.calcxpy(self.xmat, self.yvec, self.xpy)
                if self.updateind_xmat == 1: 
                    #self.xpx = np.dot(self.xmat.transpose(), self.xmat)
                    reg_helper.calcxpx(self.xmat, self.xpx)
                    self.cholvobar = np.linalg.cholesky(self.xpx)
                
                if 'index' not in kwargs:
                    self.betaobar = np.linalg.solve(self.xpx, self.xpy)
                    self.updateind_xmat = 0
                    self.updateind_yvec = 0

                else:
                    index = kwargs['index']
                    self.cholvobar = np.linalg.cholesky(self.xpx[index][:, index])
                    self.betaobar[index] = np.linalg.solve(self.xpx[index][:,index],
                                                       self.xpy[index])

    def __calculate_normal(self, sigma, **kwargs):
        if self.algorithm == 'SVD':
            if 'index' in kwargs:
                index = kwargs['index']
                #if index always recalculate
                self.Amat[:self.nobs, index] = self.xmat[:,index] / sigma 
                self.U, self.S, self.V = np.linalg.svd(self.Amat[:, index],
                                                      full_matrices = False)
            else:
                self.Amat[:self.nobs, :] = self.xmat / sigma
                self.U, self.S, self.V = np.linalg.svd(self.Amat,
                                           full_matrices = False)

            pinv = np.dot(self.V.T, np.multiply(1. / self.S.reshape(self.kreg, 1),
                      self.U.T))
            self.rhs[:self.nobs] = self.yvec / sigma
            
            if 'index' in kwargs:
                self.betaobar[index] = np.dot(pinv, self.rhs)

            else:
                
                self.betaobar = np.dot(pinv, self.rhs)

        else:
            if  self.updateind_xmat == 1 or self.updateind_yvec == 1 \
                or self.updateind_prior == 1:
                if  self.updateind_xmat == 1 or self.updateind_yvec == 1:
                    #self.xpy = np.dot(self.xmat.transpose(), self.yvec)
                    reg_helper.calcxpy(self.xmat, self.yvec, self.xpy)
                    if self.updateind_xmat == 1: 
                        #self.xpx = np.dot(self.xmat.transpose(), self.xmat)
                        reg_helper.calcxpx(self.xmat, self.xpx)
                    self.updateind_xmat = 0
                    self.updateind_yvec = 0
                self.vbobar = self.xpy + self.vbubar
                self.vobar = self.vubar + self.xpx/sigma**2
                self.vbobar = self.xpy/sigma**2 + self.vbubar
                self.updateind_prior = 0
            if 'index' in kwargs:
                index = kwargs['index']

                self.betaobar[index] = np.linalg.solve(self.vobar[index][:,index],
                            self.vbobar[index])
            else:
                self.betaobar = np.linalg.solve(self.vobar, self.vbobar)

    def __calculate_g_prior(self, sigma, **kwargs):
        if 'index' in kwargs:
            index = kwargs['index']

            if  self.updateind_xmat == 1 or self.updateind_yvec == 1 \
                or self.updateind_prior == 1:
                if  self.updateind_xmat == 1 or self.updateind_yvec == 1:
                #self.xpy = np.dot(self.xmat.transpose(), self.yvec)
                    reg_helper.calcxpy(self.xmat, self.yvec, self.xpy)
                    if self.updateind_xmat == 1: 
                        #self.xpx = np.dot(self.xmat.transpose(), self.xmat)
                        reg_helper.calcxpx(self.xmat, self.xpx)
                    self.betahat[index] = np.linalg.solve(self.xpx[index][:, index],
                                                   self.xpy[index])
                    self.updateind_xmat = 0
                    self.updateind_yvec = 0
                self.updateind_prior = 0
            self.betaobar[index] = self.gratio * \
                    (self.betahat[index] + self.betaubar[index]/self.g)
            self.vobar[index][:,index] = 1.0/(sigma**2 * self.gratio) * \
                self.xpx[index][:,index]

        else:
            if  self.updateind_xmat == 1 or self.updateind_yvec == 1 \
                or self.updateind_prior == 1:
                #self.xpy = np.dot(self.xmat.transpose(), self.yvec)
                if  self.updateind_xmat == 1 or self.updateind_yvec == 1:
                    reg_helper.calcxpy(self.xmat, self.yvec, self.xpy)
                    if self.updateind_xmat == 1: 
                        #self.xpx = np.dot(self.xmat.transpose(), self.xmat)
                        reg_helper.calcxpx(self.xmat, self.xpx)
                    self.betahat = np.linalg.solve(self.xpx, self.xpy)
                    self.updateind_xmat = 0
                    self.updateind_yvec = 0
                self.betaobar = self.gratio * (self.betahat + self.betaubar/self.g)
                self.vobar = 1.0/(sigma**2 * self.gratio) * self.xpx

    def sample(self, sigma, **kwargs):
        """Returns a sample from the posterior of the linear model conditional on the
        scale parameter.

        arguments:
            sigma - scale parameter for the linear model.
        """

        return self.__sample(sigma, **kwargs)

    def __sample_gen(self, sigma, **kwargs):
        """This function returns a sample of beta"""
        self.__calculate(sigma, **kwargs)
        if 'index' in kwargs:
            index = kwargs['index']
            kreg = (index > 0).sum()
            if self.algorithm == 'SVD':
                rvec = np.dot(self.V / self.S, np.random.randn(kreg))
                beta = self.betaobar[index] + rvec

            elif self.algorithm == 'Cholesky':
                self.cholvobar[:kreg, :kreg] = \
                        np.linalg.cholesky(self.vobar[index][:, index])
                beta = self.betaobar[index] + \
                        np.linalg.solve(self.cholvobar[:kreg, :kreg].T,
                                                       np.random.randn(kreg))

            return beta

        else:
            if self.algorithm == 'SVD':
                rvec = np.dot(self.V / self.S, np.random.randn(self.kreg))
                
                beta = self.betaobar + rvec
            elif self.algorithm == 'Cholesky':
                self.cholvobar = np.linalg.cholesky(self.vobar)
                beta = self.betaobar + np.linalg.solve(self.cholvobar.T,
                                                       np.random.randn(self.kreg))

            return beta

    def __sample_jeffreys(self, sigma, **kwargs):
        self.__calculate(**kwargs)
        if 'index' in kwargs:
            index = kwargs['index']
            kreg = (index > 0).sum()
            if self.algorihm == 'SVD':
                rvec = np.dot(self.V / self.S, np.random.randn(kreg))
                beta = self.betaobar[index] + sigma * rvec
            elif self.algorithm == 'Cholesksy':
                beta = self.betaobar[index] +  \
                    np.linalg.solve(self.cholvobar[:kreg, :kreg].T,
                                               np.random.randn(kreg))

        else:
            if self.algorithm == 'SVD':
                rvec = np.dot(self.V / self.S, np.random.randn(self.kreg))
                beta = self.betaobar +  rvec

                
            elif self.algorithm == 'Cholesky':                                            
                beta = self.betaobar + np.linalg.solve(self.cholvobar.T,
                                               np.random.randn(self.kreg))

        return beta



    def update_prior(self, prior):
        """Function updates prior for for the linear model.

        argument:
            prior - new prior for the linear model. The prior
                    specification must be the same as when the
                    class was instantiated.
        """

        self.prior = prior
        self.updateind_prior = 1
        if prior[0] == 'normal':
            assert(len(prior) == 3)
            assert self.prior[0] == 'normal'
            self.betaubar = self.prior[1]
            self.vubar = self.prior[2]

        elif prior[0] == 'g_prior':
            assert(len(prior) == 3)
            assert self.prior[0] == 'g_prior'
            self.betaubar = self.prior[1]
            self.g = float(self.prior[2])
            self.gratio = self.g/(1.+self.g)
            self.betahat = np.zeros(self.kreg)

    def get_prior(self):
        """Returns the prior for the linear model."""
        return self.prior
        
    def get_marginal_posterior_mean(self):
        """Returns the marginal posterior mean for the regression
        coefficients."""

        return self.betaobar

    def get_marginal_posterior_precision(self):
        """Returns the marginal posterior precision for the 
        regression coefficients."""

        return self.vobar

    def residuals(self, beta, **kwargs):
        """returns residuals from yvec - dot(xmat, beta).
        
        argument:
            beta - Regression coefficient for the linear model.
        """
        if 'index' in kwargs:
            index = kwargs['index']
            return self.yvec - np.dot(self.xmat[:, index], beta)

        return self.yvec - np.dot(self.xmat, beta)
    
    def update_yvec(self, yvec):
        """
        This function updates the vector of observations. This is often useful
        when the class is being used as a part of the MCMC sampling
        scheme.

        argument:
            yvec - vector of observations.
        """

        self.yvec = yvec
        self.updateind_yvec = 1
        if self.algorithm == 'SVD':
            self.rhs[:self.nobs] = self.yvec

    def update_xmat(self, xmat):
        """
        This function updates the matrix of regressors. This is often useful
        when the class is being used as a part of the MCMC sampling
        scheme.

        argument:
            xmat - matrix of regressors.
        """

        if xmat.ndim == 1:
            self.xmat = np.asfortranarray(xmat.reshape(xmat.shape[0], 1))
        else:
            self.xmat = np.asfortranarray(xmat)
        self.updateind_xmat = 1

        if self.algorithm == 'SVD':
            self.Amat[:self.nobs, :] = self.xmat



class CondScaleSampler:
    def __init__(self, **kwargs):
        """class is used to sample the scale given the residuals from a linear
        model.

        kwargs (optional arguments):
            prior - is a tuple or list containing the hyperparamers that
            describe the prior. If it is not specified the Jeffrey's
            prior is used instead. The options are:
                ['gamma', nu, S],
                ['inverted-gamma', nu, S],
                ['wishart', nu, S];
                where nu is the degrees of freedom parameter and S
                is the inverse of the scale parameter(matrix) (for the distribution).

        """
        
        self.nuubar = 0.
        self.Subar = 0.
        self.__sample = self.__sample_inverted_gamma

        if 'prior' in kwargs:
            self.prior = kwargs['prior']
            priorname = self.prior[0]
            if type(self.prior[0])!= types.StringType:
                print "Warning: Jeffery's prior used as prior was \
incorectly specified"

            else: 
                if priorname not in ['gamma', 'inverted_gamma', 'wishart']:
                    print """\nWarning: Prior type unknown for \
CondSigSample. Defaulting to Jeffrey's prior\n"""

                elif priorname =='gamma':
                    self.nuubar = self.prior[1]
                    self.Subar = self.prior[2]
                    self.__sample = self.__sample_gamma
                    

                elif priorname == 'inverted_gamma':
                    self.nuubar = self.prior[1]
                    self.Subar = self.prior[2]
                    self.__sample = self.__sample_inverted_gamma

                else:
                    #wishart prior is used
                    self.nuubar = self.prior[1]
                    self.Subar = np.atleast_2d(self.prior[2])
                    self.__sample = self.__sample_wishart2
                    self.p = self.Subar.shape[0]
                    self.Sobar = np.zeros((self.p, self.p), order = 'F')
                    self.simwishart = SampleWishart(self.p)


    def sample(self, residual, raxis = 0):
        """Returns a sample of the scale from the posterior distribution of
        the linear model.

        arguments:
            residual - matrix or vector of the residuals.
        """

        return self.__sample(residual, raxis)

    def __sample_gamma(self, residual, raxis):
        nuobar = self.nuubar + residual.shape[raxis]
        Sobar = self.Subar + np.sum(residual**2, axis = raxis)
        return 2. / Sobar * np.random.gamma(nuobar/2., 1.)

    def __sample_inverted_gamma(self, residual, raxis):
        return 1. / np.sqrt(self.__sample_gamma(residual, raxis))

    #def __sample_wishart(self, residual, raxis):
    #    residual = np.atleast_2d(residual)
    #    assert residual.shape[1 - raxis] == self.p
    #    self.nuobar = self.nuubar + residual.shape[raxis]
    #    self.randnvec = np.random.randn(self.n_randn)
    #    self.randchivec = np.random.chisquare(self.nuobar - self.work_chisq)
    #    if raxis == 1:
    #        wishart.calc_sobar(self.Subar, self.Sobar, np.asfortranarray(residual.T))
    #    if raxis == 0:
    #        wishart.calc_sobar(self.Subar, self.Sobar, np.asfortranarray(residual))
    #    self.cmat = np.asfortranarray(np.linalg.cholesky(np.linalg.inv(self.Sobar)).T)
    #    wishart.chol_wishart(self.randnvec, self.randchivec, self.umat,
    #                         self.cmat, self.rmat)

        #return np.dot(self.rmat.T, self.rmat)

    def __sample_wishart2(self, residual, raxis):
        if residual.ndim == 1:
            if raxis == 0:
                residual.reshape(residual.shape[0],1)
            else:
                residual.reshape(1, residual.shape[0])
            
       
        if self.p > 1:
            assert residual.shape[1 - raxis] == self.p
            
        self.nuobar = self.nuubar + residual.shape[raxis]
        
        if raxis == 1:
            wishart.calc_sobar(self.Subar, self.Sobar,
                               np.asfortranarray(residual.T))
        else:
            wishart.calc_sobar(self.Subar, self.Sobar,
                               np.asfortranarray(residual))

        return self.simwishart.sample(self.nuobar, self.Sobar)










