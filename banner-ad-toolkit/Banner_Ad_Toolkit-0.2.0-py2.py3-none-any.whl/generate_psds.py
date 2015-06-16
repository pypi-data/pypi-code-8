# -- coding: utf-8 --

# Copyright 2015 Tim Santor
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Generates PSDs a set sizes with desired filenames."""

# -----------------------------------------------------------------------------

# Prevent compatibility regressions
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# Standard
import argparse
import os
import pkg_resources
import sys

# 3rd Party
from bashutils import bashutils
from bashutils import logmsg

# App
from adkit.adkit import AdKitBase
from adkit.config import Config

# -----------------------------------------------------------------------------


class Main(AdKitBase):

    """Generates PSDs a set sizes with desired filenames."""

    @staticmethod
    def check_requirements():
        """Check requirements."""
        if not bashutils.cmd_exists('convert'):
            logmsg.log_error('ImageMagick is not installed')
            sys.exit()

    @staticmethod
    def generate_filename(row):
        """
        Generates a filename given a row from the manifest CSV.
        """
        size = '{0}x{1}'.format(row['Width'], row['Height'])
        prefix = row['Prefix']
        suffix = row['Suffix']

        if prefix:
            prefix = '{0}_'.format(prefix)

        if suffix:
            suffix = '_{0}'.format(suffix)

        filename = '{0}{1}{2}.psd'.format(prefix, size, suffix)
        return filename

    @staticmethod
    def create_psd(size, filepath):
        """
        Create a blank PSD file at a specific size.

        :param str size: width x height (eg - 300x250)
        :param str filepath: output file path
        :rtype bool:
        """
        # create a 8bit RGB 72 dpi blank PSD (color BG to force RGB as white or black
        # will cause it to be grayscale due to lack of color)
        cmd = 'convert \
                -size %s xc:wheat \
                -colorspace RGB \
                -depth 8 \
                -units pixelsperinch \
                -density 72 \
                "%s"' % (size, filepath)
        bashutils.exec_cmd(cmd)

    @staticmethod
    def generate_psds(csv_data, output_dir):
        """
        Generates PSDs from manifest CSV.
        """
        num_files = 0

        for row in csv_data:
            if row['Type'] not in ['Flash'] and (row['Width'] and row['Height']):
                size = '{0}x{1}'.format(row['Width'], row['Height'])
                filename = Main.generate_filename(row)
                filepath = os.path.join(output_dir, filename)

                # do not overwrite existing PSDs (that would be bad)
                if os.path.isfile(filepath):
                    logmsg.log_warning('"{0}" already exists'.format(filename))
                    continue

                #print('Create {0} PSD with filename {1}'.format(size, filename))

                Main.create_psd(size, filepath)
                num_files += 1

        logmsg.log_success('Generated {0} PSD files'.format(num_files))

    @staticmethod
    def get_defaults():
        """
        Get defaults from config file if it exists.
        """
        # load config file, overwriting any defaults
        defaults = {
            "manifest": "manifest.csv",
            "output": "PSD",
        }

        # load config file
        config = Config()
        config.load()

        # update defaults with config file options
        defaults = config.update_defaults(defaults, 'default')
        defaults = config.update_defaults(defaults, 'psd')

        return defaults

    @staticmethod
    def get_parser():
        """Return arg parser."""
        # get defaults (from config if it exists)
        defaults = Main.get_defaults()

        # https://docs.python.org/2/howto/argparse.html
        parser = argparse.ArgumentParser(description='Generate PSDs at \
                                         specific sizes with set filenames.')

        # set defaults
        parser.set_defaults(**defaults)

        # optional arguments
        parser.add_argument("-m", "--manifest", help="manifest file (.csv)")
        parser.add_argument("-o", "--output", help="output directory")
        #parser.add_argument("-v", "--verbose",
        #                    help="increase output verbosity",
        #                    action="store_true")
        version = pkg_resources.require("banner-ad-toolkit")[0].version
        parser.add_argument('-V', '--version',
                            action='version', version=version)

        return parser

    @staticmethod
    def run():
        """Run script."""
        # Ensure proper command line usage
        parser = Main.get_parser()
        args = parser.parse_args()

        output_dir = os.path.join(args.output, '')

        # Check requirements
        Main.check_requirements()

        # Open the CSV
        logmsg.log_header('Get deliverables data from CSV...')
        csv_data = Main.get_list_from_csv(args.manifest)

        # Create the dir we need
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        logmsg.log_header('Generating PSDs...')
        Main.generate_psds(csv_data, output_dir)

# -----------------------------------------------------------------------------


def main():
    """Main script."""
    script = Main()
    script.run()

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
