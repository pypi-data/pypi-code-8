# -- coding: utf-8 --

# Copyright 2015 X Studios Inc
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Downloads any number of images from lorempixel.com."""

# -----------------------------------------------------------------------------
# Prevent compatibility regressions
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# Standard
import argparse
import os
import pkg_resources
import requests

# 3rd Party
from bashutils.logmsg import log_header, log_success
#from bashutils.bashutils import *
from progressbar import ProgressBar
from six.moves import range

# -----------------------------------------------------------------------------

BASE_URL = 'http://lorempixel.com/'


def get_size(size):
    """
    Returns a size "widthxheight" as "width/height"
    """
    return size.replace('x', '/')


def download_file(url, directory, filename):
    """
    Downloads a file and saves it to disk.
    """
    local_file_name = filename
    req = requests.get(url, stream=True)

    with open(directory + '/' + local_file_name, 'wb') as ofile:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                ofile.write(chunk)
                ofile.flush()
                os.fsync(ofile.fileno())


def get_parser():
    """
    Ensure proper command line usage.
    https://docs.python.org/2/howto/argparse.html
    """
    parser = argparse.ArgumentParser(
        description="Downloads images from Lorem Pixel."
    )

    parser.add_argument("size", help="image size (eg - 512x512)")
    parser.add_argument("num", help="number of images", type=int)

    default_dir = os.path.join(os.getcwd(), 'lorem-pixel-downloads')
    parser.add_argument("-o", "--output",
                        help="output directory",
                        default=default_dir)
    parser.add_argument("-c", "--category",
                        help="image category", default='cats',
                        choices=['abstract', 'animals', 'business', 'cats',
                                 'city', 'food', 'nightlife', 'fashion',
                                 'people', 'nature', 'sports', 'technics',
                                 'transport'])

    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="store_true")

    version = pkg_resources.require("python-lorem-pixel")[0].version
    parser.add_argument('-V', '--version',
                        action='version',
                        version=version)

    # parse our arguments
    return parser


def run():
    """Run script."""
    # Ensure proper command line usage
    parser = get_parser()
    args = parser.parse_args()

    #verbose = args.verbose
    output_dir = os.path.join(args.output, args.category, '')

    log_header('Downloading images from Lorem Pixel...')

    # create directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # create a progress bar
    pbar = ProgressBar(term_width=80, maxval=args.num).start()

    for i in range(0, args.num):
        # update progress bar
        pbar.update(i+1)

        # get the size in the format of (width/height)
        size = get_size(args.size)

        # download file and give it a name
        filename = "%03d.jpg" % (i+1)
        download_file(BASE_URL+size+'/'+args.category, output_dir, filename)

    # ensure progress bar in finished state
    pbar.finish()

    print('Time Elapsed: {0}'.format(pbar.seconds_elapsed))
    log_success('Downloaded {0} images in the "{1}"" category'.format(args.num, args.category))

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    run()
