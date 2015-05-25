#!/usr/bin/env python

# **********************************************************************************************************
# ** The module ez_setup install or upgrades setuptools in the case is not present on the destination system
# **********************************************************************************************************

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(name="atd",
      version="0.1.3",
      description="McAfee ATD API",
      author="Carlos Munoz",
      author_email="charly.munoz@gmail.com",
      packages=['atd'],
      install_requires=["requests >=2.7.0"],
      scripts=["bin\\atddir.py", "ez_setup.py"],
      url='http://www.mcafee.com/atd',
      )