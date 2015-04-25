#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

description = 'A command manager (i.e. Commander) for Python modules and packages.'

install_requires = [
    'click==4.0',
    'pluginbase==0.3',
    'python-easyconfig==0.1.0',
]


def get_version():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'cmdr/__init__.py')) as f:
        locals = {}
        exec(f.read(), locals)
        return locals['__version__']
    raise RuntimeError('No version info found.')


setup(
    name='Python-Cmdr',
    version=get_version(),
    author='RussellLuo',
    author_email='luopeng.he@gmail.com',
    maintainer='RussellLuo',
    maintainer_email='luopeng.he@gmail.com',
    keywords='Commander, Command manager, Python',
    description=description,
    license='MIT',
    long_description=description,
    packages=find_packages(exclude=['tests']),
    url='https://github.com/RussellLuo/cmdr',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'cmdr = cmdr.commander:main',
        ],
    },
)
