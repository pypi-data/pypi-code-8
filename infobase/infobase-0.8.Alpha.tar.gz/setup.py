from setuptools import setup

def README():
	with open('README.rst', 'r') as f:
		return f.read()

setup(
	name = 'infobase',
	version = '0.8.Alpha',
	description = 'A Minimalistic Database System in Python',
	long_description = README(),
	classifiers = [
		'Development Status :: 3 - Alpha',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 2.7',
		'Intended Audience :: Developers',
	],
	url = 'encry.cpnerd.koding.io/infobase.py',
	author = 'CPNerd',
	author_email = 'shadow889566@gmail.com',
	license = 'MIT',
	packages = ['infobase'],
	install_requires = ['cpfile'],
	zip_safe = False
	)