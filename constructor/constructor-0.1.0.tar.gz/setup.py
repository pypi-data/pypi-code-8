#!/usr/bin/env python
# coding=utf8
import sys

from setuptools import setup, find_packages

required_packages = ['awscli']

if sys.version_info[:2] == (2, 6):
    # For python2.6 we have to require argparse since it
    # was not in stdlib until 2.7.
    required_packages.append('argparse>=1.1')

setup(
    name="constructor",
    version="0.1.0",
    description="A tool for building up infrastructure.",
    long_description="Constructor can be used to automate infrastructure creation and provisioning.",
    url="http://istvan-antal.github.io/constructor/",
    author="István Miklós Antal",
    author_email="istvan.m.antal@gmail.com",
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords="infrastructure build provisioning aws automate",
    packages=find_packages('.'),
    package_data={
        'constructor': ['20auto-upgrades'],
    },
    install_requires=required_packages,
    entry_points={
        'console_scripts': [
            'construct = constructor.cli:main'
        ]
    }
)