#
# Copyright (C) 2015 Jerome Kelleher <jerome.kelleher@well.ox.ac.uk>
#
# This file is part of kingman.
#
# kingman is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kingman is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kingman.  If not, see <http://www.gnu.org/licenses/>.
#
"""
The command line interface for the kingman package.
"""
from __future__ import print_function
from __future__ import division

import argparse
import json
import sys

import kingman


def get_parser():
    """
    Returns an argparse based command line argument parser for
    the kingman program.
    """
    description = (
        "A simple command line interface for the Kingman simulator. "
        "Outputs a simulated coalescent history in the form of an "
        "oriented forest in JSON format. Time is measured in units"
        "of 4Ne."
    )
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("sample_size", type=int, help="Sample size")
    parser.add_argument(
        "-s", "--random-seed", type=int, help="Random seed",
        default=None)
    return parser


def run_simulation(sample_size, random_seed, output):
    """
    Runs the simulation for the specified sample_size and random
    seed, writing out oriented forest output to the specified file
    in JSON format.
    """
    parent, time = kingman.simulate(sample_size, random_seed)
    d = {"parent": parent[1:], "time": time[1:]}
    json.dump(d, output)
    # Write a trailing newline.
    print(file=output)


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.sample_size < 2:
        parser.error("Sample size must be >= 2")
    run_simulation(args.sample_size, args.random_seed, sys.stdout)
