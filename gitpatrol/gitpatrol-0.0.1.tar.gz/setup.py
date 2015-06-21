#!/usr/bin/env python

from codecs import open
from os import path
from setuptools import setup, find_packages
import sys

if sys.version_info[:2] < (2, 7):
    sys.exit("Git Patrol requires Python 2.7 or higher.")

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="gitpatrol",
    version="0.0.1",
    description="Flexible Git Pre-Commit Hooks",
    long_description=long_description,
    keywords="git development version control gitpatrol patrol",
    author="Arthur Burkart",
    author_email="artburkart@gmail.com",
    url="https://github.com/artburkart/gitpatrol",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7"
    ],
    py_modules=["gitpatrol"],
    packages=["lib"],
    tests_require=[
        "nose",
        "parameterizedtestcase",
        "coverage"
    ],
    install_requires=[
        "toml>=0.9.0"
    ],
    zip_safe=False,
    entry_points={
        "console_scripts": ["gitpatrol=gitpatrol:main"]
    }
)
