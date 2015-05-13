from setuptools import setup

def readme():
	with open('README.rst', 'r') as f:
		return f.read()

setup(name='Encry',
      version='1.0.2.Beta',
      description='A simple encryption module',
      long_description=readme(),
      scripts=['bin/Encry'],
      url='encry.cpnerd.koding.io/Encry.py',
      author='CPNerd',
      author_email='shadow889566@gmail.com',
      license='MIT',
      packages=['Encry'],
      zip_safe=False)