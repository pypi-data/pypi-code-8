#!/usr/bin/env python3

from setuptools import setup

# jump through some hoops to get access to versionstring()
from sys import path
from os.path import abspath, dirname, join
topdir = abspath(dirname(__file__))
exec(open(join(topdir, "cifparser/version.py"), "r").read())

# load contents of README.rst
readme = open("README.rst", "r").read()
    
# load install requirements
with open("requirements.txt", "r") as f:
    install_requirements = [requirement for requirement in f.read().split('\n') if requirement]

# load test requirements
with open("test_requirements.txt", "r") as f:
    test_requirements = [requirement for requirement in f.read().split('\n') if requirement]

setup(
    # package description
    name = "cifparser",
    version = versionstring(),
    description="CIF (Configuration Interchange Format) parser",
    long_description=readme,
    author="Michael Frank",
    author_email="msfrank@syntaxockey.com",
    url="https://github.com/msfrank/cifparser",
    # installation dependencies
    install_requires=install_requirements,
    # package classifiers for PyPI
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License", 
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        ],
    # package contents
    packages=[
        "cifparser",
        ],
    test_suite="test",
    tests_require=test_requirements,
)
