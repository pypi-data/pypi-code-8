#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

try:
    with open('requirements.txt') as f:
        requirements = [item for item in f.readlines()
            if not item.strip().startswith('#')]
except IOError:
    requirements = []

from fdfs_tornado import __version__ as version

setup(
    name='fdfs-tornado',
    version=version,
    description="Async FDFS Client for tornado",
    long_description=readme,
    author="WangST",
    author_email='wangst321@gmail.com',
    url='http://git.elenet.me/opdev/eoc-api.git',
    packages=['fdfs_tornado'],
    install_requires=requirements,
    # include_package_data=True,
    # install_requires=requirements,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
    ],
)

