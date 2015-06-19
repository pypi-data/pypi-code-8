# Basic Setup Script
# Requires Python3

# Written by Joseph Jeffers
# Updated Feb 15 2015

from setuptools import setup, find_packages

setup(name='GeneWordSearch',
version='1.9',
license='GPLv2',
description='Annotation finder for genes.',
author='Joe Jeffers',
author_email='jeffe174@umn.edu',
url='https://github.com/monprin/geneWordSearch/',
packages=find_packages(),
package_data={
'databases':['*/totalWordCounts.*','*/geneNotes.*'],
'webapp':['templates/home.html','static/formProcess.js']},
long_description=open('README.rst').read(),
scripts=['bin/gws'],
install_requires=['flask','numpy','scipy'])
