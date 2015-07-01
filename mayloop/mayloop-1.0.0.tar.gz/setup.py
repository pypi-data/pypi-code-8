import ez_setup
ez_setup.use_setuptools()

import platform
from setuptools import setup, find_packages

from mayloop.version import __version__


entry_points = {}
#entry_points['console_scripts'] = ['wallp=wallp.main:main']

setup(	name='mayloop',
	version=__version__,
	description='An asynchronous i/o library.',
	author='Amol Umrale',
	author_email='babaiscool@gmail.com',
	url='http://pypi.python.org/pypi/mayloop/',
	packages=find_packages(),
	entry_points=entry_points,
	install_requires=['zope.interface', 'mutils'],
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Operating System :: POSIX :: Linux',
		'Operating System :: Microsoft :: Windows',
		'Programming Language :: Python :: 2.7'
	]
)

