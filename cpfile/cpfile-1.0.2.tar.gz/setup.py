from setuptools import setup

def readme():
	with open('README.rst', 'r') as f:
		return f.read()

setup(name='cpfile',
      version='1.0.2',
      description='A python module ment to make working with files much easier',
      long_description=readme(),
      url='encry.cpnerd.koding.io/cpfile.py',
      scritps=['/cpfile/cpfile.py'],
      author='CPNerd',
      classifiers=[
      	'Development Status :: 5 - Production/Stable',
      	'Intended Audience :: Developers',
      	],
      author_email='shadow889566@gmail.com',
      license='MIT',
      packages=['cpfile'],
      zip_safe=False)