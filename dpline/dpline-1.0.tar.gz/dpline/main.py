#!/usr/bin/env python
# -*- coding: utf-8 -*-

# main.py is part file of dpline.

# Copyright 2015  Dimitris Zlatanidis  <d.zlatanidis@gmail.com>
# All rights reserved.

# dpline is tool to remove duplicate lines from file

# https://github.com/dslackw/dpline

# Alarm is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import os
import sys


__prog__ = "dpline"
__author__ = "dslackw"
__version_info__ = (1, 0)
__version__ = "{0}.{1}".format(*__version_info__)
__license__ = "GNU General Public License v3 (GPLv3)"
__email__ = "d.zlatanidis@gmail.com"


OPTIONS = [
    "-h", "--help",
    "-v", "--version",
    "-d", "--display",
    "-p", "--preview",
    "--ignore-blank",
    "--case-ins"
]


def dpline(arg, filename, ignore_blank, case_insensitive):
    """Remove duplicate lines from text files"""
    newfile = []
    if os.path.isfile(filename):
        with open(filename, "r") as r:
            oldfile = r.read().splitlines()
            for line in oldfile:
                if case_insensitive:
                    line = line.lower()
                if ignore_blank and not line:
                    newfile.append(line)
                elif line not in newfile:
                    newfile.append(line)
                else:
                    if arg in OPTIONS[4:5] or arg in OPTIONS[6:7]:
                        print(line)
        if arg not in OPTIONS[6:7]:
            with open(filename, "w") as w:
                for line in newfile:
                    w.write(line + "\n")
    else:
        not_access(filename)


def arguments(args):
    """Usage: dpline [OPTION] <file> [--ignore-blank, [--case-ins]]

dpline is tool to remove duplicate lines from file

Optional arguments:
  -h, --help          Print this help message and exit
  -v, --version       Print program version and exit
  -d, --display       Display removed lines
  -p, --preview       Preview duplicate lines before removal
  --ignore-blank      Ignore blank lines from remove
  --case-ins          Matching upper- and lowercase letters
  """
    args, ignore_blank, case_insensitive = flags(args)
    if len(args) == 1 and args[0] in OPTIONS[:2]:
        print(arguments.__doc__)
    elif len(args) == 1 and args[0] in OPTIONS[2:4]:
        version()
    elif len(args) == 2 and args[0] in OPTIONS[4:5]:
            dpline(args[0], args[1], ignore_blank, case_insensitive)
    elif len(args) == 2 and args[0] in OPTIONS[6:7]:
            dpline(args[0], args[1], ignore_blank, case_insensitive)
    elif len(args) == 1:
        if os.path.isfile(args[0]):
            dpline("", args[0], ignore_blank, "")
        else:
            not_access(args)
    else:
        usage()


def flags(args):
    """Manage flags"""
    ignore_blank, case_insensitive = False, False
    for flag in (OPTIONS[8] + OPTIONS[9]):
        if len(args) >= 2:
            if args[-1] == OPTIONS[8]:
                ignore_blank = True
                index = args.index(args[-1])
                del args[index]
            if args[-1] == OPTIONS[9]:
                case_insensitive = True
                index = args.index(args[-1])
                del args[index]
    return args, ignore_blank, case_insensitive


def not_access(args):
    """Cannot access message and exit"""
    sys.exit("%s: cannot access %s: No such file" % (__prog__, args[0]))


def usage():
    """Usage message and exit"""
    sys.exit("Usage: dpline [OPTION] <file> [--ignore-blank, [--case-ins]]\n\n"
             "Type dpline --help to see a list of all options")


def version():
    """Print version and exit"""
    sys.exit("%s %s" % (__prog__, __version__))


def main():
    args = sys.argv
    args.pop(0)
    arguments(args)

if __name__ == "__main__":
    main()
