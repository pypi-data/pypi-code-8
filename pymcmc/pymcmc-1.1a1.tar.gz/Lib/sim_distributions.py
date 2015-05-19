# A Bayesian module for simulating from useful distributions in
#PyMCMC. PyMCMC is a Python package for
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

import sys
import wishart
import numpy as np
import random_mtar as rmt

class SampleWishart:
    """Sample from the p-dimensional Wishart distribution. """

    def __init__(self, p):
        
        self.p = p
        #Define work arrays
        self.work_chisq = np.arange(self.p)
        self.n_randn = (self.p * (self.p - 1)) / 2
        self.randnvec = np.zeros(self.n_randn)
        self.randchivec = np.zeros(self.p)
        self.cmat = np.zeros((self.p, self.p), order = 'F')
        self.rmat = np.zeros((self.p, self.p), order = 'F')
        self.umat = np.zeros((self.p, self.p), order = 'F')

    def sample(self, nu, Smat):
        """Function samples D from the Wishart distribution such
        that D~W(nu,inv(S)). Note that nu is the degrees of freedom
        and S is a (p x p) scale matrix
        """

        Smat = np.asfortranarray(Smat)
        self.randnvec = np.random.randn(self.n_randn)
        self.randchivec = np.random.chisquare(nu - self.work_chisq)
        info = np.array(0)
        wishart.chol_wishart2(self.randnvec, self.randchivec, self.umat,
                  self.cmat, Smat, info)

        try:
            assert info == 0
        except:
            Error = "Cholesky decomposition failed in Wishart simulation"
            raise NameError(Error)

        return self.umat.copy()


class Crandom:
    def __init__(self):
        self.mag01 = np.zeros(2, dtype = 'i')
        self.argv = np.zeros(6, dtype = 'i')
        rmt.mt_initln(self.argv, self.mag01)
        self.cached = np.array(0.0)

    def randu(self, array = None):
        state = np.random.get_state()
        mt = state[1]
        self.argv[0] = state[2]
        args = [mt, self.mag01, self.argv]
        
        func = (rmt.genrand_res53, rmt.randv, rmt.randm, rmt.randa3d)
        rnd = self.__rand(func, args, array)
        nstate = (state[0], mt,  self.argv[0], state[3], state[4])
        np.random.set_state(nstate)
        return rnd

    def randexp(self, array = None):
        state = np.random.get_state()
        self.argv[0] = state[2]
        mt = state[1]
        args = [mt, self.mag01, self.argv]

        func = (rmt.rand_exp, rmt.randv_exp, rmt.randm_exp, rmt.randa3d_exp)
       
        rnd =  self.__rand(func, args,  array)
        nstate = (state[0], mt, self.argv[0], state[3], state[4])
        np.random.set_state(nstate)
        return rnd

    def randn(self, array = None):
        state = np.random.get_state()
        self.argv[0] = state[2]
        
        args = [state[1], self.mag01, self.argv, self.cached]

        func = (rmt.randn, rmt.randv_norm, rmt.randm_norm, rmt.randa3d_norm)
        rnd =  self.__rand(func, args, array)
        nstate = (state[0], state[1], self.argv[0], state[3], self.cached)
        np.random.set_state(nstate)
        return rnd

    def randtnorm(self, a, b,  array = None):
        state = np.random.get_state()
        self.argv[0] = state[2]
        if array != None:
            a = np.atleast_1d(a)
            b = np.atleast_1d(b)
        
        args = [a, b, state[1], self.mag01, self.argv, self.cached]

        func = (rmt.tnorm, rmt.randv_tnorm, rmt.randm_tnorm, rmt.randa3d_tnorm)
        rnd =  self.__rand(func, args, array)
        nstate = (state[0], state[1], self.argv[0], state[3], self.cached)
        np.random.set_state(nstate)
        return rnd




    def __rand(self, func, args, array = None):
        if array == None:
            rnd = func[0](*args)
            return rnd
        elif type(array) == np.ndarray:
            if array.ndim == 0:
                array[0] = func(0)(*args)
            elif array.ndim == 1:
                func[1](array, *args) 
            elif array.ndim == 2:
                if np.isfortran(array) == False:
                    farray = np.zeros(array.shape, order = 'F')
                    func[2](farray, *args) 
                    array[:,:] = farray[:,:]
                else:
                    func[2](array, *args) 
            elif array.ndim == 3:
                if np.isfortran(array) == False:
                    farray = np.zeros(array.shape, order = 'F')
                    func[3](farray, *args) 
                    array[:,:] = farray[:,:]
                else:
                    func[3](array, *args) 
            else:
                print "randu accepts arrays of maximum dimension of 3"
                sys.exit()


        return None
