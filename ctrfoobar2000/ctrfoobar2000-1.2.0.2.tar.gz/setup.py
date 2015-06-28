#!/usr/bin/env python
import ctrfoobar2000
""" ctrfoobar2000 installation script """

VERSION = ctrfoobar2000.__version__
TEST	= ctrfoobar2000.__test__

try:
	from setuptools import setup, Extension
except:
	from distutils.core import setup, Extension

setup(
		name					= 'ctrfoobar2000',
		version					= '{0}.{1}'.format(VERSION, TEST),
		description 			= 'Control Foobar2000 with python + Command line',
		license 				= 'MIT',
		author					= 'Laode Hadi Cahyadi',
		author_email			= 'licface@yahoo.com',
		url						= 'https://codecumulus13.wordpress.com',
        platforms       		= ['Platform Independent'],
		download_url    		= 'https://github.com/cumulus13/ctrfoobar2000/archive/v{0}(t{1}).tar.gz'.format(VERSION, TEST),
		keywords 				= ['foobar2000', 'foobar', 'com', 'http', 'cli', 'command line'],
		packages				= ['ctrfoobar2000'],
		# package_dir             = {'ctrfoobar2000': 'ctrfoobar2000'},
		package_data   			= {'ctrfoobar2000': ['pyfoobar.ini']},
		# data_files              = [('ctrfoobar2000', ['ctrfoobar2000/pyfoobar.ini'])],
		# ext_modules             = [Extension('ctrfoobar2000', ['pyfoobar.ini'])],
		# include_package_data 	= True,
		scripts					= ['foobar.py'],
		entry_points    		= {'console_scripts': [
                'foobar 		= ctrfoobar2000.foobar:main',
    	]},
    	# install_requires 		= [
					# 		        "requests",
					# 		        "bcrypt",
					# 		      ],
		zip_safe        		= False,
		classifiers 			= [
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


