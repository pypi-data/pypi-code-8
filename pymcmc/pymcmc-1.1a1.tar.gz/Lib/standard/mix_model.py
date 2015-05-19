# Python code used in the Bayesian estimation of mixture models.
# Copyright (C) 2011  Chris Strickland

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
import pdb
import sys
import pymcmc.mixture_model as mm
from pymcmc.mcmc import CFsampler, MCMC, RWMH
from pymcmc.regtools import LinearModel
from pymcmc.sim_distributions import SampleWishart
#from munkres import Munkres
from pymcmc.standard.utilities import LabelSwitch
from scipy.cluster.vq import *
from random import randint
from scipy.stats import itemfreq


class MixtureModel:
    def __init__(self, nit, burn, ymat, nmix, **kwargs):
        """
        Purpose
        =======
        The class MixtureModel can be used for the Bayesian MCMC
        estimation of a normal mixture model.

        Arguments
        =========

        nit - Is an integer refering to the number or iterations
              the MCMC sampler should be run for.

        burn - Is an integer that defines the length of the burnin
               for the MCMC estimation.

        ymat - Is an (n x p) matrix that contains the observations.
               If a vector of order n is passed in then a univariate 
               normal mixture is assumed

        nmix - Is an integer that specifies the number of components
               in the mixture.

                
        Optional Arguments (**kwargs)
        =============================

        regressors - Is an optional argument (for the univariate mixture
                     case only) used if regressors are to
                     be included in the model. The simplest way to
                     specify the inclusino of regressors is to include
                     the optional argument regressors = xmat, where xmat
                     is a (n x k) matrix of regressors. There is also
                     the option to specify a prior for the regression
                     coefficients. This is done following
                     regressors = [xmat, ['normal', betaubar, vubar]],
                     where betaubar is the prior mean vector and vubar
                     is the prior precision matrix. If no prior is
                     specified then a flat prior is assumed.

        weights - Is an option that can be used to specify a prior on the
                  weights of the mixture. There are two options. Specifically,
                  weights =['dirichlet', pubar] or 
                  weights = ['potts', num_neighbours, index_neighbours, phi_min and phi_max],
                  where num_neighbours is an array containing the number of
                  neighbours for observations i = 1,2,...,n, index_neighbours
                  is an array of neighbouring indicies stacked on top of
                  each other. For example:
                  Suppose for a (4 x 1) vector of observations y, we have the following
                  adjacency list:
                      y[1] - 2, 3
                      y[2] - 1, 4
                      y[3] - 1, 4
                      y[4] - 2, 3

                      then we have
                      num_neighbours[1] = 2
                      num_neighbours[2] = 2
                      num_neighbours[3] = 2
                      num_neighbours[4] = 2
                    
                      and
                      index_neighbours[1] = 2
                      index_neighbours[2] = 3
                      index_neighbours[3] = 1
                      index_neighbours[4] = 4
                      index_neighbours[5] = 1
                      index_neighbours[6] = 4
                      index_neighbours[7] = 2  
                      index_neighbours[8] = 3
                


            
                  The term phi_min is the minimum level of spatial
                  cohesion, for positive relationships this number must
                  be greater than zero and phi_max is the upper allowable
                  level of spatial influence. If the optional argument weights
                  is not specified then a dirichlet prior is assumed with pubar
                  equal to a vector of ones.

        prior_mean_scale - We allow for three alternative prior specifications.
                      First the normal inverted gamma prior, which is specified as
                      prior_mean_scale = ['normal_inverted_gamma', nubar, Subar,


                      The second prior specification specifies an independent
                      normal inverted gamma prior. In this case the prior is
                      specified as prior_mean_scale = ['ind_normal_inverted_gamma',
                      nubar, subar, alphaubar, vubar]. 
                      The third prior specification

                      The third prior specfication is a normal-Wishart prior, which 
                      is used in the multivariate case. This is specified as 
                      prior_mean_scale = ['normal-wishart', nubar, Subar, alphaubar,
                                           n0'].
                      Note that Subar is the inverse of the scale parameter for the
                      Wishart distribution, nubar is the degrees of freedom parameter,
                      alphaubar is the mean vector for the multivariate normal 
                      distribution and vubar is the prior precision for the normal
                      distribution.

                      DEFAULTS:
                      In the univariate case if no prior is specified then
                      the default prior is the normal inverted gamma prior where
                      nubar = 1, Subar = 0.01, alphaubar is the datamean and
                      mjubar= 5.

                      In the multivariate case if no prior is specified then
                      the default prior is the normal-Wishart prior, where
                      nubar = 3, Subar = 1.3 * sample precision, alphaubar =
                      data mean and n0 = 1. These default priors are recommended
                      by Robert(1996). 

        initial_sigma - Initial value for sigma (component scale parameters)

        initial_alpha - Initial value for alpha (component means)

        """
    
        self.ymat = ymat
        self.nobs = ymat.shape[0]
        if ymat.ndim == 2:
            if ymat.shape[1] == 1:
                self.ymat = ymat.flatten()
                self.dseries = 1
            else:
                self.flag_multivariate = True
                self.dseries = ymat.shape[1]
        else:
            #use a univariate mixture
            self.dseries = 1

        #Declare workspace dummy
        self.ystar = None
        self.nmix = nmix
        
        #assert nobs > nmix
        try:
            assert self.nobs > self.nmix
        except:
            raise NameError("The number of observations must be \
                            greater than the number of components")

        #flip ymat for efficiency in Fortran
        
        self.ymat = self.ymat.T

        self.compute_ind = False
        self.nit, self.burn = nit, burn
        

        if 'weights' in kwargs:
            
            weights = kwargs['weights']

            if weights[0] == 'dirichlet':
                #Use dirichlet prior on weights
                self.pubar = self.weights[1]
                self.weights_prior = 'dirichlet'

            elif weights[0] == 'potts':
                centroids, label = kmeans2(ymat,nmix)
	        start_values_z = label.T
                print itemfreq(start_values_z)
                #Assumption of Potts prior on the weights
                self.num_neighbours = np.hstack([1, np.cumsum(weights[1]) + 1])
                self.index_neighbours = weights[2]
                self.phi_min = weights[3]
                self.phi_max = weights[4]
                self.weights_prior = 'potts'
                self.prev_evec = np.ones((self.nmix, self.nobs), order = 'F')*start_values_z
                self.neigh_mat = np.zeros((self.nmix, self.nobs), order = 'F')
        else:
            #use dirichlet prior by default
            self.pubar = np.ones(nmix)
            self.weights_prior = 'dirichlet'

        #Use for debugging only
        if 'simd' in kwargs:
            self.simd = kwargs['simd']

        #check for label switching algorithm
        if 'label_switching' not in kwargs:
            #Default to CronWest
            kwargs['label_switching'] = ['CronWest', 100]

        if 'label_switching' in kwargs:
            #If list string identifyer should be first argument
            if type(kwargs['label_switching']) in (type(()), type([])):
                label_switch = kwargs['label_switching'][0]
            else:
                label_switch = kwargs['label_switching']

            try:
                assert label_switch in ['CronWest', 'stupid_method']
                #Check it is one of the two possible options
                #CronWest is based on relabling of classifications
                #stupid_method is reordering based on means
                #(can work ok in univariate case)
            except:
                error = """label switching there is two options. It stupid method
                or CronWest."""
                raise Exception(error)

            if label_switch == 'CronWest':
                self.ls_flag = 'CronWest'
                #Work variables for cron west method
                self.__cw_store_prob = np.zeros(nmix)
                self.__cw_work = np.zeros(self.dseries)

                self.LSCW = LabelSwitch(self.log_likelihood, 'evec',
                        kwargs['label_switching'][1], nmix)


            else:
                self.ls_flag = 'stupid_method'

            #Pointer to function
            if self.dseries == 1:
                self.__log_normal = self.__log_normal_scalar
            else:
                self.__log_normal = self.__log_normal_multi

            if self.weights_prior == 'potts':
		self.__log_likelihood = self.__log_pseudo_likelihood
	    else:
		self.__log_likelihood = self.__log_likelihood_std
		

        if 'regressors' in kwargs:
            if self.dseries == 1:
                raise NameError("Regressors option currently not allowed for \
                                multivariate mixture.")

            
            self.regressors_ind = True

            if type(kwargs['regressors']) != type([]):
                self.xmat = kwargs['regressors']
                if self.xmat.ndim == 1:
                    self.xmat = self.xmat.reshape(self.nobs, 1)
                self.nreg = self.xmat.shape[1]
                self.betaubar = np.zeros(self.nreg)
                self.vubar = np.zeros((self.nreg, self.nreg), order = 'F')

            else:
                self.xmat = kwargs['regressors'][0]
                self.nreg = self.xmat.shape[1]
                self.prior = kwargs['regressors'][1]
                self.betaubar = self.prior[1]
                self.vubar = self.prior[2]

            assert self.xmat.shape[0] == self.nobs
            self.ystar = np.zeros(self.nobs)
            self.vobar = np.zeros((self.nreg, self.nreg), order = 'F')
            self.xxp = np.zeros((self.nreg, self.nreg, self.nobs), order = 'F')
            mm.calcxxp(self.xxp, self.xmat)

        else:
            self.regressors_ind = False

        if 'prior_mean_scale' in kwargs:
            #converts nuubar and subar from scalars to vectors if necessary.
            prior = kwargs['prior_mean_scale']
            if prior[0] == 'normal_inverted_gamma':
                self.nuubar = self.check_scalar(prior[1])
                self.mjubar = self.check_scalar(prior[4])
                self.nj = np.zeros(self.nmix)
                if self.dseries == 1:
                    #univariate mixture
                    self.subar = self.check_scalar(prior[2])
                    self.alphaubar = self.check_scalar(prior[3]) 
                    self.ybarj = np.zeros(self.nmix)
                    self.__simsigma = self.__simsigma_NIG
                    self.__simalpha = self.__simalpha_NIG
                else:
                    #multivariate mixture
                    self.subar = self.check_matrix(prior[2])
                    self.alphaubar = self.check_vector(prior[3])
                    self.ybarj = np.ybarj(self.dseries, self.nmix)
                    self.__simsigma = self.__simsigma_NW
                    self.__simalpha = self.__simalpha_NW

            else:
                #We only allow this prior for the univariate case
                try:
                    assert self.dseries == 1
                except:
                    raise NameError("Don't allow this prior for Multivariate \
                                    case")
                                    
                self.nuubar = self.check_scalar(prior[1])
                self.subar = self.check_scalar(prior[2])
                self.alphaubar = self.check_scalar(prior[3]) 
                self.vubar = self.check_scalar(prior[4])
                self.rvec = np.zeros(self.nobs)
                self.__simsigma = self.__simsigma_ind_NIG
                self.__simalpha = self.__simalpha_ind_NIG
        else:
            #default prior specification
            self.mjubar = np.ones(self.nmix)* 5
            self.nj = np.zeros(self.nmix)

            if self.dseries == 1:
                #univariate case
                self.ybarj = np.zeros(self.nmix)
                self.nuubar = np.ones(self.nmix) * 10
                self.subar = np.ones(self.nmix) * 0.01
                self.alphaubar = self.ymat.mean() * np.ones(self.nmix)
                self.__simsigma = self.__simsigma_NIG
                self.__simalpha = self.__simalpha_NIG
            else:
                #multivariate case
                self.work = np.zeros((self.dseries, 2), order = 'F')
                self.ybarj = np.zeros((self.dseries, self.nmix), order = 'F')
                self.sumysq = np.zeros((self.dseries, self.dseries), order = 'F')
                self.nuubar = 6 * np.ones(self.nmix) #* (self.dseries + 2)
                subar = np.linalg.inv(np.cov(self.ymat))*2 / (3)
                self.subar = np.repeat(subar, self.nmix).reshape(self.dseries,
                                                                 self.dseries,
                                                                 self.nmix)
                self.alphaubar = np.column_stack([self.ymat.mean(axis = 1)] * self.nmix)


                #Define class for Wishart
                self.sim_wishart = SampleWishart(self.dseries)

                #Define work function for simulating the mixture
                #scale and mean parameters
                self.__simsigma = self.__simsigma_NW
                self.__simalpha = self.__simalpha_NW
                
                
	self.evec = np.zeros(self.nobs, dtype = 'i')
	#self.evec = np.ones(self.nobs, dtype = 'i')*(label-1)
        #print self.evec.shape
        #print self.evec
        self.logp = np.zeros((self.nmix, self.nobs), order = 'F')
        self.pobar = np.zeros((self.nmix, self.nobs), order = 'F')
        self.nuobar = np.zeros(self.nmix)
        self.randu = np.zeros(self.nobs)
        if self.dseries == 1:
            #univariate case
            self.sobar = np.zeros(self.nmix)
        else:
            #multivariate case
            self.logdet_sobar = np.zeros(self.nmix)
            self.sobar = np.zeros((self.dseries, self.dseries, self.nmix))

        #stores order of means  for current iterations
        self.order = np.zeros(self.nmix, dtype = 'i')

        #code to set up mcmc sampling scheme
        if self.regressors_ind:
            breg = LinearModel(ymat, self.xmat)
            init_sig, init_beta = breg.posterior_mean()
            init_sig = np.tile(init_sig, nmix)
        else:
            if self.dseries == 1:
                #univariate case
                init_sig = np.tile(np.std(ymat), nmix)
            else:
                #multivate case
                #note sig here refers to the precision
                subar = np.linalg.inv(np.cov(self.ymat) * 0.75)
                init_sig = np.repeat(subar, self.nmix).reshape(self.dseries,
                                                                 self.dseries,
                                                                 self.nmix)
        if 'initial_sigma' in kwargs:
            try:
                assert kwargs['initial_sigma'].shape == init_sig.shape
            except:
                error = "Dimension of initial sigma is incorrect."
                raise AssertionError(error)

            init_sig = kwargs['initial_sigma']

	centroids, label = kmeans2(ymat,nmix)
	start_values_alpha = centroids.T
        print "Starting alpha"

        if self.dseries == 1:
            #univariate case
            #init_alpha = np.tile(np.mean(ymat), nmix)
	    init_alpha = start_values_alpha
                        
        else:
            #multivate case
            init_alpha = start_values_alpha
            
            #init_alpha = np.column_stack([self.ymat.mean(axis = 1)] * self.nmix)
        print init_alpha

        if 'initial_alpha' in kwargs:
	    
            try:
                assert kwargs['initial_alpha'].shape == init_alpha.shape
            except:
                error = "Dimension of initial alpha is incorrect."
                raise AssertionError(error)

            init_alpha = kwargs['initial_alpha']
                
            

            

        init_p = np.tile(1./nmix, nmix)

        blocks = []

        sampleevec = CFsampler(self.simevec, np.zeros(self.nobs, dtype = 'i'),
                               'evec', store = 'none')
        blocks.append(sampleevec)

        if 'runtime_output' in kwargs:
            RO = kwargs['runtime_output']
        else:
            RO = False

        if self.regressors_ind:
            samplebeta = CFsampler(self.simbeta, init_beta, 'beta')
            blocks.append(samplebeta)
        
        sample_sigma_alpha = CFsampler(self.sample_sigma_alpha,
                                   [init_sig, init_alpha], [ 'sigma', 'alpha'])
        blocks.append(sample_sigma_alpha)

        if self.weights_prior == 'dirichlet':
            samplep = CFsampler(self.simp, init_p, 'p')
            blocks.append(samplep)
            transform = {'sigma': self.__transform_sigma,
                         'p': self.__transform_p,
                         'alpha': self.__transform_alpha}

        if self.weights_prior == 'potts':
            init_phi = (self.phi_max - self.phi_min) / 2.
            samplephi = RWMH(self.log_posterior_phi, 0.2,  init_phi, 'phi',
                             adaptive =  'GFS')
            calculate_p = CFsampler(self.calc_p,
                                    np.zeros((self.nobs, self.nmix)),
                                    'p', store = 'none')
            blocks.append(samplephi)
            blocks.append(calculate_p)

            transform = {'sigma': self.__transform_sigma,
                         'alpha': self.__transform_alpha,
                         'p': self.__transform_psp}

        data = {'ymat': self.ymat}

        #number of parameters
        npa = self.nmix * (1 + self.dseries + self.dseries + self.dseries *\
                         (self.dseries + 1) / 2)
        if self.weights_prior == 'potts':
            npa = 1
        loglike = (self.log_likelihood, npa, 'ymat')
        self.mcmc = MCMC(nit, burn, data, blocks, transform = transform,
                        runtime_output = RO, loglike = loglike)

    def check_scalar(self, x):
        x = np.atleast_1d(x)
        if x.shape[0] == 1:
            return np.tile(x, self.nmix)
        else:
            assert x.shape[0] == self.nmix
            return x

    def check_vector(self, x):
        x = np.atleast_1d(x)
        if x.ndim == 1:
            p = x.shape[0]
            assert p == self.dseries
            x = np.repeat(x[:,np.newaxis], self.nmix).reshape(p,self.nmix)
        else:
            assert x.shape[0] == self.dseries
            assert x.shape[0] == self.nmix
            return x

    def check_matrix(self, X):
        X = np.atleast_2d(X)
        p = X.shape[0]
        if X.shape[2] == 1:
            return np.repeat(X, self.nmix).reshape(p, p, self.nobs)
        else:
            assert X.shape[2] == self.nmix
            return X

    def compute(self):
        self.mcmc.sampler()
        self.compute_ind = True

    def output(self, **kwargs):
        if self.compute_ind == False:
            self.compute()

        self.mcmc.output(**kwargs)


    def CODAoutput(self, **kwargs):
        self.mcmc.CODAoutput(**kwargs)

    def plot(self, name, **kwargs):
        self.mcmc.plot(name, **kwargs)

    def get_mean_var(self, name):
        return self.mcmc.get_mean_var(name)

    def get_parameter_exburn(self, name):
        """Returns an array of the parameter iterates excluding burnin"""
        return self.mcmc.get_parameter_exburn(name)

    def get_parameter(self, name):
        """Returns an array of the parameter iterates including burnin"""
        return self.mcmc.get_parameter(name)
        
    def __correct_order(self, x):
        """function imposes identifcation restrictions on mixture model
        by re-ordering the parameters following the means"""

        if self.dseries == 1:
            self.order = x.argsort()
            
        else:
            #normvec = np.array([np.linalg.norm(alpha[:,i]) for i in xrange(self.nmix)])
            #self.order = normvec.argsort()
            self.order = x.argsort()
            raise NotImplementedError()
            


    def __transform_alpha(self, store):
        if self.dseries == 1:
            return store['alpha'][self.order]
        
        return store['alpha'][:, self.order]

    def __transform_p(self, store):
        return store['p'][self.order]

    def __transform_psp(self, store):
        return store['p'][:, self.order]

    def __transform_sigma(self, store):
        
        if self.dseries == 1:
            return store['sigma'][self.order]
        
        return store['sigma'][:,:,self.order]

    
    def calc_p(self, store):
        return self.pobar.T


    def simevec(self, store):
        """
        function samples the allocation vector evec from its
        full conditional posterior distribution.

        arguments:
            store - dictionary class that is automatically passed to functions
                    that are called from PyMCMC.
        """

        if self.regressors_ind:
            self.ystar = self.ymat - np.dot(self.xmat, store['beta'])
        else:
            self.ystar = self.ymat

        self.randu = np.random.rand(self.nobs)

        if self.weights_prior == 'dirichlet':
            if self.dseries == 1:
                #univariate case
                mm.sim_evec(self.evec, self.randu, self.ystar, self.logp, store['alpha'],
                store['sigma'], self.pobar, np.log(store['p']))
            else:
                #multivariate case
                mm.sim_evec_m(self.evec, self.randu, self.ystar, self.logp,
                              store['alpha'], store['sigma'], self.logdet_sobar,
                              self.pobar, np.log(store['p']), self.work)


        elif self.weights_prior == 'potts':
            if self.dseries == 1:
            	mm.neighbj(self.neigh_mat, self.evec, self.num_neighbours, 
                           self.index_neighbours)

            	mm.sim_evec_sp(self.evec, self.randu, self.ystar, self.logp, store['alpha'],
                      store['sigma'], self.pobar, self.neigh_mat, store['phi'])
	    else:
		# multivariate case
		mm.neighbj(self.neigh_mat, self.evec, self.num_neighbours, 
                           self.index_neighbours)

            	mm.sim_evec_spmv(self.evec, self.randu, self.ystar, self.logp, store['alpha'],
                          store['sigma'], self.pobar, self.neigh_mat, store['phi'],
                          self.logdet_sobar, self.work)


        else:
            print "Error; no potts and dirichlet are the only options"
            sys.exit(0)


        return self.evec

    def simbeta(self, store):
        """
        function samples beta from its full conditional posterior
        distribution.

        arguments:
            store - dictionary class that is automatically passed to functions
                    that are called from PyMCMC.
        """


        #self.sigsqj = store['sigma'][store['evec']] ** 2
        self.vobar = np.zeros((self.nreg, self.nreg), order = 'F')
        mm.calcvobar(self.vubar, self.vobar, self.xxp, 1. / store['sigma'] ** 2,
                    self.evec)
        vbubar = np.dot(self.vubar, self.betaubar)

        xstar = np.zeros(self.nreg)
        xpy = np.zeros(self.nreg)
        mm.calcxpy(xpy,self.ymat, self.xmat, xstar, store['alpha'],
                   1.0 / store['sigma'] ** 2, self.evec)

        #self.ystar = (self.ymat - store['alpha'][store['evec']]) / self.sigsqj
        #xstar = self.xmat * self.ystar.reshape(self.nobs, 1)
        #xpy = np.sum(xstar, axis = 0)
        vbobar = vbubar + xpy
        bobar = np.linalg.solve(self.vobar, vbobar)
        cholvobar = np.linalg.cholesky(self.vobar)
        bsim = bobar + np.linalg.solve(cholvobar.T, np.random.randn(self.nreg))
        return bsim

    def sample_sigma_alpha(self, store):
        """This function is used to sample sigma and alpha

        arguments:
            store - dictionary class that is automatically passed to functions
                    that are called from PyMCMC.
        """

        sigma = self.__simsigma(store)
        store['sigma'] = sigma
        alpha = self.__simalpha(store)

        if self.dseries == 1:
            if self.ls_flag == 'stupid_method':
                self.__correct_order(alpha)
            else:
                self.order = self.LSCW.compute(store)

        return sigma, alpha 


    def __simsigma_ind_NIG(self, store):
        """
        function samples sigma from its full conditional posterior
        distribution. This assumes an independendent normal inverted gamma prior

        arguments:
            store - dictionary class that is automatically passed to functions
                    that are called from PyMCMC.
        """

        self.nuobar = self.nuubar + \
                np.array([np.sum(store['evec'] == i) for i in xrange(self.nmix)])
        if self.regressors_ind:
            mm.calcsobarr(self.rvec,self.ymat, store['evec'], np.dot(self.xmat,
                         store['beta']), store['alpha'], self.subar, self.sobar)

        else:
            mm.calcsobar(self.rvec, self.ymat, store['evec'], store['alpha'],
                         self.subar, self.sobar)

        return 1. / np.sqrt(np.random.gamma(self.nuobar / 2., 2. / self.sobar))

    def __simsigma_NIG(self, store):
        """
        function samples sigma from its full conditional posterior
        distribution. This assumes an normal inverted gamma prior

        arguments:
            store - dictionary class that is automatically passed to functions
                    that are called from PyMCMC.
        """

        if self.regressors_ind:
            ymat = self.ymat - np.dot(self.xmat, store['beta'])
        else:
            ymat = self.ymat

        mm.calcsobar2(ymat, self.ybarj, self.nj, store['evec'],
                     self.subar, self.sobar,  self.alphaubar, self.mjubar)

        self.nuobar = self.nuubar + self.nj + 1
        if any(np.isnan(self.sobar) == True):
            pdb.set_trace()
                
        return 1. / np.sqrt(np.random.gamma(self.nuobar / 2., 2. / self.sobar))

    def __simsigma_NW(self,store):
        """
        Function samples precision for the multivariate normal mixture from
        its full conditional posterior distribution.
    
        arguments:
            store - dictionary class that is automatically passed to functions
                    that are called from PyMCMC.
        """

        
        mm.calcsobarm(self.ymat, self.ybarj, self.nj, store['evec'], self.subar, self.sobar,
                      self.alphaubar, self.sumysq, self.mjubar) 

        self.nuobar = self.nuubar + self.nj

        
        
        for i in xrange(self.nmix):
            store['sigma'][:,:,i] = self.sim_wishart.sample(self.nuobar[i],
                                                     self.sobar[:,:,i])

            #compute log determinant
            S = store['sigma'][:,:,i]
            self.logdet_sobar[i] = 2.* np.sum(np.diag(np.linalg.cholesky(S)))
        

        return store['sigma']



    def __simalpha_ind_NIG(self, store):
        """
        function samples alpha from its full conditional posterior
        distribution. This function assumes an independent normal inverted gamma
        prior

        arguments:
            store - dictionary class that is automatically passed to functions
                    that are called from PyMCMC.
        """
        vobar = np.zeros((self.nmix, self.nmix), order = 'F')
        vaubar = self.vubar * self.alphaubar
        vaobar = np.zeros(self.nmix)
        if self.regressors_ind:
            ymat = self.ymat - np.dot(self.xmat, store['beta'])
        else:
            ymat = self.ymat

        #sigjsq = store['sigma'][store['evec']] ** 2
        mm.calcvobara(self.vubar, vobar, store['evec'], store['sigma'] ** 2)
        
        mm.calcvbobara(vaubar, vaobar, store['sigma'] ** 2, store['evec'], ymat)
        alphaubar = np.linalg.solve(vobar, vaobar)
        alphasim = alphaubar + np.linalg.solve(np.linalg.cholesky(vobar).T, np.random.randn(self.nmix))
        if self.dseries == 1:
            if self.ls_flag == 'stupid_method':
                self.__correct_order(alphasim)
            else:
                self.order = self.LSCW.compute(store)

        return alphasim

    def __simalpha_NIG(self, store):
        """
        function samples alpha from its full conditional posterior
        distribution. This function assumes an normal inverted gamma
        prior.

        arguments:
            store - dictionary class that is automatically passed to functions
                    that are called from PyMCMC.
        """

        meanalpha = (self.mjubar * self.alphaubar + self.nj * self.ybarj)
        denom = self.nj + self.mjubar
        meanalpha = meanalpha / denom
        sigalpha = store['sigma'] / np.sqrt(denom)
        return meanalpha + sigalpha * np.random.randn(self.nmix)

    def __simalpha_NW(self, store):
        """
        Function samples alpha from its full conditional posterior
        distribution. This function assumes a n normal-Wishart
        prior.

        
        arguments:
            store - dictionary class that is automatically passed to functions
                    that are called from PyMCMC.
        """
        
        meanalpha = (self.mjubar * self.alphaubar + self.nj * self.ybarj)
        denom = (self.nj + self.mjubar).astype('float')
        meanalpha = meanalpha / denom

        #print "Allocated to each group"
        #print self.nj
        #print "Alpha mean is"
        #print meanalpha
        #print "y mean is"
        #print self.ybarj
        #print "Prior means are"
        #print self.alphaubar
        
        
        for i in xrange(self.nmix):
            
            store['alpha'][:, i] = meanalpha[:,i] + \
                np.linalg.solve(np.linalg.cholesky(store['sigma'][:,:,i].T * denom[i]),
                                np.random.randn(self.dseries))

        self.order = self.LSCW.compute(store) 
  
        
        return store['alpha']
        



    def simp(self, store):
        pobar = self.pubar + np.array([np.sum(store['evec'] == i) for i in xrange(self.nmix)])
        
        p = np.random.dirichlet(pobar)
        if self.dseries > 1:
            assert self.ls_flag == 'CronWest'
            self.order = self.LSCW.compute(store)
        return p
	   

    def potts_p(self, store):
        """Computes weighted neighbourhood for potts model"""

        mm.neighbj(self.pobar, self.evec, self.num_neighbours, self.index_neighbours)

    def __log_normal_scalar(self, store):
        """Function returns log probability of univariate normal."""
        n = self.ymat.shape[0]
        for i in xrange(self.nmix):
            res = self.ymat - store['alpha'][i]
            sigma = store['sigma'][i] 
            self.__cw_store_prob[i] = \
                    -0.5 * (np.log(sigma * sigma) * n + np.dot(res, res)\
                            / sigma ** 2 + \
                           np.log(2*np.pi) * n) \
                    + np.log(store['p'][i])

    def __log_normal_multi(self, store):
        """Function returns log probability of multivariate normal."""

        #calls fortran function for the multivariate normal
        for i in xrange(self.nmix):
            self.__cw_store_prob[i] = mm.log_normm_f(self.ymat,
                    store['alpha'][:, i],
                    np.linalg.cholesky(store['sigma'][:, :, i]),
                    self.__cw_work) + np.log(store['p'][i]) - \
                    0.5 * self.ymat.size * np.log(2. * np.pi)


    def __log_likelihood_std(self, store):
        """Function computes the log likelihood function for the standard
        mixture model."""

        self.__log_normal(store)
        #sum of logs
        maxp = self.__cw_store_prob.max()
        sumlog = np.log(np.exp(self.__cw_store_prob - maxp).sum()) + maxp
        
        return sumlog

    def log_likelihood(self, store):
        """Function returns the log-likelihood for the non-spatial 
        mixture model and returns the pseduo log likelihood for the
        spatial mixture model."""

        return self.__log_likelihood(store)


    def __log_pseudo_likelihood(self, store):
        """function computes the log-pseudo-likelihood for the potts model"""

        return mm.pseudolike(self.neigh_mat, store['evec'], store['phi'])

    def log_posterior_phi(self, store):
        """This function returns the log posterior probability for phi"""

        if store['phi'] > self.phi_min and store['phi'] < self.phi_max:
            return self.__log_pseudo_likelihood(store)
        else:
            return -1E256


