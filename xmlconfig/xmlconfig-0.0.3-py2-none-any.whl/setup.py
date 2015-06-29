# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

setup(
    name='xmlconfig',
    version='0.0.1',
    description='XML config helper',
    author='Gustavo Maia Neto (Guto Maia)',
    author_email='guto@guto.net',
    license='GPL3',
    packages=find_packages(),
    scripts=['bin/xmlconfig'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
    ],
    url='http://github.com/gutomaia/xmlconfig/'
)
