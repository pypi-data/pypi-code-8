#!/usr/bin/env python
from ez_setup import use_setuptools
use_setuptools("0.7.0")

from setuptools import setup, find_packages

setup(
    name="travis-tox",
    version='0.1.0',
    author="Thomas Grainger",
    author_email="travis-tox@graingert.co.uk",
    maintainer="Thomas Grainger",
    maintainer_email = "travis-tox@graingert.co.uk",
    keywords = "travis, tox",
    description = "Generate your travis config from tox",
    url="https://github.com/graingert/travis-tox",
    package_dir={'': 'src'},
    packages=find_packages('src', exclude="tests"),
    zip_safe=True,
    include_package_data=False,
)
