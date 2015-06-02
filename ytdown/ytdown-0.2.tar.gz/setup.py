#!/usr/bin/python
from setuptools import setup

setup(
		name='ytdown',
		version='0.2',
		description='Download videos and audios from YouTube',
		author = 'Sharat',
		author_email = 'cr.sharat@gmail.com',
		license = 'Free',
		packages=['ytdown'],
		install_requires=['pafy'],
		
		zip_safe=False
	)