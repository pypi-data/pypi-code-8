# /test/test_setuptools_green.py
#
# Tests for setuptools-green.
#
# See /LICENCE.md for Copyright information
"""Tests for setuptools-green."""

# pychecker seems to think that all these modules are being re-imported -
# they aren't, but just suppress the errors for now.

import sys  # suppress(PYC70)

from distutils.errors import DistutilsArgError  # suppress(PYC70)

import green.cmdline  # suppress(PYC70)

from mock import Mock  # suppress(PYC70)

from setuptools import Distribution  # suppress(PYC70)

from setuptools_green import GreenTestCommand  # suppress(PYC70)

from testtools import ExpectedException, TestCase  # suppress(PYC70)
from testtools.matchers import (Contains, Not)  # suppress(PYC70)


class TestGreenTestCommand(TestCase):

    """Test cases for the GreenTestCommand class."""

    def __init__(self, *args, **kwargs):
        """Initialize instance variables on this test case."""
        super(TestGreenTestCommand, self).__init__(*args, **kwargs)

    def setUp(self):  # suppress(N802)
        """Patch out functions to monitor GreenTestCommand behavior."""
        super(TestGreenTestCommand, self).setUp()

        self.patch(green.cmdline, "main", Mock(spec=green.cmdline.main))
        self.patch(sys, "exit", Mock(spec=green.cmdline.main))

    def test_run_quiet(self):
        """Run green tests quietly."""
        cmd = GreenTestCommand(Distribution())
        cmd.quiet = True
        cmd.ensure_finalized()
        cmd.run()
        self.assertThat(green.cmdline.sys.argv, Not(Contains("-vvv")))

    def test_invalid_option(self):  # suppress(no-self-use)
        """Invalidly formed options throw."""
        with ExpectedException(DistutilsArgError):
            cmd = GreenTestCommand(Distribution())
            cmd.quiet = "A string"
            cmd.ensure_finalized()
            cmd.run()

    def test_run_verbose(self):
        """Run green tests verbosely."""
        GreenTestCommand(Distribution()).run()
        self.assertThat(green.cmdline.sys.argv, Contains("-vvv"))

    def test_use_exit_status(self):  # suppress(no-self-use)
        """Use Green's exit status."""
        green.cmdline.main.return_value = 1
        GreenTestCommand(Distribution()).run()
        sys.exit.assert_called_with(1)
