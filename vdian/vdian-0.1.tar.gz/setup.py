# encoding=utf-8
# !/usr/bin/env python

from setuptools import setup, find_packages
from vdian import VERSION

url = "https://coding.net/u/jeff/p/vdian/git"

long_description = u"微店 python SDK"

setup(
    name="vdian",
    version=VERSION,
    description=long_description,
    maintainer="jeff kit",
    maintainer_email="bbmyth@gmail.com",
    url=url,
    long_description=long_description,
    install_requires=['requests', ],
    packages=find_packages('.'),
)
