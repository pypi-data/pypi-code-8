# This file is part of Ubuntu Continuous Integration virtual machine tools.
#
# Copyright 2014, 2015 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess


from ucivms import (
    errors,
)


def run(args):
    """Run the specified command capturing output and errors.

    :param args: A list of a command and its arguments.

    :return: A tuple of the return code, the output and the errors as unicode
        strings.
    """
    proc = subprocess.Popen(args,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()
    out = out.decode()
    err = err.decode()
    if proc.returncode:
        raise errors.CommandError(args, proc.returncode, out, err)
    return proc.returncode, out, err


def raw_run(args):
    """Run the specified command without redirecting anything.

    This is mainly useful to wrap a command leaving std{in,out,err}
        untouched so the user can interact.

    :param args:  A list of a command and its arguments.

    :return: The return code.
    """
    proc = subprocess.Popen(args)
    proc.wait()
    return proc.returncode


def pipe(args):
    """Run the specified command as a pipe.

    The caller is responsible for processing the output and the errors.

    :param args:  A list of a command and its arguments.

    :return: The Popen object.
    """
    proc = subprocess.Popen(args,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc
