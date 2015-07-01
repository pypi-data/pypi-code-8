#!/usr/bin/env python

"""
Setup script to install mkterm
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
        name="mkterm",
        version="1.0.0",
        description="Make multiple terminals",
        long_description="Make multiple terminals on your desktop",
        url="http://github.com/leibrockoli/mkterm",
        author="Steven L",
        author_email="leibrockoli@gmail.com",
        license="MIT",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            ],
        keywords="terminal emulator mkterm desktop",
        packages=["mkterm"],
        install_requires=[],
        extras_require={},
        package_data={},
        entry_points={
            'console_scripts':[
                'mkterm=mkterm.app:main',
                ],
            }
)

# end
