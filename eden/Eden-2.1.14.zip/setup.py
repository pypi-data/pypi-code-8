import os

from setuptools import setup

def read (*paths):
	with open (os.path.join (*paths), 'r') as aFile:
		return aFile.read()

setup (
	name = 'Eden',
	version = '2.1.14',
	description = 'Eden - Event Driven Evaluation Nodes, tested with Kivy 1.9.0',
	long_description = (
		read ('README.rst') + '\n\n' +
		read ('qQuickLicence.txt')
	),
	keywords = ['eden', 'kivy', 'winforms', 'observer', 'functional'],
	url = 'http://www.qquick.org',
	license = 'qQuickLicence',
	author = 'Jacques de Hooge',
	author_email = 'jacques.de.hooge@qquick.org',
	packages = ['eden'],	
	include_package_data = True,
	install_requires = ['Kivy == 1.9.0'],
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: Other/Proprietary License',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2.7',
	],
)
