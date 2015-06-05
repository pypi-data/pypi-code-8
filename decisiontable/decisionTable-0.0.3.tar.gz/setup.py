#!/usr/bin/env python
# -*- coding: utf-8 -*-
import decisionTable

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    'pylint',
    'flake8',
    'coveralls'
]

setup(
    name='decisionTable',
    version=decisionTable.__version__,
    description=decisionTable.__description__,
    long_description=readme + '\n\n' + history,
    author=decisionTable.__author__,
    author_email=decisionTable.__email__,
    url='https://github.com/urosjarc/decisionTable',
    packages=[
        'decisionTable',
        'decisionTable.view'
    ],
    package_dir={
        'decisionTable': 'decisionTable'
    },
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='decisionTable',
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
