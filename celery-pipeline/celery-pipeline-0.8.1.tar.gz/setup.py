#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pip.req import parse_requirements

install_reqs = parse_requirements(
    'requirements.txt',
    session=False
)
reqs = [str(ir.req) for ir in install_reqs]

# see above
#version = pipeline.__version__
version = '0.8.1'

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

#readme = open('README.rst').read()
#history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='celery-pipeline',
    version=version,
    description="""Runtime-configured execution pipeline built on celery.""",
    author='Mike Waters',
    author_email='robert.waters@gmail.com',
    url='https://github.com/mikewaters/pipeline',
    packages=[
        'pipeline',
    ],
    include_package_data=True,
    install_requires=reqs,
    license="BSD",
    zip_safe=False,
    keywords='pipeline',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
    ],
)
