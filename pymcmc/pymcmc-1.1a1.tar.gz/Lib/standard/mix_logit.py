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

#Helper classes for Probit model

#Python code for binomial logit model using auxilary mixture approach
import os
import numpy as np
from pymcmc.mix_logit_helper import sample_ind
from pymcmc.regtools import CondRegressionSampler, LinearModel
from pymcmc.mcmc import CFsampler
import pdb
import cProfile
import pstats
import pymcmc

class MixLogit:
    """Class for binomial logit model using auxiliary mixture approach."""
    def __init__(self, data, xmat, name, **kwargs):

        self.name = name

        #placeholders
        self.xmat = None
        self.yvec = None
        self.ni = None

        self.ind_1 = None
        self.yvec_ind_1 = None
        self.ind_2 = None
        self.nmy_ind2 = None
        self.svec = None
        self.wvec = None
        self.ptr = None

        #initialisation flag
        self.flag_initialise = False

        #function updates xmat
        self.update_xmat(xmat)
        
        #Obtain dimensions from xmat
        self.nobs, self.nreg = xmat.shape

        #read in weights
        path = os.path.join(os.path.dirname(pymcmc.__file__), 'Lib/standard')
        fh_weights = open(os.path.join(path,'GL-mixture_weights.txt'))
        weight_txt = fh_weights.readlines()
        #remove names from list
        names = weight_txt.pop(0)
        weight_rf = [wt.strip('\n').split('\t') for wt in weight_txt]
        #Create list of floating points for weights and nan where theres is no weight
        self.weight = []
        for weight in weight_rf:
            self.weight.append([np.nan if dt == '' else float(dt) for dt in weight])

        #Read in ssq
        fh_ssq = open(os.path.join(path, 'GL-mixture_ssq.txt'))
        ssq_txt = fh_ssq.readlines()
        names = ssq_txt.pop(0)
        ssq_rf = [ss.strip('\n').split('\t') for ss in ssq_txt]

        #Create list of floating points for ssq and nan where theres is no ssq
        self.ssq = []
        for ssq in ssq_rf:
            self.ssq.append([np.nan if ss == '' else float(ss) for ss in ssq])
        #Update dependent data
        self.update_data(data)


        if all(self.ni != 1):
            #need to remove nan
            pdb.set_trace()

        
        #compute weight vector and svector
        #note we use a compressed storage format

        #workspace variables
        self.srvec = np.zeros(self.nobs)
        self.xbeta = np.zeros(self.nobs)
        self.lamb = np.zeros(self.nobs)
        self.randu = np.zeros(self.nobs)
        self.prvec = np.zeros(5)

        #class for regression

        if 'prior' in kwargs:
            prior = kwargs['prior']
            try:
                assert prior[0] == 'normal'
            except:
                error = "Only the option of a normal prior is currently given."
                raise NotImplementedError(error)
            self.breg = CondRegressionSampler(self.yvec, self.xmat,
                                             prior = prior)
            
        else:
            self.breg = CondRegressionSampler(self.yvec, self.xmat)

    def update_xmat(self, xmat):
        """Function updates matrix of regressors."""

        if xmat.ndim == 1:
            self.xmat = xmat[:, np.newaxis]
        else:
            try:
                assert xmat.ndim == 2
            except:
                raise Exception("Matrix of regressors should be 1 or 2 dimensional.")

            self.xmat = xmat

    def update_data(self, data):
        """Function updates observation data."""

        if data.ndim == 2:
            #general binomial logit case
            try:
                assert data.shape[1] == 2
            except:
                error = """Data for the general binomial case should be
                           passed in as a matrix with two columns where the 
                           first column is the number of accepts and the
                           second column is the number of trials."""
                raise Exception(error)

            self.yvec = data[:, 0].astype('i')
            self.ni = data[:, 1].astype('i')
        else:
            #bernoulli logit case
            self.yvec = data.astype('i')
            self.ni = np.ones(self.nobs, dtype = 'i')

        #set up indicator variables
        #I(y_i > 0)
        self.ind_1 = self.yvec > 0
        self.yvec_ind_1 = self.yvec[self.ind_1]

        #I(y_i < N_i)
        self.ind_2 = self.yvec < self.ni
        self.nmy_ind2 = self.ni[self.ind_2] - self.yvec[self.ind_2]

        #Check dimensions of observations match that of regressors
        try:
            assert self.yvec.shape[0] == self.nobs
        except:
            raise Exception("Observations and regressors should be the same dimension.")


        #only recompte in two dimensional case
        if self.flag_initialise == False or data.ndim == 2:
            self.flag_initialise = True
            #compute weight vector and svector
            #note we use a compressed storage format
            ptr = [1]
            wlist = []
            ssqlist = []
            for i in xrange(self.nobs):
                if self.ni[i] < 61:
                    incr = len(self.weight[self.ni[i] - 1])
                elif self.ni[i] < 601:
                    incr = 2
                else:
                    incr = 1
                    
                ptr.append(ptr[i] + incr)

                if self.ni[i] < 61:
                    wlist.append(self.weight[self.ni[i] - 1])
                    ssqlist.append(self.ssq[self.ni[i] - 1])
                elif self.ni[i] < 601:
                        ssq, we = self.compute_ssq_w(self.ni[i])
                        ssqlist.append(ssq)
                        wlist.append(we)
                else:
                    ssqlist.append(np.array(1.))
                    wlist.append(np.array(1.))

            self.svec = np.sqrt(np.hstack(ssqlist))
            self.wvec = np.log(np.hstack(wlist))
            self.ptr = np.hstack(ptr)

    def setup_mcmc(self, **kwargs):
        """Setup MCMC algorithm."""

        #Initial values
        breg = LinearModel(self.yvec, self.xmat)
        sig, init_beta = breg.posterior_mean()

        samplebeta = CFsampler(self.sample_beta, init_beta, self.name)

        blocks = [samplebeta]
        data = {}
        return blocks, data
        

        
                

    def compute_ssq_w(self, nu):
        """Computes ssq for the case nu > 600."""

        ssq_nu = np.pi ** 2 / 3 - 2 * sum([1. / k ** 2 for k in xrange(1, nu)])
        ssq1 = ssq_nu * (-0.4973255E-7 * nu ** 2 + 0.024036101167 * nu + 1) / \
                (0.024403981536 * nu + 1.165357272312)

        ssq2 = ssq_nu * (-0.42821294E-6 * nu ** 2 + 0.027883528610 * nu + 1) / \
                (0.027266080794 * nu + 0.843603549826)

        w1 = (ssq_nu - ssq2) / (ssq1 - ssq2)
        w2 = 1 - w1

        return np.array((ssq1, ssq2)), np.array(( w1, w2))

    def sim_ystar(self, store):
        """Function to sample auxiliary variables."""

        self.xbeta = np.dot(self.xmat, store[self.name])
        self.lamb = np.exp(self.xbeta)

        Uvec = np.random.gamma(self.ni, 1. / (1. + self.lamb))
        Vvec = np.random.gamma(self.yvec_ind_1, 1)
        Wvec = np.random.gamma(self.nmy_ind2, 1. / self.lamb[self.ind_2])

        m1 = Uvec.copy()
        m2 = Uvec.copy()

        m1[self.ind_1] = m1[self.ind_1] + Vvec
        m2[self.ind_2] = m2[self.ind_2] + Wvec
        ystar = np.log(m1 / m2)
        return ystar

    def sample_beta(self, store):
        """Function samples beta."""

        ystar = self.sim_ystar(store)
        

        #Sampple srvec
        self.randu[:] = np.random.rand(self.nobs)
        

        sample_ind(self.srvec, self.randu, self.svec,
               self.prvec, self.wvec, self.ptr,
               ystar, self.xbeta)
        
            

        #weighted least squares
        ytil = ystar / self.srvec
        xmattil = self.xmat / self.srvec[:, np.newaxis]
        self.breg.update_yvec(ytil)
        self.breg.update_xmat(xmattil)

        return self.breg.sample(1.)



#testing
def logit_link(x):
    return 1./(1+np.exp(-x))


def simdata(N, kreg):
    """function simulates binomial data for logit model"""
    beta = np.random.randn(kreg)
    print "simulated beta = ", beta
    xmat = np.hstack([np.ones((N, 1)), np.random.randn(N, kreg-1)])
    yvec = np.zeros(N, dtype = 'i')
    xbeta = np.dot(xmat, beta)
    pvec = logit_link(xbeta)
    randu = np.random.rand(N)
    ind = pvec > randu
    yvec[ind] = 1
    return yvec, xmat, beta

#def main():

#    yvec, xmat, beta = simdata(1000, 4)
#    logit = mix_logit(yvec, xmat)
#  
#main()

    
#cProfile.run('main()', 'mainprof')
#p = pstats.Stats('mainprof')

#p.sort_stats('time')
#p.print_stats(10)
