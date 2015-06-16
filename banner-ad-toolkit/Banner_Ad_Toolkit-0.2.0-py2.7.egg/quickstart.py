# -- coding: utf-8 --

# Copyright 2015 Tim Santor
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Generates `adkit.ini` and `manifest.xlsx` files."""

# -----------------------------------------------------------------------------

# Prevent compatibility regressions
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# Standard
import argparse
import os
import pkg_resources
import shutil

# 3rd Party
from bashutils import logmsg

# App
from adkit.adkit import AdKitBase

# -----------------------------------------------------------------------------


class Main(AdKitBase):

    """Generates `adkit.ini` and `manifest.xlsx` files."""

    def __init__(self):
        self.verbose = False

    def copy_files(self):
        """
        Copy quickstart files from data folder to current working directory.
        """
        # Loop through all non-hidden files in quickstart directory
        files = [f for f in os.listdir(Main.get_data('quickstart')) if not f.startswith('.')]
        for filename in files:
            src = os.path.join(Main.get_data('quickstart'), filename)
            dst = os.path.join(os.getcwd(), filename)
            if not os.path.isfile(filename):
                shutil.copy2(src, dst)
                if self.verbose:
                    print('Copied {0}'.format(filename))
            else:
                logmsg.log_warning('"{0}" already exists'.format(filename))

    @staticmethod
    def get_parser():
        """Return arg parser."""
        # https://docs.python.org/2/howto/argparse.html
        parser = argparse.ArgumentParser(
            description="Copy starter files - adkit.ini & manifest.xlsx"
        )

        parser.add_argument("-v", "--verbose",
                            help="increase output verbosity",
                            action="store_true")
        version = pkg_resources.require("banner-ad-toolkit")[0].version
        parser.add_argument('-V', '--version',
                            action='version',
                            version=version)

        return parser

    def run(self):
        """Run script."""
        # Ensure proper command line usage
        parser = Main.get_parser()
        args = parser.parse_args()

        self.verbose = args.verbose

        logmsg.log_header('Copy quickstart files...')
        self.copy_files()

        logmsg.log_success('DONE!')

# -----------------------------------------------------------------------------


def main():
    """Main script."""
    script = Main()
    script.run()

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
