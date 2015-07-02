#!/usr/bin/env python

"""
Setup script to install mkterm
"""

from setuptools import setup, find_packages
from codecs import open
from os import path
import mkterm.info

here = path.abspath(path.dirname(__file__))

long_desc = """
Rapidly spawn terminals on your desktop. Intended for users 
with Tiling Window Managers who would like to populate a workspace
with terminals
"""

conf = {
        "name":"mkterm",
        "version":mkterm.info.__version__,
        "description":mkterm.info.__description__,
        "long_description":long_desc,
        "url":mkterm.info.__url__,
        "author":mkterm.info.__author__,
        "author_email":mkterm.info.__email__,
        "license":mkterm.info.__license__,
        "classifiers":[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            ],
        "keywords":"terminal emulator mkterm desktop",
        "packages":["mkterm"],
        "install_requires":[],
        "extras_require":{},
        "package_data":{},
        "entry_points":{
            'console_scripts':[
                'mkterm=mkterm.app:main',
                ]
        }
    }

setup(**conf)
# end
