#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twid

from setuptools import setup, find_packages

setup(
    name = "twid",
    version = twid.__version__,
    description = "The relevant functions about Taiwan Identification Card system.",
    author = "Plenty Su",
    author_email = "plenty.su@gmail.com",
    license = "MIT",
    packages = find_packages()
)
