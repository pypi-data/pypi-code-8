#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import sponsors

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = sponsors.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-sponsors',
    version=version,
    description="""Django App to easily manage project sponsors""",
    long_description=readme + '\n\n' + history,
    author='Miguel Fiandor',
    author_email='miguel.fiandor.gutierrez@gmail.com',
    url='https://github.com/miguelfg/django-sponsors',
    packages=[
        'sponsors',
    ],
    include_package_data=True,
    install_requires=['python-dateutil', 'django-stdimage'],
    license="MIT",
    zip_safe=False,
    keywords=['django', 'sponsors', 'sponsor', 'logos', 'logo'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
    ],
)
