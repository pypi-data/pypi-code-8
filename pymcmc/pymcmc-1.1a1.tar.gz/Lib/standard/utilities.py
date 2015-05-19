# Python code with useful MCMC utilties
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


from munkres import Munkres
import pymcmc.mixture_model as mm
import numpy as np
import types


class LabelSwitch:
    """A class used to help with label switching.
    loglikelihood - loglikelihood function, which should take one
                    argment; store.
    name - string which identifies vector of indicators used in auxiliary
           mixture representation.

    step - compute reference set every step iterations during burnin 

    nmix - the number of components in the mixture.
    """

    def __init__(self, loglikelihood,  name, step, nmix):

        self.name = name
        assert type(name) == types.StringType

        self.log_likelihood = loglikelihood
        self.nmix = nmix
        self.order = np.arange(nmix)

        #flag for likelihood calc
        self.flag_like = False
        
        self.__cw_step = step
        #Work variables for cron west method
        self.__cw_evec = None
        self.__cw_max_like = -1E256 #Guarantees it will get replaced
        self.__cw_cost_matrix = np.zeros((self.nmix, self.nmix),
                                       order = 'F')


    def compute(self, store):
        """
        Function to compute label switching information.
        """
        
        if store['iteration'] < store['length_of_burnin']:
           if store['iteration'] % self.__cw_step == 0:
                current_like = self.log_likelihood(store)
                if current_like > self.__cw_max_like:
                    self.flag_like = True
                    self.__cw_max_like = current_like
                    self.__cw_evec = store[self.name].copy()



        else:
            if self.flag_like == False:

                error = """ 
                Error in label switching class.  No reasonable likelihood
                calculation was obtained during the burn-in period.  Possible
                mistake in your code."""

                raise Exception(error)

            #compute cost matrix
            mm.cost_matrix(store[self.name], self.__cw_evec,
                       self.__cw_cost_matrix)
                
            munk = Munkres()
            self.order = np.array(munk.compute(self.__cw_cost_matrix))[:, 1]

        return self.order

