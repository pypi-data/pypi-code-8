"""
PIP setup script for the Pythia Charm library.
"""
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

description=\
  """
  Enables both client-side and server-side password hardening using a 
  remote cryptographic server that provides an unpdateable, verifiable, 
  and secure psuedorandom function (PRF) service.

  NOTE: Pythia requires the Charm Crypto library for Python 
  http://www.charm-crypto.com/Download.html but there isn't a PIP
  package yet in existence.
  """
description = ' '.join(description.split())

setup(name='pythiacrypto',
      version='1.0',
      description=description,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Unix',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Topic :: Security',
          'Topic :: Security :: Cryptography',
      ],
      url='https://pages.cs.wisc.edu/~ace/projects/pythia.html',
      author='Adam Everspaugh',
      author_email='ace@cs.wisc.edu',
      license='MIT',
      packages=['pythiacrypto'],
      zip_safe=False)
