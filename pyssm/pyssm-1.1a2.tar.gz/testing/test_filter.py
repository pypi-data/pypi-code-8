#Python code for running unit tests on Filter class

from pyssm.ssm import Filter
import unittest
import numpy as np


class TestFilter(unittest.TestCase):
    """Class used to run unit tests on Filter class. Ensures all updates are
    handled correctly."""

    def setUp(self):
        "Define size of SSM for test."
        self.nobs = 10    # number of time series observations
        self.nseries = 2  # number of time series
        self.nstate = 3   # state dimension
        self.rstate = 2   # state covariance dimension

        #In the case of regressors in the model
        self.nreg = 2   # regressors in measurement equation
        self.sreg = 3   # regressors in the state equation
        np.random.seed(12345)  # initialise seed

    def filter_class(self, timevar, a1, p1, zt, ht, tt, gt, qt, rt, **kwargs):
        "Function defines filter class."

        #Define Filter Class
        filter = Filter(self.nobs, self.nseries, self.nstate, self.rstate, timevar,
                       **kwargs)
        if 'beta' not in kwargs:
            filter.initialise_system(a1, p1, zt, ht, tt, gt, qt, rt)
        else:
            #regressors in model
            filter.initialise_system(a1, p1, zt, ht, tt, gt, qt, rt,
                                    beta=kwargs['beta'])

        #Reset seed
        np.random.seed(12346)

        #Simulate data
        filter.simssm()

        return filter

    def ntv_system(self, regressors=False):
        "Class defines non time varying system matrices used in most tests."

        #Define system matrices for tests"
        zt = np.random.randn(self.nseries, self.nstate)
        tt = np.random.randn(self.nstate, self.nstate)
        gt = np.random.randn(self.nstate, self.rstate)
        a1 = np.random.randn(self.nstate)

        #Note convient specification for testing
        #Compressed storage cases
        rt = np.diag(np.random.randn(self.nseries))

        #Define positive definite covariance matrrices
        temp = np.random.randn(self.nstate, self.nstate * 5)
        p1 = np.dot(temp, temp.T)

        temp = np.random.randn(self.rstate, self.rstate * 5)
        qt = np.dot(temp, temp.T)

        #Note convienient specification
        #for testing compressed storage case
        ht = np.diag(np.random.randn(self.nseries) ** 2)

        if regressors is False:
            return a1, p1, zt, ht, tt, gt, qt, rt

        else:
            #Regressors in SSM
            xmat = np.random.randn(self.nseries, self.nreg, self.nobs)
            wmat = np.random.randn(self.nstate, self.sreg, self.nobs)
            beta = np.random.randn(self.nreg + self.sreg)

            return a1, p1, zt, ht, tt, gt, qt, rt, xmat, wmat, beta

    def test_smoother(self):
        "Function tests classical smoothing algorithm."
        #Set up filter class for the non-time varying case.
        a1, p1, zt, ht, tt, gt, qt, rt = self.ntv_system()
        filter = self.filter_class(False, a1, p1, zt, ht, tt, gt, qt, rt)

        #Run classical smoother for the non-timevarying case

        filter.smoother()

        #obtain smoother states
        ahat = filter.ahat

        #Set up filter class for time varying case.
        #Set up filter class for time varying case.
        tv_zt, tv_ht, tv_tt, tv_gt, tv_qt, tv_rt = \
                self.convert_system_tv(zt, ht, tt, gt, qt, rt)

        filter_tv = self.filter_class(True, a1, p1, tv_zt, tv_ht,
                                      tv_tt, tv_gt, tv_qt, tv_rt)

        #Run classical smoother for the time varying case
        filter_tv.smoother()

        ahat_tv = filter_tv.ahat

        self.assertTrue(np.allclose(ahat, ahat_tv))

        #Test compressed storage options (Note different fortran functions for likelihood
        #rt = diag and ht = diag

        filter_comp = self.filter_class(False, a1, p1, zt, np.diag(ht), tt, gt, qt,
                                   np.diag(rt),
                                   properties={'rt': 'diag',
                                                 'ht': 'diag'})
        #Run classical smoother for the non-timevarying case (compresssed storage)
        filter_comp.smoother()

        #obtain smoother states
        ahat_comp = filter_comp.ahat
        self.assertTrue(np.allclose(ahat_comp, ahat))

        #Time varying case (compressed storage)
        tv_rt_diag = np.column_stack([np.diag(rt)] * self.nobs)
        tv_ht_diag = np.column_stack([np.diag(ht)] * self.nobs)
        filter_tv_comp = self.filter_class(True, a1, p1, tv_zt,
                                           tv_ht_diag, tv_tt, tv_gt, tv_qt,
                                           tv_rt_diag, properties={'rt': 'diag',
                                                                   'ht': 'diag'})

        #Run smoothing algorihm for the time varying case.
        filter_tv_comp.smoother()
        ahat_tv_comp = filter_tv_comp.ahat

        self.assertTrue(np.allclose(ahat, ahat_tv_comp))

    def test_smoother_reg(self):
        "Function tests classical smoothing algorithm."
        #Set up filter class for the non-time varying case,
        #with regressors.
        a1, p1, zt, ht, tt, gt, qt, rt, xmat, wmat, beta = self.ntv_system(True)
        filter = self.filter_class(False, a1, p1, zt, ht, tt, gt, qt, rt,
                                  xmat=xmat,
                                  wmat=wmat,
                                  beta=beta)

        #Run classical smoother for the non-timevarying case

        filter.smoother()

        #obtain smoother states
        ahat = filter.ahat

        #Set up filter class for time varying case.
        #Set up filter class for time varying case.
        tv_zt, tv_ht, tv_tt, tv_gt, tv_qt, tv_rt = \
                self.convert_system_tv(zt, ht, tt, gt, qt, rt)

        filter_tv = self.filter_class(True, a1, p1, tv_zt, tv_ht, tv_tt,
                                      tv_gt, tv_qt, tv_rt,
                                     xmat=xmat,
                                     wmat=wmat,
                                     beta=beta)

        #Run classical smoother for the time varying case
        filter_tv.smoother()

        ahat_tv = filter_tv.ahat

        self.assertTrue(np.allclose(ahat, ahat_tv))

        #Test compressed storage options (Note different fortran functions for likelihood
        #rt = diag and ht = diag

        filter_comp = self.filter_class(False, a1, p1, zt, np.diag(ht), tt, gt, qt,
                                   np.diag(rt),
                                   properties={'rt': 'diag',
                                                 'ht': 'diag'},
                                       xmat=xmat,
                                       wmat=wmat,
                                       beta=beta)
        #Run classical smoother for the non-timevarying case (compresssed storage)
        filter_comp.smoother()

        #obtain smoother states
        ahat_comp = filter_comp.ahat
        self.assertTrue(np.allclose(ahat_comp, ahat))

        #Time varying case (compressed storage)
        tv_rt_diag = np.column_stack([np.diag(rt)] * self.nobs)
        tv_ht_diag = np.column_stack([np.diag(ht)] * self.nobs)
        filter_tv_comp = self.filter_class(True, a1, p1,
                               tv_zt, tv_ht_diag, tv_tt, tv_gt, tv_qt,
                               tv_rt_diag, properties={'rt': 'diag',
                                                       'ht': 'diag'},
                                                       xmat=xmat,
                                                       wmat=wmat,
                                                       beta=beta)

        #Run smoothing algorihm for the time varying case.
        filter_tv_comp.smoother()
        ahat_tv_comp = filter_tv_comp.ahat

        self.assertTrue(np.allclose(ahat, ahat_tv_comp))

    def test_likelihood_reg(self):
        "Function tests likelihood function computation with regressors"

        #Set up filter class for the non-time varying case.
        a1, p1, zt, ht, tt, gt, qt, rt, xmat, wmat, beta = self.ntv_system(True)
        filter = self.filter_class(False, a1, p1, zt, ht, tt, gt, qt, rt,
                                  xmat=xmat,
                                  wmat=wmat,
                                  beta=beta)

        #compute log-likelihood non-time varying case

        log_like_ntv = filter.log_likelihood()

        #Set up filter class for time varying case.
        tv_zt, tv_ht, tv_tt, tv_gt, tv_qt, tv_rt = \
                self.convert_system_tv(zt, ht, tt, gt, qt, rt)

        filter_tv = self.filter_class(True, a1, p1, tv_zt, tv_ht, tv_tt,
                                     tv_gt, tv_qt, tv_rt,
                                     xmat=xmat,
                                     wmat=wmat,
                                     beta=beta)

        #compute the log likelihood for the time varying case.
        log_like_tv = filter_tv.log_likelihood()

        self.assertTrue(np.allclose(log_like_ntv, log_like_tv))

        #Test compressed storage options (Note different fortran functions for likelihood
        #rt = diag and ht = diag

        filter = self.filter_class(False, a1, p1, zt, np.diag(ht), tt, gt, qt,
                                   np.diag(rt),
                                   properties={'rt': 'diag',
                                               'ht': 'diag'},
                                  xmat=xmat,
                                  wmat=wmat,
                                  beta=beta)

        log_like_ntv_diag_rt_ht = filter.log_likelihood()  # Non time varying case

        self.assertTrue(np.allclose(log_like_ntv, log_like_ntv_diag_rt_ht))

        tv_rt_diag = np.column_stack([np.diag(rt)] * self.nobs)
        tv_ht_diag = np.column_stack([np.diag(ht)] * self.nobs)
        filter_tv = self.filter_class(True, a1, p1, tv_zt, tv_ht_diag,
                                      tv_tt, tv_gt, tv_qt,
                                      tv_rt_diag, properties={'rt': 'diag',
                                                              'ht': 'diag'},
                                     xmat=xmat,
                                     wmat=wmat,
                                     beta=beta)

        #compute the log likelihood for the time varying case.
        log_like_tv_diag_rt_ht = filter_tv.log_likelihood()

        self.assertTrue(np.allclose(log_like_ntv, log_like_tv_diag_rt_ht))

    def convert_system_tv(self, zt, ht, tt, gt, qt, rt):
        """Function converts system matrices to equivalent time varying
        matrices to aid in testing."""

        tv_ht = np.repeat(ht, self.nobs).reshape(self.nseries, self.nseries, self.nobs)
        tv_rt = np.repeat(rt, self.nobs).reshape(self.nseries, self.nseries, self.nobs)
        tv_zt = np.repeat(zt, self.nobs).reshape(self.nseries, self.nstate, self.nobs)
        tv_tt = np.repeat(tt, self.nobs).reshape(self.nstate, self.nstate, self.nobs)
        tv_gt = np.repeat(gt, self.nobs).reshape(self.nstate, self.rstate, self.nobs)
        tv_qt = np.repeat(qt, self.nobs).reshape(self.rstate, self.rstate, self.nobs)

        return tv_zt, tv_ht, tv_tt, tv_gt, tv_qt, tv_rt

    def test_likelihood(self):
        "Function tests likelihood function gives correct result."

        #Set up filter class for the non-time varying case.
        a1, p1, zt, ht, tt, gt, qt, rt = self.ntv_system()
        filter = self.filter_class(False, a1, p1, zt, ht, tt, gt, qt, rt)

        #compute log-likelihood non-time varying case

        log_like_ntv = filter.log_likelihood()

        #Set up filter class for time varying case.
        tv_zt, tv_ht, tv_tt, tv_gt, tv_qt, tv_rt = \
                self.convert_system_tv(zt, ht, tt, gt, qt, rt)

        filter_tv = self.filter_class(True, a1, p1, tv_zt, tv_ht, tv_tt, tv_gt, tv_qt, tv_rt)

        #compute the log likelihood for the time varying case.
        log_like_tv = filter_tv.log_likelihood()

        self.assertTrue(np.allclose(log_like_ntv, log_like_tv))

        #Test compressed storage options (Note different fortran functions for likelihood
        #rt = diag and ht = diag

        filter = self.filter_class(False, a1, p1, zt, np.diag(ht), tt, gt, qt,
                                   np.diag(rt),
                                   properties={'rt': 'diag',
                                               'ht': 'diag'})

        log_like_ntv_diag_rt_ht = filter.log_likelihood()  # Non time varying case

        self.assertTrue(np.allclose(log_like_ntv, log_like_ntv_diag_rt_ht))

        tv_rt_diag = np.column_stack([np.diag(rt)] * self.nobs)
        tv_ht_diag = np.column_stack([np.diag(ht)] * self.nobs)
        filter_tv = self.filter_class(True, a1, p1, tv_zt, tv_ht_diag,
                                      tv_tt, tv_gt, tv_qt,
                                      tv_rt_diag, properties={'rt': 'diag',
                                                              'ht': 'diag'})

        #compute the log likelihood for the time varying case.
        log_like_tv_diag_rt_ht = filter_tv.log_likelihood()

        self.assertTrue(np.allclose(log_like_ntv, log_like_tv_diag_rt_ht))


#Run unit tests
suite = unittest.TestLoader().loadTestsFromTestCase(TestFilter)
unittest.TextTestRunner(verbosity=2).run(suite)
