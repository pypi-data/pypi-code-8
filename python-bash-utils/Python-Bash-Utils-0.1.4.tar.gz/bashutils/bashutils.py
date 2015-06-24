# -- coding: utf-8 --

# Copyright 2015
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Common methods to help assist when creating bash style python scripts."""

# -----------------------------------------------------------------------------

# Prevent compatibility regressions
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# Python
import os
import platform
import shutil
import subprocess

# -----------------------------------------------------------------------------
# Get OS
# -----------------------------------------------------------------------------


def get_os():
    """Returns the current OS name (OSX, Fedora, CentOS, Debian or Ubuntu)."""
    uname = platform.system()
    if uname == 'Darwin':
        return 'OSX'

    if uname == 'Linux':
        find = ['Fedora', 'CentOS', 'Debian', 'Ubuntu']
        # If lsb_release then test that output
        status = exec_cmd('hash lsb_release &> /dev/null')
        if status:
            for search in find:
                status = exec_cmd('lsb_release -i | grep %s > /dev/null 2>&1' % search)
                if status:
                    return search

        # Try to cat the /etc/*release file
        else:
            for search in find:
                status = exec_cmd('cat /etc/*release | grep %s > /dev/null 2>&1' % search)
                if status:
                    return search

    return 'unknown'

# -----------------------------------------------------------------------------
# Execute Command
# -----------------------------------------------------------------------------


def exec_cmd(cmd):
    """Executes a command and returns the status, stdout and stderror."""
    # call command
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

    # talk with command i.e. read data from stdout and stderr. Store this info in tuple
    stdout, stderr = proc.communicate()

    # wait for terminate. Get return returncode
    status = proc.wait()
    if status == 0:
        status = True
    else:
        status = False

    return (status, stdout, stderr)


def cmd_exists(program):
    """Returns True if a command exists."""
    cmd = "where" if platform.system() == "Windows" else "which"
    status = exec_cmd('{0} {1}'.format(cmd, program))
    return status

# -----------------------------------------------------------------------------
# Files / Directory
# -----------------------------------------------------------------------------


def file_exists(filepath):
    """Returns True is a file exists."""
    return os.path.isfile(filepath)


def dir_exists(directory):
    """Returns True if a directory exists."""
    return os.path.isdir(directory)


def delete_file(filepath):
    """Deletes a file if it exists."""
    if file_exists(filepath):
        os.remove(filepath)


def make_dir(directory):
    """Makes a directory if it does not exist."""
    if not dir_exists(directory):
        os.makedirs(directory)


def delete_dir(directory):
    """Deletes a directory if it exists."""
    if dir_exists(directory):
        shutil.rmtree(directory)


def copy_dir(src, dest):
    """Copies a directory recursively if it exists."""
    if dir_exists(src):
        shutil.copytree(src, dest)


def copy_file(src, dest):
    """Copies a file if it exists."""
    if file_exists(src):
        shutil.copy(src, dest)

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    print(get_os())
    print(cmd_exists('git'))
