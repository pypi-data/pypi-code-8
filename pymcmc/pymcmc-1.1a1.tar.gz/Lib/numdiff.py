
#PyMCMC - A Python package for Bayesian estimation
#Copyright (C) 2014  Chris Strickland

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.# file containing mcmc_utilites used by pymcmc.

#Python code for compute numerical derivatives using 
#finite differencing

import numpy as np

def gradient(func, theta, h = None):
    """Function evaluates first gradient vector for function 
    using the forward difference method."""

    theta = np.atleast_1d(theta)
    assert theta.dtype == np.float64
    assert theta.ndim == 1

    grad = np.zeros(theta.shape[0])
    if h == None:
        hvec = compute_hvec(theta)
    else:
        hvec = np.ones(theta.shape[0]) * h

    #Evaluate ftheta
    ftheta = func(theta)

    #evaluate gradient
    for i in xrange(theta.shape[0]):
        temp = theta[i]
        theta[i] = theta[i] +  hvec[i]
        grad[i] = (func(theta) - ftheta) / hvec[i]
        theta[i] = temp

    return grad

def compute_h(x):
    """computes h for finite difference."""
    #get machine epsilon
    eps = np.finfo(float).eps
    h = np.sqrt(eps) * x
    tmp = x + h
    h = x - tmp
    return h

def compute_hvec(theta):
    """computes vector of h when theta is a vector."""

    hvec = np.zeros(theta.shape[0])
    for i in xrange(theta.shape[0]):
        hvec[i] = compute_h(theta[i])

    return hvec


def hessian(func, theta, h = None):
    """Function evaluates Hessian using finite difference
    method."""

    theta = np.atleast_1d(theta)
    assert theta.ndim == 1
    assert theta.dtype == np.float64
    ntheta = theta.shape[0]

    if h == None:
        hvec = np.sqrt(np.abs(compute_hvec(theta)))
    else:
        hvec = h * np.ones(theta.shape[0])
    hsq = hvec ** 2

    hess = np.zeros((ntheta, ntheta))
    fdiagplus = np.zeros(ntheta)
    fdiagminus = np.zeros(ntheta)
    ftheta = func(theta)

    #compute diagonal elements
    for i in xrange(ntheta):
        temp = theta[i]
        theta[i] = temp +  hvec[i]
        fdiagplus[i] = func(theta)
        theta[i] = temp - hvec[i]
        fdiagminus[i] = func(theta)
        hess[i, i] = (fdiagplus[i] - 2 * ftheta + fdiagminus[i]) / hsq[i]
        theta[i] = temp

    

    #compute off diagonal elements
    for i in xrange(ntheta):
        for j in xrange(i+1, ntheta):
            temp1 = theta[i]
            temp2 = theta[j]
            theta[i] = temp1 + hvec[i]
            theta[j] = temp2 + hvec[j]
            fpp = func(theta)
            theta[i] = temp1 - hvec[i]
            theta[j] = temp2 - hvec[j]
            fmm = func(theta)
            theta[i] = temp1 + hvec[i]
            #fpm = func(theta)
            #theta[i] = temp1 - hvec[i]
            #theta[j] = temp2 + hvec[j]
            #fmp = func(theta)
            #hess[i, j] = (fpp - fpm - fmp + fmm) / (4. * hvec[i] * hvec[j])
            hess[i, j] = (fpp - fdiagplus[i] - fdiagplus[j] + \
                    2. * ftheta - fdiagminus[i] - fdiagminus[j] + \
                  fmm) /  (2. * hvec[i] * hvec[j])
            
            theta[i] = temp1
            theta[j] = temp2
            hess[j, i] = hess[i, j]

    return hess
