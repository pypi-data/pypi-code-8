#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup, find_packages

setup(name='LabtoolSuite',
	version='0.1.3',
	description='Package to deal with LabToolSuite',
	author='Jithin B.P.',
	author_email='jithinbp@gmail.com',
	url='https://www.jithinbp.in/',
	install_requires = ['numpy>=1.8.2','scipy>=0.13.3','pyqtgraph>=0.9.10'],
	packages=find_packages(),#['Labtools', 'Labtools.widgets'],
	scripts=["Labtools/bin/oscilloscope","Labtools/bin/Stream"]
	)
