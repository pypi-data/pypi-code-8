#Main Algorithms for PyMCMC - A Python package for Bayesian estimation
#Copyright (C) 2010  Chris Strickland

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.# MCMC routines



import warnings
warnings.filterwarnings('ignore', '.*')

import pdb
import copy
import types
import multiprocessing
from copy import deepcopy
from collections import deque

import scipy as sp
import numpy as np


from mcmcplots import *
from mcmc_utilities import *



class Attributes:
    """Class contains parameter attributes and statistics.
    Used by BaseSampler""" 

    def __init__(self, init_theta, name):
        self.ltheta = copy.deepcopy(init_theta)
        self.calculatestats = False
        self.seq_count = 1 #counter used in computing statistics sequentially
        if type(init_theta) in [types.FloatType, types.IntType, np.float64]:
            #scalar types
            self.nparam = [1]
            self.mean_theta = 0.
            self.var_theta = 0.
            #note used in calculation of autocorrelation
            #self.first_theta = 0.
            #self.lag_theta = 0.
            #self.cross_theta = 0.

        elif type(init_theta) == np.ndarray:
            #array type
            self.nparam = list(init_theta.shape)
            if init_theta.ndim <= 3:
                self.mean_theta = np.zeros(init_theta.shape)
                self.var_theta = np.zeros(init_theta.shape)
                #self.first_theta 
                #self.lag_theta = np.zeros(init_theta.shape[0])
                #self.cross_theta = np.zeros(init_theta.shape[0])

            else:
                error = 'Parameters 3D maximum, ' + name + ' is ' + \
                        str(init_theta.ndim) + ' dimensional.'
                
                raise NameError(error)
        else:
            print "error", name

        self.name = name #name of parameter
        self.transformed = {}
        self.update_stats = self.__update_stats_std
        #self.index_auto = False
        self.store = None


    def get_nparam(self):
        """returns the number of parameters being sampled in the block"""
        return self.nparam

    def get_name(self):
        """returns the name of the parameters being sampled in the block"""
        return self.name

    def get_store(self):
        """Returns 'all' or 'none' representing the storage
        in the group case"""

        return self.store

        

    def __update_stats_std(self):
        """used to update the posterior mean and variance at each iteration"""
        #self.mean_theta = self.mean_theta + self.ltheta
        #self.var_theta = self.var_theta + self.ltheta ** 2

        #More accurate way to compute mean and variance sequentially
        self.var_theta += float(self.seq_count - 1) * \
                (self.ltheta - self.mean_theta) ** 2 / (self.seq_count)
        self.mean_theta += (self.ltheta - self.mean_theta) / self.seq_count
        self.seq_count += 1

        #if self.index_auto == False: 
        #    self.lag_theta = self.ltheta
        #    self.index_auto = True
        #else:
        #    self.first_theta = self.ltheta
        #    self.lag_theta = self.ltheta
        #    self.update_stats = self.__update_stats_std_post
    
    def __update_stats_std_post(self):
        """used to update the posterior mean and variance at each iteration"""
        #self.mean_theta = self.mean_theta + self.ltheta
        #self.var_theta = self.var_theta + self.ltheta**2
        #More accurate way to compute mean and variance sequentially
        self.var_theta += float(self.seq_count - 1) * \
                (self.ltheta - self.mean_theta) / (self.seq_count)
        self.mean_theta += (self.ltheta - self.mean_theta) / self.seq_count
        self.seq_count += 1
        #self.cross_theta = self.cross_theta +  self.ltheta * self.lag_theta
        self.lag_theta = self.ltheta

    def __update_stats_transformed(self):
        theta = self.transformed[self.name]
        #self.mean_theta = self.mean_theta + theta
        #self.var_theta = self.var_theta + theta**2
        #More accurate way to compute mean and variance sequentially
        self.var_theta += float(self.seq_count - 1) * \
                (theta - self.mean_theta) ** 2 / (self.seq_count)
        self.mean_theta += (theta - self.mean_theta) / self.seq_count
        self.seq_count += 1
        #if self.index_auto == False:
        #    self.lag_theta = theta
        #    self.index_auto = True
        #else:
        #    self.first_theta = theta
        #    self.lag_theta = theta
        #    self.update_stats = self.__update_stats_transformed_post

    def __update_stats_transformed_post(self):
        theta = self.transformed[self.name]
        #self.mean_theta = self.mean_theta + theta
        #self.var_theta = self.var_theta + theta**2

        #More accurate way to compute mean and variance sequentially
        self.var_theta += float(self.seq_count - 1) * \
                (theta - self.mean_theta) ** 2 / (self.seq_count)
        self.mean_theta += (theta - self.mean_theta)  / self.seq_count
        self.seq_count += 1
        #self.cross_theta = self.cross_theta + self.lag_theta * theta
        self.lag_theta = theta

    def update_transformed(self, transformed):
        self.transformed = transformed

    def use_transformed(self):
        self.update_stats = self.__update_stats_transformed


    def calculate_stats(self, nit, burn):
        """Procedures caalculates estimates of the marginal posterior mean
        and variance for
        the MCMC estimation. The function arguments are:
        nit - thet number of iterations
        burn - is the length of the burn in
        """
        
        #calculate rho
        #nstar = float(nit - burn - 1)
        #lag_mean = (self.mean_theta - self.lag_theta) / nstar
        #lead_mean = (self.mean_theta - self.first_theta) / nstar
        #xx = self.var_theta - self.lag_theta ** 2
       # 

        #rho = (self.cross_theta - nstar * lag_mean * lead_mean) / \
        #    (xx - nstar * lag_mean ** 2)
        #print self.cross_theta
        #print nstar + 1
        #print rho


        #calculate mean and variance
        
        self.mean_theta = self.mean_theta
        #self.var_theta = self.var_theta - float(nit - burn) * self.mean_theta**2
        self.var_theta = self.var_theta/float(nit - burn - 1)



    def get_stats(self, nit, burn):
        """Procedure returns estimates of the marginal
        posterior mean and variance for
        the MCMC estimation. The function arguments are:
        nit - thet number of iterations
        burn - is the length of the burn in
        """
        
        if self.calculatestats == False:
            self.calculate_stats(nit, burn)

        self.calculatestats = True
        return self.mean_theta, self.var_theta


class BaseSampler:
    """
    
    The base class for samplers used by class MCMC.

    Arguments:
      init_theta - is the initial value for the parameters of interest
      name - is the name of the parameters of interest
      kwargs - optional parameters:
        store - 'all'; (default) stores every iterate for parameter of
                interest
              - 'none'; do not store any of the iterates
        output - list; provide an index in the form of a list for
                       the parameters to be
                       that output is to be provide for. If not
                       provided print all of
                       theta               
        fixed_parameter - Is used if the user wants to fix the parameter
        value that is returned. This is used for testing. This is used for testing MCMC sampling schemes.
        label - If the user wants to replace the automatic name for each element in theta with
                 user defined names. The names should be in the form of a list. 
                 Eg: ['car', 'bus', 'train']

        exit_function - Function takes store as argument and as excuted after
                        sample function in inherited class.
        entry_function - Function takes store as argument and is executed
                        before sample function in inherited class
    """

    def __init__ (self, init_theta, name, **kwargs):

        #ensure that name is either a string or a list
        try:
            assert type(name) in [types.StringType, type([])]
        except:
            print "name, type = ", name, type(name)
            error = "Name must be of type string or list"
            raise TypeError(error)

        if type(name) != type([]):
            #name is of type string
            self.attrib = Attributes(init_theta, name)
            self.mblock_ind = False
            self.number_groups = 1
            self.ind_list = False
            self.nparam = self.attrib.get_nparam()

            if 'label' in kwargs:
                self.label = kwargs['label']
            else:
                self.label = None

        else:
            #Name is of type list
            self.ind_list = True
            assert type(init_theta) == type([])
            assert len(init_theta) == len(name)
            if 'fixed_parameter' in kwargs and \
               kwargs['fixed_parameter'] != None:
                assert type(kwargs['fixed_parameter']) == type([]) 
                assert len(kwargs['fixed_parameter']) == len(name) 
            self.attrib = []
            self.nparam = []
            self.mblock_ind = True
            self.number_groups = len(name)
            self.ltheta = []
            for i in xrange(len(name)):
                self.attrib.append(Attributes(init_theta[i], name[i]))
                self.nparam.append(self.attrib[i].get_nparam())
                self.ltheta.append(init_theta[i])


        if 'fixed_parameter' in kwargs and\
                kwargs['fixed_parameter'] != None:
            self.fixed_parameter = kwargs['fixed_parameter']
            self.sample = self.__sample_fixed_parameter
            self.update_ltheta(self.fixed_parameter)
            self.accept = 1
            self.count = 1
        else:
            self.sample = self.sampler
            self.accept = 0
            self.count = 0
           
        self.name = name
        
        if 'store' in kwargs.keys():
            self.store = kwargs['store']
            #Allow for group option check groups are of the correct type
            if type(self.store) == type([]):
                dum = self.store
                for i in self.store:
                    if i not in ['all', 'none']:
                        dum = 'all'
                self.store = dum
                try:
                    assert len(self.store) == self.number_groups
                except:
                    error = "Miss-specification of store argument for" \
                            + self.name
                    raise Exception(error)

            #self.store should be a string
            else:
                if self.store not in ['all', 'none']:
                    self.store ='all'
        else:
            self.store ='all'

        if self.number_groups > 1:
            #make sure self.store is a list
            if type(self.store) != type([]):
                self.store = [self.store for i in xrange(self.number_groups)]
                for i, store in enumerate(self.store):
                    self.attrib[i].store = store


        

        if self.ind_list == False:
            self.update_stats = self.__update_stats_ng
            self.update_transformed = self.__update_transformed

        else:
            self.update_stats = self.__update_stats_g
            self.update_transformed = self.__update_transformed_groups

        if 'index' in kwargs:
            self.index = kwargs['index']
        else:
            self.index = 0

        if 'exit_function' in kwargs and kwargs['exit_function'] != None:
            self.exit_function = kwargs['exit_function']
        else:
            self.exit_function = self.__dummy_exit_function

        if 'entry_function' in kwargs and kwargs['entry_function'] != None:
            self.entry_function = kwargs['entry_function']
        else:
            self.entry_function = self.__dummy_entry_function

        #stores whether last value was accepted for block
        #Note default True
        self.last_accept = True

    def __dummy_exit_function(self, store):
        """Dummy exit function, does nothing."""
        pass

    def __dummy_entry_function(self, store):
        """Dummy entry function, does nothing."""
        pass

    def get_last_accept(self):
        """returns whether or not the last candidate was accepted."""

        return self.last_accept

    
    def get_ltheta(self):
        if self.ind_list == False:
            return self.attrib.ltheta
        else:
            for i in xrange(self.number_groups):
                self.ltheta[i] = self.attrib[i].ltheta
            return self.ltheta

    def update_ltheta(self, ltheta):
        if self.ind_list == False:
            self.attrib.ltheta = ltheta
        else:
            for i in xrange(self.number_groups):
                self.attrib[i].ltheta = ltheta[i]


    def get_number_groups(self):
        return self.number_groups

    def get_label(self):
        return self.label
    
    def __sample_fixed_parameter(self, store):
        return self.fixed_parameter
        
    def acceptance_rate(self):
        """returns the acceptance rate for the MCMC sampler"""
        return float(self.accept)/self.count

    def get_nparam(self):
        """returns the number of parameters being sampled in the block"""
        return self.nparam

    def get_name(self):
        """returns the name of the parameters being sampled in the block"""
        return self.name

    def get_index(self):
        return self.index

    def __update_stats_ng(self):
        self.attrib.update_stats()

    def __update_stats_g(self):
        for i in xrange(self.number_groups):
            self.attrib[i].update_stats()

    def __update_transformed(self, transformed):
        self.attrib.update_transformed(transformed)

    def __update_transformed_groups(self, transformed):
        for i in xrange(self.number_groups):
            self.attrib[i].update_transformed(transformed)

    def use_transformed(self, names):
        if self.ind_list == False:
            self.attrib.use_transformed()
        else:
            for i in xrange(self.number_groups):
                name = self.attrib[i].get_name()
                if name in names:
                    self.attrib[i].use_transformed()
            

    def calculate_stats(self, nit, burn):
        """Procedures cancules estimates of the marginal posterior mean and variance for
        the MCMC estimation. The function arguments are:
        nit - the number of iterations
        burn - is the length of the burn in
        """
        
        if self.mblock_ind == False:
            self.attrib.calculate_stats(nit, burn)

        else:
            for i in xrange(len(self.name)):
                self.attrib[i].calculate_stats(nit, burn)

    def get_stats(self, nit, burn):
        """Procedure returns estimates of the marginal posterior mean and variance for
        the MCMC estimation. The function arguments are:
        nit - thet number of iterations
        burn - is the length of the burn in
        """
        
        if self.mblock_ind == False:
            return self.attrib.get_stats(nit, burn)

        else:
            meanv = []
            varv = []
            for i in xrange(len(self.name)):
                meani, vari = self.attrib[i].get_stats(nit, burn)
                meanv.append(meani)
                varv.append(vari)

            return meanv, varv


   
    def get_store(self):
        return self.store



class CFsampler(BaseSampler):
    """
    CFsampler is used to sample from closed form solutions in the MCMC sampler.
    arguments:
    func - is a function that samples from the posterior distribution of interest
    init_theta - is an initial value for theta (parameters of
    interest)
    name - name of theta
    kwargs - optional parameters:
        store - 'all'; (default) stores every iterate for parameter of
                interest
              - 'none'; do not store any of the iterates
        output - list; provide an index in the form of a list for the parameters to be
                       that output is to be provide for. If not provided print all of
                       theta               
        additional_output - function that produces additional output.                
        fixed_parameter - Is used is the user wants to fix the parameter
        value that is returned. This is used for testing.
        additional_arguments - Is used if specifical additional arguments are
                               required for the function call. In this case
                               func should take two arguments; store and a
                               list of additional arguments. That is
                               func(store, list_args), should be the function
                               signature. Note that additional_arguments =
                               list_args is how the arguments should be passed
                               into CFsampler.

        custom_acceptance - Is used if the 'func' called from CFsampler is
                            not for a closed form solution and is a function
                            which requires an acceptance rate. The function
                            custom_acceptance should be a function that
                            returns the increment required to update both
                            count nnd accept.

        """

    def __init__(self, func, init_theta, name, **kwargs):
        BaseSampler.__init__(self, init_theta, name, **kwargs)
        self.func = func
        self.accept = 1
        self.count = 1
        
        if 'additional_arguments' in kwargs:
            self.list_args = kwargs['additional_arguments']  # Extract list
            assert type(self.list_args) == type([])   # Must be a list
            self.__sampler = self.__aug_sampler  # Define function to use
        else:
            self.__sampler = self.__std_sampler 
        
        
        if 'custom_acceptance' in kwargs:            
            self.__update_accept_count = kwargs['custom_acceptance']
            self.update_accept_count = True
        else:
            self.update_accept_count = False
        

    def sampler(self, store):
        """returns a sample from the defined sampler"""
        self.__sampler(store)        
        if self.update_accept_count == True:
            inc_accept, inc_count = self.__update_accept_count(store)
            self.accept = self.accept + inc_accept
            self.count = self.count + inc_count
        return self.get_ltheta()

    def __std_sampler(self, store):
        self.update_ltheta(self.func(store))

    def __aug_sampler(self, store):  
        self.update_ltheta(self.func(store, self.list_args))
    

class SliceSampler(BaseSampler):
    """SliceSampler is a class that can be used for the slice sampler 
    func - k dimensitonal list containing log functions
    init_theta - float used to initialise slice sampler.
    ssize - is a user defined value for the typical slice size
    sN - is an integer limiting slice size to sN * ssize 
    **kwargs - optional arguments
        store - 'all'; (default) stores every iterate for parameter of
        interest
              - 'none'; do not store any of the iterates
        fixed_parameter - Is used is the user wants to fix the parameter
        value that is returned. This is used for testing.
        additional_arguments - Is used if specifical additional arguments are
                               required for the function call. In this case
                               func should take two arguments; store and a
                               list of additional arguments. That is
                               func(store, list_args), should be the function
                               signiture. Note that additional_arguments =
                               list_args is how the arguments should be passed
                               into CFsampler.

    """
    def __init__(self, func, ssize, sN, init_theta, name, **kwargs):
        BaseSampler.__init__(self, init_theta, name, **kwargs)
        try:
            self.init_theta = float(init_theta)
            self.ssize = ssize
            self.accept = 1
            self.count = 1
            self.sN = sN
            if type(func) == type([]):
                self.func = func
                self.k = len(func)
            else:
                self.k = 1
                self.func = [func]
            self.omega = np.zeros(self.k)
        except TypeError:
            raise TypeError("Error: SliceSampler is only used to sample scalars")
        
        if 'additional_arguments' in kwargs:
            self.list_args = kwargs['additional_arguments']
            assert type(self.list_args) == type([])
            self.__func = self.__aug_func
        else:
            self.__func = self.__std_func

    def __std_func(self, i, store):
        return self.func[i](store)

    def __aug_func(self, i, store):
        return self.func[i](store, self.list_args)

    def sampler(self, store): 
        # self.omega = [np.exp(function(self.ltheta)) * np.random.rand(1, 1)[0] for function in func]
        for i in xrange(self.k):
            store[self.attrib.name] = self.get_ltheta()
            self.omega[i] = self.__func(i, store) + np.log(np.random.rand(1)[0])
        bounds = np.array([self.__step_out(i, store) for i in xrange(self.k)])
        max_lower = bounds[:, 0].max()
        min_upper = bounds[:, 1].min()
        return self.__pick_by_shrink(max_lower, min_upper, store)

    def __pick_by_shrink(self, max_lower, min_upper, store):
        lower = max_lower
        upper = min_upper
        falselist = [False] * self.k
        tt = False
        i = 0
        while any(falselist) == False:
            falselist = [False] * self.k
            candtheta = lower + np.random.rand(1)[0] * (upper - lower)
            store[self.attrib.name] = candtheta
            # print exp(self.omega), [function(store) for function in self.func]
            tt = True
            i = 0
            while tt == True and i < self.k:
                if self.omega[i] < self.__func(i, store):
                    falselist[i] = True
                    tt = True
                    i = i + 1
                else:
                    tt = False
                    falselist[i] = False
                    i = 0
                    if candtheta < self.get_ltheta():
                        lower = candtheta
                    else:
                        upper = candtheta

        self.update_ltheta(candtheta)
        return candtheta


    def __step_out(self, i, store):
        lower_bound = self.get_ltheta() - self.ssize * np.random.rand(1)[0]
        upper_bound = lower_bound + self.ssize
        J = np.floor(self.sN * np.random.rand(1)[0])
        Z = self.sN - 1-J
        store[self.attrib.name] = lower_bound
        while J > 0 and self.omega[i] < (self.__func(i, store)):
            lower_bound = lower_bound - self.ssize
            J = J - 1
        store[self.attrib.name] = upper_bound
        while Z > 0 and self.omega[i] < (self.__func(i, store)):
            upper_bound = upper_bound + self.ssize
            Z = Z - 1

        return lower_bound, upper_bound

class RWMH(BaseSampler):
    """This class is used for the random walk Metropolis Hastings. Argumemts:
    post - Is a user defined function for the log of full conditional
        posterior distribution for the parameters of interest
    csig - The scale parameter for the random walk MH algorithm.
    init_theta - The initial value for the parameter of interest
    name - the name of the parameter of interest
    kwargs - Optional arguments:
        store - 'all'; (default) stores every iterate for parameter of
                interest
              - 'none'; do not store any of the iterates 
        fixed_parameter - Is used is the user wants to fix the parameter
        value that is returned. This is used for testing.
        additional_arguments - Is used if specifical additional arguments are
                               required for the function call. In this case
                               func should take two arguments; store and a
                               list of additional arguments. That is
                               func(store, list_args), should be the function
                               signiture. Note that additional_arguments =
                               list_args is how the arguments should be passed
                               into RWMH.
	
	adaptive - Options GFS (Garthwaite, Fan and Scisson),
		   HST (Haario, Saksman and Tamminen (2001)) 

        parallel - If set to True will evaluate candidate and actual
                   probabilites in parallel. NOT WORKING


    """


    def __init__(self, post, csig, init_theta, name, **kwargs):
        BaseSampler.__init__(self, init_theta, name, **kwargs)
        self.__updateSig = self.__update_sig_standard

        #Check for the correct specification of adaptive MH algorithms
        if 'adaptive' in kwargs.keys():
            try:
                assert kwargs['adaptive'] in ['GFS', 'GYS', 'HST', 'RR', True]
            except:
                error = "adaptive should be of type 'GFS', 'HST', 'RR', or True."
                raise ValueError(error)


        #default
        self.Our_recompute = None

        if np.atleast_1d(init_theta).shape[0] == 1:
            self.theta = float(init_theta)
            self.Sig = csig
            self.__sampletheta = self.__sampletheta_float

            #Adaptive flag singles to use an adaptive version of the random
            #walk MH algorithm.

            
            if 'adaptive' in kwargs.keys():
                #Use the adaptive MH algorithm of Garthwaite, Fan and Scisson
                if kwargs['adaptive'] in  ['GFS', 'GYS']:
                    #Note I just put GYS as an option as there was a mistake
                    #in the earlier acronymn so I just wanted to keep backwards
                    #compatability
                    self.start_sig = self.Sig
                    self.last_restart = 0
                    self.number_restart = 0
                    self.adjust_i = 0 # used to allow for restarts in adaptive process
                    self.pstar = 0.44
                    self.pstarr =  (1. - self.pstar) / self.pstar
                    self.n0 = int(5. / self.pstarr)
                    self.__updateSig = self.__update_sig_adaptive_burn
                    self.__updatesig = self.__update_sig_adaptive
                    self.__check = self.__check_scalar
                    self.__get_sig = self.__sig_scalar

                #Use the adaptive algorithm of Haario, Saksman and Tamminnen
                elif kwargs['adaptive'] in ['HST', 'RR']:
                    #Optional argument to specify the number of iterations to 
                    #run the algorithm prior to adaption

                        
                    if 'HST_i0' in kwargs:
                        self.hst_t0 = kwargs['HST_i0']
                    else:
                        #Shouldn't need to be long in the univariate case
                        self.hst_t0 = 100

                    #scale parameter from paper
                    self.sd = 2.4

                    #Parameter ensures the covariance matrix remains positive
                    #definite
                    if 'HST_epsilon' in kwargs:
                        self.epsilon = kwargs['HST_epsilon']
                    else:
                        #not necessary for the scalar case
                        self.epsilon = 0.0

                    #Initialise mean and covariance for the scalar case
                    self.cum_theta = 0.0
                    self.theta_thetap = 0.0

                    #Pointer to function to update sig
                    self.__updateSig = self.__update_adaptive_HST_scalar

                elif kwargs['adaptive'] == True:
                    #Our Scheme based on MALA scheme
                    self.Our_a = 0.03
                    self.Our_ncov = self.MR_K #
                    self.Our_ti = self.MR_K   #Point of updating covariance
                    self.Our_cum_theta = 0.0
                    self.Our_theta_thetap = 0.0
                    self.Our_cov = 1.
                    self.Our_chol = 1.
                    self.Our_epsilon = 0.0
                    self.Sig = 1.
                    self.Our_target = 0.44

                    #Adaption during burnin
                    self.Our_K = 1000  #Don't adapt Covariance before K
                    self.Our_b = None #Place holder
                    self.Our_r = 0.1
                    self.Our_M = 20
                    self._last_accept = deque()
                    self.__updateSig = self.__update_adaptive_Our

        else:
            assert type(init_theta) == np.ndarray
            self.theta = init_theta
            
            self.__sampletheta = self.__sampletheta_ndarray

            if 'adaptive' in kwargs.keys():
                #Use the adaptive MH algorithm of Garthwaite, Fan and Scisson
                if kwargs['adaptive'] in ['GFS', 'GYS']:
                    #Note I just put GYS as an option as there was a mistake
                    #in the earlier acronymn so I just wanted to keep backwards
                    #compatability
                    self.pstar = 0.234
                    self.last_restart = 0
                    self.number_restart = 0
                    self.adjust_i = 0 # used to allow for restarts in adaptive process
                    alpha = -sp.stats.norm.ppf(self.pstar / 2.)
                    self.m = init_theta.shape[0]
                    self.pstarr =  (1. - self.pstar) / self.pstar
                    self.c = (1. - 1. / self.m) * np.sqrt(2. * np.pi) * \
                            np.exp(alpha ** 2/2.)/\
                            (2. * alpha) + 1. / (self.m * self.pstar * \
                            (1. - self.pstar))
                    self.thetabar = np.zeros(self.m)
                    self.sig = csig
                    self.eye = np.eye(self.m)
                    self.Sigsq = self.eye
                    self.Sig = self.eye
                    self.start_sig = csig
                    self.n0 = int(5. / self.pstarr)
                    self.__updateSig = self.__update_sig_adaptive_burn

                    self.__updatesig = self.__update_sig_adaptive_ndarray
                    self.__check = self.__check_ndarray
                    self.__get_sig = self.__sig_ndarray

                #Use the adaptive algorithm of Haario, Saksman and Tamminnen
                elif kwargs['adaptive'] in ['HST', 'RR']:
                    
                    #Initialise Sigma
                    self.Sig = np.linalg.cholesky(csig)

                    #The dimension of theta
                    self.m = init_theta.shape[0]
                    if kwargs['adaptive'] == 'RR':
                        #use Roberts and Rosenthal mixture component
                        self.RR = True
                        self.RR_I = np.eye(self.m) /\
                                np.sqrt(self.m)
                    else:
                        self.RR = False

                    #Optional argument to specify the number of iterations to 
                    #run the algorithm prior to adaption
                    if 'HST_i0' in kwargs:
                        self.hst_t0 = kwargs['HST_i0']
                    else:
                        #Default value for t0
                        self.hst_t0 = self.m * 2 + 100

                    #scale parameter from paper
                    self.sd = 2.4 / np.sqrt(self.m)

                    #Parameter ensures the covariance matrix remains positive
                    #definite
                    if 'HST_epsilon' in kwargs:
                        self.epsilon = kwargs['HST_epsilon'] * np.eye(self.m)
                    else:
                        #Default value for epsilon
                        self.epsilon = 0.01 * np.eye(self.m)

                    #Initialise mean and covariance for the scalar case
                    self.cum_theta = np.zeros(self.m)
                    self.theta_thetap = np.zeros((self.m, self.m))

                    #Pointer to function to update sig
                    self.__updateSig = self.__update_adaptive_HST_ndarray

                elif kwargs['adaptive'] == True:
                    #Adaption during burnin
                    self.scale = csig
                    self.m = init_theta.shape[0]
                    self.Our_K = 1000  #Don't adapt Covariance before K
                    if 'Our_K' in kwargs:
                        self.Our_K = kwargs['Our_K']
                    self.Our_b = None #Place holder
                    self.Our_r = 0.1
                    if 'Our_M' in kwargs:
                        self.Our_M = kwargs['Our_M']
                    else:
                        self.Our_M = 20
                    self.Our_epsilon = 0.01 * np.eye(self.m)
                    if 'Our_epsilon' in kwargs:
                        self.Our_epsilon = kwargs['Our_epsilon'] * np.eye(self.m)
                    if 'Our_M' in kwargs:
                        self.Our_M = kwargs['Our_M']
                    self._last_accept = deque()
                    self.__updateSig = self.__update_sig_adaptive_Our

                    #Our Scheme based on MALA scheme
                    self.Our_a = 0.03
                    self.Our_ncov = self.Our_K #
                    self.Our_ti = self.Our_K   #Point of updating covariance
                    self.Our_cum_theta = np.zeros(self.m)
                    self.Our_theta_thetap = np.zeros((self.m, self.m))
                    self.Our_cov = np.eye(self.m)
                    self.Our_chol = np.eye(self.m)
                    self.Sig = self.Our_chol.copy()
                    if 'Our_target' in kwargs and kwargs['Our_target'] != None:
                        self.Our_target = kwargs['Our_target']
                        assert self.Our_target > 0.
                    else:
                        self.Our_target = 0.23
                    self.Our_init_sc = 10.

                    if 'Our_mix' in kwargs and kwargs['Our_mix'] == True:
                        self.Our_mix = True
                    else:
                        self.Our_mix = False

                    #recompute the loglikelihood every fixed number of steps
                    #useful for particle filter
                    if 'Our_recompute' in kwargs:
                        self.Our_recompute = kwargs['Our_recompute']
                    else:
                        self.Our_recompute = None

                    #class instance for scale multiplier
                    self.adapt = Adaptive(self.Our_target)

                    
            else:
                #for the non-adaptive case csig should be the covariance matrix
                self.Sig = np.linalg.cholesky(csig)


        #currently not working
        if 'parallel' in kwargs and kwargs['parallel'] == True:
            self.parallel_flag = True
        else:
            self.parallel_flag = False

        #storeage for previous log probability

        self.post = post

        if 'additional_arguments' in kwargs:
            self.list_args = kwargs['additional_arguments']
            assert type(self.list_args) == type([])
            self.__post = self.__aug_post
        else:
            self.__post = self.__std_post

    def __std_post(self, store):
        return self.post(store)

    def __aug_post(self, store):
        return self.post(store, self.list_args)

    def eval_post(self, theta, store):
        store[self.attrib.name] = theta
        return self.__post(store)

    def calculate(self, func, args):
        return func(*args)

        
    def sampler(self, store): # note theta is a dummy argument 
        self.count = self.count + 1.
        self.randomvec = np.random.randn(self.attrib.nparam[0])
        candtheta = self.__sampletheta(store)
       #recompute last probability, useful when estimating likelihood
        if self.Our_recompute != None \
           and store['iteration'] % self.Our_recompute == 0:
            flag = False
        else:
            flag = True
        #store[self.attrib.name] = candtheta
        #lnpr = self.__post(store)
        if self.parallel_flag == False:
            if store['iteration'] > 0 and store['mcmc_nblocks'] == 1 and flag:
                self.lnpr = self.eval_post(candtheta, store)
            else:
                self.lnpr = self.eval_post(candtheta, store)
                #store[self.attrib.name] = self.get_ltheta()
                #llnpr = self.__post(store)
                self.llnpr = self.eval_post(self.get_ltheta(), store)
        else:
            pool = multiprocessing.Pool(2)
            storecopy = deepcopy(store)
            ltheta = self.get_ltheta()
            func = self.eval_post
            theta_list = ((func, (candtheta, store)), (func, (ltheta, storecopy)))
            results = [pool.apply_async(self.calculate, i) for i in theta_list]
            self.lnpr, self.llnpr = [r.get() for r in results]

        alpha = np.exp(self.lnpr - self.llnpr)
        if np.random.rand(1) < alpha:
            self.last_accept = True
            self.update_ltheta(candtheta)
            self.accept = self.accept + 1.
            self.theta = candtheta
            self.__updateSig(True, store)
            self.llnpr = self.lnpr
        else:
            self.last_accept = False
            self.__updateSig(False, store)
            self.theta = self.get_ltheta()

        return self.theta
    
    def __sampletheta_float(self, store):
        return store[self.attrib.name] + self.Sig * self.randomvec[0]

    def __update_sig_standard(self, accept, store):
        self.Sig = self.Sig

    def __update_sig_adaptive(self, accept, store):
        c = self.Sig * self.pstarr
        n = (store['iteration'] + 1 - self.adjust_i)
        if accept == False:
            self.Sig = self.Sig - c * self.pstar / n
        else:
            self.Sig = self.Sig + c * (1. - self.pstar) / n


    def __update_sig_adaptive_Our(self, accept, store):
        """Updates scale parameter for our implementation
        of an adaptive RWMH algorithm."""

        if self.m > 1:
            #Multivariate version update covariance
            self.__update_adaptive_Our_cov(store)

        if store['iteration'] < self.Our_K:
            if (store['iteration']) >= self.Our_M:
                AR = float(self.accept - self._last_accept.popleft()) \
                        / (self.Our_M)
                self._last_accept.append(self.accept)

                sm = self.adapt.scale(AR)
                self.scale = self.scale * sm


            else:
                self._last_accept.append(self.accept)

            if store['iteration'] == self.Our_M - 1:
                #self.Our_b = self.scale * 0.001 * store['iteration'] ** self.Our_r
                self.adapt.initialise_MR(self.scale, store['iteration'])

            


        else:
            AR = float(self.accept - self._last_accept.popleft()) \
                    / (self.Our_M)

            self._last_accept.append(self.accept)

            self.scale = self.adapt.MR_scale(AR, self.scale, store['iteration'])


        if self.Our_mix:
            if np.random.rand > 0.05:
                self.Sig = self.scale * self.Our_chol
            else:
                self.Sig = self.scale * 0.1 * np.eye(self.m)
        else:
            self.Sig = self.scale * self.Our_chol


    def __update_adaptive_Our_cov(self, store):
        """Updates covariance for Our adaptive scheme."""

        theta = store[self.name]
        self.Our_cum_theta = self.Our_cum_theta + theta
        self.Our_theta_thetap = self.Our_theta_thetap + \
                np.outer(theta, theta)

        if store['iteration'] == self.Our_ti:

            #update covariance
            mean_theta = self.Our_cum_theta / self.Our_ncov
            self.Our_cov = self.Our_theta_thetap - self.Our_ncov * np.outer(mean_theta, mean_theta)
            
            sca = self.Our_init_sc 
            self.Our_cov = self.Our_cov / (self.Our_ncov - 1) + sca * self.Our_epsilon
            self.Our_init_sc = 1.
            
            
            #scale to ensure the determinant is one
            sc = (1. / np.linalg.det(self.Our_cov)) ** (1. / self.m)
            self.Our_cov = self.Our_cov * sc
            

            #compute cholesky decomposition
            try:
                self.Our_chol = np.linalg.cholesky(self.Our_cov)
            except:
                pdb.set_trace()
                

            self.Our_ncov = np.floor((1. + self.Our_a) * self.Our_ncov)
            self.Our_ti = self.Our_ti + self.Our_ncov

            #Reset cumulative storage to zero
            self.Our_theta_thetap = np.zeros((self.m, self.m))
            self.Our_cum_theta = np.zeros(self.m)


    def __update_sig_adaptive_burn(self, accept, store):
        """algorithm handles updates for GFS adaptive MCMC
        algorithm - univariate case
        for the burn in period"""

        if store['iteration'] < store['length_of_burnin']:
            it_since_start = store['iteration'] - self.last_restart 
            if it_since_start < 100 and \
               self.number_restart < 5 and \
               it_since_start > self.n0:

                if self.__check():
                    #restart calculate of self.Sig
                    self.adjust_i = store['iteration']
                    self.last_restart = store['iteration']
                    self.number_restart = self.number_restart + 1
                    self.start_sig = self.__get_sig()
            
        else:
            self.__updateSig = self.__updatesig

        self.__updatesig(accept, store)

    def __check_scalar(self):
        return self.Sig / self.start_sig > 3. or self.start_sig / self.Sig > 3.

    def __check_ndarray(self):
        return self.sig / self.start_sig > 3. or self.start_sig / self.sig > 3.

    def __sig_scalar(self): return self.Sig

    def __sig_ndarray(self): return self.sig

    def __update_adaptive_HST_scalar(self, accept,  store):
        """Function computes update for the HST adaptive algorithm
        for the scalar case."""

        t = store['iteration'] + 1
        self.cum_theta = self.cum_theta + self.theta
        self.theta_thetap = self.theta_thetap + self.theta ** 2
        mean_theta = self.cum_theta / t
        cov = self.theta_thetap / t - (float(t) / float(t-1)) * mean_theta ** 2


        if t > self.hst_t0:
            self.Sig = self.sd * np.sqrt( cov + self.epsilon)

    def __update_adaptive_HST_ndarray(self, accept, store):
        """Function computes update for the HST adaptive algorithm
        for the array case."""

        t = store['iteration'] + 1
        self.cum_theta = self.cum_theta + self.theta
        self.theta_thetap = self.theta_thetap + \
                np.outer(self.theta, self.theta)



        if t > self.hst_t0:
            mean_theta = self.cum_theta / t
            cov = self.theta_thetap / (t - 1) - (float(t) / float(t-1)) *\
                    np.outer(mean_theta, mean_theta)
            if self.RR:
                #Roberts and Rosenthal mixture component
                if np.random.rand() < 0.05:
                    self.Sig = self.RR_I.copy()
                else:
                    self.Sig = self.sd * np.linalg.cholesky(cov + self.epsilon)
            else:
                self.Sig = self.sd * np.linalg.cholesky(cov + self.epsilon)
            
            


    def __update_sig_adaptive_ndarray(self, accept, store):
        it = store['iteration'] - self.adjust_i
        if it > 200:
            self.__update_Sigsq_ndarray(it)
            self.__update_sigma_ndarray(accept, it)
            self.Sig = self.sig * np.linalg.cholesky(self.Sigsq + \
                                 (self.sig ** 2 / (it + 1)) * self.eye)
            


        elif it > 100:
            if accept == False:
                self.sig = self.sig - self.c * self.pstar / (it + 1)
            else:
                self.sig = self.sig + self.c * (1. - self.pstar) / (it + 1)
            self.__update_Sigsq_ndarray(it)
            self.Sig = self.sig * np.linalg.cholesky(self.Sigsq + \
                                 (self.sig ** 2 / (it + 1)) * self.eye)

        else:
            if accept == False:
                self.sig = self.sig - self.c * self.pstar / (it + 1)
            else:
                self.sig = self.sig + self.c * (1. - self.pstar) / (it + 1)
            self.Sig = self.sig * np.sqrt(self.eye + self.sig ** 2 / (it + 1) * self.eye)
            self.Sigsq = self.Sigsq + np.outer(self.theta, self.theta)
            self.thetabar = self.thetabar + self.theta
            if it == 100:
                self.Sigsq = self.Sigsq / store['iteration']
                self.Sig = self.sig * np.linalg.cholesky(self.Sigsq + \
                                 (self.sig ** 2 / (it + 1)) * self.eye)
                self.thetabar = self.thetabar / store['iteration']

    def __update_sigma_ndarray(self, accept, it):
        c = self.sig * self.c
        if accept == True:
            self.sig = self.sig + c * (1. - self.pstar) / \
                    max([200., float(it) / self.m])
        else:
            self.sig = self.sig - c * self.pstar / max([200.,  float(it) / self.m])

    def __update_Sigsq_ndarray(self, it):
            lthetabar = self.thetabar.copy()
            #mcmc_helper.up_ssq(it, self.thetabar, self.lthetabar, self.theta, self.Sigsq)
            self.thetabar =  1. / (it + 1.) * (it * self.thetabar +  self.theta)
            self.Sigsq = (it - 1.) / it * self.Sigsq + np.outer(lthetabar, lthetabar) -\
                    float(it + 1.) / it * np.outer(self.thetabar, self.thetabar) + \
                    1. / it * np.outer(self.theta, self.theta)



    def __sampletheta_ndarray(self, store):
        return store[self.attrib.name] + np.dot(self.Sig, self.randomvec)

class OBMC(BaseSampler):
    """This is a a class for the orientational bias Monte Carlo algorithm.
    The arguments:
    post - is a user defined function for the log of full conditional posterior
        distribution for the parameters of interest. 
    ntry - the number of candidates. A scalar.
    csig - the scale parameter it can be a float or a Numpy array.
    init_theta - The initial value for the parameter of interest. Scalar or
      1-d numpy array.

    kwargs - Optional arguments:
        store - 'all'; (default) stores every iterate for parameter of
                interest
              - 'none'; do not store any of the iterates 
        fixed_parameter - Is used is the user wants to fix the parameter
        value that is returned. This is used for testing.
        additional_arguments - Is used if specifical additional arguments are
                               required for the function call. In this case
                               func should take two arguments; store and a
                               list of additional arguments. That is
                               func(store, list_args), should be the function
                               signiture. Note that additional_arguments =
                               list_args is how the arguments should be passed
                               into CFsampler.
    """


    def __init__(self, post, ntry, csig, init_theta, name, **kwargs):
        BaseSampler.__init__(self, init_theta, name, **kwargs)

        ##first type checking for ntry:
        if not np.isscalar(ntry):
            raise TypeError("ntry must be a scalar")

        self.post = post
        self.ntry = ntry
        try:
            if np.isscalar(init_theta):
                nelements = sum([ntry] + self.attrib.nparam)
            else:
                if init_theta.ndim > 1:
                    raise TypeError(
                        "init_theta must be either scalar or 1-d")
                nelements = [ntry] + self.attrib.nparam
            self.xtil = np.zeros(nelements)
            self.randnvec = np.zeros(nelements)
            self.multicand = np.zeros(nelements)
            self.multicandcum = np.zeros(ntry)

            self.multicandcump = np.zeros(ntry + 1)
            self.numvec = np.zeros(ntry)
            self.denomvec = np.zeros(ntry)
            if type(csig) == types.FloatType:
                self.CholCsig = np.sqrt(csig)
                self.__sampletheta = self.__sampletheta_float
            else:
                self.CholCsig = np.linalg.cholesky(csig)
                self.__sampletheta = self.__sampletheta_ndarray
            self.candtheta = np.zeros(self.attrib.nparam)

        except TypeError as e:
            print e
            raise TypeError("argument init_theta seems to be the wrong type")
        except Exception as e:
            print "unexpected error"
            print e
            raise
        
        if 'additional_arguments' in kwargs:
            self.list_args = kwargs['additional_arguments']
            assert type(self.list_args) == type([])
            self.__post = self.__aug_post
        else:
            self.__post = self.__std_post

    def __std_post(self, store):
        return self.post(store)

    def __aug_post(self, store):
        return self.post(store, self.list_args)


    def sampler(self, store):             
        self.count = self.count + 1
        self.randnvec = np.random.randn(self.ntry, self.attrib.nparam[0])
        # self.__sampletheta(self.ntry, self.multicand, self.numvec, self.ltheta, store)
        for i in xrange(self.ntry):
            self.multicand[i] = self.get_ltheta() + np.dot(self.CholCsig, self.randnvec[i])
            store[self.attrib.name] = self.multicand[i]
            self.numvec[i] = self.__post(store)
        
        intconst = self.numvec.max()
        self.multicandcum = np.add.accumulate(np.exp(self.numvec - intconst))
        self.multicandum = self.multicandcum/self.multicandcum[self.ntry - 1]
        
        randu = np.random.rand(1)
        self.multicandcump[0:self.ntry] = self.multicandcum
        self.multicandcump[self.ntry] = randu
        self.multicandcump.sort()
        index = self.multicandcump.searchsorted(randu)
        self.candtheta = self.multicand[index[0]]    
        
        self.xtil[self.ntry - 1] = self.get_ltheta()
        store[self.attrib.name] = self.xtil[self.ntry - 1]
        self.denomvec[self.ntry - 1] = self.__post(store)
        if self.ntry > 1:
            self.randnvec = np.random.randn(self.ntry - 1, self.attrib.nparam[0])
            # self.__sampletheta(self.ntry - 1, self.xtil, self.denomvec, self.candtheta, store)
            for i in xrange(self.ntry - 1):
                self.xtil[i] = self.candtheta + np.dot(self.CholCsig, self.randnvec[i])
                store[self.attrib.name] = self.xtil[i]
                self.denomvec[i] = self.__post(store)

        # intconst = np.hstack((self.numvec, self.denomvec)).max()
        sumdenom = sum(np.exp(self.denomvec - intconst))
        sumnum = sum(np.exp(self.numvec - intconst))
        alpha = sumnum/sumdenom

        # print alpha, sumnum, sumdenom, self.candtheta, self.numvec, self.multicand
        # print alpha, sumnum, sumdenom, self.denomvec, intconst 
        if np.random.rand(1) < alpha:
            self.last_accept = True
            self.update_ltheta(self.candtheta)
            self.accept = self.accept + 1.
            return self.candtheta
        else:
            self.last_accept = False
            return self.get_ltheta()
            
    def __sampletheta_float(self, nt, lhs, lhs2, meanv, store):
        for i in xrange(nt):
            lhs[i] = meanv + self.CholCsig * self.randnvec[i, 0]
            store[self.attrib.name] = lhs[i]
            lhs2[i] = self.__post(store)

    def __sampletheta_ndarray(self, nt, lhs, lhs2, meanv, store):
        meanvtmp = meanv.copy()
        for i in xrange(nt):
            lhs[i][:] = (meanvtmp + np.dot(self.CholCsig, self.randnvec[i]))[:]
            store[self.nattrib.ame][:] = lhs[i][:]
            lhs2[i] = self.__post(store)



class MH(BaseSampler):
    """This class is used for the Metropolis Hastings algorithm. The function
    arguments are:
    func - Is a user defined function that returns a sample for the
    parameter of interest. 
    actualprob - Is a user defined function that returns the log probability of
                 the parameters of interest evaluated using the target  density.
    probcandgprev - Is a user defined function that returns the log probability
                    of the parameters of interest evaluated at the previous
                    iteration conditional on the candidate.
    probprevgcand - Is a user define function that returns the log probability
                    of the previous given the log candidate
                    
    init_theta - Initial value for the parameters of interest. 
    name - The name of the parameter of interest. 
    kwargs - optional parameters:
        store - 'all'; (default) stores every iterate for parameter of
                interest
              - 'none'; do not store any of the iterates
        output - list; provide an index in the form of a list for the parameters to be
                       that output is to be provide for. If not provided print all of
                       theta               
        fixed_parameter - Is used is the user wants to fix the parameter
        value that is returned. This is used for testing.
        additional_arguments - Is used if specifical additional arguments are
                               required for the function call. In this case
                               func should take two arguments; store and a
                               list of additional arguments. That is
                               func(store, list_args), should be the function
                               signiture. Note that additional_arguments =
                               list_args is how the arguments should be passed
                               into CFsampler.
    """


    def __init__(self, func, actualprob, probcandgprev, probprevgcand, init_theta, name, **kwargs):
        BaseSampler.__init__(self, init_theta, name, **kwargs)

        self.func = func
        self.actualprob = actualprob
        self.probcandgprev = probcandgprev
        self.probprevgcand = probprevgcand

        #workspace variable
        self.lnprprev = 0.0
        
        if self.ind_list == False:
            self.previous_name ='previous_' + self.name
        else:
            self.previous_name = ['previous_' + x for x in self.name]

        if type(init_theta) == types.FloatType or type(init_theta) == types.IntType:
            self.attrib.nparam = [1]
            self.candtheta = 0.
              
        elif type(init_theta) == np.ndarray:
            self.attrib.nparam = list(init_theta.shape)
            if init_theta.ndim == 1:
                self.candtheta = np.zeros(init_theta.shape[0])
            elif init_theta.ndim == 2:
                dim = list(init_theta.shape)
                self.candtheta = np.zeros(dim)
                dim.insert(0, len(self.range))

        if self.ind_list == False:
            self._set_store = self.__set_store_single
        else:
            self._set_store = self.__set_store_multiple

        #function used for adaption. The function will be passed
        #store and contain the accepted parameter value. Used for development
        #purposes.

        if 'adaptive' in kwargs:
            self.adaptive = kwargs['adaptive']
        else:
            self.adaptive = None


        if 'additional_arguments' in kwargs:
            self.list_args = kwargs['additional_arguments']
            assert type(self.list_args) == type([])
            self.__func = self.__aug_func
            self.__actual_prob = self.__aug_actual_prob
            self.__probprevgcand = self.__aug_probprevgcand
            self.__probcandgprev = self.__aug_probcandgprev
        else:
            self.__func = self.__std_func
            self.__actual_prob = self.__std_actual_prob
            self.__probprevgcand = self.__std_probprevgcand
            self.__probcandgprev = self.__std_probcandgprev

    def __std_actual_prob(self, store):
        return self.actualprob(store)

    def __aug_actual_prob(self, store):
        return self.actualprob(store, self.list_args)

    def __std_probcandgprev(self, store):
        return self.probcandgprev(store)

    def __aug_probcandgprev(self, store):
        return self.probcandgprev(store, self.list_args)

    def __std_probprevgcand(self, store):
        return self.probprevgcand(store)

    def __aug_probprevgcand(self, store):
        return self.probprevgcand(store, self.list_args)

    def __std_func(self, store):
        return self.func(store)

    def __aug_func(self, store):
        return self.func(store, self.list_args)


    def sampler(self, store):
        self.count = self.count + 1.
        candtheta = self.__func(store)
        
        if store['iteration'] > 0 and store['mcmc_nblocks'] == 1:
            self._set_store(store, self.name, candtheta)
            lnprcand = self.__actual_prob(store)

        else:
            self._set_store(store, self.name, self.get_ltheta())
            self.lnprprev = self.__actual_prob(store)

            self._set_store(store, self.name, candtheta)
            lnprcand = self.__actual_prob(store)

        self._set_store(store, self.previous_name, self.get_ltheta())
        llnpr = self.__probprevgcand(store)
        llncand = self.__probcandgprev(store)
    
        num = (lnprcand - self.lnprprev)
        denom = (llncand - llnpr)
        alpha = np.exp(num - denom)
        
                                 
        if np.random.rand() < alpha:
            self.last_accept = True
            self.update_ltheta(candtheta)
            self.accept = self.accept + 1.
            self.lnprprev = lnprcand
            return candtheta
        else:
            self.last_accept = False
            return self.get_ltheta()

        if self.adaptive != None:
            self.adaptive(store)

    def __set_store_single(self, store, name, theta):
        store[name] = theta

    def __set_store_multiple(self, store, name, theta):
        for i in xrange(self.number_groups):
            store[name[i]] = theta[i]

class MALA(MH):
    """This class is used for the Metropolis adjusted Langvin algorithm.

    arguments:
        posterior - returns the log posterior probability
        scale - scale parameter for algorithm
        score - function returns store vector
        init_theta - initial value for parameters
        name - string that names the parameter
    optional arguments (kwargs):
        hessian - function that returns the hessian (MMALA algortihm used
                  instead)
        store - 'all'; (default) stores every iterate for parameter of
                interest
              - 'none'; do not store any of the iterates
        output - list; provide an index in the form of a list for the parameters to be
                       that output is to be provide for. If not provided print all of
                       theta               
        fixed_parameter - Is used is the user wants to fix the parameter
        value that is returned. This is used for testing.
        additional_arguments - Is used if specifical additional arguments are
                               required for the function call. In this case
                               func should take two arguments; store and a
                               list of additional arguments. That is
                               func(store, list_args), should be the function
                               signiture. Note that additional_arguments =
                               list_args is how the arguments should be passed
                               into CFsampler.
    """

    def __init__(self, posterior, scale, score, init_theta, name, **kwargs):
        
        MH.__init__(self, self.candidate, posterior, self.candgprev,
                   self.prevgcand, init_theta, name, **kwargs)

        self.scale = scale
        self.scale_sq = scale ** 2
        self.score = score
        self.ntheta = init_theta.shape[0]

        #placeholders
        self.mean_current = None
        self.mean_past = None

        #Store last acceptance rate (used in optimisation)
        self.laccept = 0
                                                     

        #Default functions (MALA)
        self.__mean_cand = self.__mean_cand_MALA
        self.__candidate = self.__candidate_MALA
        self.__candidate_density = self.__candidate_density_MALA
        self.__prevgcand = self.__prevgcand_MALA
        self.__candgprev = self.__candgprev_MALA

        #if 'information_matrix' in kwargs:
        #    self.information = kwargs['information_matrix']

        #default no hessian
        self.hessian = None

        if 'hessian' in kwargs:
            self.hessian = kwargs['hessian']

            #Placeholders used in calculations
            self.hessian_current = None
            self.hessian_past = None

            self.HS_current = None
            self.HS_past = None

            self.hessian_logdet_current = None
            self.hessian_logdet_past = None

            self.__mean_cand = self.__mean_cand_MMALA_H
            self.__candidate = self.__candidate_MMALA_H
            self.__candidate_density = self.__candidate_density_MMALA_H
            self.__prevgcand = self.__prevgcand_MMALA_H
            self.__candgprev = self.__candgprev_MMALA_H
           

        self.ind_tune_burn = False

        if 'adaptive' in kwargs:
            if kwargs['adaptive'] == 'burnin':
                #Apply heuristics to tune scale during burnin
                self.__tune_it = 20
                self._last_accept = deque()
                self.__tune_accept_start = 0
                self.ind_tune_burn = True
                self.adaptive = 'burnin'

            elif kwargs['adaptive'] == 'MR':
                #Use the adaptive MCMC procedure of Marshall and Roberts (2012).
                #Pointers to functions
                if self.hessian == None:
                    self.__candidate = self.__candidate_MALA_adapt
                    self.__candidate_density = self.__candidate_density_MALA_adapt

                #Tuning parameters for algorithm
                #Don't adapt Covariance before K
                if 'MR_K' in kwargs:
                    self.MR_K = kwargs['MR_K']
                else:
                    self.MR_K = 1000 + init_theta.shape[0]
                self.MR_b = None #Place holder
                self.MR_r = 0.1
                if 'MR_M' in kwargs:
                    self.MR_M = kwargs['MR_M']
                else:
                    self.MR_M = 20
                self.MR_epsilon = 0.01 * np.eye(self.ntheta)
                self.adaptive = 'MR'
                self.MR_sc = 10
                self._last_accept = deque()

                if self.hessian == None:
                    #Update Covariance 
                    self.MR_a = 0.03
                    self.MR_ncov = self.MR_K #
                    self.MR_ti = self.MR_K   #Point of updating covariance
                    self.MR_cum_theta = np.zeros(self.ntheta)
                    self.MR_theta_thetap = np.zeros(self.ntheta)
                    self.MR_cov = np.eye(self.ntheta)
                    self.MR_chol = np.eye(self.ntheta)

                #Adaption during burnin
                self.__burn_step = 20
                self.__tune_accept_start = 0

                self.adapt = Adaptive(0.57)

                #Set values of tuning parameters through kwargs

                if 'MR_a' in kwargs:
                    try:
                        assert self.hessian != None
                    except:
                        raise Exception("Parameter MR_a only required for MMALA algorithm.")

                    self.MR_a = kwargs['MR_a']


                if 'MR_r' in kwargs:
                    self.MR_r = kwargs['MR_r']


                if 'MR_cov' in kwargs:
                    self.MR_cov = kwargs['MR_cov']
                    self.MR_chol = np.linalg.cholesky(self.MR_chol)
                    try:
                        assert self.hessian != None
                    except:
                        raise Exception("Parameter MR_cov only required for MMALA algorithm.")

                if 'MR_epsilon' in kwargs:
                    try:
                        assert self.hessian != None
                    except:
                        raise Exception("Parameter MR_epsilon only required for MMALA algorithm.")
                    self.MR_epsilon = kwargs['MR_epsilon'] * np.eye(self.ntheta)

        else:
            self.adaptive = None



    def __tune_scale_burnin(self, store):
        if store['iteration'] < store['length_of_burnin']:
            if (store['iteration']) >= self.__tune_it:
                AR = float(self.accept - self._last_accept.popleft()) \
                        / (self.__tune_it)
                self._last_accept.append(self.accept)
                
                self.__tune_accept_start = self.accept

                sm = self.adapt.scale(AR)

                self.scale = self.scale * sm
                
                
                #if AR > 0.99:
                #    self.scale = self.scale / 0.9
                #elif AR > 0.80:
                #    self.scale = self.scale / 0.97
                #elif AR > 0.6:
                #    self.scale = self.scale / 0.99
                #elif AR < 0.0001:
                #    self.scale = self.scale * 0.5
                #elif AR < 0.001:
                #    self.scale = self.scale * 0.7
                #elif AR < 0.01:
                #    self.scale = self.scale * 0.94
                #elif AR < 0.4:
                #    self.scale = self.scale * 0.97
                #elif AR < 0.5:

                #    self.scale = self.scale * 0.99

                self.scale_sq = self.scale ** 2
            else:
                self._last_accept.append(self.accept)

        else:
            self.ind_tune_burn = False

    def __adapt_MR_MALA_Cov(self, store):
        """Function adapts covariance for use in MALA algorithm."""

        theta = store[self.name]
        self.MR_cum_theta = self.MR_cum_theta + theta
        self.MR_theta_thetap = self.MR_theta_thetap + \
                np.outer(theta, theta)

        if store['iteration'] == self.MR_ti:

            #update covariance
            mean_theta = self.MR_cum_theta / self.MR_ncov
            self.MR_cov = self.MR_theta_thetap - self.MR_ncov * np.outer(mean_theta, mean_theta)
            sca = self.MR_sc
            
            self.MR_cov = self.MR_cov / (self.MR_ncov - 1) + sca * self.MR_epsilon
            self.MR_sc = 1.

            
            #scale to ensure the determinant is one
            sc = (1. / np.linalg.det(self.MR_cov)) ** (1. / self.ntheta)
            self.MR_cov = self.MR_cov * sc

            #compute cholesky decomposition
            self.MR_chol = np.linalg.cholesky(self.MR_cov)

            self.MR_ncov = np.floor((1. + self.MR_a) * self.MR_ncov)
            self.MR_ti = self.MR_ti + self.MR_ncov

            #Reset cumulative storage to zero
            self.MR_theta_thetap = np.zeros((self.ntheta, self.ntheta))
            self.MR_cum_theta = np.zeros(self.ntheta)
            
    def __adapt_MR_MALA(self, store):
        """Algorithm used to adapt scale parameter in standard
        MALA algorithm. Note based on Marshall and Roberts (2012).
        """

        if self.hessian == None:
            self.__adapt_MR_MALA_Cov(store)

        if store['iteration'] < self.MR_K:
            if (store['iteration']) >= self.MR_M:
                AR = float(self.accept - self._last_accept.popleft()) \
                        / (self.MR_M)
                self._last_accept.append(self.accept)

                if AR > 0.99:
                    self.scale = self.scale / 0.9

                elif AR > 0.80:
                    self.scale = self.scale / 0.97
                elif AR > 0.6:
                    self.scale = self.scale / 0.99
                elif AR < 1E-10:
                    self.scale = self.scale * 0.1
                elif AR < 0.0001:
                    self.scale = self.scale * 0.5
                elif AR < 0.001:
                    self.scale = self.scale * 0.7
                elif AR < 0.01:
                    self.scale = self.scale * 0.94
                elif AR < 0.4:
                    self.scale = self.scale * 0.97
                elif AR < 0.5:
                    self.scale = self.scale * 0.99

                self.scale_sq = self.scale ** 2

            else:
                self._last_accept.append(self.accept)

            #Start storing acceptances to compute rolling acceptance rate
            #if store['iteration'] >= self.MR_K - self.MR_M:
            #    self._last_accept.append(self.accept)
            if store['iteration'] == self.MR_M - 1:
                self.MR_b = self.scale * 0.001 * store['iteration'] ** self.MR_r

        else:
            
            #tune scale according to Marshall and Roberts Algorithm
            AR = float(self.accept - self._last_accept.popleft()) \
                    / (self.MR_M)
            self._last_accept.append(self.accept)

            scale_star = max((0.001 * self.scale),
                             self.MR_b * store['iteration'] ** (-self.MR_r))

            if AR < 0.574:
                self.scale = self.scale - scale_star
            else:
                self.scale = self.scale + scale_star

            self.scale_sq = self.scale ** 2



    def candidate(self, store):
        if self.adaptive == 'burnin':
            if store['iteration'] < store['length_of_burnin']:
                self.__tune_scale_burnin(store)
            
        elif self.adaptive == 'MR':
            self.__adapt_MR_MALA(store)
        #if store['iteration'] % 50 == 0: pdb.set_trace()
        return self.__candidate(store)


    def __mean_cand_MALA(self, store):
        ssq = self.scale_sq
        theta = store[self.name]
        
        mean = theta + 0.5 * ssq * self.score(store)
        #print mean, ssq, self.scale
        return mean

    def __mean_cand_MMALA_H(self, store, HS):
        ssq = self.scale_sq
        theta = store[self.name]
        mean = theta + 0.5 * ssq * HS
        return mean

    def __candidate_MALA(self, store):

        if store['iteration'] > 0 and store['mcmc_nblocks'] == 1:
            if self.accept > self.laccept:
                #Accept move last iteration
                self.mean_past = self.mean_current.copy()
            self.mean_current = self.__mean_cand(store)
        else:
            self.mean_current = self.__mean_cand(store)
            store[self.name] = self.get_ltheta()
            self.mean_past = self.__mean_cand(store)

        return self.mean_current + self.scale * np.random.randn(self.attrib.nparam[0])

    def __candidate_MMALA_H(self, store):
        #Store negative hessian
        if store['iteration'] > 0 and store['mcmc_nblocks'] == 1:
            #Optimisation for single block MCMC algorithms
            if self.accept > self.laccept:
                #Accept move last iteration
                self.mean_past = self.mean_current.copy()
                self.hessian_past = self.hessian_current.copy()
                self.hessian_logdet_past = self.hessian_logdet_current

            self.hessian_current = -self.hessian(store)
            cholH = np.linalg.cholesky(self.hessian_current)
            self.HS_current = np.linalg.solve(self.hessian_current, self.score(store))
            self.mean_current = self.__mean_cand(store, self.HS_current)
            self.hessian_logdet_current = np.log(np.diag(cholH)).sum() 
        else:
            #compute current
            self.hessian_current = -self.hessian(store)
            cholH = np.linalg.cholesky(self.hessian_current)
            self.HS_current = np.linalg.solve(self.hessian_current, self.score(store))
            self.mean_current = self.__mean_cand(store, self.HS_current)

            #compute log half determinant
            self.hessian_logdet_current = np.log(np.diag(cholH)).sum() 

            #compute past
            store[self.name] = self.get_ltheta()
            self.hessian_past = -self.hessian(store)
            cholHP = np.linalg.cholesky(self.hessian_past)
            self.HS_past = np.linalg.solve(self.hessian_past, self.score(store))
            self.mean_past = self.__mean_cand(store, self.HS_past)

            #compute half the log determinant
            self.hessian_logdet_past = np.log(np.diag(cholHP)).sum() 

        return self.mean_current + self.scale * np.linalg.solve(cholH.T, 
                                                    np.random.randn(self.attrib.nparam[0]))


    def __candidate_MALA_adapt(self, store):
        "Adaptive version of MALA based on Marshall and Roberts."

        self.mean_current =  store[self.name] + \
                0.5 * self.scale_sq * np.dot(self.MR_cov,
                                             self.score(store))
        if self.accept > self.laccept:
            #Accept move last iteration
            self.mean_past = self.mean_current.copy()

        if store['iteration'] == 0 or store['mcmc_nblocks'] == 1:

            store[self.name] = self.get_ltheta()
            self.mean_past = self.get_ltheta() + \
                    0.5 * self.scale_sq * np.dot(self.MR_cov,
                                                 self.score(store))
        return self.mean_current + \
                self.scale * np.dot(self.MR_chol, np.random.randn(self.ntheta))

    def __candidate_density_MALA_adapt(self, theta, meanv):
        "evalutes candidate density for adaptive version of MALA, based on Marshall and Roberts."

        res = theta - meanv
        wres = np.linalg.solve(self.MR_chol, res)
        lnpr = -0.5 * self.scale_sq *np.dot(wres, wres)
        return lnpr


    def __candidate_density_MALA(self, theta, mean):
        "Function returns log probability for the candidate distribution for MALA."
        res = theta - mean
        lnpr = -0.5 / self.scale_sq * np.dot(res, res)
        return lnpr

    def __candidate_density_MMALA_H(self, theta, mean, H, halflogdet):
        "Function returns log probability for the candidate distribution for MMALA."
        res = theta - mean
        lnpr = halflogdet -0.5 / self.scale_sq * np.dot(res,np.dot(H, res))
        return lnpr

    def candgprev(self, store):
        return self.__candgprev(store)

    def prevgcand(self, store):
        return self.__prevgcand(store)

    def __candgprev_MALA(self, store):
        theta = store[self.name]
        mean = self.mean_past
        return self.__candidate_density(theta, mean)

    def __prevgcand_MALA(self, store):
        prev_theta = store[self.previous_name]
        mean = self.mean_current
        return self.__candidate_density(prev_theta, mean)

    def __candgprev_MMALA_H(self, store):
        theta = store[self.name]
        mean = self.mean_past
        return self.__candidate_density(theta,
                                      mean, self.hessian_past,
                                       self.hessian_logdet_past)

    def __prevgcand_MMALA_H(self, store):
        prev_theta = store[self.previous_name]
        mean = self.mean_current
        return self.__candidate_density(prev_theta,
                                  mean, self.hessian_current,
                                       self.hessian_logdet_current)

class IndMH(BaseSampler):
    """
    IndMH is for the independent Metropolis Hastings algorithm
    arguments:
    func - is a function that calculates the candidate for theta
    actualprob - Is a user defined function that returns the log
                 probability of the parameters of interest
                 evaluated using the target density.
    candprob - Is a user defined function that returns the log
               probability of the parameters of interest
               evaluated using the canditate density.
    init_theta - is the initial value for theta
    name - is the name of the parameter of interest
    kwargs - optional parameters:
        store - 'all'; (default) stores every iterate for parameter of
                interest
              - 'none'; do not store any of the iterates 
        fixed_parameter - Is used is the user wants to fix the parameter
        value that is returned. This is used for testing.
        additional_arguments - Is used if specifical additional arguments are
                               required for the function call. In this case
                               func should take two arguments; store and a
                               list of additional arguments. That is
                               func(store, list_args), should be the function
                               signiture. Note that additional_arguments =
                               list_args is how the arguments should be passed
                               into CFsampler.

        multiple_try - An integer specifying the number of trys for the multiple
                       try algorithm

        force_accept - An interger to specify how many iterations to force 
                       acceptance
  """


    def __init__(self, func, actualprob, candprob, init_theta, name, **kwargs):
        BaseSampler.__init__(self, init_theta, name, **kwargs) 

        self.func = func
        self.actual_prob = actualprob
        self.cand_prob = candprob

        if 'multiple_try' in kwargs and kwargs['multiple_try'] != None:
            self.ntrials = kwargs['multiple_try']
            self.__sampler = self.__mt_sampler
        else:
            self.__sampler = self.__std_sampler

        
        if self.ind_list == False:
            self.__set_store = self.__set_store_single
        else:
            self.__set_store = self.__set_store_multiple

        if 'additional_arguments' in kwargs:
            self.list_args = kwargs['additional_arguments']
            assert type(self.list_args) == type([])
            self.__func = self.__aug_func
            self.__actual_prob = self.__aug_actual_prob
            self.__cand_prob =  self.__aug_cand_prob
        else:
            self.__func = self.__std_func
            self.__actual_prob = self.__std_actual_prob
            self.__cand_prob = self.__std_cand_prob

        if 'force_accept' in kwargs:
            self.force_accept = kwargs['force_accept']
            try:
                assert type(self.force_accept) == types.IntType
            except:
                raise TypeError("force_accept must be of type int")

            #after self.force_accept iterations, witch to self.__sampler
            self.__switch_sampler = self.__sampler
            self.__sampler = self.__force_accept_sampler
            
    def __std_func(self, store):
        return self.func(store)

    def __aug_func(self, store):
        return self.func(store, self.list_args)            
            
    def __std_actual_prob(self, store):
        return self.actual_prob(store)

    def __aug_actual_prob(self, store):
        return self.actual_prob(store, self.list_args)

    def __std_cand_prob(self, store):
        return self.cand_prob(store)

    def __aug_cand_prob(self, store):
        return self.cand_prob(store, self.list_args)

    def __mt_sampler(self, store):
        """Basic implementation of the multiple try metropolis independence sampler."""
        self.count = self.count + 1.
        lnpr = []
        lncand = []
        candidate = []
        for i in xrange(self.ntrials):
            self.candtheta = self.__func(store)
            candidate.append(self.candtheta)
            self.__set_store(store, self.name, self.candtheta)
            lnpr.append(self.__actual_prob(store))
            lncand.append(self.__cand_prob(store))
        wvec = np.array([lnpr[i] - lncand[i] for i in xrange(self.ntrials)])
        #sum log of weights
        W = self.__sumlog(wvec)

        #construct probability mass function
        pmf = np.exp(wvec - W)

        if np.allclose(pmf.sum(), 1.0) != True:
            #Reject automatically
            return self.get_ltheta()
        

        #Draw randomly from pmf
        index = np.random.multinomial(1, pmf.flatten()).argmax()
        self.candtheta = candidate[index]
        wcand = wvec[index] 
            
        self.__set_store(store, self.name, self.get_ltheta())
        llnpr = self.__actual_prob(store)
        llncand = self.__cand_prob(store)
        wlast = llnpr - llncand

        #compute acceptance probability
        maxw = max(W, wcand, wlast)
        denom = np.log(np.exp(W-maxw) - np.exp(wcand - maxw) + \
                       np.exp(wlast - maxw)) + maxw
        alpha = np.exp(W - denom)
        if np.random.rand(1) < alpha:
            self.update_ltheta(self.candtheta)
            self.accept = self.accept + 1.
            return self.candtheta
        else:
            return self.get_ltheta()

    def __sumlog(self, x):
        maxp = x.max()
        return np.log(np.exp(x - maxp).sum()) + maxp

    def __force_accept_sampler(self, store):
        if store['iteration'] < self.force_accept:
            self.count = self.count + 1.
            self.candtheta = self.__func(store)
            self.last_accept = True
            self.update_ltheta(self.candtheta)
            self.accept = self.accept + 1.
            return self.candtheta
        else:
            self.__sampler = self.__switch_sampler
            return self.__sampler(store)

    def sampler(self, store):
        """Samples from independent MH algorithm."""
        return self.__sampler(store)

    def __std_sampler(self, store):
        self.count = self.count + 1.
        self.candtheta = self.__func(store)
        #store[self.attrib.name] = self.candtheta
        self.__set_store(store, self.name, self.candtheta)
        lnpr = self.__actual_prob(store)  
        lncand = self.__cand_prob(store)            
        
        #store[self.attrib.name] = self.get_ltheta()
        self.__set_store(store, self.name, self.get_ltheta())
        
        llnpr = self.__actual_prob(store)
        llncand = self.__cand_prob(store)
        
        num = lnpr - llnpr
        denom = lncand - llncand                    
        alpha = np.exp(num - denom)
        
        if np.random.rand(1) < alpha:
            self.last_accept = True
            self.update_ltheta(deepcopy(self.candtheta))
            self.accept = self.accept + 1.
            return self.candtheta
        else:
            self.last_accept = False
            return self.get_ltheta()
        
    def __set_store_single(self, store, name, theta):
        store[name] = theta

    def __set_store_multiple(self, store, name, theta):
        for i in xrange(self.number_groups):
            store[name[i]] = theta[i]

 
class HMC(BaseSampler):
    """This class is used for Hamiltonian Monte Carlo.
    arguments:
    post - Evaluates the log of the posterior.
    gradient - Evaluates the gradient of the posterior.
    scale - The scale parameter, or starting parameter for the
            scale parameter in the adaptive case.
    L - Either an integer of range [LBint, UBint] for the number
        of leapfrog steps
    init_theta - An initial value for parameters in block.
    name - Name of parameter for HMC.

    Optional Arguments(**kwargs):
    adaptive - True; use adaption to find scale.
    
    """

    def __init__(self, post, gradient, scale, L, init_theta,
                 name, **kwargs):
        
        BaseSampler.__init__(self, init_theta, name, **kwargs)

        hessian = None
        self.post = post
        self.gradient = gradient
        if hessian == None:
            self.__Update_position = self.__std_Update_position
            self.__kinetic_energy = self.__std_kinetic_energy
        else:
            self.__Update_position = self.__hessian_Update_position
            self.__kinetic_energy = self.__he_kinetic_energy

        self.hessian = hessian
        self.scale = scale
        assert type(L) in (types.IntType, type([]))
        self.L = L
        if type(self.L) == type([]):
            assert len(self.L) == 2
            assert type(self.L[0]) == types.IntType
            assert type(self.L[1]) == types.IntType
            assert self.L[1] >= self.L[0]

            self.__simL = self.__Llist
        else:
            self.__simL = self.__Lint
            


        nparam = np.atleast_1d(init_theta).shape[0]

        
        #Adaptive parameter
        if 'adaptive' in kwargs and kwargs['adaptive'] == True:
            #Don't start diminishing adaption before self.ad_K
            self.adaptive = True
            self.ad_K = 1000

            #Adaptive target
            self.ad_target = 0.645
            #adaptive window for acceptance rate
            self.ad_W = 5
            self.ad_W2 = 10
            self.ad_b = None #Placeholder
            self.ad_r = 0.1
            self.ad_ti = self.ad_K
            self.ad_cum_theta = np.zeros(nparam)
            self.ad_theta_thetap = np.zeros((nparam, nparam))
            self.ad_cov = np.eye(nparam)
            self.ad_epsilon = 0.01 * np.eye(nparam)
            self.ad_a = 0.03
            self.ad_ncov = self.ad_K
            #self.ad_chol = np.eye(nparam)
            self.accept_window = deque()
            self.adapt = Adaptive(self.ad_target)
        else:
            self.adaptive = False

        ##Function to call on exit
        #if 'exit_function' in kwargs:
            #self.exit_function = kwargs['exit_function']
        #else:
            #self.exit_function = None

        #momentum vector
        self.pvec = np.zeros(nparam)
        self.pvec0 = np.zeros(nparam)

        #check for bounds in kwargs
        if 'bounds' in kwargs:
            self.bounds = kwargs['bounds']
            assert type(self.bounds) == np.ndarray
            assert self.bounds.ndim == 2
        else:
            self.bounds = np.column_stack([np.ones(nparam) * -1E256, 
                                           np.ones(nparam) * 1E256])


        #placeholder
        self.sample_path = None

    def __Lint(self):
        return self.L

    def __Llist(self):
        return np.random.randint(self.L[0], self.L[1] + 1)
        

    def __std_kinetic_energy(self, store,  pvec, theta):
        """Take M = I to evaluate the kinetic energy."""

        return 0.5 * np.dot(pvec, pvec)

    def __he_kinetic_energy(self, store, pvec, theta):
        """Take the -hessian as M in evaluting the kinetic energy."""
        store[self.attrib.name] = theta
        neghessian = -self.hessian(store)
        
        cholnh = np.linalg.cholesky(neghessian)
        p = np.linalg.solve(cholnh, pvec)
        halflndet = np.log(np.diag(cholnh)).sum()
        return halflndet + 0.5 * np.dot(p, p)
        

    def sampler(self, store):
        """Sample from posterior using HMC."""

        #parameter name
        name = self.attrib.name

        #increment count
        self.count = self.count + 1

        candtheta = self.LeapFrog(store)
        

        #check bounds
        if candtheta != None:

            #potential evaluated at candidate
            store[name] = candtheta
            
            candU = -self.post(store)

            #kinetic evaluate at candidate
            candK = self.__kinetic_energy(store, self.pvec,
                                          candtheta)

            #potential evaluate at previous
            store[name] = self.get_ltheta()
            prevU = -self.post(store)

            #kinetic evaluate at candidate
            prevK = self.__kinetic_energy(store, self.pvec0,
                                          self.get_ltheta())

            #compute acceptance probability
            alpha = np.exp(prevU - candU + prevK - candK)
            #print candtheta
            #print alpha
            #if store['iteration'] % 10 == 0:
                #pdb.set_trace()
        else:
            #automatically reject as outside bounds
            alpha = -1.

        if np.random.rand(1) < alpha:
            self.last_accept = True
            self.update_ltheta(candtheta)
            self.accept = self.accept + 1.
            theta = candtheta
           
        else:
            self.last_accept = False
            theta = self.get_ltheta()

        #if self.exit_function != None:
            #self.exit_function(theta, store)
        
        if self.adaptive == True:
            self.__adapt_scale(store)
            #self.__update_cov(store)
        return theta


    def __update_cov(self, store):
        """Function updates covariance."""
        
        theta = store[self.name]
        self.ad_cum_theta = self.ad_cum_theta + theta
        self.ad_theta_thetap = self.ad_theta_thetap + \
                np.outer(theta, theta)

        if store['iteration'] == self.ad_ti:

            #update covariance
            mean_theta = self.ad_cum_theta / self.ad_ncov
            self.ad_cov = self.ad_theta_thetap - self.ad_ncov * \
                    np.outer(mean_theta, mean_theta)

            self.ad_ncov = np.floor((1. + self.ad_a) * self.ad_ncov)
            self.ad_ti = self.ad_ti + self.ad_ncov

    def __adapt_scale(self, store):
        """Function adapts scale."""
        self.accept_window.append(self.last_accept)
        if store['iteration'] > self.ad_W:
            AR = float(sum(self.accept_window)) / len(self.accept_window)
            self.accept_window.popleft()
                

            if store['iteration'] < self.ad_K:
                #Use heuristic for adaption

                sm = self.adapt.scale(AR)
                self.scale = self.scale * sm

            elif store['iteration'] == self.ad_K:
                #Enforce diminishin adaption
                #comput b
                #self.ad_W = self.ad_W2
                
                self.ad_b = self.scale * 0.001 * store['iteration'] ** self.ad_r
            else:
                scale_star = max((0.001 * self.scale),
                                 self.ad_b * store['iteration'] ** (-self.ad_r))

                if AR < self.ad_target:
                    self.scale = self.scale - scale_star
                else:
                    self.scale = self.scale + scale_star



    def __std_Update_position(self, store, theta):
        """Updates the position vector following Neal(2010)."""

        theta = theta + self.scale * self.pvec
        return theta

    def __hessian_Update_position(self, store, theta):
        """Updates position vector following Girolami and Calderhead(2011)."""

        #compute -hessian
        store[self.attrib.name] = theta
        neghessian = -self.hessian(store)
        theta = theta + self.scale * np.linalg.solve(neghessian, theta)
        return theta

    def plot_path(self, i):
        plt.plot(np.array(self.sample_path)[:, i])
        plt.show()

    def LeapFrog(self, store):
        """Function makes L steps of the leapfrog estimator."""


        #get name and nparam
        name = self.attrib.name
        nparam = self.attrib.nparam[0]

        #sample momentum vector from N(0, I)
        #chneghess = np.linalg.cholesky(-self.hessian(store))
        #self.pvec0 = np.dot(chneghess, np.random.randn(nparam))
        self.pvec0 = np.random.randn(nparam)
        self.pvec = self.pvec0.copy()

        #initial position
        init_theta = store[name]
        theta = init_theta.copy()
        self.sample_path = [theta.copy()]

        #compute halfscale
        halfscale = 0.5 * self.scale

        #compute half step for momentum
        store[name] = theta
        grad = self.gradient(store)

        #half step for momentum at begininning
        self.pvec = self.pvec + halfscale * grad 

        #Compute L leapfrog steps
        L = self.__simL()
        for i in xrange(L):

            #update position vector
            theta = self.__Update_position(store, theta)
            self.sample_path.append(theta.copy())
            
            if any(theta < self.bounds[:, 0]) or\
               any(theta > self.bounds[:, 1]):
                
                return None

            #compute gradient at current position
            store[name] = theta
            grad = self.gradient(store)

            #update momentum vector
            if i != L-1:
                self.pvec = self.pvec + self.scale * grad
            else:
                self.pvec = self.pvec + halfscale * grad 

        #Negate momentum at to ensure symmetric proposal
        self.pvec = -self.pvec

        return theta
