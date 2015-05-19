##find and import the example
import os
import pyssm
import pyssm.ssm as ssm
import sys
import numpy as np
from pyssm.ssm import SimSmoother
from pymcmc.regtools import LinearModel, CondScaleSampler
from pymcmc.mcmc import MCMC, CFsampler, IndMH, RWMH

exampledir = os.path.join(os.path.dirname(pyssm.__file__), 'examples')
datadir = os.path.join(os.path.dirname(pyssm.__file__), 'data')

sys.path.append(exampledir)
import example_ssm_ar1_reg as egar1
import example_spline as egspline
import example_ssm_trendcycle2 as trendcycle
#import test_ar
import unittest


class TestExamples(unittest.TestCase):
    """
    Class to run unit tests on our distributed examples.
    """

    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(pyssm.__file__), 'data')
        np.random.seed(12345)

    def test_example_ssm_ar1_reg(self):
        """
        Run a cut down version of our example, to make sure
        it all works.
        """
        nobs = 500
        nstate = 1
        rstate = 1
        yvec, simulated_state = egar1.simdata(nobs)
        data = {'yvec': yvec}

        ht = 1.0
        tt = 0.9
        zt = 1.0
        qt = 0.4
        gt = 1.0
        rt = 1.0
        p1 = qt / (1. - tt ** 2)
        mu = np.mean(yvec)
        a1 = mu
        beta = mu * (1 - tt)
        wmat = 1.0

        data['simsm'] = SimSmoother(yvec, nstate, rstate,
                                    False, properties={'gt': 'eye'},
                                    wmat=wmat)
        data['simsm'].initialise_system(a1, p1, zt, ht, tt, gt,
                                        qt, rt, beta=beta)
        data['scale_sampler'] = CondScaleSampler(prior=['inverted_gamma',
                                                        10.0, 0.01])
        data['bayes_reg'] = LinearModel(yvec[1:nobs],
                                        np.column_stack([np.ones(nobs - 1),
                                                         yvec[0:nobs - 1]]))
        samplestate = CFsampler(egar1.simstate, np.zeros((nstate, nobs)),
                                'state')
        sampleht = CFsampler(egar1.simht, ht, 'ht')
        samplesigbetarho = IndMH(egar1.cand_rho_sigma, egar1.post_rho_sigma,
                                 egar1.cand_prob, [np.sqrt(qt), 0.1, tt],
                                 ['sigma', 'beta', 'rho'])
        blocks1 = [samplestate, sampleht, samplesigbetarho]
        mcmc = MCMC(1000, 500, data, blocks1,
                    transform={'beta': egar1.transform_beta})
        mcmc.sampler()
        means, vars = mcmc.get_mean_var('state')
        self.assertTrue(True)

    def test_example_spline(self):
        """
        A cut down version of our distributed example.
        """
        np.random.seed(1234)
        data = np.loadtxt(os.path.join(self.datadir, 'motorcycle.txt'))
        data = data[data[:, 1] > 0]
        yvec = data[:, 2]
        delta = data[:, 1]
        nobs = yvec.shape[0]
        nstate = 2
        rstate = 2
        data = {'yvec': yvec}

        sigeps = 0.9
        ht = sigeps ** 2
        rt = 1.
        zt = np.array([[1.0, 0.0]])
        tt = np.zeros((2, 2, nobs))
        tt[0, 0, :] = 1.
        tt[1, 1, :] = 1.
        tt[0, 1, :] = delta

        sigma = 0.3
        qt = np.zeros((2, 2, nobs))
        qt[0, 0, :] = delta ** 3 / 3.
        qt[0, 1, :] = qt[1, 0, :] = delta ** 2 / 2
        qt[1, 1, :] = delta

        gt = np.eye(nstate) * sigma
        a1 = np.zeros(2)
        p1 = np.eye(2)
        wmat = np.zeros((2, 2, nobs))

        data['simsm'] = ssm.SimSmoother(yvec, nstate, rstate,
            timevar={'tt': True, 'qt': True},
            properties={'rt': 'eye'}, wmat=wmat,
            joint_sample=['diffuse', np.eye(2)])

        data['simsm'].initialise_system(a1, p1, zt, ht, tt, gt, qt, rt)
        data['scale_sampler'] = CondScaleSampler(prior=['inverted_gamma',
                                                        10, 0.1])

        samplestate = CFsampler(egspline.simstate, np.zeros((nstate, nobs)),
                                'state', store='none')
        sample_ht = CFsampler(egspline.sim_ht, np.var(yvec), 'ht')
        sample_sigma = RWMH(egspline.post_sigma, 1., 0.2, 'sigma',
                            adaptive='GFS')

        blocks = [samplestate, sample_ht, sample_sigma]
        mcmc = MCMC(1000, 300, data, blocks, runtime_output=False)
        mcmc.sampler()
        means, vars = mcmc.get_mean_var('state')
        self.assertTrue(True)

    def test_example_ssm_trendcycle2(self):
        """
        Cut down version of our distributed example.
        """
        filename = os.path.join(self.datadir, 'farmb.txt')
        ymat = np.loadtxt(filename).T / 1000.
        nseries, nobs = ymat.shape
        data = {'ymat': ymat}

        nstate = 4
        rstate = 3
        ht = np.eye(nseries)
        zt = np.column_stack([np.ones(nseries), np.zeros(nseries),
                              np.ones(nseries), np.zeros(nseries)])
        rt = np.ones(nseries)
        tt = np.zeros((nstate, nstate))
        rho = 0.9
        lamb = 2. * np.pi / 20.
        tt[0, 0] = 1.0
        tt[0, 1] = 1.0
        tt[1, 1] = 1.0
        tt[2, 2] = rho * np.cos(lamb)
        tt[2, 3] = rho * np.sin(lamb)
        tt[3, 2] = -tt[2, 3]
        tt[3, 3] = tt[2, 2]

        sig_cycle = 0.3
        sig_level = 0.3
        qt = np.diag(np.array([sig_level, sig_cycle, sig_cycle]) ** 2)
        gt = np.zeros((nstate, rstate))
        gt[0, 0] = 1.0
        gt[2:, 1:] = np.eye(2)
        a1 = np.array([7.5, 0.000, 0.0, 0.0])
        p1 = np.zeros((nstate, nstate))
        p1[0, 0] = 10.
        p1[1, 1] = 10.
        p1[2, 2] = qt[2, 2] / (1 - rho ** 2)
        p1[3, 3] = p1[2, 2]

        timevar = False
        data['simsm'] = SimSmoother(ymat, nstate, rstate, timevar,
                                    properties={'rt': 'eye'})
        data['simsm'].initialise_system(a1, p1, zt, ht, tt, gt, qt, rt)

        prior_wishart = ['wishart',
                         10 * np.ones(nseries), 0.1 * np.eye(nseries)]
        data['scale_sampler'] = CondScaleSampler(prior=prior_wishart)
        data['scale_sampler2'] = CondScaleSampler(
            prior=['inverted_gamma', 10, 0.1])

        samplestate = CFsampler(trendcycle.simstate,
                                     np.zeros((nstate, nobs)),
                                     'state', store='none')
        sampleht = CFsampler(trendcycle.simht, ht, 'ht')
        samplesig_level = CFsampler(trendcycle.simsig_level,
                                         sig_level, 'sigma_level')
        samplesig_cycle = RWMH(trendcycle.posterior_sig_cycle, 0.05,
                                    sig_cycle ** 2, 'sigma_cycle',
                                    adaptive='GFS')
        samplerho = RWMH(trendcycle.posterior_rho, 0.09, rho, 'rho',
                         adaptive='GFS')
        samplelambda = RWMH(trendcycle.posterior_lambda, 1.03, lamb,
                                 'lambda', adaptive='GFS')

        blocks = [samplestate, sampleht, samplesig_cycle,
                  samplesig_level, samplerho, samplelambda]
        mcmcobj = MCMC(1000, 300, data, blocks, runtime_output=False)
        mcmcobj.sampler()
        means, vars = mcmcobj.get_mean_var('state')
        self.assertTrue(True)

    # def test_ar(self):
    #     """
    #     do the ar test using simulated data.
    #     """
    #     test_ar.mainroutine()
    #     self.assertTrue(True)


#Run unit tests
suite = unittest.TestLoader().loadTestsFromTestCase(TestExamples)
unittest.TextTestRunner(verbosity=2).run(suite)
