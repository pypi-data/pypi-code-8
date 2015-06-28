# Probsim setup
# (TSK, 2015-06-28)

from sys import version
if version < '2.2.3':
	from distutils.dist import DistributionMetadata
	DistributionMetadata.classifiers = None
	DistributionMetadata.download_url = None
	
from distutils.core import setup

setup(
	name='eventsim',
	version='0.4.3',
	description='various useful tools in simulating discrete system events based on outcome and probabilities',
	long_description = open('README').read(),
	author='Taiwo Kareem',
	author_email='taiwo.kareem36@gmail.com',
	url='http://bitbucket.org/tushortz/eventsim',
	packages=['eventsim'],
	package_data={'eventsim': ['*.txt', 'eventsim/*.txt']},
	platforms='any',
	license='MIT',
	classifiers=[
		'Intended Audience :: Developers',
		'Intended Audience :: Education', 
		'Intended Audience :: Financial and Insurance Industry',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3.4',
		'Topic :: Software Development :: Libraries :: Python Modules',
	],
)

