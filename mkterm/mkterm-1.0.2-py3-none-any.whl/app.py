#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
App.py
Contains application code
"""

from argparse import ArgumentParser
from os import system
from os.path import join, isfile, isdir, expanduser
from .info import __version__, __description__

def create_settings():
    """
    Create a blank settings file template in $HOME
    Should only be one line, 'terminal=xterm'
    """
    print("Creating default settings file ~/.mkterm")
    with open(join(expanduser("~"), ".mkterm"), "w") as setf:
        setf.write("terminal=xterm\n")

def load_settings_file():
    """
    Try to load a user script from ~/.mkterm
    Assert errors if we can't use the file at all
    """
    with open(join(expanduser("~"), ".mkterm"), "r") as setf:
        lines = setf.readlines()
    assert(len(lines) == 1)
    assert("terminal" in lines[0])
    return {'terminal' : lines[0].split("=").pop().strip().strip('\n')}

def spawn_instances(terminal="urxvt", num=1):
    """
    Function to spawn multiple terminal instances
    Assert errors based on bad input
    """
    assert(num > 0)
    assert(isinstance(terminal, str))
    return [system("{term} &".format(term=terminal)) for x in range(num)]

def main(*args, **kwargs):
    """
    Main application function to call
    Initializes argparser, creates/reads settings file
    Spawns instances based on arguments
    """
    ap = ArgumentParser(description=__description__, prog='mkterm')
    ap.add_argument('num', type=int, metavar='num', default=1,
                    help="Number of terminals to spawn")
    ap.add_argument('-v', '--version', action='version', 
                    version="%(prog)s version={0}".format(__version__))
    args = ap.parse_args()
    create_settings() if not isfile(join(expanduser("~"), ".mkterm")) else 0
    try:
        defsets = load_settings_file()
    except Exception as e:
        print("Settings loading went horribly wrong")
        print("Exception: {0}".format(e))
        print("Using default terminal 'xterm'")
        defsets = {'terminal': 'xterm', 'num': 1}
    try:
        defsets['num'] = args.num
        spawn_instances(**defsets)
        print("{1} instances spawned: {0}".format(args.num, defsets["terminal"]))
    except Exception as e:
        print("Exception encountered: {0}".format(str(e)))
    return True

if __name__ == "__main__":
    main()
