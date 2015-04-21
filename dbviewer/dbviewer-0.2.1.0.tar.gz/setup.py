#! /usr/bin/python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
		name = "dbviewer",
		version = "0.2.1.0",
		author = 'seabass808',
		author_email='jyathux23@yahoo.co.jp',
		license='BSD',
		url = " https://github.com/seabass808",
		description = ' SQLite database editor/viewer',
		packages = find_packages(),
		package_data={'src' : ['icons / *.png']},
		install_requires = open('requirements.txt').read().splitlines(),
		classifiers = [
					'Programming Language :: Python',
					'Programming Language :: Python :: 2',
					'Programming Language :: Python :: 2.7',
					'Topic :: Database',
					'License :: OSI Approved :: BSD License',
					'Operating System :: Unix',
					'Operating System :: POSIX',
					],
		entry_points="""
					[console_scripts]
					dbvw=src.controlpanel:main
					""",)













