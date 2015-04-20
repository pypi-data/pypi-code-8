#! /usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from docs import getVersion


changelog = open('CHANGES.rst').read()
long_description = "\n\n".join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    changelog
])


setup(
    name='marcxml2mods',
    version=getVersion(changelog),
    description="Module for conversion from MARC XML / OAI to MODS used in NK CZ.",
    long_description=long_description,
    url='https://github.com/edeposit/marcxml2mods',

    author='Edeposit team',
    author_email='edeposit@email.cz',

    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    license='GPL2+',

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,

    # scripts=[''],

    zip_safe=False,
    install_requires=[
        "lxml",
        "xmltodict",
        "pydhtmlparser>=2.0.9",
        "marcxml_parser",
        "remove_hairs",
    ],
    extras_require={
        "test": [
            "pytest"
        ],
        "docs": [
            "sphinx",
            "sphinxcontrib-napoleon",
        ]
    },
)
