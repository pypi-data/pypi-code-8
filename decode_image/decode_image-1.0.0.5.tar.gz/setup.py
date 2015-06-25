#!/usr/bin/env python
import decode_image
""" decode_image installation script """

VERSION = decode_image.__VERSION__
TEST	= decode_image.__TEST__

try:
	from setuptools import setup, find_packages
except:
	from distutils.core import setup

setup(
		name			= 'decode_image',
		version			= '{0}.{1}'.format(VERSION, TEST),
		description 	= 'Simple Command line and module for Decode/Encode Image File',
		license 		= 'MIT',
		author			= 'Laode Hadi Cahyadi',
		author_email	= 'licface@yahoo.com',
		url				= 'https://codecumulus13.wordpress.com',
        platforms       = ['any'],
		download_url    = 'https://github.com/cumulus13/decode_image/archive/v{0}(t{1}).tar.gz'.format(VERSION, TEST),
		keywords 		= ['decode', 'encode', 'cli', 'command line'],
		packages		= ['decode_image'],
		scripts			= ['decode_image.py'],
		entry_points    = {'console_scripts': [
          'decode_image = decode_image.decode_image:main',
    	]},
		zip_safe        = False,
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


