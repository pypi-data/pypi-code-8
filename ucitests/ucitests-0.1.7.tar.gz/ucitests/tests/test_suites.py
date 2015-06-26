# This file is part of the Ubuntu Continuous Integration test tools
#
# Copyright 2015 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
import unittest
try:
    from cStringIO import StringIO
except:
    from io import StringIO

from ucitests import (
    fixtures,
    results,
    scenarii,
    suites,
)


load_tests = scenarii.load_tests_with_scenarios


class TestSuiteSetup(unittest.TestCase):

    scenarios = [('unittest', dict(case_maker=fixtures.make_case)),
                 ('testtools', dict(case_maker=fixtures.make_testtools_case))]

    def run_suite(self, suite):
        res = results.TextResult(StringIO(), verbosity=0)
        res.startTestRun()
        suite.run(res)
        res.stopTestRun()
        return res

    def test_setup_pass(self):
        self.setup_called = False

        class Suite(suites.TestSuite):

            def setUp(inner):
                super(Suite, inner).setUp()
                self.setup_called = True

        suite = fixtures.make_suite(['pass', 'pass'], suite_maker=Suite)
        res = self.run_suite(suite)
        self.assertTrue(self.setup_called)
        self.assertTrue(res.wasSuccessful())
        self.assertEqual(2, res.testsRun)
        self.assertEqual(0, len(res.errors))
        self.assertEqual(0, len(res.failures))

    def test_setup_errors(self):
        self.setup_called = False

        class Suite(suites.TestSuite):

            def setUp(inner):
                super(Suite, inner).setUp()
                self.setup_called = True
                raise AssertionError

        suite = fixtures.make_suite(['pass', 'pass'], suite_maker=Suite)
        res = self.run_suite(suite)
        # An error during the setup fails the run without running the tests
        self.assertTrue(self.setup_called)
        self.assertFalse(res.wasSuccessful())
        self.assertEqual(0, res.testsRun)
        self.assertEqual(1, len(res.errors))
        self.assertEqual(0, len(res.failures))
        self.assertEqual(
            'ucitests.tests.test_suites.Suite({:x})'.format(id(suite)),
            res.errors[0][0].id())

    def test_tests_pass(self):
        self.setup_called = False
        self.cleanup_called = False

        class Suite(suites.TestSuite):

            def setUp(inner):
                super(Suite, inner).setUp()
                self.setup_called = True

                def cleanup():
                    self.cleanup_called = True
                inner.addCleanup(cleanup)

        suite = fixtures.make_suite(['pass', 'pass'], suite_maker=Suite)
        res = self.run_suite(suite)
        # When the tests pass, setup and cleanups are called.
        self.assertTrue(self.setup_called)
        self.assertTrue(self.cleanup_called)
        self.assertTrue(res.wasSuccessful())
        self.assertEqual(2, res.testsRun)
        self.assertEqual(0, len(res.errors))
        self.assertEqual(0, len(res.failures))

    def test_tests_errors(self):
        self.setup_called = False
        self.cleanup_called = False

        class Suite(suites.TestSuite):

            def setUp(inner):
                super(Suite, inner).setUp()
                self.setup_called = True

                def cleanup():
                    self.cleanup_called = True
                inner.addCleanup(cleanup)

        suite = fixtures.make_suite(['pass', 'error'], suite_maker=Suite)
        res = self.run_suite(suite)
        # If a test fails, the cleanups are called
        self.assertTrue(self.setup_called)
        self.assertTrue(self.cleanup_called)
        self.assertFalse(res.wasSuccessful())
        self.assertEqual(2, res.testsRun)
        self.assertEqual(1, len(res.errors))
        self.assertEqual(0, len(res.failures))

    def test_cleanup_errors(self):
        class Suite(suites.TestSuite):

            def setUp(inner):
                super(Suite, inner).setUp()

                def cleanup():
                    raise AssertionError
                inner.addCleanup(cleanup)

        suite = fixtures.make_suite(['pass', 'pass'], suite_maker=Suite)
        res = self.run_suite(suite)
        # If a cleanup fails, the suite fails even if the tests succeed
        self.assertFalse(res.wasSuccessful())
        self.assertEqual(2, res.testsRun)
        self.assertEqual(1, len(res.errors))
        self.assertEqual(0, len(res.failures))
        self.assertEqual(
            'ucitests.tests.test_suites.Suite({:x})'.format(id(suite)),
            res.errors[0][0].id())
