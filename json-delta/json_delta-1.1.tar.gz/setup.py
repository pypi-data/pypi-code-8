#!/usr/bin/env python

from setuptools import setup

with open('README') as f:
    LONG_DESC = f.read()

setup(
    name="json_delta",

    version="1.1",

    description="A diff/patch pair for JSON-serialized data structures.",
    long_description=LONG_DESC,
    url="http://json-delta.readthedocs.org/",

    author="Phil Roberts",
    author_email="himself@phil-roberts.name",

    license="BSD",

    classifiers=[
        'Development Status :: 4 - Beta',
        
        'Intended Audience :: Developers',

        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    package_dir={'': 'src'},
    packages=['json_delta'],

    scripts=['src/json_cat', 'src/json_diff', 'src/json_patch']
)
