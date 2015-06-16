# -- coding: utf-8 --

# Copyright 2015 Tim Santor
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Exports PSDs as static files."""

# -----------------------------------------------------------------------------

# Prevent compatibility regressions
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# Standard
import argparse
#import uuid
import os
import sys
import pkg_resources

# 3rd Party
from bashutils import bashutils
from bashutils import logmsg
from progressbar import ProgressBar

# App
from adkit.adkit import AdKitBase
from adkit.config import Config

# -----------------------------------------------------------------------------


class Main(AdKitBase):

    """Exports PSDs as static files."""

    def __init__(self):
        self.border_color = None
        self.csv_data = None
        self.format = None
        self.input_dir = None
        self.input_file = None
        self.output_dir = None
        self.override_max_size = False
        self.verbose = False

    @staticmethod
    def check_requirements():
        """Check requirements."""
        if not bashutils.cmd_exists('pngquant'):
            logmsg.log_error('pngquant is not installed')
            sys.exit()

        if not bashutils.cmd_exists('convert'):
            logmsg.log_error('ImageMagick is not installed')
            sys.exit()

    def get_border_settings(self):
        """Return border settings."""
        return '-strip -shave 1x1 -bordercolor "{0}" -border 1'.format(self.border_color)

    def convert_to_png(self, filepath):
        """
        Convert a PSD to a PNG.
        """
        # get filename and extension
        basename = os.path.basename(filepath)
        name = os.path.splitext(basename)[0]

        # create output filename
        output = os.path.join(self.output_dir, name+'.png')

        # quote input and output paths in case of spaces
        cmd = 'convert {2} "{0}[0]" "{1}"'.format(filepath, output, self.get_border_settings())
        bashutils.exec_cmd(cmd)

    def convert_to_jpg(self, filepath, max_size='40KB'):
        """
        Convert a file to a JPG while ensuring is is no larger than a
        specific file size.
        """
        # get filename and extension
        basename = os.path.basename(filepath)
        name = os.path.splitext(basename)[0]

        # create output filename
        output = os.path.join(self.output_dir, name+'.jpg')

        # quote input and output paths in case of spaces
        cmd = 'convert -quality 99 -define jpeg:extent={0} {3} "{1}[0]" "{2}"'\
            .format(max_size, filepath, output, self.get_border_settings())
        bashutils.exec_cmd(cmd)

    def convert_to_gif(self, filepath, max_size='40KB', colors=256):
        """
        Convert a file to a GIF while ensuring is is no larger than a
        specific file size.
        """
        # get filename and extension
        basename = os.path.basename(filepath)
        name = os.path.splitext(basename)[0]

        # create output filename
        output = os.path.join(self.output_dir, name+'.gif')

        # quote input and output paths in case of spaces
        cmd = 'convert -dither FloydSteinberg -colors {2} {3} "{0}[0]" "{1}"'\
            .format(filepath, output, colors, self.get_border_settings())
        status = bashutils.exec_cmd(cmd)

        if status:
            # check file size of compressed file
            # NOTE: ImageMagick does not have a gif:extent=40KB equivelent, so
            # we have to resort to this VERY slow manual method
            max_kb = Main.convert_string_size_to_bytes(max_size)
            if os.path.getsize(output) >= max_kb:
                if colors <= 8:
                    print('stopping attempts to compress further')
                    return
                colors = colors - 8  # colors / 2
                self.convert_to_gif(filepath, max_size, colors)

    def png_crush(self):
        """
        Crush all the PNGs in the output directory to make them smaller.
        """
        num_files = 0

        # get the output dir files
        files = [f for f in os.listdir(self.output_dir) if f.endswith('.png')]

        # create a progress bar
        pbar = ProgressBar(term_width=80, maxval=len(files)).start()

        for filen in files:
            filepath = os.path.join(self.output_dir, filen)
            if os.path.isfile(filepath):
                # crush png
                cmd = 'pngquant --ext .png --force 256 {0}'.format(filepath)
                bashutils.exec_cmd(cmd)

                num_files += 1

                # update progress bar
                pbar.update(num_files)

        # ensure progress bar is finished
        pbar.finish()
        time_elapsed = "(Time Elapsed: {0})".format(pbar.seconds_elapsed)

        logmsg.log_success('Crushed {0} files {1}'.format(num_files, time_elapsed))

    def get_max_size(self, filepath):
        """
        Return string such as 40KB
        """
        size = Main.get_size_from_filename(filepath)

        # get width height based on size string (eg - 300x250)
        width, height = size.split('x')

        # look in our CSV data for the banner matching this size
        for row in self.csv_data:
            if row['Type'] not in ['Flash'] and (row['Width'] == width and row['Height'] == height):
                if row['Max Size'] is not None and row['Max Size'] is not "":
                    if self.verbose:
                        print('{0} must be less than {1}'.format(size, row['Max Size']))
                    return row['Max Size']
                else:
                    return None

        return None

    @staticmethod
    def convert_string_size_to_bytes(string):
        """
        Convert 40KB to 40000 (bytes)
        """
        string = string.lower()

        if 'kb' in string:
            size = string.replace('kb', '')
            size = int(size) * 1000

        if 'mb' in string:
            size = string.replace('mb', '')
            size = int(size) * 100000

        return size

    def compress_to_max_size(self, filetype='jpg'):
        """
        Loop through all files in the output directory and compress them so
        that they are under/at their max file size.
        """
        num_files = 0

        # get the output dir files
        files = [f for f in os.listdir(self.input_dir) if not f.startswith('.')]

        # create a progress bar
        pbar = ProgressBar(term_width=80, maxval=len(files)).start()

        for filen in files:
            filepath = os.path.join(self.input_dir, filen)
            if os.path.isfile(filepath):
                # get max size
                max_size_string = self.get_max_size(filepath)

                if max_size_string is None:
                    bname = os.path.basename(filepath)
                    logmsg.log_error('No max size specified for {0}, assuming 40KB'.format(bname))
                    max_size_string = '40KB'

                # manually override max size
                if self.override_max_size:
                    max_size_string = self.override_max_size

                if filetype == 'png':
                    self.convert_to_png(filepath)

                # compress to max size
                if filetype == 'jpg':
                    self.convert_to_jpg(filepath, max_size_string)

                if filetype == 'gif':
                    self.convert_to_gif(filepath, max_size_string)

                num_files += 1

                # update progress bar
                pbar.update(num_files)

        # ensure progress bar is finished
        pbar.finish()
        time_elapsed = "(Time Elapsed: {0})".format(pbar.seconds_elapsed)

        logmsg.log_success('Compressed {0} files {1}'.format(num_files, time_elapsed))

    @staticmethod
    def get_defaults():
        """
        Get defaults from config file if it exists.
        """
        # load config file, overwriting any defaults
        defaults = {
            "manifest": "manifest.csv",
            "input": "PSD",
            "output": "PSD/Static",
            "format": "jpg",
            'border_color': "#cccccc"
        }

        # load config file
        config = Config()
        config.load()

        # update defaults with config file options
        defaults = config.update_defaults(defaults, 'default')
        defaults = config.update_defaults(defaults, 'static')

        #print defaults
        return defaults

    @staticmethod
    def get_parser():
        """Return arg parser."""
        # get defaults (from config if it exists)
        defaults = Main.get_defaults()

        # https://docs.python.org/2/howto/argparse.html
        parser = argparse.ArgumentParser(
            description="Export static files from PSDs while \
                ensuring each is under or at a max file size."
        )

        # set defaults
        parser.set_defaults(**defaults)

        # optional arguments
        parser.add_argument("-m", "--manifest", help="manifest file (.csv)")
        parser.add_argument("-i", "--input", help="input directory")
        parser.add_argument("-o", "--output", help="output directory")
        parser.add_argument("-f", "--format", help="output format",
                            choices=['jpg', 'png', 'gif'])
        parser.add_argument("-bc", "--border_color", help="border color")
        parser.add_argument("--max_size", help="max size string")

        parser.add_argument("-v", "--verbose",
                            help="increase output verbosity",
                            action="store_true")
        version = pkg_resources.require("banner-ad-toolkit")[0].version
        parser.add_argument('-V', '--version', action='version', version=version)

        return parser

    def run(self):
        """Run script."""
        # Ensure proper command line usage
        parser = Main.get_parser()
        args = parser.parse_args()

        self.input_file = args.manifest
        self.input_dir = os.path.join(args.input, '')
        self.output_dir = os.path.join(args.output, '')
        self.verbose = args.verbose
        self.format = args.format
        self.border_color = args.border_color
        self.override_max_size = False

        if args.max_size:
            self.override_max_size = args.max_size

        # Check requirements
        Main.check_requirements()

        # Check if the input dir exists
        if not os.path.isdir(self.input_dir):
            logmsg.log_error('"{0}" does not exist'.format(self.input_dir))
            sys.exit()

        # Open the CSV
        logmsg.log_header('Get deliverables data from CSV...')
        self.csv_data = Main.get_list_from_csv(self.input_file)

        # Create the dir we need
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Compress to max size
        logmsg.log_header('Create static versions from PSDs...')
        self.compress_to_max_size(args.format)

        if self.format == 'png':
            logmsg.log_header('Crushing PNGs...')
            self.png_crush()

# -----------------------------------------------------------------------------


def main():
    """Main script."""
    script = Main()
    script.run()

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
