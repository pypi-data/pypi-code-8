#!/usr/bin/env python

""" keyserver installation script """
import keyserver

VERSION = keyserver.__VERSION__
TEST    = keyserver.__TEST__

try:
	from setuptools import setup
except:
	from distutils.core import setup

setup(
		name			= 'keyserver',
		version			= '{0}.{1}'.format(VERSION, TEST),
		description 	= 'Command line Pub key generator from keyserver.ubuntu.com',
		license 		= 'MIT',
        platforms       = ['any'],
		author			= 'Laode Hadi Cahyadi',
		author_email	= 'licface@yahoo.com',
		url				= 'https://codecumulus13.wordpress.com',
		download_url    = 'https://github.com/cumulus13/keyserver/archive/v{0}(t{1}).tar.gz'.format(VERSION, TEST),
		keywords 		= ['keyserver', 'cli', 'command line'],
		packages		= ['keyserver'],
		scripts			= ['keyserver.py'],
		entry_points    = {'console_scripts': [
             'keyserver = keyserver.generator:main',
    	]},
		classifiers 	= [
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Topic :: Text Processing :: General',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Software Distribution',
            'Topic :: Utilities',
            'Operating System :: OS Independent',
      ]
)


