#!/usr/local/bin/python
# coding: utf-8

# -----------------------------------------------------------------------------

# Python
import os
import platform
import shutil
import subprocess

# 3rd party
from colors import *
from logmsg import *

# -----------------------------------------------------------------------------
# Get OS
# -----------------------------------------------------------------------------


def get_os():
    uname = platform.system()
    if uname == 'Darwin':
        return 'OSX'

    if uname == 'Linux':
        find = ['Fedora', 'CentOS', 'Debian', 'Ubuntu']
        # If lsb_release then test that output
        status, stdout, stderr = exec_cmd('hash lsb_release &> /dev/null')
        if status:
            for search in find:
                status, stdout, stderr = exec_cmd('lsb_release -i | grep %s > /dev/null 2>&1' % search)
                if status:
                    return search

        # Try to cat the /etc/*release file
        else:
            for search in find:
                status, stdout, stderr = exec_cmd('cat /etc/*release | grep %s > /dev/null 2>&1' % search)
                if status:
                    return search

    return 'unknown'

# -----------------------------------------------------------------------------
# Execute Command
# -----------------------------------------------------------------------------


def exec_cmd(cmd):
    # call command
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

    # talk with command i.e. read data from stdout and stderr. Store this info in tuple
    stdout, stderr = p.communicate()

    # wait for terminate. Get return returncode
    status = p.wait()
    if status == 0:
        status = True
    else:
        status = False

    return (status, stdout, stderr)

def cmd_exists(program):
    cmd = "where" if platform.system() == "Windows" else "which"
    status, stdout, stderr = exec_cmd('{0} {1}'.format(cmd, program))
    return status

# -----------------------------------------------------------------------------
# Files / Directory
# -----------------------------------------------------------------------------


def file_exists(filepath):
    return os.path.isfile(filepath)

def dir_exists(directory):
    return os.path.isdir(directory)

def delete_file(filepath):
    if file_exists(filepath):
        os.remove(filepath)
        return True

    return False

def make_dir(directory):
    if not dir_exists(directory):
        os.makedirs(directory)

def delete_dir(directory):
    if dir_exists(directory):
        shutil.rmtree(directory)

def copy_dir(src, dest):
    if dir_exists(src):
        shutil.copytree(src, dest)
        return True

    return False

def copy_file(src, dest):
    if file_exists(src):
        shutil.copy(src, dst)
        return True

    return False

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    pass
