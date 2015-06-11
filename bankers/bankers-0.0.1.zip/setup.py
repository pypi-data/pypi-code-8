#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup

setup(name="bankers",
      version="0.0.1",
      description="Bankers - This is an implementation of the banker's deadlock algorithm",
      author="Max Klingmann <KlingmannM@gmail.com>",
      author_email="KlingmannM@gmail.com",
      packages=['bankers'],
      license="GPLv3",
      url="https://github.com/mkli90/Bankers",
      package_data={
          'tmz': ['LICENSE']
      },
      classifiers=[
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Natural Language :: English",
          "Programming Language :: Python :: 3.4",
          "Topic :: Software Development :: Libraries",
      ],
)
