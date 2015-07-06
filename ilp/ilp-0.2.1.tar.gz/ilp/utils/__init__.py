#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ilp - a tag based file indexer
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

import os as _os
import subprocess as _subprocess

from .funcset import funcset
from .funcmap import funcmap
from .functuple import functuple

def check_program(name):
    '''Check if the given program is available.

    XXX: This just tries to run the program with -h, which for MOST programs
    will either display a help text, or cause it to complain that the option
    doesn't exist. Don't use this if the program does something else when called
    with -h!

    '''
    try:
        devnull = open(_os.devnull)
        _subprocess.Popen(
            [name, '-h'], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == _os.errno.ENOENT:
            return False
    return True
