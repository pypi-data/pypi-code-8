#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from setuptools import setup, find_packages


# Variables ===================================================================
CHANGELOG = open('CHANGES.rst').read()
LONG_DESCRIPTION = "\n\n".join([
    open('README.rst').read(),
    CHANGELOG
])


# Functions ===================================================================
def allSame(s):
    return not any(filter(lambda x: x != s[0], s))


def hasDigit(s):
    return any(char.isdigit() for char in s)


def getVersion(data):
    """
    Parse version from changelog written in RST format.
    """
    data = data.splitlines()
    return next((
        v
        for v, u in zip(data, data[1:])  # v = version, u = underline
        if len(v) == len(u) and allSame(u) and hasDigit(v) and "." in v
    ))


# Actual setup definition =====================================================
setup(
    name='kwargs_obj',
    version=getVersion(CHANGELOG),
    description='Class that maps .__init__(self, **kwargs) to attributes.',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/Bystroushaak/kwargs_obj',

    author='Bystroushaak',
    author_email='bystrousak@kitakitsune.org',

    classifiers=[
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        "License :: OSI Approved :: MIT License",
    ],
    license='MIT',

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=True,

    test_suite='py.test',
    tests_require=["pytest"],
    extras_require={
        "test": [
            "pytest"
        ],
    },
)
