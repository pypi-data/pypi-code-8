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

# User should never want to actually spawn more than 10 terminals
# Otherwise could be used for malicious intent
# Additionally, you can't spawn less than 1 terminal 
MIN = 1
MAX = 10

# This is the path for mkterm dotfile
DOTFILE = join(expanduser("~"), ".mkterm")

def test_error(expression, emsg="Error occured"):
    """
    Test issues via ternary expression
    """
    return True if expression else throw_error(emsg) 

def throw_error(emsg):
    """
    Container for throwing errors (raise is a keyword)
    """
    raise Exception(emsg)

def create_settings():
    """
    Create a blank settings file template in $HOME
    Should only be one line, 'terminal=xterm'
    """
    print("Creating default settings file ~/.mkterm")
    with open(DOTFILE, "w") as setf:
        setf.write("terminal=xterm\n")

def load_settings_file():
    """
    Try to load a user script from ~/.mkterm
    Throw errors if we can't use the file at all
    """
    with open(DOTFILE, "r") as setf:
        lines = setf.readlines()
    data = {k:v for k, v in (l.strip().split("=") for l in lines)}
    test_error("terminal" in data, "Invalid dotfile at {0}".format(DOTFILE))
    test_error(len(data) == 1, "Too many variables in dotfile")
    return data

def spawn_instances(terminal="urxvt", num=1):
    """
    Function to spawn multiple terminal instances
    Throw errors based on bad input
    """
    test_error(num > MIN, "Input too small")
    test_error(num < MAX, "Input too large") 
    return [system("{term} &".format(term=terminal)) for x in range(num)]

def main(*args, **kwargs):
    """
    Main application function to call
    Initializes argparser, creates/reads settings file
    Spawns instances based on arguments
    """
    ap = ArgumentParser(description=__description__, prog='mkterm')
    ap.add_argument('num', type=int, nargs='?', metavar='num', default=1,
                    help="Number of terminals to spawn")
    ap.add_argument('-v', '--version', action='version', 
                    version="%(prog)s version={0}".format(__version__))
    args = ap.parse_args()
    create_settings() if not isfile(DOTFILE) else 0
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
        print("{1}'s  spawned: {0}".format(args.num, defsets["terminal"]))
    except Exception as e:
        print("Exception encountered: {0}".format(str(e)))
    return True

if __name__ == "__main__":
    main()
