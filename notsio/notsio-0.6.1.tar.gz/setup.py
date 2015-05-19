# -*- coding: utf-8 -*-
import re
from setuptools import setup

setup(
    name='notsio',
    version = re.search(r'''^__version__\s*=\s*["'](.*)["']''', open('notsio/__init__.py').read(), re.M).group(1),
    description='cli - notsio note and bookmark command line utility',
    long_description = open('README').read(),
    author='Nico Di Rocco',
    author_email='dirocco.nico@gmail.com',
    url='http://nrocco.github.io',
    install_requires=[
        'pycli-tools>=2.0.2',
        'requests'
    ],
    packages = [
        'notsio'
    ],
    entry_points = {
        'console_scripts': [
            'notsio = notsio.__main__:main'
        ]
    },
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities'
    ],
)
