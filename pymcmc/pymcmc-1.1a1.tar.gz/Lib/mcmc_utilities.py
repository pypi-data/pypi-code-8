#MCMC utilities for PyMCMC - A Python package for Bayesian estimation
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
#along with this program.  If not, see <http://www.gnu.org/licenses/>.# file containing mcmc_utilites used by pymcmc.

import numpy as np
import scipy as sp
import timeseriesfunc
import pdb

def hpd(x, alpha):
    '''
    highest posterior density interval
    '''
    n = len(x)
    m = max(1, np.ceil(alpha * n))
    x2 = x.copy()
    x2.sort()
    a = x2[0:m]
    b = x2[(n - m):n]
    i = np.argmin( (b - a) )
    return [a[i], b[i]]


class InefficiencyFactor:
    def __init__(self):
        self.IFactor = 0.0
        self.Bandwidth = 0.0
        self.MCSE = 0.0

    def calculate(self, mc):
        if mc.ndim == 1:
            try:
                return self.compute(mc)
            except:
                return np.nan


        elif mc.ndim == 2:
            ifvec = np.zeros(mc.shape[1])
            for i in xrange(mc.shape[1]):
                try:
                    ifvec[i] = self.compute(mc[:, i])
                except:
                    ifvec[i] = np.nan
            return ifvec

        elif mc.ndim == 3:
            ifmat = np.zeros((mc.shape[1], mc.shape[2]))
            for i in xrange(mc.shape[1]):
                for j in xrange(mc.shape[2]):
                    try:
                        ifmat[i,j] = self.compute(mc[:,i,j])
                    except:
                        ifmat[i,j] = np.nan

            return ifmat
        else:
            assert mc.ndim == 4
            ifmat = np.zeros(mc.shape[1:])
            for i in xrange(mc.shape[1]):
                for j in xrange(mc.shape[2]):
                    for k in xrange(mc.shape[3]):
                        try:
                            ifmat[i,j,k] = self.compute(mc[:,i,j,k])
                        except:
                            ifmat[i,j,k] = np.nan

            return ifmat
            


    
    def compute(self, mc):
        self.Bandwidth = np.ceil(self.calc_b(mc)) + 1
        QS = self.QSkernel(self.Bandwidth)
        corr = np.zeros(self.Bandwidth)
        timeseriesfunc.acf(mc, corr)
        product = QS * corr
        sumproduct = sum(product)
        IF = 1.+2.*(float(self.Bandwidth)/(float(self.Bandwidth) - 1.)) * sumproduct;
        return IF
    

    def QSkernel(self, B):
        ind = map(lambda x: x/B, range(1, int(B) + 1))
        ind = np.array(ind)
        d = 6.*np.pi * ind/5.
        a = 25./(12.*np.pi**2 * ind**2)
        b = np.sin(d)/d
        c = np.cos(d)
        QS = a * (b - c)
        return QS

    def calc_b(self, mc):
        n = mc.shape[0]
        xmat = np.vstack([np.ones(n - 1), mc[0:n - 1]]).transpose()
        yvec = mc[1:n]
        xpx = np.dot(xmat.transpose(), xmat)
        xpy = np.dot(xmat.transpose(), yvec)
        beta = np.linalg.solve(xpx, xpy)
        #print mc.shape
        #print (yvec * xmat[:,1]).sum()
        #print beta 
        res = mc[1:n] - np.dot(xmat, beta)
        sigsq = sum(res**2)/float(n - 2)
        a = 4.*beta[1]**2 * sigsq**2/((1.-beta[1])**8)
        b = sigsq**2/((1 - beta[1])**4)
        alpha = a/b
        B = 1.3221 * (alpha * n)**(1./5.)
        return B

    # def __init__(self):
    #    self.IFactor = 0.0
    #    self.Bandwidth = 0.0
    #    self.MCSE = 0.0

    # def calculate(self, mc):
    #    if mc.ndim == 1:
    #        try:
    #            return self.compute(mc)
    #        except:
    #            return -9999


    #    else:
    #        ifvec = np.zeros(mc.shape[1])
    #        for i in xrange(mc.shape[1]):
    #            try:
    #                ifvec[i] = self.compute(mc[:, i])
    #            except:
    #                ifvec[i] =-9999
    #    return ifvec
   # 
    # def compute(self, mc):
    #    self.Bandwidth = np.ceil(self.calc_b(mc)) + 1
    #    QS = self.QSkernel(self.Bandwidth)
    #    corr = np.zeros(self.Bandwidth)
    #    timeseriesfunc.acf(mc, corr)
    #    product = QS * corr
    #    sumproduct = sum(product)
    #    IF = 1.+2.*(float(self.Bandwidth)/(float(self.Bandwidth) - 1.)) * sumproduct;
    #    return IF
   # 

    # def QSkernel(self, B):
    #    ind = map(lambda x: x/B, range(1, int(B) + 1))
    #    ind = np.array(ind)
    #    d = 6.*np.pi * ind/5.
    #    a = 25./(12.*np.pi**2 * ind**2)
    #    b = np.sin(d)/d
    #    c = np.cos(d)
    #    QS = a * (b - c)
    #    return QS

    # def calc_b(self, mc):
    #    n = mc.shape[0]
    #    xmat = np.vstack([np.ones(n - 1), mc[0:n - 1]]).transpose()
    #    yvec = mc[1:n]
    #    xpx = np.dot(xmat.transpose(), xmat)
    #    xpy = np.dot(xmat.transpose(), yvec)
    #    beta = np.linalg.solve(xpx, xpy)
    #    res = mc[1:n] - np.dot(xmat, beta)
    #    sigsq = sum(res**2)/float(n - 2)
    #    a = 4.*beta[1]**2 * sigsq**2/((1.-beta[1])**8)
    #    b = sigsq**2/((1 - beta[1])**4)
    #    alpha = a/b
    #    B = 1.3221 * (alpha * n)**(1./5.)
    #    return B

class Adaptive:
    """Class has helper functions for adaptive methods."""

    def __init__(self, target, **kwargs):
        self.target = target

        xgrid = np.linspace(0, 1, 1000)

        self.y = np.hstack([self.adapt_h(x) for x in np.nditer(xgrid)])

        ind = np.arange(1000)[self.y > 0.2]
        self.minind = ind[0]
        self.maxind = ind[-1]
        self.minx = xgrid[self.minind]
        self.maxx = xgrid[self.maxind]

        #parameters for Robins-Monro
        #assert 'nparam' in kwargs
        #self.nparam = kwargs['nparam']

        #self.RM_m = 200
        #alpha = -sp.stats.norm.ppf(self.pstar / 2.)
        #self.RM_pstarr = (1. - self.target) / self.target
        #self.RM_c = (1. - 1. / self.nparam) * np.sqrt(2. * np.pi) * \
                            #np.exp(alpha ** 2/2.)/\
                            #(2. * alpha) + 1. / (self.nparam * self.target * \
                            #(1. - self.target))

        #Marshal and Roberts style of adaption

        self.MR_a = 0.03
        self.MR_b = None #placeholder
        self.MR_r = 0.1
        self.__MR_scale = self.__MR_cscale

    def initialise_MR(self, scale, it):
        """Initialise Marshal Roberts style of adaption."""

        self.MR_b = scale * 0.001 * it ** self.MR_r
        

        return self.__MR_scale(scale, it)

    def __MR_cscale(self, scale, it):
        """Marshal Roberts style of adaption."""

        scale_star = max((0.001 * scale), self.MR_b * it ** (-self.MR_r))
        return scale_star

    def MR_scale(self, AR, scale, it):
        """Compute new scale based on Marshal Roberts style of adaption."""

        scale_star = self.__MR_scale(scale, it)
        if AR < self.target:
            scale = scale - scale_star
        else:
            scale = scale + scale_star

        return scale

        

    def RM(self, scale, last_accept, it):
        """Robins Monro."""

        self.RM_c = self.RM_c * scale

        if last_accept == True:
            scale = scale + self.RM_c * (1. - self.target) / \
                    max([200., float(it) / self.nparam])
        else:
            scale = scale - self.RM_c * self.nparam / \
                    max([200.,  float(it) / self.nparam])

        return scale

    def scale(self, AR):
        """Return scale multiplier given AR."""

        y = self.minx + (self.maxx - self.minx) * AR
        return self.adapt_h_mult(y)

    def adapt_h(self, x):
        """Adaptive helper function."""

        g = lambda x, p: 1 - np.abs(np.tanh(x - p))
        if x < self.target:
            x2 = 2. * np.pi / self.target * x - 2 * np.pi
        else:
            x2 = 2. * np.pi / (1. - self.target) * (x-self.target)

        return g(x2, 0)

    def adapt_h_mult(self, x):
        """Adaptive helper function."""

        g = lambda x, p: 1 - np.abs(np.tanh(x - p))
        if x < self.target:
            x2 = 2. * np.pi / self.target * x - 2 * np.pi
            sm =  g(x2, 0)
        else:
            x2 = 2. * np.pi / (1. - self.target) * (x-self.target)
            sm =  1. / g(x2, 0)

        return sm

