#!/usr/bin/env python

from setuptools import setup

setup(name="trust",
      version="1.0.0",
      description="A hierarchical database engine with read-only access to "
                  "data, ideally used for cross-application settings and "
                  "infrastructure description.",
      long_description=open("README.markdown").read(),
      author="Arseni Mourzenko",
      author_email="arseni.mourzenko@pelicandd.com",
      url="http://go.pelicandd.com/n/python-trust",
      license="MIT",
      keywords="database json settings",
      install_requires=[
          "markdown==2.6.1",
          "passlib==1.6.2"
      ])
