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
import os
import sys
import types
import time
#import curses

import numpy as np

try:
    import matplotlib.pyplot as plt
    import matplotlib
    from mcmcplots import *
    FLAG_PLOT = True
    #Matplotlib is installed
except:
    #Matplotlib is not installed
    FLAG_PLOT = False

from mcmc_utilities import *
from mcmc_algorithms import *


class BlockScheme_i:
    """Class manages the ith blocking scheme. Used by MCMC class"""

    def __init__(self, blocks):

        #storage objects

        self.nblocks = len(blocks) #the number of blocks in the MCMC scheme
        self.ngroups = []
        self.group_names = []
        self.name_group = {}
        self.all_keys = []
        self.storeblock = {} #stores individual blocks in MCMC scheme

        #Form MCMC sampling scheme
        for i in xrange(len(blocks)):
            self.group_names.append('group'+str(i)) #name of group
            name = blocks[i].get_name() #name of block i
            ngroups = blocks[i].get_number_groups() #number of groups in block i
            ind_list = blocks[i].ind_list  #either true of false
            self.ngroups.append(ngroups) #stores the number of groups in block
            self.storeblock[self.group_names[i]] = blocks[i] #name of block
            if ind_list == False:
                #one parameter name for block
                self.all_keys.append(name)
                self.name_group[name] = self.group_names[i]
            else:
                #possible multiple parameter names for block
                for iname in name:
                    self.all_keys.append(iname)
                    self.name_group[iname] = self.group_names[i]


class BlockScheme:
    """Class manages the blocksing schemes."""

    def __init__(self, blocks, **kwargs):

        #Placeholders
        self.nblocks = None
        self.ngroups = None
        self.group_names = None
        self.name_group = None
        self.all_keys = None
        self.storeblock = None

        #Placeholder for multiple blocking scheme case
        self.multi_BS = None
        self.BS_prob = None

        #Check that blocks is of type list or tuple
        try:
            assert type(blocks) in [type(()), type([])]
            assert len(blocks) >= 1
        except:
            error = """Argument blocks in MCMC, must be of type
            tuple or list and of length greater or equal to one."""
            raise Exception(error)

        #check if blocks constains lists or tuples
        if type(blocks[0]) in [type(()), type([])]:
            if len(blocks[0]) == 1:
               blocks = blocks[0]
               single_blocking_scheme = True
            else:
               single_blocking_scheme = False
        else:
            single_blocking_scheme = True

        if single_blocking_scheme == True:
            #Single blocking scheme
            BS = BlockScheme_i(blocks)
            self.group_names = BS.group_names
            self.nblocks = BS.nblocks
            self.ngroups = BS.ngroups
            self.name_group = BS.name_group
            self.all_keys = BS.all_keys
            self.storeblock = BS.storeblock
            self.__update_BS = self.__no_update
        else:
            #multiple blocking schemes
            self.multi_BS = [bs for bs in blocks]

            #Initialise blocking scheme probabilities
            self.BS_prob = np.ones(len(blocks)) / len(blocks)

            #The first blocking scheme will be the one in the
            #code.

            self.switch_blocking_scheme(0)

            #default updating scheme
            self.__update_BS = self.__std_update

            if "custom_BS_update" in kwargs:
                self.__update_BS = kwargs['custom_BS_update']

    def switch_blocking_scheme(self, i):
        """Switch to blocking scheme i."""
        self.nblocks = BS.nblocks
        self.group_names = BS.group_names
        self.ngroups = BS.ngroups
        self.ngroups = self.multi_BS[i].ngroups
        self.name_group = self.multi_BS[i].name_group
        self.all_keys = self.multi_BS[i].all_keys
        self.storeblock = self.multi_BS[i].storeblock

    def update_blocking_scheme(self, store):
        """Function called at every iteration to update
        which kernel to call."""

        index = self.__update_BS(store)
        
        if index != None:
            self.switch_blocking_scheme(index)

    def __std_update(self, store):
        """Default blocking scheme for updating blocking scheme"""

        return np.random.multinomial(1, self.BS_prob).argmax()

    def __no_update(self, store):
        """Dummy function for the case of no update."""
        return None



class MCMC:
    """
    class for MCMC sampler. This class is initialised with:
    nit - the number of iterations
    burn - the burn in for the MCMC sampler
    data - A dictionary containing any data, functions or classes
           that may be required by any of the functions 
    blocks - a list containing functions that are used to sample from the
    full conditional posterior disitrbutions of interest
    kwargs - allows for optional arguments
        loglike - tuple containing a function that evaluates the
        log-likelihood, number of parameters in the likelihood and the name of
        the dataset. Eg: loglike = (loglike, nparam, 'yvec'). If the data contains
        a flag that represents non data, then that flag should be included as a 
        4th element in the data. Eg (loglike, nparam, 'yvec', flag). 

        DIC - function(store) the function used to calculate DIC.
        
        transform - [function(store), [parameternames]]. function(store) is the
            function that is used to transform the parameters, while
            [parameternames] is a list of parameter names that are being
            transformed. Summary statistics will be re-calculated for each of the
            parameters in the list. All of the parameters used in the transformation
            are required to be stored.

        runtime_output - If set to True, runtime output will print to screen. Is
                         set to False by default, as the curses environment makes
                         debugging difficult
        initialise - A function, which takes store as an argument, that is run
                     at the start of an MCMC scheme.
    """
    def __init__(self, nit, burn, data, blocks, **kwargs):
        self.burn = burn #length of burnin
        self.nit = nit   #number of iterations

        #check that blocks is either a list or a tuple
        try:
            assert type(blocks) in [type([]),  type(())]
        except:
            error = """blocks must either be of type tuple or list."""
            raise TypeError(error)

        #initialise class for blocking scheme
        self.block_s = BlockScheme(blocks)

        #self.nblocks = len(blocks) #the number of blocks in the MCMC scheme
        self.storeparam = {} #storage for all iterations
        self.totaltime = 0
        #self.all_keys = []
        assert type(data) == type({})
        self.currentparam = data
        #self.storeblock = {} #stores individual blocks in MCMC scheme
        #infomation that can be obtained in custom functions in blocks
        self.currentparam['iteration'] = 0
        self.currentparam['number_of_iterations'] = nit
        self.currentparam['length_of_burnin'] = burn
        self.currentparam['index'] = 0
        self.currentparam['mcmc_nblocks'] = self.block_s.nblocks
        self.currentparam['last_accept'] = [False] * self.block_s.nblocks
        #self.ngroups = []
        #self.group_names = []
        #self.name_group = {}
        self.update_param = {}
        self.not_stored_param = []
        self.current_transformed = {}

        #placeholder 
        self.ifstore = {}
        self.__post_transform = None

        #check for initialisation routine in kwargs
        if 'initialise' in kwargs and kwargs['initialise'] != None:
            #initialisation routine
            self.initialise = kwargs['initialise']
        else:
            self.initialise = None

        if 'post_transform' in kwargs:
            self.__post_transform = kwargs['post_transform']


        #allocate storage space
        for i in xrange(len(blocks)):
            BSSB = self.block_s.storeblock[self.block_s.group_names[i]]
            nparam = BSSB.get_nparam()
            ind_list = BSSB.ind_list
            name = BSSB.get_name()
            ngroups = BSSB.get_number_groups()
            
            if ind_list == False: #One parameter per block
                if BSSB.get_store() == 'all':
                    self.storeparam[name] = np.zeros([self.nit] + nparam)
                else:
                    self.not_stored_param.append(name)
                self.currentparam[name] = BSSB.get_ltheta()
        
            else:
                ltheta = BSSB.get_ltheta()
                for j in xrange(ngroups):
                    if BSSB.get_store()[j] == 'all':
                        self.storeparam[name[j]] = np.zeros([self.nit]+nparam[j])
                    self.currentparam[name[j]] = ltheta[j]

        self.numdec = 3
        self.meanstore = {}
        self.varstore = {}
        if 'loglike' in kwargs:
            if type(kwargs['loglike']) == type(()) and len(kwargs['loglike']) == 3:
                self.loglike = kwargs['loglike'][0]
                self.nparamlike = kwargs['loglike'][1]
                self.calcbic = True
                self.dataname = kwargs['loglike'][2]
                self.flag = False

            elif type(kwargs['loglike']) == type(()) and len(kwargs['loglike']) == 4: 
                self.loglike = kwargs['loglike'][0]
                self.nparamlike = kwargs['loglike'][1]
                self.calcbic = True
                self.dataname = kwargs['loglike'][2]
                self.flag = kwargs['loglike'][3]

                
            else:
                self.calcbic = False
                print "Warning; specification of tuple loglike in incorrect"
                print "Will not calculate BIC"
        else:
            self.calcbic = False

        #if 'transform' in kwargs:
        #    assert type(kwargs['transform']) == type([])
        #    assert len(kwargs['transform']) == 2
        #      
        #    self.transformfunc = kwargs['transform'][0]
        #    self.transform_list = kwargs['transform'][1]
        #    assert type(self.transform_list) == type([])
        #               
        #    self.transformfunc_ind = True
        #else:
        #    self.transformfunc_ind = False

        if 'DIC' in kwargs:
            self.DICfunction = kwargs['DIC']
            self.DIC_ind = True
        else:
            self.DIC_ind = False

        for key in self.block_s.all_keys:
            self.update_param[key] = self.__simple_update

        if 'transform' in kwargs and kwargs['transform'] != False: 
            assert type(kwargs['transform']) == type({})
            self.transform2_ind = True
            self.transform2 = kwargs['transform']
            for key in self.transform2:                                                
                try:
                    assert key in self.block_s.all_keys
                except:
                    message = key + ' not in ' + str(self.block_s.all_keys)
                    raise NameError(message)

                self.update_param[key] = self.__transform_update
            
            self.not_stored_param = list(set(self.not_stored_param).intersection(set(self.transform2.keys())))
            #for key in self.not_stored_param:
            #    if key not in self.transform2:
            #        self.not_stored_param.remove(key)
            #code 
            
            for i in xrange(self.block_s.nblocks):
                names = self.block_s.storeblock[self.block_s.group_names[i]].get_name()[:]		
                if self.block_s.ngroups[i] == 1:
                    if names in self.transform2:			
                        self.block_s.storeblock[self.block_s.group_names[i]].use_transformed(names)
                else:                    
                    for name in names:
                        if(name in self.transform2):
                            self.block_s.storeblock[self.block_s.group_names[i]].use_transformed(name)
        else:
            self.transform2_ind = False

        #placeholder for start time
        self.starttime = None

        #setup output from analysis
        if 'runtime_output' in kwargs and kwargs['runtime_output'] == True:
            self.toolbar_width = 40
            self.out_grid = None
            self.out_count = 0
            self.ind_runtime = True
        else:
            self.ind_runtime = False

        ##initialise curses
        #if 'runtime_output' in kwargs and kwargs['runtime_output'] == True:
        #    self.ind_runtime = True
        #    self.curses_count = 0
        #    self.increment = 0

        #    #Note declaring placeholders
        #    self.stdscr = None
        #    self.curses_num = None
        #    self.curses_grid = None
        #    
        #else:
        #    self.ind_runtime = False


    def sampler(self):
        """Runs the MCMC sampler"""
        self.starttime = time.time()        

        if self.initialise != None:
            #run initialisation routine
            
            self.initialise(self.currentparam)

        if self.ind_runtime:
            try:
                self.__init_runtime_output()
                for it in xrange(self.nit):
                    self.__scan_blocks(it)
                    self.post_transform(it)
                    self.block_s.update_blocking_scheme(self.currentparam)
                    self.__runtime_output(it)
            finally:
                self.__finish_runtime_output()
        else:
            for it in xrange(self.nit):
                self.__scan_blocks(it)
                self.post_transform(it)
                self.block_s.update_blocking_scheme(self.currentparam)
                
            

        self.totaltime = time.time() - self.starttime
        #if self.transformfunc_ind == True:
        #    try:
        #        self.transformfunc(self.storeparam)
        #    except:
        #        print "Could not transform iterates, specified parameter was not stored"

    def __scan_blocks(self, it):
        """Function produces one iteration of MCMC sampling scheme"""
        self.currentparam['iteration'] = it #set current iteration
        for i in xrange(self.block_s.nblocks): #iterate over block
            BSSB = self.block_s.storeblock[self.block_s.group_names[i]]
            
            #indicator true or false (one name in block)
            ind_list = BSSB.ind_list
            
            #Optional identifier for block; 0 by default
            self.currentparam['index'] = BSSB.get_index()

            #entru function
            BSSB.entry_function(self.currentparam)

            #samples parameter from block
            sample = BSSB.sample(self.currentparam)
            self.currentparam['last_accept'][i] = \
                BSSB.get_last_accept()


            #name of parameter in block
            name = BSSB.get_name()

            if ind_list == False:
                #one parameter in block

                #set current value to sampled parameter
                self.currentparam[name] = sample 

                if BSSB.get_store() == 'all':                    
                    #store parameters in block
                    try: 
                        self.storeparam[name][it] = self.update_param[name](name)
                    except:
                        raise ValueError("dimensions don't match for " + name)
            else:
                #more than one parameter in block
                for j in xrange(self.block_s.ngroups[i]):
                    #iterate over groups

                    #set current parameter j to sample
                    self.currentparam[name[j]] = sample[j]
                                          
                for j in xrange(self.block_s.ngroups[i]): #iterate over groups
                    if BSSB.get_store()[j] == 'all':
                        #store parameter
                        try:
                            self.storeparam[name[j]][it] = self.update_param[name[j]](name[j])
                        except ValueError as err:
                            print "ERROR, problem with %s" % name[j]
                            print "\t%s has shape" % name[j],self.storeparam[name[j]][it].shape
                            print "\tupdate_param has shape", self.update_param[name[j]](name[j]).shape
                            print err
                            sys.exit(1)
            BSSB.exit_function(self.currentparam)
            if it >= self.burn:
                if self.transform2_ind == True:
                    self.__update_transformed_not_stored()
                    if self.block_s.ngroups[i] == 1:
                        if name in self.transform2:
                            BSSB.update_transformed(self.current_transformed)
                    else:
                        if self.__eitherstored(name, self.transform2):
                            BSSB.update_transformed(self.current_transformed)
                BSSB.update_stats()

    def post_transform(self, it):
        """Function transforms after scan_blocks is complete."""

        if self.__post_transform != None:
            #run function to transform current parameter values
            self.__post_transform(self.currentparam)
            for i in xrange(self.block_s.nblocks): #iterate over block
                BSSB = self.block_s.storeblock[self.block_s.group_names[i]]

                #indicator true or false (one name in block)
                ind_list = BSSB.ind_list

                #name of parameter in block
                name = BSSB.get_name()

                if ind_list == False:
                    #store parameters in block
                    if BSSB.get_store() == 'all':
                        try: 
                            self.storeparam[name][it] = self.currentparam[name]
                        except:
                            raise ValueError("dimensions don't match for " + name)
                else:
                    #more than one parameter in block
                                              
                    for j in xrange(self.block_s.ngroups[i]): #iterate over groups
                        if BSSB.get_store()[j] == 'all':
                            #store parameter
                            try:
                                self.storeparam[name[j]][it] = self.currentparam[name[j]]
                            except ValueError as err:
                                print "ERROR, problem with %s" % name[j]
                                print "\t%s has shape" % name[j],self.storeparam[name[j]][it].shape
                                print "\tupdate_param has shape", self.update_param[name[j]](name[j]).shape
                                print err
                                sys.exit(1)

    def __eitherstored(self, names, transform2):
        for name in names:
            if name in transform2:
                return True
        return False

    def __simple_update(self, name):
        return self.currentparam[name]

    def __transform_update(self, name):
        theta = self.transform2[name](self.currentparam)
        self.current_transformed[name] = theta
        return theta

    def __update_transformed_not_stored(self):
        for name in self.not_stored_param:
            self.current_transformed[name] = self.transform2[name](self.currentparam)

    def return_array(self, arr):
        if arr.shape[0] > 1:
            return arr
        else:
            return arr[0]
    
    def get_parameter(self, name):
        """Returns an array of the parameter iterates including burnin"""
        try:
            return self.storeparam[name]
        except KeyError as e:
            print e
            raise KeyError("ERROR: %s has not been stored!!" % name)
   
    def get_parameter_exburn(self, name):
        """Returns an array of the parameter iterates excluding burnin"""
        try:
            return self.storeparam[name][self.burn:self.nit, :]
        except KeyError as e:
            print e
            raise KeyError("ERROR: %s has not been stored!!" % name)

    def get_HPD(self, name, alpha):
        """Function returns the (1 - alpha) HPD interval for the
        parameter defined by the string 'name'"""

        paramstore = self.get_parameter_exburn(name)
        ## and we calculate the hpd's for this
        out05 = np.apply_along_axis(hpd, 0, paramstore, 0.05)
        return out05

        
   
   
    def get_mean_cov(self, listname):
        """returns the posterior covariance matrix for the parameters named
        in listname"""
        assert(type(listname) == type([]))
        i = 0
        for name in listname:
            tmp = self.storeparam[name]
            if i == 0:
                mat = tmp
            else:
                mat = np.hstack([mat, tmp])
            i = i + 1
        #    mat.append(self.storeparam[name])
        return np.mean(mat, axis = 0), np.cov(mat.T)

    def get_acceptance_rate(self, name):
        """Returns the acceptance rate from the MCMC estimation for the parameter
        corresponding to name."""

        return self.block_s.storeblock[self.block_s.name_group[name]].acceptance_rate()

    def get_mean_var(self, name):
        """Returns the estimate from the MCMC estimation for the posterior mean and
        variance"""
        
        ngroups = self.block_s.storeblock[self.block_s.name_group[name]].get_number_groups()
        if ngroups == 1:
             mean_var =  self.block_s.storeblock[self.block_s.name_group[name]].\
                    get_stats(self.nit, self.burn)

             if type(mean_var[0]) == type([]):
                 mean_var = (mean_var[0][0], mean_var[1][0])
             
             return mean_var



        else:
            meanvar = self.block_s.storeblock[self.block_s.name_group[name]].\
                    get_stats(self.nit, self.burn)
            names = self.block_s.storeblock[self.block_s.name_group[name]].get_name()
            index = names.index(name)
            meanp = meanvar[0][index]
            varp = meanvar[1][index]
            return meanp, varp
    
            

        
    def set_number_decimals(self, num):
        """Sets the number of decimal places for the output"""
        self.numdec = num

    # def AddBlock(self, block):
    #    self.block_s.storeblock[block[0].get_name()] = block

    def calc_BIC(self):
        loglike = self.loglike(self.currentparam)
        numparam = self.nparamlike
        if self.flag == False:
            nobs = self.currentparam[self.dataname].size 
        else:
            nobs = np.sum(self.currentparam[self.dataname] != self.flag)

        bic =-2.*loglike + float(numparam) * np.log(nobs) 
        return bic, loglike 

    def __init_runtime_output(self):

        num_it = 'The number of iterations = ' + str(self.nit)
        num_burn = 'The length of the burnin = ' + str(self.burn)
        self.out_grid = (np.linspace(0, self.nit, self.toolbar_width+1)).astype('i')
        
        print "PyMCMC is now running"
        print
        print num_it
        print num_burn
        print
        sys.stdout.write("[%s]" % (" " * self.toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (self.toolbar_width + 1))
                         
                          
        

        
    #def __init_runtime_output(self):
    #    self.stdscr = curses.initscr()
    #    height, width = self.stdscr.getmaxyx()
    #    self.curses_num = min(width, 40)
    #    self.curses_grid = (np.linspace(0, self.nit, self.curses_num-6)).astype('i')
    #    num = self.curses_num

    #    self.stdscr.addstr(0, 0, 'PyMCMC is now running')
    #    num_it = 'The number of iterations = ' + str(self.nit)
    #    num_burn = 'The length of the burnin = ' + str(self.burn)
    #    if max(len(num_it), len(num_burn)) <= self.curses_num:
    #        self.increment = 2
    #        self.stdscr.addstr(2,0, num_it)
    #        self.stdscr.addstr(3,0, num_burn)

    #    incr = self.increment
    #    self.stdscr.addch(4 + incr,0,'[')

    #    self.stdscr.addch(4 + incr,num-6,']')
    #    self.stdscr.addstr(4 + incr,num-4,'% ')
    #    self.stdscr.refresh()

    def __runtime_output(self, iteration):
        if iteration < self.nit:
            if iteration == self.out_grid[self.out_count]:
                sys.stdout.write("#")
                sys.stdout.flush()
                self.out_count = self.out_count + 1

    #def __runtime_output(self, iteration):
    #    num = self.curses_num
    #    incr = self.increment
    #    if iteration < self.nit:
    #        if iteration == self.curses_grid[self.curses_count]:
    #            self.stdscr.addch(4 + incr,1+self.curses_count, '#')
    #            self.curses_count = self.curses_count + 1
    #            percent = int((100. * self.curses_count) / (num - 7))
    #            time_taken = time.time() - self.starttime
    #            self.stdscr.addstr(4 + incr, num-2,str(percent))
    #            
    #            approx_time = 'Time elapsed = ' + str(int(time_taken))
    #            est_time = time_taken / (percent / 100.)
    #            estimated_total_time = 'Total time = ' + str(int(est_time))
    #            estimated_time = 'Time remaining = ' + str(int(est_time - time_taken))

    #            self.stdscr.addstr(6 + incr,0,'Approximate timings in seconds')
    #            self.stdscr.addstr(7 + incr, 0, approx_time)
    #            self.stdscr.addstr(8 + incr, 0, "           ")
    #            self.stdscr.addstr(8 + incr, 0, estimated_time)
    #            self.stdscr.addstr(9 + incr, 0, estimated_total_time)
    #            self.stdscr.refresh()

    def __finish_runtime_output(self):
        #curses.endwin()
        sys.stdout.write("\n")
        

        



    def get_plot_suffix(self):
        '''
        get a suitable string for the
        plot type. This depends on the backend
        '''
        if FLAG_PLOT == False:
            error = """Matplotlib is not installed on this system. You cannot
            use function get_plot_suffix without it."""
            raise Exception(error)

        backend = matplotlib.get_backend()
        ## later 
        return backend

    def get_default_filename(self, basename ="pymcmc"):
        '''
        get a suitable default filename that suits
        the plot type.
        '''
        
        if FLAG_PLOT == False:
            error = """Matplotlib is not installed on this system. You cannot
            use function get_default_filename without it."""
            raise Exception(error)

        output_backends = ['svg', 'pdf', 'ps', 'eps','gdk',
                           'agg', 'emf', 'svgz', "jpg", 'Qt4Agg']
        output_suffixes = ['.svg', '.pdf', '.ps', '.eps','.gdk',
                           '.png', '.emf', '.svgz', ".jpg", '.png']
        thisbackend = matplotlib.get_backend().lower()
        for i in range(len(output_backends)):
            if thisbackend == output_backends[i]:
                filename = "%s%s" % (basename, output_suffixes[i])
                return filename
        return None

    def get_plot_dimensions(self, kwargs):
        nelements = len(kwargs['elements'])
        ## now work out the dimension
        totalplots = nelements * len(kwargs['plottypes'])
        if kwargs.has_key('individual') and kwargs['individual']:
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
            cols = len(kwargs['plottypes']) * np.floor(np.sqrt(totalplots)/len(
                kwargs['plottypes']))
            if cols == 0:
                cols = len(kwargs['plottypes'])
            rows = int(np.ceil(totalplots/cols))
        else:
            rows = kwargs['rows']
            cols = kwargs['cols']

        totalpages = np.ceil(totalplots/(cols*rows))
        plotdims = {'totalplots':totalplots,
                    'cols':int(cols),
                    'rows':int(rows),
                    'figsperplot':int(rows * cols),
                    'totalpages':int(totalpages)}
        return plotdims

        
    def plot(self, blockname, **kwargs):
        '''
        The basic plotting approach for the MCMC class.

        Create summary plots of the MCMC sampler. By default, a plot
        of the marginal posterior density, an ACF plot and a trace
        plot are produced for each parameter in the block. The
        plotting page is divided into a number of subfigures. By
        default, the number of number of columns are approximately
        equal to the square root of the total number of subfigures
        divided by the number of different plot types.
        
        Arguments:

          blockname: The name of the parameter for which summary plots
          are to be generated.

        Keyword arguments:

          elements: a list of integers specifying which elements are
          to be plotted. For example, if the blockname is beta and
          beta has n elements in it, you may specify elements as
          elements = [0, 2, 5], where any of the list containing
          integers less than n.

          plottypes: a list giving the type of plot for each
          parameter. By default the plots are density, acf and
          trace. A single string is also acceptable.

          filename: A string providing the name of an output file for
          the plot. Since a plot of a block may be made up of a number
          of sub figures, the output name will be modified to give a
          separate filename for each subfigure. For example, if the
          filename is passed as plot.png, this will be interpreted
          as plot%03d.png, and will produce the files plot001.png,
          plot002.png, etc. The type of file is determined by the
          extension of the filename, but the output format will also
          depend on the plotting backend being used. If the filename
          does not have a suffix, a default format will be chosen
          based on the graphics backend. Most backends support png,
          pdf, ps, eps and svg, but see the documentation for
          matplotlib for more details.

          individual: A boolean option. If true, then each sub plot
          will be done on an individual page.

          rows: Integer specifying the number of rows of subfigures on
          a plotting page.

          cols: Integer specifying the number of columns of subfigures
          on a plotting page.

        '''


        if FLAG_PLOT == False:
            error = """Matplotlib is not installed on this system. You cannot
            use function plot without it."""
            raise Exception(error)

        ## plt.figure()
        paramstore = self.get_parameter_exburn(blockname)
        if not kwargs.has_key('elements'):
            ## we assume you want all the parameters
            kwargs['elements'] = range(paramstore.shape[1])
            
        ## which plots do you want
        if kwargs.has_key('plottypes'):
            ## if you pass a single string, it should
            ## still work:
            if isinstance(kwargs['plottypes'], basestring):
                kwargs['plottypes'] = [kwargs['plottypes']]
        else:
            ## then we assume you want
            ## the following
            kwargs['plottypes'] = ['density', 'acf', 'trace']
            
        nelements = len(kwargs['elements'])
        
        ## now work out the dimension
        plotdims = self.get_plot_dimensions(kwargs)

        ## see if we need a filename 
        defaultfilename = self.get_default_filename()
        if not kwargs.has_key('filename') and defaultfilename:
            ## then we need a default filename
            kwargs['filename'] = defaultfilename

        ## if you need a filename, then not in interactive
        if defaultfilename:
            interactive = False
        else:
            interactive = True
        
        
        ## set up the subfigure
        ## I think you can set up a function in here
        ## until then I'll just use a loop
        plotcounter = 0
        pagecounter = 0
        
        ## check to see if blockname is a latex word
        try:
            aa = latexysmbols.index(blockname)
            ptitle = r'$\%s$' % blockname
        except:
            ptitle = blockname
        for i in kwargs['elements']:
            for plottype in kwargs['plottypes']:
                ## do we need a new figure?
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
                try:
                    aa = latexsymbols.index(blockname)
                    title = r'$\%s_%d$' % (blockname, i)
                except:
                    title = "%s_%d" % (blockname, i)
                if plottype == 'acf':
                    bwcalc = InefficiencyFactor()
                    bw = bwcalc.calc_b(paramstore[:, i])
                    maxlag = max(round(1.5 * bw/10.) * 10, 10)
                    PlotACF(paramstore[:, i], maxlag, "ACF Plot %s" % title)
                elif plottype == "density":
                    ##avoid overlapping labels
                    if plotdims['figsperplot'] > 4:
                        ntick = 5
                    else:
                        ntick = 10
                    PlotMarginalPost(paramstore[:, i],
                                     "MPD %s" % title, plottype="both",
                                     maxntick=ntick)
                elif plottype == "trace":
                    ##avoid overlapping labels
                    if plotdims['figsperplot'] > 4:
                        ntick = 5
                    else:
                        ntick = 10
                    PlotIterates(paramstore[:, i], "Trace %s" % title,ntick)
                else:
                    pass
        pagecounter = pagecounter + 1
        ## then already plotted something,
        ## we might want to save it
        if kwargs.has_key('filename'):
            if plotdims['totalpages'] > 1:
                (base, suffix) = os.path.splitext(kwargs['filename'])
                fname = "%s%03d%s" % (base, pagecounter, suffix)
            else:
                fname = kwargs['filename']
            plt.savefig(fname) 
        if interactive:
            plt.show()


    def showplot(self):
        '''
        show any plots you have created.
        '''


        if FLAG_PLOT == False:
            error = """Matplotlib is not installed on this system. You cannot
            use function showplot without it."""
            raise Exception(error)

        plt.show()
        

    def CODAwrite(self, param, paramname, fobj, findixobj,
                  prange, start, thin, offset):
        '''
        Writes the stored results to file in CODA format.
        Each simulation is written on a single line, preceded
        by the simulation number.

        Arguments:
          param: the data from store (numpy array)
          paramname: the name of the parameter
          fobj: a file handle to write the iterates to.
          findixobj: a file handle to write the index to
          prange: a list of indices. If false, we assume
                  you want all components.
          start: the start the iterates. If burnin is
                 included, this will be 1, otherwise
                 it will be the burnin
          thin: In case you want to thin the output. Every
                jth line will be written, with j=thin.
          offset: Required to write the index file. The
                index file requires line numbers, so if
                you have already written some values to
                file, you need to know the offset.

        Output:
          offset: this will be the value of offset +
                the total number of lines written.

        '''
        nrow = param.shape[0]
        dim = param.shape[1:]
        if not prange:
            prange = [np.unravel_index(i,dim) for i in range(np.prod(dim))]
        itnumbers = np.arange(start, start + nrow, thin)
        nitems = len(itnumbers)
        totalitems = 0
        for pos in prange:
            if len(pos) == 1:
                myslice = np.index_exp[::thin,pos[0]]
                if np.prod(dim)==1:
                    pname = paramname
                else:
                    pname = "%s[%d]" % (paramname,pos[0])
            elif len(pos) == 2:
                myslice = np.index_exp[::thin,pos[0],pos[1]]
                pname = "%s[%d,%d]" % (paramname,pos[0],pos[1])
            elif len(pos) == 3:
                myslice = np.index_exp[::thin,pos[0],pos[1],pos[2]]
                pname = "%s[%d,%d,%d]" % (paramname,pos[0],pos[1],pos[2])
            elif len(pos) == 4:
                myslice = np.index_exp[::thin,pos[0],pos[1],pos[2],pos[3]]
                pname = "%s[%d,%d,%d,%d]" % (
                    paramname,pos[0],pos[1],pos[2],pos[3])
            else:
                print "Can't write coda output for arrays with dim > 4"
            tmp = np.transpose(np.array([itnumbers, param[myslice]]))
            np.savetxt(fobj, tmp, ["%d", "%.06f"])
            findixobj.write("%s %d %d\n" % (pname, start + offset,
                                            start + offset + nitems -1))
            start = start + nitems
            totalitems = totalitems + nitems
        return offset + totalitems
        
            
    def CODAoutput(self, **kwargs):
        '''
        
        Output the results in a format suitable for reading in using CODA.

        Write the output to file  in a format that can be read in by CODA.
        By default, there will be two files created, coda.txt and coda.ind.

        Keyword arguments:

         filename: A string to provide an alternative filename for the
          output. If the file has an extension, this will form the
          basis for the data file, and the index file will be named by
          replacing the extension with ind. If no extension is in the
          filename, then two files will be created and named by adding
          the extensions .txt and .ind to the given filename.

         parameters: a string, a list or a dictionary.
          As in output, kwargs can contain a parameters arguemnt. 
          This tells us what we want to save to file.
          It can be is something like 'alpha'
           or it can be a list (eg ['alpha', 'beta'])
           or it can be a dictionary (eg {'alpha':{'range':[0, 1, 5]}},
          If you supply a dictionary, the key is the parameter name
          then you can have a range key with a range of elements.
          If the range isnt supplied, we assume that we want all the elements.
          You can use, for example,
          parameters = {'beta':{'range':[0, 2, 4]}}

         thin: integer specifying how to thin the output. 
          
        '''
        if kwargs.has_key('thin'):
            thin = kwargs['thin']
        else:
            thin = 1
        ## delete any previous output
        if kwargs.has_key('filename'):
            ## work out the two file names
            fname = kwargs['filename']
            ## see if it has an extension:
            basename, extension = os.path.splitext(fname)
            if len(extension) == 0:
                ## you didn't give an extension
                ## so we make one up
                fname = "%s.txt" % basename
            findexname = "%s.ind" % basename
        else:
            fname = "coda.txt"
            findexname = "coda.ind"
        if os.path.exists(fname):
            os.unlink(fname)
        if os.path.exists(findexname):
            os.unlink(findexname)
        fobj = open(fname, "a")
        findobj = open(findexname, "a")
        start = 1
        #indrow refers to the line number of the
        #txt file for the parameter. It is used in
        #the ind file
        indrow = 1
        if 'parameters' in kwargs:
            ## since parameters could be a dictionary
            ## but not necessarily,
            ## we will force it to be one.
            ## If it is passed as a dictionary, it might have
            ## a range argument, which we check later.
            parameters = kwargs['parameters']            
            ## first see if it is a single string
            if type(kwargs['parameters']) == types.StringType:
                parameters = {kwargs['parameters']:{}}
            elif type(kwargs['parameters']) == types.ListType:
                parameters = {}
                for pname in kwargs['parameters']:
                    parameters[pname] = {}
            else:
                parameters = kwargs['parameters']
        else:
            ## then we make up a dictionary ourselves:
            parameters = {}
            
            for i in range(self.block_s.nblocks):
                groupname = self.block_s.group_names[i]
                thisblock = self.block_s.storeblock[groupname]
                ## seems that this can be a list or a string
                ## so we check
                thisname = thisblock.get_name()
                if thisblock.get_store() == 'all':
                    if not isinstance(thisname, list):
                        thisname = [thisname]
                    for keyname in thisname:
                        parameters[keyname] = {}
        offset = 0
        for blockname in parameters.keys():
            if kwargs.has_key('exclude_burnin') and kwargs['exclude_burnin']:
                paramstore = self.get_parameter_exburn(blockname)
                nitems = (self.nit - self.burn)/thin
                start = self.burn
            else:
                paramstore = self.get_parameter(blockname)
                nitems = self.nit/thin
                start = 1
            if 'range' in parameters[blockname]:
                #then we want a subset
                tmprange = parameters[blockname]['range']
                prange = []
                try:
                    for i in tmprange:
                        if type(i) == types.IntType:
                            prange.append( (i, ) )
                        else:
                            ## assume already a tuple
                            prange.append(i)
                except:
                    print "Couldn't make sense of your selected range"
                    print "Using all elements"
                    prange = False
            else:
                prange = False
            offset = self.CODAwrite(paramstore, blockname, fobj, findobj,
                           prange, start, thin, offset)
        fobj.close()
            


    def print_header(self, destination, totaltime, nblocks, colwidth):
        '''
        Print a generic header for the output
        '''
        print >>destination, ""
        print >>destination, \
              "--------------------------------------------------------"
        print >>destination, ""
        print >>destination, \
          "The time (seconds) for the MCMC sampler = %.2f" % totaltime
        print >>destination, "Number of blocks in MCMC sampler = ", nblocks
        print >>destination, ""
        print >>destination, "{0: >{2}}{1: >{3}}".format("mean", "sd",
                                                         colwidth * 2, colwidth),
        print >>destination, "{0: >{2}}{1: >{2}}".   \
              format("2.5%", "97.5%", colwidth),
        print >>destination, "{0: >{1}}".format("IFactor", colwidth)

        
    def formatPosition(self, position):
        '''a position is the index of an element.
        eg (2, 1). I want to format it in a particular way
        eg (2, 1) -> [2, 1]
        but (2, ) -> [2]
        and () ->
        '''
        aa = format(position)
        if len(position) == 0:
            aa = ""
        elif len(position) == 1:
            aa = '[%d]' % position[0]
        else:
            aa = '[%s]' % ', '.join([str(i) for i in position])
        return aa
    
        


    def print_summary(self, destination, paramname, meanval, sdval,
                     ifactor, hpdintervals, hpd05,
                     prange, colwidth, sigfigs):
        '''
        format the output for a single line.
        Arguments are the name of the parameter, its
        mean value, the standard deviation and the ifactor.
        '''
        ## now, the elements might be a single no.
        ## or a 1 d array,
        ## or a 2 d array
        b = np.ndenumerate(meanval)
        name = paramname
        all_summary_vals = np.array([])
        summary_names = []
        for position, value in b:
            summary_vals = np.zeros( (5,), float)
            #if the position is found in prange,
            #or if you didn't specify a prange,
            if (prange and position in prange) or not prange:
                if meanval.flatten().shape[0] > 1:
                    name = "{0}{1}".format(
                        paramname, self.formatPosition(position)
                        )
                print >>destination, "{name: >{colwidth}}\
{val1: >0{colwidth}.{sigfigs}g}{val2: >0{colwidth}.{sigfigs}g}".format(
                    name = name,
                    val1 = value,
                    val2 = sdval[position],
                    colwidth = colwidth, sigfigs = sigfigs),
                summary_names.append(name)
                summary_vals[0] = value
                summary_vals[1] = sdval[position]
                if hpdintervals:
                ## now for the hpd's
                    print  >>destination, "{val1: >0{colwidth}.{sigfigs}g}\
{val5: >0{colwidth}.{sigfigs}g}".format(
                        val1 = hpd05[0][position],
                        val5 = hpd05[1][position],
                        colwidth = colwidth, sigfigs = sigfigs),
                    summary_vals[2] = hpd05[0][position]
                    summary_vals[3] = hpd05[1][position]
                else:
                    for i in range(2):
                       print  >>destination, \
                        "{0: >0{colwidth}}".format("NA", colwidth = colwidth - 1),
                    summary_vals[2] = np.nan
                    summary_vals[3] = np.nan

                thisifactor = ifactor[position]
                ##check for Chris's nan value
                if np.isnan(float(thisifactor)):
                    thisifactor = 'NA'
		if type(thisifactor) == type('a string'):
                    ## then not numeric.
                    ## Is there a better way of testing?
		    print  >>destination,     \
                       "{val1: >0{colwidth}}".format(val1 = thisifactor,
                                                     colwidth = colwidth)
                    summary_vals[4] = np.nan
                else:
                    print >>destination,      \
                          "{val1: >0{colwidth}.{sigfigs}g}".format(
                        val1 = float(thisifactor),
                        colwidth = colwidth, sigfigs = sigfigs)
                    summary_vals[4] = ifactor[position]
                all_summary_vals = np.r_[all_summary_vals,summary_vals]
        return summary_names,all_summary_vals


    def output(self, **kwargs):
        """
        Produce output for MCMC sampler.

        By default output is produced for all parameters. Function
        takes the following options:
           * parameters: A dictionary, list or string
             specifying which parameters are going to be presented.

             If a string (eg 'beta'), all elements of that parameter
             are given.

             If a list, (eg ['alpha', 'beta']), all elements of each
             parameter in the list are given.

             If a dictionary (eg {'alpha':{'range':[range(5)]}}), then
             there is the possibility to add an additional argument
             'range', which tells the output to only print a subset
             of the parameters. The above example will print
             information for alpha[0],alpha[1],...alpha[4] only.
             For 2d and higher arrays, the range should be specified
             so for a 3d array, it would look like:
                'range':( (i,j,k),(l,m,n) )

           * custom - A user define function that produces custom output.
           * filename - A filename to which the output is printed. By
             default output will be printed to stdout.
        """
        summary_vals = np.array([])
        summary_names = []
        acceptance_rates = {}
        if kwargs.has_key("filename"):
            destination = open(kwargs['filename'], 'w')
        else:
            destination = sys.stdout
        if kwargs.has_key("custom"):
            kwargs['custom'](destination)
        else:
            if 'parameters' in kwargs:
                ## since parameters could be a dictionary
                ## but not necessarily,
                ## we will force it to be one.
                ## If it is passed as a dictionary, it might have
                ## a range argument, which we check later.
                parameters = kwargs['parameters']            
                ## first see if it is a single string
                if type(kwargs['parameters']) == types.StringType:
                    parameters = {kwargs['parameters']:{}}
                elif type(kwargs['parameters']) == types.ListType:
                    parameters = {}
                    for pname in kwargs['parameters']:
                        parameters[pname] = {}
                else:
                    parameters = kwargs['parameters']
            else:
                ## then we make up a dictionary ourselves:
                parameters = {}
                for i in range(len(self.block_s.all_keys)):
                    parameters[self.block_s.all_keys[i]] = {}


            IF = InefficiencyFactor()
            ## these should be set somewhere within 
            colwidth = 12
            sigfigs = self.numdec

            self.print_header(destination, self.totaltime, self.block_s.nblocks, colwidth)

            for paramname in parameters.keys():
                meanp, varp = self.get_mean_var(paramname)
                    
                #if self.transformfunc_ind == True:
                #    if paramname in self.transform_list:
                #        meanp = np.mean(self.get_parameter_exburn(paramname), axis = 0)
                #        varp = np.var(self.get_parameter_exburn(paramname), axis = 0)
                
                self.meanstore[paramname] = meanp
                self.varstore[paramname] = varp
                BSSB = self.block_s.storeblock[self.block_s.name_group[paramname]]

                
                store = False
                if type(BSSB.get_store()) == type([]):
                    for i, name in enumerate(BSSB.get_name()):
                        if name == paramname:
                            if BSSB.get_store()[i] == 'all':
                                store = True

                        
                
                elif BSSB.get_store() == 'all':
                    store = True
                if store:
                    ifactor = IF.calculate(self.get_parameter_exburn(paramname)).\
                      round(self.numdec)
                    self.ifstore[paramname] = ifactor
                else:
                    if type(meanp) == types.FloatType or type(meanp) == np.float64:
                        ifactor = [np.nan]
                    elif np.array(meanp).ndim == 1:
                        ifactor = [np.nan] * len(meanp)
                    elif np.array(meanp).ndim == 2:
                        ifactor =  np.resize(np.array([np.nan]),meanp.shape)
                    else:
                        print "ERROR: I don't know how to deal with arrays of shape",meanp.shape,"yet"
                        return None
                ## ifactor.shape = meanp.shape
                ## and calc hpds'
                if store:
                    out05 = self.get_HPD(paramname, 0.05)
                    #paramstore = self.get_parameter_exburn(paramname)
                    ### and we calculate the hpd's for this
                    #out05 = np.apply_along_axis(hpd, 0, paramstore, 0.05)
                    hpdintervals = True
                else:
                    hpdintervals = False
                    out05 = None
                if 'range' in parameters[paramname]:
                    ## then we want a subset
                    tmprange = parameters[paramname]['range']
                    ## we do some minimal massaging of this list
                    ## each element should be a tuple. If its not
                    ## we assume it should be
                    prange = []
                    try:
                        for i in tmprange:
                            if type(i) == types.IntType:
                                prange.append( (i, ) )
                            else:
                                ## assume already a tuple
                                prange.append(i)
                    except:
                        print "Couldn't make sense of your selected range"
                        prange = False
                    
                else:
                    ## not sure how we should deal with
                    ## 2/3d arrays...
                    prange = False                    
                these_names,thisval = (self.print_summary(destination, paramname,
                                  np.atleast_1d(meanp),
                                  np.atleast_1d(np.sqrt(varp)),
                                  np.atleast_1d(ifactor),
                                  hpdintervals,
                                  np.atleast_1d(out05),
                                  prange,
                                  colwidth, sigfigs))
                summary_vals = np.r_[summary_vals,thisval]
                summary_names.extend(these_names)
                ## this is where you would put the acceptance rate info in.
            if self.calcbic == True:
                for paramname in parameters.keys():
                    meanp, varp = self.get_mean_var(paramname)
                    self.meanstore[paramname] = meanp
                    self.varstore[paramname] = varp
                    self.currentparam[paramname] = self.meanstore[paramname]
                BIC, LOGLIKE = self.calc_BIC();

            print ""
            for name in parameters.keys():
                print >>destination, 'Acceptance rate ', name, ' = ', \
                self.get_acceptance_rate(name)
                acceptance_rates[name] = self.get_acceptance_rate(name)
            summary_vals = summary_vals.reshape( (-1,5))
            self.output_dictionary = {'parameter names':summary_names,
                                      'summary values':summary_vals,
                                      'acceptance rates':acceptance_rates
                                      }
            if self.calcbic == True:
                #convert to float if needed
                try:
                    BIC = BIC[0]
                    LOGLIKE = LOGLIKE[0]
                except:
                    pass
                print >>destination, "BIC = {bic: .{sigfigs}f}".format(
                    bic = BIC,sigfigs=sigfigs)
                
                print >>destination, \
                      "Log likelihood = {loglik: .{sigfigs}f}".format(
                    loglik = float(LOGLIKE) ,sigfigs=sigfigs)
                self.output_dictionary['BIC'] = BIC
                self.output_dictionary['LOGLIKE'] = LOGLIKE
            if self.DIC_ind:
                # we have a DIC function, so we do the
                # calculation and present the result.
                for paramname in parameters.keys():
                    meanp, varp = self.get_mean_var(paramname)
                    self.currentparam[paramname] = meanp
                DIC = self.DICfunction(self.currentparam)
                print >>destination, "DIC = {bic: .{sigfigs}f}".format(
                    bic = DIC,sigfigs=sigfigs)
 
                
