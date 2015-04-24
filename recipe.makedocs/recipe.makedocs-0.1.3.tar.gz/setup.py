#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


setup(
    name='recipe.makedocs',
    version='0.1.3',
    description="zc.buildout recipe to generate and build Sphinx-based documentation in the buildout",
    author='',
    author_email='',
    include_package_data=True,
    install_requires=[
        'setuptools',
        'zc.buildout',
        'sphinx',
    ],
    extras_require={'tests': ['zc.buildout']},
    zip_safe=False,
    packages=find_packages('.'),
    namespace_packages=['recipe'],
    classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points = {"zc.buildout": ["default = recipe.makedocs:Recipe"]}

)
