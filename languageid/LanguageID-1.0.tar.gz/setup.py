from setuptools import setup, find_packages
import sys, os

version = '1.0'

setup(name='LanguageID',
      version=version,
      author='Amish Goyal',
      author_email='amish1804@gmail.com',
      packages=find_packages(),
      scripts=['app.py'],
)