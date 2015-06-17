from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='flimfret',
      version='0.3',
      description='Pipeline for FLIM FRET analysis',
      url='http://github.com/casalex/flimfret',
      author='Alex Casella',
      author_email='alexmcasella@gmail.com',
      license='MIT',
      packages=['flimfret'],
      classifiers=['Development Status :: 3 - Alpha','Programming Language :: Python :: 2.7'],
      install_requires=['numpy'],
      zip_safe=False)