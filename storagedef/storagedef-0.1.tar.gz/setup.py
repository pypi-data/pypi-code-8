#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup


description = 'Abstract storage interfaces'
here = os.path.abspath(os.path.dirname(__file__))
try:
    readme = open(os.path.join(here, 'README.rst')).read()
    changes = open(os.path.join(here, 'CHANGES.txt')).read()
    long_description = '\n\n'.join([readme, changes])
except:
    long_description = description


requires = (
    'botocore_paste',
    'pastedeploy',
    'zope.interface',
)

setup(
    name='storagedef',
    version='0.1',
    description=description,
    long_description=long_description,
    author='OCHIAI, Gouji',
    author_email='gjo.ext@gmail.com',
    url='https://github.com/gjo/storagedef',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    test_suite='storagedef',
    classifiers=[
        'Framework :: Paste',
        'Framework :: Pyramid',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
    ],
)
