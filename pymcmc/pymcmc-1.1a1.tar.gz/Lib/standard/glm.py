# Python code used for the estimation of GLMs
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


import pdb
import numpy as np
from pymcmc.mcmc import MCMC, RWMH, MALA
from pymcmc.regtools import LinearModel
import pymcmc.logit as logitm
import pymcmc.loglinear as loglinearm
from glm_helper import Logit, LogLinear
from probit_helper import Probit
from mix_logit import MixLogit


class GLM:
    """
    This class is used for the MCMC estimation of the Logit, 
    probit or loglinear model

    arguments:
        data - Is an (n x 1) vector of observations. In most cases.
               Logit:
                   Is either an (n x 1) vector of 1s or 0s, or
                   is an (n x 2) matrix where the first column denotes
                   the number of successes and the second column denotes
                   the number of trials.
               Probit:
                   Is an (n x 1) vector of 1s and 0s.

               Loglinear:
                   Is an (n x 1) vector of count data.


        xmat - Is an (n x k) vector of regressors

        family - Used to specify the link function for the generalise linear model.
               The options for link are 'binomial', 'binomial-probit', 'poisson',
               where 'binomial' is for the logit link, whilst binomial-probit is for the probit
               link.

        nit - An integer that specifies how many iterations to run the
              MCMC scheme for. The default number of iterations is 15000.

        burn - The number of observations from the MCMC sampler that
               should be discarded when doin an MCMC analysis. The default
               number of iterations is 5000. This probably should not be reduced
               as the MALA algorithm adapts during the burnin.

    optional arguments(**kwargs):
        prior - Used to specify the prior on the regression
                coefficients. To specify set 
                prior = ['normal', betaubar, vubar], where 'normal'
                signifies that the prior is normally distributed and
                and betaubar is a (k x 1) prior mean vector, while vubar
                is the (k x k) prior precision. If no argument is given
                the default assumption of a flat prior is assumed


        algorithm - Can be used to choose algorithm for the 'binomial' and
                    'poisson' case. The algorithms to choose from are
                    1. Random walk Metropolis Hastings
                    2. Metropolis adjusted Langvin algorithm
                    3. full manifold Metropolis adjust Langvin algorithm
                    4. Adaptive random walk Metropolis Hastings 
                        (Garthwaite, Fan and Scisson)

    public member functions:
        output(**kwargs) - Produces output for the MCMC analysis.
        
        By default output is produced for all parameters. 

        Optional arguments (**kwargs)
            parameters: A dictionary, list or string
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

        CODAoutput(**kwargs) - Output the results in a format suitable for
        reading in using CODA.

        Write the output to file  in a format that can be read in by CODA.
        By default, there will be two files created, coda.txt and coda.ind.

        Optional Arguments(**kwargs)

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

            log_posterior(beta) - Returns the log of the posterior for the logit model
                              evaluated at beta.

            log_prior(beta) - Returns the log prior probability given beta.

            log_likelihood(beta) - Returns the log-likelihood function evaluated at
                               beta.


    """

    def __init__(self,  yvec, xmat, family, nit = 15000, burn = 5000, **kwargs):

        self.nit, self.burn = nit, burn
        self.xmat = np.asfortranarray(xmat)
        self.yvec = yvec.astype(float)
        self.link = family
        self.nobs, self.kreg = xmat.shape

        #storage used in estimation
        self.score = np.zeros(self.kreg)
        self.hessian = np.zeros((self.kreg, self.kreg), order = 'F')
        self.xbeta = np.zeros(self.nobs)

        #prior
        if 'prior' in kwargs:
            self.prior = kwargs['prior']
            assert self.prior[0] == 'normal'
            self.betaubar = self.prior[1]
            self.vubar = self.prior[2]
            log_det_vubar = 2.0 * np.sum(np.log(np.diag(self.vubar)))
            self.prior_const = - 0.5 * self.kreg * np.log(2. * np.pi) + \
                    0.5 * log_det_vubar

            self.__log_prior = self.__log_normal_prior

        else:
            #specify a flat prior by default
            self.prior = ['flat']
            self.__log_prior = self.__flat_prior

        #link function
        try:
            assert self.link in ['binomial', 'binomial-probit', 'poisson']
        except:
            error_message = 'Family only implemented for binomial, binomial-probit and poisson'
            raise NotImplementedError(error_message)


        if self.link == 'binomial':
            if self.yvec.ndim == 2:
                num_trials = self.yvec[:, 1]
                self.yvec = self.yvec[:, 0]
            else:
                num_trials = np.ones(self.nobs)
            self.xxp = np.zeros((self.kreg, self.kreg, self.nobs), order = 'F')
            logitm.calcxxp(self.xxp, self.xmat, num_trials)
            self.glm_standard = Logit(num_trials)
            if 'algorithm' not in kwargs or kwargs['algorithm'] == 5:
                ml = MixLogit(yvec, xmat, 'beta', **kwargs)
                self.__setup_mcmc = ml.setup_mcmc

            else:
                #Algoriths 1, 2, 3, 4
                self.__setup_mcmc = self.__setup_standard
            #storage for newton raphson
            self.lbeta = np.zeros(self.kreg)
        elif self.link == 'binomial-probit':
            self.glm_standard = Probit(yvec, xmat)
            self.__setup_mcmc = self.glm_standard.setup_mcmc
            

        else:
            assert self.link == 'poisson'
            self.xxp = np.zeros((self.kreg, self.kreg, self.nobs), order = 'F')
            loglinearm.calcxxp(self.xxp, self.xmat)
            self.glm_standard = LogLinear(self.kreg)
            self.__setup_mcmc = self.__setup_standard
            #storage for newton raphson
            self.lbeta = np.zeros(self.kreg)
                
        #Optional algorithms for binomial and poisson families
        if 'algorithm' in kwargs:
            self.algorithm = kwargs['algorithm']
            if self.algorithm not in [1,2,3,4]:
                #use default
                if self.link == 'poisson':
                    self.algorithm == 3
                else:
                    self.algorithm = 5
            #Note
            #1 = RWMH
            #2 = MALA
            #3 = MMALA
            #4 = Adaptive RWMH (GFS)
            #5 = Auxiliary mixture (logit only currently)
        else:
            #Default MALA
            if self.link == 'poisson':
                self.algorithm = 2
            else:
                self.algorithm = 5




        
        blocks, data = self.__setup_mcmc(**kwargs)
        data['yvec'] = self.yvec
        loglike = (self.__loglikelihood, self.kreg, 'yvec')
        if 'runtime_output' in kwargs and kwargs['runtime_output'] == True:
            RO = True
        else:
            RO = False

        self.mcmc = MCMC(self.nit, self.burn, data, blocks, loglike = loglike,
                         runtime_output = RO)
        self.compute_ind = 0


    def __setup_standard(self, **kwargs):
        
        #Initial values for newton raphson
        breg = LinearModel(self.yvec, self.xmat)
        sig, beta = breg.posterior_mean()
    
        #Initial value for MCMC scheme
        self.__newton_raphson(beta)
        #beta = self.IWLS()
        self.hessian = self.calc_hessian(beta)
        cov = np.linalg.inv(-self.hessian.copy())
        

        #MCMC estimation
        if self.algorithm == 1:
            simbeta = RWMH(self.__log_post, cov, beta, 'beta')
        elif self.algorithm == 2:
            #Adaptive MALA 
            if self.prior[0] == 'flat':
                gradient = self.__calc_gradient
            else:
                assert self.prior[0] == 'normal'
                gradient = self.__calc_gradient_with_prior
            
            simbeta = MALA(self.__log_post, 1, gradient,
                           beta, 'beta', adaptive = 'MR')
        elif self.algorithm == 3:
            #MMALA adaptive
            if self.prior[0] == 'flat':
                gradient = self.__calc_gradient
                hessian = self.__calc_hessian
            else:
                assert self.prior[0] == 'normal'
                gradient = self.__calc_gradient_with_prior
                hessian = self.__calc_hessian_with_prior

            simbeta = MALA(self.__log_post, 1, gradient,
                           beta, 'beta', hessian = hessian,
                           adaptive = 'MR')
        else:
            assert self.algorithm == 4
            #Adaptive RWMH (GFS)
            simbeta = RWMH(self.__log_post, 1., beta, 'beta', 
                           adaptive = True)


        block = [simbeta]
        data = {}
        return block, data


    def __compute(self):
        """function runs MCMC sampler"""

        if self.compute_ind == 0:
            self.mcmc.sampler()

        self.compute_ind = 1

    def plot(self, blockname, **kwargs):
        '''
        The basic plotting approach for the GLM  class.

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

        self.__compute()
        self.mcmc.plot(blockname, **kwargs)


    def output(self, **kwargs):
        """function produces output for the MCMC estimation of the
        Logit model
        By default output is produced for all parameters. 
        
        optional arguments:

            parameters: A dictionary, list or string
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

        self.__compute()
        self.mcmc.output(**kwargs)

    def get_mean_var(self):

        """Returns the marginal posterior mean and marginal
        posterior variance for beta."""

        self.__compute()
        return self.mcmc.get_mean_var('beta')



    def CODAoutput(self, **kwargs):
        """
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
         """

        self.__compute()
        self.mcmc.CODAoutput(**kwargs)
        

    def __log_post(self, store):
        """A private function returns the log posterior density evaluated
        at beta, where beta is passed as a member of store, which
        is passed from the MCMC class in PyMCMC.

        arguments:
            store - A storage data structure that is passed from PyMCMC.
        """

        return self.log_posterior(store['beta'])

    def log_posterior(self, beta):
        """function returns the log posterior density evaluated
        at beta.

        arguments:
            beta - Is a (k x 1) vector of regression coefficients
        """

        return self.loglikelihood(beta) + self.log_prior(beta)

    def log_prior(self, beta):
        """function returns the log prior probability given beta."""

        return self.__log_prior(beta)

    def __log_normal_prior(self, beta):
        """function returns the log prior density evalutated at
        beta. The normal distribution is assumed for the prior.

        arguments:
            beta - Is a (k x 1) vector of regression coefficients
        """

        dbeta = beta - self.betaubar
        kern = - 0.5 * np.dot(dbeta, np.dot(self.vubar, dbeta))
        return self.prior_const + kern

    def __flat_prior(self, beta):
        """function returns the log probability for a flat prior"""

        return 0.0

    def __gradient_normal_prior(self, beta):
        "Computes gradient for the normal prior."

        return np.dot(self.vubar, self.betaubar - beta)

    def __hessian_normal_prior(self):
        "Returns hessian for normal prior."

        return -self.vubar

    def __calc_gradient(self, store):
        "Computes gradient of likelihood"

        beta = store['beta']
        return self.calc_score(beta)

    def __calc_hessian(self, store):
        "Computes hessian of likelihoood."
        beta = store['beta']
        return self.calc_hessian(beta)

    def __calc_gradient_with_prior(self, store):
        "Computes gradient of log posterior."

        beta = store['beta']
        return self.calc_score(beta) + self.__gradient_normal_prior(beta)

    def __calc_hessian_with_prior(self, store):
        "Computes hessian with prior."

        beta = store['beta']
        return self.calc_hessian(beta) + self.__hessian_normal_prior()


    def __loglikelihood(self, store):
        return self.loglikelihood(store['beta'])
        
    def loglikelihood(self, beta):
        """function returns the log likelihood
        
        arguments:
            beta - Is a (k x 1) vector of regression coefficients
        """

        return self.glm_standard.log_likelihood(np.dot(self.xmat, beta), self.yvec)

    def calc_score(self, beta):
        """function returns the score vector
        
        arguments:
            beta - Is a (k x 1) vector of regression coefficients
        """

        self.glm_standard.calc_score(self.score, self.yvec, np.dot(self.xmat, beta), self.xmat)
        return self.score

    def calc_hessian(self, beta):
        """function returns the hessian
        
        arguments:
            beta - Is a (k x 1) vector of regression coefficients
        """
        self.hessian = np.asfortranarray(self.hessian) 
        self.glm_standard.calc_hessian(self.hessian, self.xxp, self.xbeta)
        return -self.hessian

    def __newton_raphson(self, beta):
        """function returns the maximum likelihood estimate for 
        beta. The estimation uses the newton raphson algorithm

        arguments:
            beta - Is a (k x 1) vector of regression coefficients.
                   On entry it is an initial estimate for the MLE.
                   On exit it is the ML estimate.
        """

        self.glm_standard.newton_raphson(self.yvec, self.xmat, self.xbeta, beta,
                             self.lbeta, self.hessian, self.xxp, self.score)

        return beta

    def IWLS(self):
        return self.glm_standard.iwls(self.yvec, self.xmat)
