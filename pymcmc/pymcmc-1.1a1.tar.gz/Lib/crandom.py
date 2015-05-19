# Python code Random number generator that works with numpy's random number generator
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
import sys
import numpy as np
import random_mtar as rmt
import random_mtar_ref as rmtr

class Crandom:
    def __init__(self, reflection = False):
        if reflection == False:
            self.rmt = rmt
        else:
            self.rmt = rmtr
        self.mag01 = np.zeros(2, dtype = 'i')
        self.argv = np.zeros(6, dtype = 'i')
        self.rmt.mt_initln(self.argv, self.mag01)
        self.cached = np.array(0.0)

    def randu(self, array = None):
        state = np.random.get_state()
        mt = state[1]
        self.argv[0] = state[2]
        args = [mt, self.mag01, self.argv]
        
        func = (self.rmt.genrand_res53, self.rmt.randv, self.rmt.randm, self.rmt.randa3d)
        rnd = self.__rand(func, args, array)
        nstate = (state[0], mt,  self.argv[0], state[3], state[4])
        np.random.set_state(nstate)
        return rnd

    def randexp(self, array = None):
        state = np.random.get_state()
        self.argv[0] = state[2]
        mt = state[1]
        args = [mt, self.mag01, self.argv]

        func = (self.rmt.rand_exp, self.rmt.randv_exp, self.rmt.randm_exp, self.rmt.randa3d_exp)
       
        rnd =  self.__rand(func, args,  array)
        nstate = (state[0], mt, self.argv[0], state[3], state[4])
        np.random.set_state(nstate)
        return rnd

    def randn(self, array = None):
        state = np.random.get_state()
        self.argv[0] = state[2]
        
        args = [state[1], self.mag01, self.argv, self.cached]

        func = (self.rmt.randn, self.rmt.randv_norm, self.rmt.randm_norm, self.rmt.randa3d_norm)
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

        func = (self.rmt.tnorm, self.rmt.randv_tnorm, self.rmt.randm_tnorm,
                self.rmt.randa3d_tnorm)
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
