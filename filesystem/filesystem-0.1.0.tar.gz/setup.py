# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import filesystem

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    read_md = lambda f: open(f, 'r').read()

with open('LICENSE') as f:
    license = f.read()

requirements = []
#with open("requirements.txt") as f:
#    requirements = [x.split("=")[0].strip() for x in f.readlines()]

setup(
    name='filesystem',
    version=filesystem.__version__,
    description='Deterministic password generator',
    long_description=read_md('README.md'),
    #long_description=readme,
    author='oskarnyqvist',
    author_email='oskarnyqvist@gmail.com',
    url='https://github.com/nopassword/nopassword.py',
    license=license,
    packages=["filesystem"],
    )
