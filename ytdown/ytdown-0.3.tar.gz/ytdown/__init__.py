#!/usr/bin/env python

import os
import sys
import subprocess
euid = os.geteuid()
if euid != 0:
    # print "Script not started as root. Running sudo.."
    args = ['sudo', sys.executable] + sys.argv + [os.environ]
    # the next line replaces the currently-running process with the sudo
    os.execlpe('sudo', *args)
if not os.path.exists('/../Youtube'):
	os.mkdir('/../Youtube')
else:
    pass
if not os.path.exists('/../Youtube/Audio'):
	os.mkdir('/../Youtube/Audio')
else:
    pass
if not os.path.exists('/../Youtube/Video'):
	os.mkdir('/../Youtube/Video')
else:
    pass
