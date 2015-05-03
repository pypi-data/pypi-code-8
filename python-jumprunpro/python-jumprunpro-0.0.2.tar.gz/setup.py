from setuptools import setup
from os import path

BASE_PATH = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(BASE_PATH, 'README.rst'), 'r') as f:
	long_description = f.read()

setup(
	name='python-jumprunpro',
	version='0.0.2',
	author='Nate Mara',
	author_email='natemara@gmail.com',
	description='Simple python bindings for scraping data from JumpRun Pro',
	long_description=long_description,
	license='MIT',
	test_suite='tests',
	keywords='skydiving manifest',
	url='https://github.com/natemara/jumprunpro-python',
	packages=['jumprun'],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Topic :: Utilities',
		'License :: OSI Approved :: MIT License',
		'Intended Audience :: Developers',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
	],
	install_requires=[
		'beautifulsoup4==4.3.2',
		'requests==2.6.2',
		'python-dateutil==2.4.2',
	],
)
