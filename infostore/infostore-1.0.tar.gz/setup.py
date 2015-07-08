from setuptools import setup

def README():
	with open('README.rst', 'r') as f:
		return f.read()

setup(
	name = 'infostore',
	version = '1.0',
	description = 'Various types of data storage in python',
	long_description = README(),
	classifiers = [
		'Development Status :: 5 - Production/Stable',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 2.7',
		'Intended Audience :: Developers',
	],
	url = 'encry.cpnerd.koding.io/infostore.py',
	author = 'CPNerd',
	author_email = 'shadow889566@gmail.com',
	license = 'MIT',
	packages = ['infostore'],
	install_requires = ['cpfile'],
	zip_safe = False
	)