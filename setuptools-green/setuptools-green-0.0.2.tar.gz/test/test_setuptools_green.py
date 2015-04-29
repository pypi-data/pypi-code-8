# /test/test_setuptools_green.py
#
# Tests for setuptools-green.
#
# See /LICENCE.md for Copyright information
"""Tests for setuptools-green."""

import sys

from distutils.errors import DistutilsArgError

import green.cmdline

from mock import Mock

from setuptools import Distribution

from setuptools_green import GreenTestCommand

from testtools import ExpectedException, TestCase
from testtools.matchers import (Contains, Not)


class TestGreenTestCommand(TestCase):

    """Test cases for the GreenTestCommand class."""

    def __init__(self, *args, **kwargs):
        """Initialize instance variables on this test case."""
        super(TestGreenTestCommand, self).__init__(*args, **kwargs)

    def setUp(self):
        """Patch out functions to monitor GreenTestCommand behaviour."""
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

    def test_invalid_option(self):
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

    def test_use_exit_status(self):
        """Use Green's exit status."""
        green.cmdline.main.return_value = 1
        GreenTestCommand(Distribution()).run()
        sys.exit.assert_called_with(1)
