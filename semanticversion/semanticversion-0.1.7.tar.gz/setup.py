# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import semanticversion

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print(
        "warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

with open('LICENSE') as f:
    license = f.read()


setup(
    name='semanticversion',
    version=semanticversion.__version__,
    description='Version generator tool. Semver, markdown json woohoo!',
    long_description=read_md('README.md'),
    #long_description=readme,
    author='oskarnyqvist',
    author_email='oskarnyqvist@gmail.com',
    url='https://github.com/oskarnyqvist/semanticversion',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    scripts=['bin/semanticversion'],

)
