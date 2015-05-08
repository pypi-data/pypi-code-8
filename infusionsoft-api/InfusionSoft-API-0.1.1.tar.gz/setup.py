#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

dependencies = []

links = []

setup(
    name='InfusionSoft-API',
    version='0.1.1',
    description='python wrapper for InfusionSoft API',
    author='Infusionsoft',
    maintainer='Nick Sloan',
    maintainer_email='spam+pypi@nasloan.com',
    scripts=[],
    url='https://github.com/infusionsoft/Official-API-Python-Library',
    packages=find_packages(),
    include_package_data=True,
    install_requires=dependencies,
    dependency_links=links,
)
