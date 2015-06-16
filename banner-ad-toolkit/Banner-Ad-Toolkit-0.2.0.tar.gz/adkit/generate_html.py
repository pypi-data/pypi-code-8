# -- coding: utf-8 --

# Copyright 2015 Tim Santor
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Generates HTML to preview SWF and static banner ads."""

# -----------------------------------------------------------------------------

# Prevent compatibility regressions
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# Standard
import argparse
import os
import sys
import pkg_resources
import shutil

# 3rd party
from bashutils import bashutils
from bashutils import logmsg
import six

# App
from adkit.adkit import AdKitBase
from adkit.config import Config

# -----------------------------------------------------------------------------


class Main(AdKitBase):

    """Generates HTML to preview SWF and static banner ads."""

    def __init__(self):
        self.upload_files = False
        self.verbose = False
        self.url = None
        self.ip = None
        self.remote_dir = None
        self.user = None
        self.input_dir = None

    def copy_files(self):
        """Copy files."""
        dest = os.path.join(self.input_dir, 'js')

        if not os.path.isdir(dest):
            if self.verbose:
                logmsg.log_info('Creating "js" directory...')
            shutil.copytree(Main.get_data('js'), dest)
        else:
            if self.verbose:
                logmsg.log_warning('"js" directory already exists')

    @staticmethod
    def replace_all(text, dict):
        """Replace all."""
        for src, target in six.iteritems(dict):
            text = text.replace(src, target)
        return text

    def create_html(self, filename):
        """
        Create a HTML file for a specific swf/jpg.

        :param str size: width x height (eg - 300x250)
        :param str name: output file name
        :rtype bool:
        """
        # get filename and extension
        basename = os.path.basename(filename)
        name = os.path.splitext(basename)[0]

        # get size
        size = Main.get_size_from_filename(name)

        # get width height based on size string (eg - 300x250)
        width, height = size.split('x')

        # open the template and open a new file for writing
        html = pkg_resources.resource_string(__name__, 'templates/template.html').decode("utf-8")
        print(html)
        outfile = open(filename, 'w')

        # replace the variables with the correct value
        replacements = {
            '{{filename}}': name,
            '{{size}}': size,
            '{{width}}': width,
            '{{height}}': height,
        }

        html = Main.replace_all(html, replacements)
        outfile.write(html)
        outfile.close()

        if self.verbose:
            print('Create {0} preview HTML \
                  with filename "{1}"'.format(size, os.path.basename(filename)))

    def generate_html(self):
        """
        Loop through all files in the input directory and create an HTML preview
        page for the swf and static version.
        """
        num_files = 0

        # Loop through all SWF files in the input directory
        files = [f for f in os.listdir(self.input_dir) if f.endswith('.swf')]
        for filen in files:
            filepath = os.path.join(self.input_dir, filen)
            if os.path.isfile(filepath):
                # get filename and extension
                basename = os.path.basename(filepath)
                name = os.path.splitext(basename)[0]

                # create a filename
                filename = os.path.join(self.input_dir, name+'.html')

                # do not overwrite existing HTML files (that would be bad)
                if os.path.isfile(filename):
                    if self.verbose:
                        basen = os.path.basename(filename)
                        logmsg.log_warning('"{0}" already exists'.format(basen))
                    continue

                self.create_html(filename)
                num_files += 1

        logmsg.log_success('Generated {0} HTML files'.format(num_files))

    def upload(self):
        """Upload."""
        cmd = 'rsync -avzhP --exclude .DS_Store "{0}" {1}@{2}:{3}'.\
            format(self.input_dir, self.user, self.ip, self.remote_dir)
        status = bashutils.exec_cmd(cmd)
        if status:
            logmsg.log_success("Uploaded preview files")

        # Loop through all HTML files in the input directory
        #files = [f for f in os.listdir(self.input_dir) if f.endswith('.html')]
        #for filename in files:
        #    print('{0}{1}'.format(self.url, filename))

    @staticmethod
    def get_defaults():
        """
        Get defaults from config file if it exists.
        """
        # load config file, overwriting any defaults
        defaults = {
            "input": "PSD",
        }

        # load config file
        config = Config()
        config.load()

        # update defaults with config file options
        defaults = config.update_defaults(defaults, 'flash')
        defaults = config.update_defaults(defaults, 'upload')

        #print defaults
        return defaults

    @staticmethod
    def get_parser():
        """Returns arg parser."""
        # get defaults (from config if it exists)
        defaults = Main.get_defaults()

        # https://docs.python.org/2/howto/argparse.html
        parser = argparse.ArgumentParser(
            description="Generate HTML from swfs for preview purposes."
        )

        # set defaults
        parser.set_defaults(**defaults)

        # optional arguments
        parser.add_argument("-i", "--input", help="input directory")

        group = parser.add_argument_group('upload')
        group.add_argument("-u", "--upload",
                           help="upload preview files to server",
                           action="store_true")
        group.add_argument("--user", help="ssh user")
        group.add_argument("--ip", help="remote ip address")
        group.add_argument("--remote_dir", help="remote dir path")
        group.add_argument("--url", help="URL")

        parser.add_argument("-v", "--verbose",
                            help="increase output verbosity",
                            action="store_true")
        version = pkg_resources.require("banner-ad-toolkit")[0].version
        parser.add_argument('-V', '--version', action='version',
                            version=version)

        # parse our arguments
        return parser

    def run(self):
        """Run script."""
        # Ensure proper command line usage
        parser = Main.get_parser()
        args = parser.parse_args()

        self.input_dir = os.path.join(args.input, '')
        #self.config_file = args.config
        self.upload_files = args.upload
        self.verbose = args.verbose

        self.user = args.user
        self.ip = args.ip
        self.remote_dir = args.remote_dir
        self.url = args.url

        # Check if the input dir exists
        if not os.path.isdir(self.input_dir):
            logmsg.log_error('"{0}" does not exist'.format(self.input_dir))
            sys.exit()

        # Generate HTML files
        logmsg.log_header('Generate preview HTML files...')
        self.copy_files()
        self.generate_html()

        # Upload preview files
        if self.upload_files:
            logmsg.log_header('Upload preview files...')
            self.upload()

# -----------------------------------------------------------------------------


def main():
    """Main script."""
    script = Main()
    script.run()

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
