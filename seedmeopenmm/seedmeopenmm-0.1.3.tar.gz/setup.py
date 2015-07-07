#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'openmm',
    'seedme'

]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='seedmeopenmm',
    version='0.1.3',
    description="seedmeopenmm contains a stated data reporter that connects post Openmm simulation results to SeedMe",
    long_description=readme + '\n\n' + history,
    author="Sebastian Amara",
    author_email='sqamara@ucsd.edu',
    url='https://github.com/sqamara/seedmeopenmm',
    packages=[
        'seedmeopenmm',
    ],
    package_dir={'seedmeopenmm':
                 'seedmeopenmm'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='seedmeopenmm',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
