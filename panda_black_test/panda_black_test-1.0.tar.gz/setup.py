#!/usr/bin/python
#****************************************************************#
# ScriptName: setup.py
# Author: $SHTERM_REAL_USER@alibaba-inc.com
# Create Date: 2015-04-22 19:29
# Modify Author: $SHTERM_REAL_USER@alibaba-inc.com
# Modify Date: 2015-04-30 11:39
# Function: 
#***************************************************************#
from setuptools import setup, find_packages
setup(
            name = "panda_black_test",
            version = "1.0",
            description='test for panda_black',
            url='http://www.baidu.com/',
            author='panda_black',
            author_email='xxx',
            platforms=['unix', 'linux'],
            packages = find_packages(),
            entry_points = {
                'console_scripts': [
                    'foo = panda_black_test:test',
                    'bar = panda_black_test:test',
                ]
            },
            classifiers=(
                'Programming Language :: Python :: 2.6',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.3',
            ),
            license="Apache License 2.0",
            install_requires = [
                'colorama>=0.2.5,<=0.3.3',
                ]
)
