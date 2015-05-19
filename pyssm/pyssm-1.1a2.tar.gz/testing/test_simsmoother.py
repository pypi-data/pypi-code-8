#Python code for testing SimSmoother class in PySSM.

from pyssm.ssm import Filter, SimSmoother
import unittest
import numpy as np


class TestSmoother(unittest.TestCase):
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

    def simdata(self, timevar, a1, p1, zt, ht, tt, gt, qt, rt, **kwargs):
        "Function simulates data for testing"

        #Define Filter Class
        filter = Filter(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, **kwargs)
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

        ymat = filter.get_ymat()

        return ymat

    def base_system(self):
        "Simulates sisytem matricies to be used in tests"

        #Define system matrices for tests"
        zt = np.random.randn(self.nseries, self.nstate)
        tt = np.random.randn(self.nstate, self.nstate)
        gt = np.random.randn(self.nstate, self.rstate)
        a1 = np.random.randn(self.nstate)

        # Note convient specification for testing
        # Compressed storage cases
        rt = np.diag(np.random.randn(self.nseries)) ** 2
        #Define positive definite covariance matrrices
        temp = np.random.randn(self.nstate, self.nstate * 5)
        p1 = np.dot(temp, temp.T)

        temp = np.random.randn(self.rstate, self.rstate * 5)
        qt = np.dot(temp, temp.T)

        #Note convienient specification
        #for testing compressed storage case
        ht = np.diag(np.random.randn(self.nseries) ** 2)
        return a1, p1, zt, ht, tt, gt, qt, rt

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

    def test_simsm(self):
        "Function tests simulation smoother."

        #Define system matrices for tests"
        a1, p1, zt, ht, tt, gt, qt, rt = self.base_system()
        ymat = self.simdata(False, a1, p1, zt, ht, tt, gt, qt, rt)

        #Instantiate class for simulation smoothing.
        simsm = SimSmoother(ymat, self.nstate, self.rstate, False)
        simsm.initialise_system(a1, p1, zt, ht, tt, gt, qt, rt)

        np.random.seed(12345)  # Set Seed
        state_ntv = simsm.sim_smoother()

        simsm_comp = SimSmoother(ymat, self.nstate, self.rstate, False,
                            properties={'rt': 'diag',
                                          'ht': 'diag'})
        simsm_comp.initialise_system(a1, p1, zt, np.diag(ht),
                                     tt, gt, qt, np.diag(rt))

        np.random.seed(12345)  # Set Seed
        state_ntv_comp = simsm_comp.sim_smoother()

        self.assertTrue(np.allclose(state_ntv_comp, state_ntv))

        #Set up system matrices for time varying case.
        tv_zt, tv_ht, tv_tt, tv_gt, tv_qt, tv_rt = \
                self.convert_system_tv(zt, ht, tt, gt, qt, rt)

        simsm = SimSmoother(ymat, self.nstate, self.rstate, True)
        simsm.initialise_system(a1, p1, tv_zt, tv_ht, tv_tt, tv_gt,
                               tv_qt, tv_rt)

        np.random.seed(12345)  # Set Seed
        state_tv = simsm.sim_smoother()

        self.assertTrue(np.allclose(state_ntv, state_tv))

        #Test compressed storage algorithms time varying algorithm
        comp_ht = np.column_stack([np.diag(tv_ht[:, :, i]) for i in xrange(self.nobs)])
        comp_rt = np.column_stack([np.diag(tv_rt[:, :, i]) for i in xrange(self.nobs)])
        simsm = SimSmoother(ymat, self.nstate, self.rstate, True,
                            properties={'rt': 'diag',
                                        'ht': 'diag'})
        simsm.initialise_system(a1, p1, tv_zt, comp_ht, tv_tt, tv_gt,
                               tv_qt, comp_rt)

        np.random.seed(12345)  # Set Seed
        state_tv_comp = simsm.sim_smoother()

        self.assertTrue(np.allclose(state_tv_comp, state_ntv))

    def test_update_ymat(self):
        "Function tests if update_ymat function works correctly."

        #Define system matrices for tests"
        a1, p1, zt, ht, tt, gt, qt, rt = self.base_system()

        ymat = self.simdata(False, a1, p1, zt, ht, tt, gt, qt, rt)

        #Instantiate class for simulation smoothing.
        simsm = SimSmoother(ymat, self.nstate, self.rstate, False)
        ymat2 = ymat * 2
        #Update ymat
        simsm.update_ymat(ymat2)

        self.assertTrue(np.allclose(simsm.get_ymat(), ymat2))

    def test_residual(self):
        "Function checks whether residuals are computed correctly."

        #Define system matrices for tests"
        a1, p1, zt, ht, tt, gt, qt, rt = self.base_system()

        ymat = self.simdata(False, a1, p1, zt, ht, tt, gt, qt, rt)

        #Instantiate class for simulation smoothing.
        simsm = SimSmoother(ymat, self.nstate, self.rstate, False)
        simsm.initialise_system(a1, p1, zt, ht, tt, gt, qt, rt)

        #Run simulation smoother
        np.random.seed(12345)  # Set Seed
        simsm.sim_smoother()

        state = simsm.get_state()  # state from simulation smoother

        #Compute residuals using python code
        gresiduals = np.zeros((self.nstate, self.nobs - 1))
        for t in xrange(self.nobs - 1):
            gresiduals[:, t] = state[:, t + 1] - np.dot(tt, state[:, t])

        self.assertTrue(np.allclose(simsm.compute_gresidual(), gresiduals))

        residuals = np.dot(np.linalg.pinv(gt), gresiduals)
        self.assertTrue(np.allclose(simsm.get_state_residual(), residuals))

        #compare for time varying case
        tv_zt, tv_ht, tv_tt, tv_gt, tv_qt, tv_rt = \
                self.convert_system_tv(zt, ht, tt, gt, qt, rt)

        simsm_tv = SimSmoother(ymat, self.nstate, self.rstate, True)
        simsm_tv.initialise_system(a1, p1, tv_zt, tv_ht, tv_tt, tv_gt,
                               tv_qt, tv_rt)

        np.random.seed(12345)  # Set Seed
        simsm_tv.sim_smoother()

        self.assertTrue(np.allclose(simsm_tv.get_state_residual(), residuals))

        #Compare measurement equation residuals
        meas_residual = np.linalg.solve(rt, ymat - np.dot(zt, state))

        self.assertTrue(np.allclose(simsm.get_meas_residual(), meas_residual))

        #time varying case
        self.assertTrue(np.allclose(simsm_tv.get_meas_residual(), meas_residual))

        #test properies

        #rt diagonal
        simsm_diag_rt = SimSmoother(ymat, self.nstate, self.rstate, False,
                            properties={'rt': 'diag'})
        simsm_diag_rt.initialise_system(a1, p1, zt, ht, tt, gt, qt, np.diag(rt))

        np.random.seed(12345)  # Set Seed
        simsm_diag_rt.sim_smoother()
        self.assertTrue(np.allclose(simsm_diag_rt.get_meas_residual(),
                                    meas_residual))

        #rt and ht diagonal (note different function)
        simsm_diag_rt_ht = SimSmoother(ymat, self.nstate, self.rstate, False,
                                    properties={'rt': 'diag', 'ht': 'diag'})
        simsm_diag_rt_ht.initialise_system(a1, p1, zt, np.diag(ht),
                                           tt, gt, qt, np.diag(rt))

        np.random.seed(12345)  # Set Seed
        simsm_diag_rt_ht.sim_smoother()
        self.assertTrue(np.allclose(simsm_diag_rt_ht.get_meas_residual(), meas_residual))

        #time_varyting case
        comp_ht = np.column_stack([np.diag(tv_ht[:, :, i]) for i in xrange(self.nobs)])
        comp_rt = np.column_stack([np.diag(tv_rt[:, :, i]) for i in xrange(self.nobs)])

        simsm_tv_diag_rt = SimSmoother(ymat, self.nstate, self.rstate, True,
                               properties={'rt': 'diag'})
        simsm_tv_diag_rt.initialise_system(a1, p1, tv_zt, tv_ht, tv_tt, tv_gt,
                               tv_qt, comp_rt)

        np.random.seed(12345)  # Set Seed
        simsm_tv_diag_rt.sim_smoother()

        self.assertTrue(np.allclose(simsm_tv_diag_rt.get_state_residual(), residuals))

        #diagonal rt and ht
        simsm_tv_diag_rt_ht = SimSmoother(ymat, self.nstate, self.rstate, True,
                                          properties={'rt': 'diag', 'ht': 'diag'})
        simsm_tv_diag_rt_ht.initialise_system(a1, p1, tv_zt, comp_ht,
                                              tv_tt, tv_gt, tv_qt, comp_rt)

        np.random.seed(12345)  # Set Seed
        simsm_tv_diag_rt_ht.sim_smoother()

        self.assertTrue(np.allclose(simsm_tv_diag_rt_ht.get_state_residual(),
                                    residuals))

    def test_log_probability_state(self):
        """Function evaluates whether the function log_probability_state
        gives the correct result."""

        #Define system matrices for tests"
        a1, p1, zt, ht, tt, gt, qt, rt = self.base_system()

        ymat = self.simdata(False, a1, p1, zt, ht, tt, gt, qt, rt)

        #Instantiate class for simulation smoothing.
        simsm = SimSmoother(ymat, self.nstate, self.rstate, False)
        simsm.initialise_system(a1, p1, zt, ht, tt, gt, qt, rt)

        #Run simulation smoother
        np.random.seed(12345)  # Set Seed
        state_ntv = simsm.sim_smoother()

        #compute log probability of state
        residual = simsm.get_state_residual()
        system = simsm.get_system()
        E, V = np.linalg.eig(system.gqg())
        lnpr = -self.nobs * self.rstate / 2. * np.log(2 * np.pi)
        lnpr = lnpr - (self.nobs - 1) / 2. * np.log(E[E > 1E-6]).sum()

        for t in xrange(self.nobs - 1):
            lnpr = lnpr - 0.5 * np.dot(residual[:, t],
                                       np.linalg.solve(qt, residual[:, t]))

        init_res = state_ntv[:, 0] - a1
        lnpr = lnpr - 0.5 * np.log(np.linalg.det(p1))\
                - 0.5 \
                * np.dot(init_res, np.linalg.solve(p1, init_res))
        self.assertAlmostEqual(lnpr, simsm.log_probability_state())
        #compare for time varying case
        tv_zt, tv_ht, tv_tt, tv_gt, tv_qt, tv_rt = \
                self.convert_system_tv(zt, ht, tt, gt, qt, rt)

        simsm_tv = SimSmoother(ymat, self.nstate, self.rstate, True)
        simsm_tv.initialise_system(a1, p1, tv_zt, tv_ht, tv_tt, tv_gt,
                               tv_qt, tv_rt)

        np.random.seed(12345)  # Set Seed
        simsm_tv.sim_smoother()

        self.assertTrue(np.allclose(lnpr, simsm_tv.log_probability_state()))

    def test_log_probability_meas(self):
        """Function evaluates whether the function log_probability_meas
        gives the correct result."""

        #Define system matrices for tests"
        a1, p1, zt, ht, tt, gt, qt, rt = self.base_system()

        ymat = self.simdata(False, a1, p1, zt, ht, tt, gt, qt, rt)

        #Instantiate class for simulation smoothing.
        simsm = SimSmoother(ymat, self.nstate, self.rstate, False)
        simsm.initialise_system(a1, p1, zt, ht, tt, gt, qt, rt)

        system = simsm.get_system()

        #Run simulation smoother
        np.random.seed(12345)  # Set Seed
        state_ntv = simsm.sim_smoother()

        #Initialise log probability
        lnpr = float(-self.nseries * self.nobs) / 2.0 * np.log(2.0 * np.pi) 
        lnpr = lnpr -0.5 *self.nobs * np.log(np.linalg.det(system.rhr()))
       

        for i in xrange(self.nobs):
            res = ymat[:, i] - np.dot(zt, state_ntv[:, i])
            lnpr = lnpr -0.5 * np.dot(res, np.linalg.solve(system.rhr(), res))

        self.assertTrue(np.allclose(lnpr, simsm.log_probability_meas()))


        #compare for time varying case
        tv_zt, tv_ht, tv_tt, tv_gt, tv_qt, tv_rt = \
                self.convert_system_tv(zt, ht, tt, gt, qt, rt)

        simsm_tv = SimSmoother(ymat, self.nstate, self.rstate, True)
        simsm_tv.initialise_system(a1, p1, tv_zt, tv_ht, tv_tt, tv_gt,
                               tv_qt, tv_rt)

        np.random.seed(12345)  # Set Seed
        simsm_tv.sim_smoother()


        lnpr_tv = simsm_tv.log_probability_meas()
        self.assertTrue(np.allclose(lnpr, lnpr_tv))




#Run unit tests
suite = unittest.TestLoader().loadTestsFromTestCase(TestSmoother)
unittest.TextTestRunner(verbosity=2).run(suite)
