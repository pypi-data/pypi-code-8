# -- coding: utf-8 --

# Copyright 2015 Tim Santor
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

# -----------------------------------------------------------------------------

# Standard
import argparse
import os
import re
import shutil
import pkg_resources

# App
from adkit import AdKitBase
from bashutils.logmsg import *
from bashutils.bashutils import *

# -----------------------------------------------------------------------------


class Main(AdKitBase):

    def copy_files(self):
        dest = self.input_dir+'js/'

        if not dir_exists(dest):
            if self.verbose:
                log_info('Creating "js" directory...')
            shutil.copytree(self.get_data('js'), dest)
        else:
            if self.verbose:
                log_warning('"js" directory already exists')

    def replace_all(self, text, dict):
        for src, target in dict.iteritems():
            text = text.replace(src, target)
        return text

    def generate_html(self):
        """
        Loop through all files in the output directory and compress them so
        that they are under/at their max file size.
        """
        num_files = 0

        # Loop through all files in the output directory
        for fn in os.listdir(self.input_dir):
            filepath = self.input_dir + fn
            if os.path.isfile(filepath):
                # get filename and extension
                basename = os.path.basename(filepath)
                name, ext = os.path.splitext(basename)

                # create a filename
                filename = self.input_dir+name+'.html'

                if ext == ".swf":
                    size = self.get_size_from_filename(name)

                    # do not overwrite existing HTML files (that would be bad)
                    if file_exists(filename):
                        if self.verbose:
                            log_warning('"{0}" already exists'.format(filename))
                        continue

                    self.create_html(size, name)
                    num_files += 1

        return num_files

    def create_html(self, size, name):
        """
        Create a HTML file for a specific swf/jpg.

        :param str size: width x height (eg - 300x250)
        :param str name: output file name
        :rtype bool:
        """
        # create a filename
        filename = self.input_dir+name+'.html'

        # get width height based on size string (eg - 300x250)
        width, height = size.split('x')

        # open the template and open a new file for writing
        #infile = open(pkg_resources.resource_filename('templates', 'template.html'))
        html = pkg_resources.resource_string(__name__, 'templates/template.html')
        outfile = open(filename, 'w')

        # replace the variables with the correct value
        replacements = {
            '{{filename}}': name,
            '{{size}}': size,
            '{{width}}': width,
            '{{height}}': height,
        }

        html = self.replace_all(html, replacements)
        outfile.write(html)

        '''for line in infile:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            outfile.write(line)'''

        # close the open files
        #infile.close()
        outfile.close()

        if self.verbose:
            print 'Create {0} HTML with filename {1}'.format(size, filename)

    def get_args(self):
        # https://docs.python.org/2/howto/argparse.html
        parser = argparse.ArgumentParser(
            description="Generate HTML from swfs for preview purposes."
        )

        # positional arguments
        #parser.add_argument("manifest", help="input file (.csv)")
        parser.add_argument("input", help="input directory")

        # optional arguments
        #parser.add_argument("-o", "--output", help="output directory")
        #parser.add_argument("-p", "--pngonly", help="export pngs only", action="store_true")
        parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

        # parse our arguments
        return parser.parse_args()

    def run(self):
        # Ensure proper command line usage
        args = self.get_args()

        #self.input_file = args.manifest
        self.input_dir = os.path.join(args.input, '')
        self.verbose = args.verbose

        # Copy required additional files
        self.copy_files()

        # Generate HTML files
        num_files = self.generate_html()

        log_success('Generated {0} HTML files'.format(num_files))

# -----------------------------------------------------------------------------


def main():
    main = Main()
    main.run()

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
