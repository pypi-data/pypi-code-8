#Python code for running unit tests on for System class

from pyssm.ssm import System, SystemReg
import unittest
import numpy as np


class TestSystem(unittest.TestCase):
    """Class used to run unit tests on System class. Ensures all updates are
    handled correctly."""

    def setUp(self):
        """Define size of SSM for test"""
        self.nobs = 10    # Number of time series observations
        self.nseries = 2  # Number of time series
        self.nstate = 3   # Dimension of state
        self.rstate = 2   # Dimension of state covariance
        np.random.seed(12345)  # Setting seed for RNG
        self.nreg = 3  # Number of regressors in measurement equation
        self.sreg = 2  # Number of regressors in state equation

    def test_a1(self):
        """Tests a1 is updated correctly"""

        #timevar and noname = False
        timevar = False
        noname = False

        missing = False

        #No defined properties
        properties = {}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test a1
        a1 = np.random.randn(self.nstate)
        system.update_a1(a1)
        self.assertTrue((a1 == system.a1()).all())

    def test_p1(self):
        """Tests a1 is updated correctly"""

        #timevar and noname = False
        timevar = False
        noname = False

        missing = False

        #No defined properties
        properties = {}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test p1
        temp = np.random.randn(self.nstate, self.nstate * 5)
        p1 = np.dot(temp, temp.T)  # Ensures p1 is positive definite

        system.update_p1(p1)
        self.assertTrue((p1 == system.p1()).all())

    def test_tt_ntv(self):
        """Tests Tt is updated correctly for the non-time
        varying case"""

        #timevar and noname = False
        timevar = False
        noname = False

        missing = False

        #No defined properties
        properties = {}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test tt
        tt = np.random.randn(self.nstate, self.nstate)
        system.update_tt(tt)
        self.assertTrue((tt == system.tt()).all())

    def test_tt_tv(self):
        """Tests Tt is update correctly in the time varying
        case"""

        #setup timevar and noname
        timevar = {'tt': True}
        noname = False

        missing = False

        #No defined properties
        properties = {}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        tt = np.random.randn(self.nstate, self.nstate, self.nobs)
        system.update_tt(tt)
        self.assertTrue((tt == system.tt()).all())

    def test_zt_ntv(self):
        """Tests Zt is updated correctly for the non-time
        varying case"""

        #timevar and noname = False
        timevar = False
        noname = False

        missing = False

        #No defined properties
        properties = {}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test zt
        zt = np.random.randn(self.nseries, self.nstate)
        system.update_zt(zt)
        self.assertTrue((zt == system.zt()).all())

    def test_zt_tv(self):
        """Tests Zt is update correctly in the time varying
        case"""

        #setup timevar and noname
        timevar = {'zt': True}
        noname = False

        missing = False

        #No defined properties
        properties = {}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        zt = np.random.randn(self.nseries, self.nstate, self.nobs)
        system.update_zt(zt)
        self.assertTrue((zt == system.zt()).all())

    def test_rt_ht_ntv(self):
        """Tests Rt and Ht is being updated correctly in the non-time
        varying case"""

        #timevar and noname = False
        timevar = False
        noname = False

        missing = False

        #No defined properties
        properties = {}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test rt
        rt = np.random.randn(self.nseries, self.nseries)
        system.update_rt(rt)
        self.assertTrue((rt == system.rt()).all())

        #test ht
        temp = np.random.randn(100, self.nseries)
        ht = np.dot(temp.T, temp)  # ensure positive definite
        ht = ht / np.linalg.norm(ht)

        system.update_ht(ht)
        self.assertTrue((ht == system.ht()).all())

        #test cholesky decomposition ht
        chol_ht = np.linalg.cholesky(ht)
        self.assertTrue((chol_ht == system.cht()).all())

        #test R(t)*cHt(t)
        rcht = np.dot(rt, chol_ht)
        self.assertTrue((rcht == system.rcht()).all())

        #test R(t)*H(t) *R(t).T
        rhr = np.dot(rt, np.dot(ht, rt.T))

        self.assertTrue(np.allclose(rhr, system.rhr()))

    def test_rt_diag_ht_ntv(self):
        """Tests Rt (diagonal) and Ht is being updated correctly in
        the non-time varying case"""

        #timevar and noname = False
        timevar = False
        noname = False

        missing = False
        #No defined properties
        properties = {'rt': 'diag'}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test rt
        rt = np.random.randn(self.nseries)
        system.update_rt(rt)

        self.assertTrue(np.allclose(rt, system.rt()))

        #test ht
        temp = np.random.randn(100, self.nseries)
        ht = np.dot(temp.T, temp)  # ensure positive definite
        ht = ht / np.linalg.norm(ht)

        system.update_ht(ht)
        self.assertTrue((ht == system.ht()).all())

        #test cholesky decomposition ht
        chol_ht = np.linalg.cholesky(ht)
        self.assertTrue((chol_ht == system.cht()).all())

        #test R(t)*cHt(t)
        rcht = rt[:, np.newaxis] * chol_ht
        self.assertTrue((rcht == system.rcht()).all())

        #test R(t)*H(t) *R(t).T
        rhr = np.dot(np.diag(rt), np.dot(ht, np.diag(rt)))
        self.assertTrue(np.allclose(rhr, system.rhr()))

    def test_rt_ht_diag_ntv(self):
        """
        Tests Rt and Ht (diagonal) is being updated correctly in the
        non-time varying case.
        """

        #timevar and noname = False
        timevar = False
        noname = False

        missing = False

        #No defined properties
        properties = {'ht': 'diag'}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test rt
        rt = np.random.randn(self.nseries, self.nseries)
        system.update_rt(rt)

        self.assertTrue(np.allclose(rt, system.rt()))

        #test ht
        ht = np.random.randn(self.nseries) ** 2

        system.update_ht(ht)

        self.assertTrue((ht == system.ht()).all())

        #test cholesky decomposition ht
        chol_ht = np.sqrt(ht)
        self.assertTrue((chol_ht == system.cht()).all())

        #test R(t)*cHt(t)
        rcht = np.dot(rt, np.diag(chol_ht))
        self.assertTrue((rcht == system.rcht()).all())

        #test R(t)*H(t) *R(t).T
        rhr = np.dot(rt, np.dot(np.diag(ht), rt.T))
        self.assertTrue(np.allclose(rhr, system.rhr()))

    def test_rt_diag_ht_diag_ntv(self):
        """
        Tests Rt (diagonal) and Ht (diagonal) is being updated
        correctly in the non-time varying case
        """

        #timevar and noname = False
        timevar = False
        noname = False

        missing = False
        #No defined properties
        properties = {'ht': 'diag', 'rt': 'diag'}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test rt
        rt = np.random.randn(self.nseries)
        system.update_rt(rt)

        self.assertTrue(np.allclose(rt, system.rt()))

        #test ht
        ht = np.random.randn(self.nseries) ** 2
        system.update_ht(ht)

        self.assertTrue((ht == system.ht()).all())

        #test cholesky decomposition ht
        chol_ht = np.sqrt(ht)
        self.assertTrue((chol_ht == system.cht()).all())

        #test R(t)*cHt(t)
        rcht = rt * chol_ht

        self.assertTrue((rcht == system.rcht()).all())

        #test R(t)*H(t) *R(t).T
        rhr = rt * ht * rt

        self.assertTrue(np.allclose(rhr, system.rhr()))

    def test_rt_ht_stv(self):
        """Tests Rt and Ht is being updated correctly in the some-time
        varying case"""

        #timevar and noname = False
        timevar = {'zt': True}
        noname = False

        missing = False

        #No defined properties
        properties = {}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test rt
        rt = np.random.randn(self.nseries, self.nseries)
        system.update_rt(rt)
        self.assertTrue((rt == system.rt()).all())

        #test ht
        temp = np.random.randn(100, self.nseries)
        ht = np.dot(temp.T, temp)  # ensure positive definite
        ht = ht / np.linalg.norm(ht)

        system.update_ht(ht)
        self.assertTrue((ht == system.ht()).all())

        #test cholesky decomposition ht
        chol_ht = np.linalg.cholesky(ht)
        self.assertTrue((chol_ht == system.cht()).all())

        #test R(t)*cHt(t)
        rcht = np.dot(rt, chol_ht)
        self.assertTrue((rcht == system.rcht()).all())

        #test R(t)*H(t) *R(t).T
        rhr = np.dot(rt, np.dot(ht, rt.T))

        self.assertTrue(np.allclose(rhr, system.rhr()))

    def test_rt_diag_ht_stv(self):
        """
        Tests Rt (diagonal) and Ht is being updated correctly in the
        non-time varying case
        """

        #timevar and noname = False
        timevar = {'zt': True}
        noname = False

        missing = False

        #No defined properties
        properties = {'rt': 'diag'}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test rt
        rt = np.random.randn(self.nseries)
        system.update_rt(rt)

        self.assertTrue(np.allclose(rt, system.rt()))

        #test ht
        temp = np.random.randn(100, self.nseries)
        ht = np.dot(temp.T, temp)  # ensure positive definite
        ht = ht / np.linalg.norm(ht)

        system.update_ht(ht)
        self.assertTrue((ht == system.ht()).all())

        #test cholesky decomposition ht
        chol_ht = np.linalg.cholesky(ht)
        self.assertTrue((chol_ht == system.cht()).all())

        #test R(t)*cHt(t)
        rcht = rt[:, np.newaxis] * chol_ht
        self.assertTrue((rcht == system.rcht()).all())

        #test R(t)*H(t) *R(t).T
        rhr = np.dot(np.diag(rt), np.dot(ht, np.diag(rt)))
        self.assertTrue(np.allclose(rhr, system.rhr()))

    def test_rt_ht_diag_stv(self):
        """
        Tests Rt and Ht (diagonal) is being updated correctly in the
        non-time varying case
        """

        #timevar and noname = False
        timevar = {'zt': True}
        noname = False

        missing = False

        #No defined properties
        properties = {'ht': 'diag'}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test rt
        rt = np.random.randn(self.nseries, self.nseries)
        system.update_rt(rt)

        self.assertTrue(np.allclose(rt, system.rt()))

        #test ht
        ht = np.random.randn(self.nseries) ** 2
        system.update_ht(ht)

        self.assertTrue((ht == system.ht()).all())

        #test cholesky decomposition ht
        chol_ht = np.sqrt(ht)
        self.assertTrue((chol_ht == system.cht()).all())

        #test R(t)*cHt(t)
        rcht = np.dot(rt, np.diag(chol_ht))
        self.assertTrue((rcht == system.rcht()).all())

        #test R(t)*H(t) *R(t).T
        rhr = np.dot(rt, np.dot(np.diag(ht), rt.T))
        self.assertTrue(np.allclose(rhr, system.rhr()))

    def test_rt_diag_ht_diag_stv(self):
        """
        Tests Rt (diagonal) and Ht (diagonal) is being updated
        correctly in the non-time varying case
        """

        #timevar and noname = False
        timevar = {'zt': True}
        noname = False

        missing = False

        #No defined properties
        properties = {'ht': 'diag', 'rt': 'diag'}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test rt
        rt = np.random.randn(self.nseries)
        system.update_rt(rt)

        self.assertTrue(np.allclose(rt, system.rt()))

        #test ht
        ht = np.random.randn(self.nseries) ** 2
        system.update_ht(ht)

        self.assertTrue((ht == system.ht()).all())

        #test cholesky decomposition ht
        chol_ht = np.sqrt(ht)
        self.assertTrue((chol_ht == system.cht()).all())

        #test R(t)*cHt(t)
        rcht = rt * chol_ht
        self.assertTrue((rcht == system.rcht()).all())

        #test R(t)*H(t) *R(t).T
        rhr = rt * ht * rt

        self.assertTrue(np.allclose(rhr, system.rhr()))

    def test_rt_ht_tv(self):
        """Tests Rt is update correctly in the time varying
        case"""

        #setup timevar and noname
        timevar = {'rt': True, 'ht': True}
        noname = False

        missing = False

        #No defined properties
        properties = {}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test rt
        rt = np.random.randn(self.nseries, self.nseries, self.nobs)
        system.update_rt(rt)
        self.assertTrue((rt == system.rt()).all())

        #test ht
        temp = np.random.randn(100, self.nseries)
        ht_temp = np.dot(temp.T, temp)  # ensure positive definite
        ht_temp = ht_temp / np.linalg.norm(ht_temp)
        ht = np.repeat(ht_temp, self.nobs).reshape(self.nseries, self.nseries,
                                              self.nobs)

        system.update_ht(ht)
        self.assertTrue((ht == system.ht()).all())

        #test cholesky decomposition ht
        chol_ht = np.zeros((self.nseries, self.nseries, self.nobs))
        for i in xrange(self.nobs):
            chol_ht[:, :, i] = np.linalg.cholesky(ht[:, :, i])

        self.assertTrue(np.allclose(chol_ht, system.cht()))

        #test R(t)*cHt(t)
        rcht = np.zeros((self.nseries, self.nseries, self.nobs))
        for i in xrange(self.nobs):
            rcht[:, :, i] = np.dot(rt[:, :, i], chol_ht[:, :, i])
        self.assertTrue((rcht == system.rcht()).all())

        #test R(t)*H(t) *R(t).T
        rhr = np.zeros((self.nseries, self.nseries, self.nobs))
        for i in xrange(self.nobs):
            rhr[:, :, i] = np.dot(rt[:, :, i], np.dot(ht[:, :, i],
                                                      rt[:, :, i].T))

        self.assertTrue(np.allclose(rhr, system.rhr()))

    def test_rt_diag_ht_tv(self):
        """Tests Rt (diagonal) and Ht is being updated correctly in the time
        varying case"""

        #timevar and noname = False
        timevar = {'rt': True, 'ht': True}
        noname = False

        missing = False

        #No defined properties
        properties = {'rt': 'diag'}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test rt
        rt = np.random.randn(self.nseries, self.nobs)

        system.update_rt(rt)

        self.assertTrue(np.allclose(rt, system.rt()))

        #test ht
        temp = np.random.randn(100, self.nseries)
        ht = np.dot(temp.T, temp)  # ensure positive definite
        ht = ht / np.linalg.norm(ht)
        ht = np.repeat(ht, self.nobs).reshape(self.nseries, self.nseries,
                                              self.nobs)

        system.update_ht(ht)
        self.assertTrue((ht == system.ht()).all())

        #test cholesky decomposition ht
        chol_ht = np.zeros((self.nseries, self.nseries, self.nobs))
        for i in xrange(self.nobs):
            chol_ht[:, :, i] = np.linalg.cholesky(ht[:, :, i])
        self.assertTrue(np.allclose(chol_ht, system.cht()))

        #test R(t)*cHt(t)
        rcht = np.zeros((self.nseries, self.nseries, self.nobs))
        for i in xrange(self.nobs):
            rcht[:, :, i] = np.dot(np.diag(rt[:, i]), chol_ht[:, :, i])
        self.assertTrue(np.allclose(rcht, system.rcht()))

        #test R(t)*H(t) *R(t).T
        rhr = np.zeros((self.nseries, self.nseries, self.nobs))
        for i in xrange(self.nobs):
            rhr[:, :, i] = np.dot(np.diag(rt[:, i]), np.dot(ht[:, :, i],
                                                            np.diag(rt[:, i])))
        self.assertTrue(np.allclose(rhr, system.rhr()))

    def test_rt_ht_diag_tv(self):
        """Tests Rt and Ht (diagonal) is being updated correctly in the time
        varying case"""

        #timevar and noname = False
        timevar = {'ht': True, 'rt': True}
        noname = False

        missing = False

        #No defined properties
        properties = {'ht': 'diag'}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test rt
        rt = np.random.randn(self.nseries, self.nseries, self.nobs)
        system.update_rt(rt)

        self.assertTrue(np.allclose(rt, system.rt()))

        #test ht
        ht = np.random.randn(self.nseries, self.nobs) ** 2
        system.update_ht(ht)

        self.assertTrue(np.allclose(ht, system.ht()))

        #test cholesky decomposition ht
        chol_ht = np.sqrt(ht)
        self.assertTrue((chol_ht == system.cht()).all())

        #test R(t)*cHt(t)
        rcht = np.zeros((self.nseries, self.nseries, self.nobs))
        for i in xrange(self.nobs):
            rcht[:, :, i] = np.dot(rt[:, :, i], np.diag(chol_ht[:, i]))
        self.assertTrue((rcht == system.rcht()).all())

        #test R(t)*H(t) *R(t).T
        rhr = np.zeros((self.nseries, self.nseries, self.nobs))
        for i in xrange(self.nobs):
            rhr[:, :, i] = np.dot(rt[:, :, i],
                                np.dot(np.diag(ht[:, i]), rt[:, :, i].T))
        self.assertTrue(np.allclose(rhr, system.rhr()))

    def test_rt_diag_ht_diag_tv(self):
        """
        Tests Rt (diagonal) and Ht (diagonal) is being updated
        correctly in the non-time varying case
        """

        #timevar and noname = False
        timevar = {'rt': True, 'ht': True}
        noname = False

        missing = False

        #No defined properties
        properties = {'ht': 'diag', 'rt': 'diag'}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test rt
        rt = np.random.randn(self.nseries, self.nobs)
        system.update_rt(rt)

        self.assertTrue(np.allclose(rt, system.rt()))

        #test ht
        ht = np.random.randn(self.nseries, self.nobs) ** 2
        system.update_ht(ht)

        self.assertTrue((ht == system.ht()).all())

        #test cholesky decomposition ht
        chol_ht = np.sqrt(ht)
        self.assertTrue((chol_ht == system.cht()).all())

        #test R(t)*cHt(t)
        rcht = rt * chol_ht

        self.assertTrue(np.allclose(rcht, system.rcht()))

        #test R(t)*H(t) *R(t).T
        rhr = rt * ht * rt
        self.assertTrue(np.allclose(rhr, system.rhr()))

    def test_gt_qt_ntv(self):
        """Tests Gt and Qt is being updated correctly in the non-time
        varying case"""

        #timevar and noname = False
        timevar = False
        noname = False

        missing = False

        #No defined properties
        properties = {}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test gt
        gt = np.random.randn(self.nstate, self.rstate)
        system.update_gt(gt)

        self.assertTrue(np.allclose(gt, system.gt()))

        #test qt
        temp = np.random.randn(self.rstate * 10, self.rstate)
        qt = np.dot(temp.T, temp)  # Ensure qt positive definite
        qt = qt / np.linalg.norm(qt)

        system.update_qt(qt)

        self.assertTrue((qt == system.qt()).all())

        #test cholesky decomposition qt
        chol_qt = np.linalg.cholesky(qt)
        self.assertTrue((chol_qt == system.cqt()).all())

        #test G(t)*cQt(t)
        gcqt = np.dot(system.gt(), chol_qt)
        self.assertTrue((gcqt == system.gcqt()).all())

        #test G(t)*Q(t) *G(t).T
        gqg = np.dot(gt, np.dot(qt, gt.T))
        self.assertTrue(np.allclose(gqg, system.gqg()))

    def test_gt_qt_tv(self):
        """Tests Gt and Qt is being updated correctly in the time
        varying case"""

        #set to timevar and noname = False
        timevar = {'gt': True, 'qt': True}
        noname = False

        missing = False

        #No defined properties
        properties = {}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test gt
        gt = np.random.randn(self.nstate, self.rstate, self.nobs)
        system.update_gt(gt)

        self.assertTrue(np.allclose(gt, system.gt()))

        #test qt
        temp = np.random.randn(self.rstate * 10, self.rstate)
        qt = np.dot(temp.T, temp)  # Ensure qt positive definite

        tqt = qt / np.linalg.norm(qt)
        qt = np.zeros((self.rstate, self.rstate, self.nobs))
        for i in xrange(self.nobs):
            qt[:, :, i] = tqt

        #update system matrix for qt
        system.update_qt(qt)

        self.assertTrue((qt == system.qt()).all())

        #test cholesky decomposition qt
        chol_qt = np.zeros(qt.shape)
        for i in xrange(self.nobs):
            chol_qt[:, :, i] = np.linalg.cholesky(qt[:, :, i])
        self.assertTrue((chol_qt == system.cqt()).all())

        #test G(t)*cQt(t)
        gcqt = np.zeros((self.nstate, self.rstate, self.nobs))
        for i in xrange(self.nobs):
            gcqt[:, :, i] = np.dot(system.gt()[:, :, i], chol_qt[:, :, i])
        self.assertTrue((gcqt == system.gcqt()).all())

        #test G(t)*Q(t) *G(t).T
        gqg = np.zeros((self.nstate, self.nstate, self.nobs))
        for i in xrange(self.nobs):
            gqg[:, :, i] = np.dot(gt[:, :, i],
                                  np.dot(qt[:, :, i], gt[:, :, i].T))

        self.assertTrue(np.allclose(gqg, system.gqg()))

    def test_reg(self):
        "Tests whether regressors are handled correctly by system class."

        #set timevar, noname and missing to false
        timevar = {'zt': True}
        noname = False
        missing = False

        #No defined properties
        properties = {}

        #initialise system class
        system = SystemReg(self.nobs, self.nseries, self.nstate, self.rstate,
                           self.nreg, self.sreg,
                        timevar, noname, properties, missing)

        #Randomly generate regressors and regression coefficients for
        #testing
        xmat = np.random.randn(self.nseries, self.nreg, self.nobs)
        wmat = np.random.randn(self.nstate, self.sreg, self.nobs)
        beta = np.random.randn(self.nreg + self.sreg)

        system.update_xmat(xmat)
        system.update_wmat(wmat)
        system.update_beta(beta)

        wbeta = np.zeros((self.nstate, self.nobs))
        xbeta = np.zeros((self.nseries, self.nobs))
        for t in xrange(self.nobs):
            wbeta[:, t] = np.dot(wmat[:, :, t], beta[:self.sreg])
            xbeta[:, t] = np.dot(xmat[:, :, t], beta[self.sreg:])

        self.assertTrue(np.allclose(wbeta, system.wbeta()))
        self.assertTrue(np.allclose(xbeta, system.xbeta()))

    def test_gt_qt_stv(self):
        """
        Tests Gt and Qt is being updated correctly in the case where
        some of the matrices are time varying.
        """

        #set to timevar and noname = False
        timevar = {'zt': True}
        noname = False

        missing = False

        #No defined properties
        properties = {}

        #initialise system class
        system = System(self.nobs, self.nseries, self.nstate, self.rstate,
                        timevar, noname, properties, missing)

        #test gt
        gt = np.random.randn(self.nstate, self.rstate)
        system.update_gt(gt)

        self.assertTrue(np.allclose(gt, system.gt()))

        #test qt
        temp = np.random.randn(self.rstate * 10, self.rstate)
        qt = np.dot(temp.T, temp)  # Ensure qt positive definite
        qt = qt / np.linalg.norm(qt)

        system.update_qt(qt)

        self.assertTrue((qt == system.qt()).all())

        #test cholesky decomposition qt
        chol_qt = np.linalg.cholesky(qt)
        self.assertTrue((chol_qt == system.cqt()).all())

        #test G(t)*cQt(t)
        gcqt = np.dot(system.gt(), chol_qt)
        self.assertTrue((gcqt == system.gcqt()).all())

        #test G(t)*Q(t) *G(t).T
        gqg = np.dot(gt, np.dot(qt, gt.T))
        self.assertTrue(np.allclose(gqg, system.gqg()))


#Run unit tests
suite = unittest.TestLoader().loadTestsFromTestCase(TestSystem)
unittest.TextTestRunner(verbosity=2).run(suite)
