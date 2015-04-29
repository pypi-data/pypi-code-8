# /setuptools_green/__init__.py
#
# Provides a setuptools command for running tests using the "green"
# test runner.
#
# See /LICENCE.md for Copyright information
"""Provide a setuptools command for running tests with green."""

from distutils.errors import DistutilsArgError

import setuptools

import sys


class GreenTestCommand(setuptools.Command):

    """Provide a test command using green."""

    def run(self):
        """Run tests using green."""
        import green.cmdline
        import green.config

        green.config.sys.argv = ["", "-t"]
        if not self.quiet:
            green.config.sys.argv.append("-vvv")

        sys.exit(green.cmdline.main())

    def initialize_options(self):  # suppress(unused-function)
        """Set all options to their initial values."""
        self.quiet = False

    def finalize_options(self):  # suppress(unused-function)
        """Finalize options."""
        if not isinstance(self.quiet, bool):
            raise DistutilsArgError("""--quiet takes no additional """
                                    """arguments.""")

    user_options = [
        ("quiet", None, "Don't show test descriptions when running")
    ]
    description = "run tests using the 'green' test runner"
