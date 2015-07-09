#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://sitechantment.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='sitechantment',
    version='0.1.0',
    description='Check a site for spelling errors',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Michael Messmore',
    author_email='mike@messmore.org',
    url='https://github.com/mmessmore/sitechantment',
    packages=[
        'sitechantment',
    ],
    package_dir={'sitechantment': 'sitechantment'},
    include_package_data=True,
    install_requires=[
        'beautifulsoup4==4.4.0',
        'click==3.3',
        'pyenchant==1.6.6',
        'requests==2.7.0',
    ],
    license='BSD',
    zip_safe=False,
    keywords='sitechantment',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    entry_points={
        'console_scripts': [
            'sitechantment=sitechantment.sitechantment:main',
        ]
    }
)
