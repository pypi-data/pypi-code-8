#!/usr/bin/env python
from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

import fnmatch
import os
import platform

from uuid import getnode

VERSION = ("0", "0", "1")
UA = 'UA-62318298-1'


def analytics(command_subclass):
    """Sends install statistics to analytics."""
    orig_run = command_subclass.run

    def modified_run(self):
        import sys
        print('-------------> INSTALL <--------------')
        try:
            try:
                from urllib2 import HTTPHandler, build_opener
                from urllib2 import urlopen, Request
                from urllib import urlencode
            except ImportError:
                from urllib.request import HTTPHandler, build_opener
                from urllib.request import urlopen, Request
                from urllib.parse import urlencode

            os_ver = platform.system()
            py_ver = '_'.join(str(x) for x in sys.version_info)
            now_ver = '_'.join(VERSION)

            code = 'os:{0},py:{1},now:{2}'.format(os_ver, py_ver, now_ver)
            action = command_subclass.action
            cid = getnode()
            payload = {
                'v': '1',
                'tid': UA,
                'cid': str(cid),
                't': 'event',
                'ec': action,
                'ea': code,
            }

            url = 'http://www.google-analytics.com/collect'
            data = urlencode(payload).encode('utf-8')
            request = Request(url, data=data)
            request.get_method = lambda: "POST"
            connection = urlopen(request)
        except:
            print(sys.exc_info())
            pass
        orig_run(self)

    command_subclass.run = modified_run
    return command_subclass


@analytics
class CustomDevelopCommand(develop):
    action = 'develop'


@analytics
class CustomInstallCommand(install):
    action = 'install'


setup(
    name = "try_analytics",
    version = '.'.join(VERSION),
    description="Try to collect install stats through google analytics",
    packages = find_packages(exclude=["tests_*", "tests"]),
    author = ("Joao Pimentel",),
    author_email = "joaofelipenp@gmail.com",
    license = "MIT",
    keywords = "google analytics setup.py",
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
    },
)
