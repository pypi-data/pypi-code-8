# Python code used to aid in the estimation of GLMs
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

#Helper classes for the generalised linear models


import numpy as np
#from condregconst import CondBetaScale1
import pymcmc.logit as logitm
import pymcmc.loglinear as loglinear
from pymcmc.regtools import LinearModel


class IWLS:
    def __init__(self, yvec, xmat, link, derivative, variance):

        self.yvec = yvec
        self.link = link
        self.derivative = derivative
        self.variance = variance
        if xmat.ndim == 1:
            self.xmat = xmat.reshape(xmat.shape[0], 1)
        else:
            self.xmat = xmat

        self.nobs, self.kreg = self.xmat.shape
        self.mu = np.zeros(self.nobs)
        self.eta = np.zeros(self.nobs)

        self.breg = LinearModel(self.yvec, self.xmat)
        self.weight = np.zeros((self.nobs, 1))
        self.tol = 1E-08
        self.zvec = np.zeros(self.nobs)

    def iwls(self):
        lnorm = 1.0
        self.initialise()
        self.updatez()
        lbeta = self.WLS()
        iter = 0
        
        while lnorm > self.tol and iter < 100:
            self.eta = self.xbeta(lbeta)
            self.mu = self.inverse(self.eta)
            self.updatez()
            beta = self.WLS()
            lnorm = np.linalg.norm(beta - lbeta)
            lbeta = beta
            #print iter
            iter = iter + 1

        return beta


    def inverse(self, eta):
        return np.exp(eta) / (1. + np.exp(eta))


    def updatez(self):
        self.eta = self.link(self.mu)
        self.zvec = self.eta + (self.yvec - self.mu) * self.derivative(self.mu)

    def initialise(self):
        self.mu = (self.yvec + self.yvec.mean()) / 2.

    def xbeta(self, beta):
        return np.dot(self.xmat, beta)



    def calc_invweight(self):
        return 1./np.sqrt(self.derivative(self.mu) ** 2 * self.variance(self.mu))

    def WLS(self):
        self.weight[:,0] = self.calc_invweight()
        yvec = self.weight[:,0] * self.zvec
        xmat = np.multiply(self.xmat, self.weight)
        self.breg.update_yvec(yvec)
        
        self.breg.update_xmat(xmat)
        sig, beta = self.breg.posterior_mean()
        return beta


class Logit:
    """
    Helper Class for Logit model."""

    def __init__(self, ntrials):
        self.ntrials = ntrials

        #container for WLS class
        self.wls = None
        self.wls_init = False


    def iwls(self, yvec, xmat):
        """class uses iterative weighted
        least squares to estimated regression
        coefficients"""

        if self.wls_init == False:
            self.wls = IWLS(yvec, xmat, self.link, self.derivative, self.variance)
            self.wls_init = True

        return self.wls.iwls()
            

    def derivative(self, mu):
        return 1. / (mu * (1. - mu))

    def variance(self, mu):
        return mu * (1. - mu)

    def link(self, mu):
        return np.log(mu / (1. - mu))

    def log_likelihood(self, *args):
        """Function returns the log-likelihood for the Logit model.
        
        arguments(*args):
            args[0] - An n-dimensional vector that stores xmat * beta.

            args[1] - An n-dimensional vector that stores the observations.

        """

        xbeta = args[0]
        yvec = args[1]
        
        return logitm.logl_logit(xbeta, yvec, self.ntrials)

    def calc_score(self, *args):
        """Function returns the score vector for the Logit model.

        arguments(*args):
            args[0] - Is a (k x 1) vector used for storing the score.

            args[1] - Is an (n x 1) vectore used to store the observations.

            args[2] - Is an (n x 1) vector used to store xmat * beta.

            args[3] - Is an (n x k) matrix used to store the regressors.


        """

        score = args[0]
        yvec = args[1]
        xbeta = args[2]
        xmat = args[3]

        logitm.score(score, yvec, xbeta, xmat, self.ntrials)

    def calc_hessian(self, *args):
        """Function is used to calculate the hessian for the logit model.

        arguments(*args):
            args[0] - Is a (k x k) matrix used to store the hessian.

            args[1] - Is a (k x k x n) array used to store x(i) * x(i)' for
                      i = 1, 2, ..., n.

            args[2] - Is a (n x 1) vector used to store xmat * beta.

        """

        hessian = args[0]
        xxp = args[1]
        xbeta = args[2]

        logitm.hessian(hessian, xxp, xbeta)

    def newton_raphson(self, *args):
        
        """Is a function used to find the MLE for the logit model.

        arguments(*args):
            args[0] - Is an (n x 1) vector used to store the observations.

            args[1] - Is an (n x k) matrix used to store the regressors.

            args[2] - Is an (n x 1) vector used to store xmat * beta.

            args[3] - Is a (k x 1) vector used to store the regression
                      coefficients.

            args[4] - Is a (k x 1) work array.

            args[5] - Is a (k x k) work array.

            args[6] - Is an (k x k x n) array that on entry stores x(i) * x(i)', for
            i = 1, 2, ..., n.

            args[7] - Is a (k x 1) work array.

        """

        yvec = args[0]
        xmat = args[1]
        xbeta = args[2]
        beta = args[3]
        lbeta = args[4]
        hessian = args[5]
        xxp = args[6]
        score = args[7]

        logitm.lnewtonr(yvec, xmat, xbeta, beta, lbeta, hessian,
                        xxp, score, self.ntrials)

class LogLinear:
    """Helper class for the log-linear model"""
    def __init__(self, kreg):
        self.ipiv = np.zeros(kreg, dtype = 'i')
        self.work = np.zeros(6 * kreg)

        #container for WLS class
        self.wls = None
        self.wls_init = False


    def derivative(self, mu):
        return 1. / mu

    def variance(self, mu):
        return mu

    def link(self, mu):
        return np.log(mu)
    
    def iwls(self, yvec, xmat):
        """class uses iterative weighted
        least squares to estimated regression
        coefficients"""

        if self.wls_init == False:
            self.wls = IWLS(yvec, xmat, self.link, self.derivative, self.variance)
            self.wls_init = True

        return self.wls.iwls()

    def log_likelihood(self, xbeta, yvec):
        return loglinear.logl(xbeta, yvec)

    def calc_score(self, score, yvec, xbeta, xmat):
        loglinear.score(score, yvec, xbeta, xmat)

    def calc_hessian(self, hessian, xxp, xbeta):
        loglinear.hessian(hessian, xxp, xbeta)

    def newton_raphson(self, yvec, xmat, xbeta, beta, lbeta, hessian,
                       xxp, score):
        loglinear.newtonr(yvec, xmat, xbeta, beta, lbeta, hessian,
                        xxp, score, self.ipiv, self.work)

