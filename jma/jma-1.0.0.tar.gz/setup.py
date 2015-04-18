#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
    setuptools_available = True
except ImportError:
    from distutils.core import setup
    setuptools_available = False


params = {}
if setuptools_available:
    params['entry_points'] = {'console_scripts': ['jma = jma:main']}
else:
    params['scripts'] = ['bin/jma']


setup(
    name = "jma",
    packages = ["jma"],
    version = "1.0.0",
    description = "Data downloader from Japan Meteorological Agency",
    author = "Kiwamu Ishikura",
    author_email = "ishikura.kiwamu@gmail.com",
    url = "https://bitbucket.org/i_kiwamu/jma_stat",
    download_url = "https://bitbucket.org/i_kiwamu/jma_stat/downloads/jma_stat_2.0.0.zip",
    kywords = ["download", "meteorological data", "japan"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: Japanese",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Utilities",
        ],
    long_description = """\
jma: Data downloader from JMA (Japan Meteorological Agency)
===========================================================

* Author: Kiwamu Ishikura
* Version: 1.0.0
* Licence: GPLv3

What's this?
------------
This is the program to get 1-hour meteorological data from JMA web site. You can retrieve data and save as csv.

Requirement
-----------
Python (>= 3.3)
*Beware that Python 2 can NOT work*

Usage
-----
Download jma_stat, you can type the followings on your console::

```
$ python3 jma.py
```

Program will ask you the beginning/final date of data you want, locations, and file name. Please follow the explanations.

If you put jmalib.py in your PYTHONLIB and put jma.py in your PATH, you can use these program anywhere. 
""",
    **params
)
