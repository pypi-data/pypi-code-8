#!/usr/bin/env python
# coding=utf-8
"""This is part of [pyspaces](https://github.com/Friz-zy/pyspaces)

License: MIT or BSD or Apache 2.0
Copyright (c) 2014 Filipp Kucheryavy aka Frizzy <filipp.s.frizzy@gmail.com>

""" 


import errno
from .libc import *
from . import cloning as cl
from contextlib import contextmanager


ns = ('ipc', 'mnt', 'net', 'pid', 'user', 'uts')


@contextmanager
def setns(pid, all=False,
        ipc=False, mnt=False, net=False,
        pid=False, user=False, uts=False
        proc='/proc'
    ):
    """
    """
    try:
        if newpid or all:
            
        if newuser or all:
            
        if newns or all:
            
        if newuts or all:
            
        if newipc or all:
            
        if newnet or all:
            
        yield
    except:
        e = ctypes.get_errno()
        raise OSError(e, errno.errorcode[e])
    finally:
        pass
