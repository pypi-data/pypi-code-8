#!/usr/bin/env python3

from setuptools import setup

setup(name="gitignore-fetcher",
      version="1.0.0",
      description="Fetch the .gitignore defined by GitHub for a given language",
      author="Andrew Lorente",
      author_email="hello@andrewlorente.com",
      url="https://git.andrewlorente.com/AndrewLorente/gitignore-fetcher",
      packages=[],
      scripts=['gitignore'],
      install_requires=[
          "requests>=0.10.1",
      ],
      )
