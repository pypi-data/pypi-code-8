from setuptools import setup

def readme():
	with open('README.rst', 'r') as f:
		return f.read()

setup(name='Encry',
      version='1.3.1.1',
      description='A simple encryption module meant for running in the command line, and from python',
      long_description=readme(),
      scripts=['Encry/Encry.py', 'Encry/encry/settings.py', 'Encry/encry/config.py'],
      url='encry.cpnerd.koding.io/Encry.py',
      author='CPNerd',
      classifiers=[
      	'Development Status :: 5 - Production/Stable',
      	'Intended Audience :: Developers',
      	'Intended Audience :: End Users/Desktop',
      	],
      author_email='shadow889566@gmail.com',
      license='MIT',
      packages=['Encry'],
      zip_safe=False)