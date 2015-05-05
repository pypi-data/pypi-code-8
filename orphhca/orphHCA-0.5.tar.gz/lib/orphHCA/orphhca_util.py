#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Function of orphHCA relative to annotation processing
"""

from __future__ import print_function
import ConfigParser, os, sys, shlex, subprocess

__author__  = "Tristan Bitard-Feildel"
__email__   = "tristan.bitard.feildel@uni-muenster.de"
__year__    = 2014
__licence__ = "MIT"
__version__ = 0.1

# checking that the environment variable is present
if not os.environ.get('ORPHHCA_DATA'):
    print("Please set the ORPHHCA_DATA environ variable to the location of "
          "PATH.ini", file=sys.stderr)
    sys.exit(1)
    
config = ConfigParser.ConfigParser()
config.read(os.path.join(os.getenv("ORPHHCA_DATA"),"PATH.ini"))


def check_program(program):  
    """ Check in the $PATH if we found the program
    TODO : probably not function for windows, I have to check that
    from http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    
    Parameter
    =========
    program : string
        the program name to look for
    Return
    ======
    path : string 
        the path to the program or None if the program is not found
    """

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    def ext_candidates(fpath):
        yield fpath
        for ext in os.environ.get("PATHEXT", "").split(os.pathsep):
            yield fpath + ext

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            for candidate in ext_candidates(exe_file):
                if is_exe(candidate):
                    return candidate
    return None
    
def check_program_config(sections=[]):
    """ check the program of the configparser
    
    Parameter
    =========
    sections: list
        list of sections to check
    """
    global config
    quit=False
    if not sections:
        sections = config.sections()
    for section in sections:
        for key, program in config.items(section):
            path = check_program(program)
            if path == None:
                print("Error : unable to find program path {} from config file ".format(program), file=sys.stderr)
                quit=True
    if quit:
        sys.exit(1)
        

def execute_cmd(cmd):
    """ run subprocess on a cmd string
    
    Parameter
    =========
    cmd: string
        the command line to execute
    """
    cmd = shlex.split(cmd)
    try:
        with open(os.devnull, "w") as ouf:
            subprocess.check_call(cmd, stderr=ouf, stdout=ouf)
    except:
        print("Failed to execute :\n{}".format(" ".join(cmd)), file=sys.stderr)
        raise
    
