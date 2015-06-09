# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name = "wp-version-checker",
    version = "0.1.1",
    packages = find_packages(),
    scripts = ['wp_version_checker.py'],
    author = "Dundee",
    author_email = "daniel@milde.cz",
    description = "Wordpress version checker",
    license = "GPL",
    keywords = "wordpress",
    url = "https://github.com/Dundee/wp-version-checker",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
    ]
)
