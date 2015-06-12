import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
version = '0.1.1'

requires = [ 'ujson' ]

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Customer Service',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Operating System :: POSIX',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
]

setup(
      name='baidupush',
      version=version,
      description='Python Client for Baidu Push APIs',
      long_description=open('README.rst', 'r').read(),
      author='Cherish Chen',
      author_email='sinchb128@gmail.com',
      maintainer='sinchb',
      maintainer_email='sinchb128@gmail.com',
      license='MIT',
      keywords=['push', 'baidu', 'android'],
      url='https://github.com/quatanium/python-baidu-push-server',
      zip_safe=False,
      packages=find_packages(exclude=['sample']),
      install_requires=requires,
      include_package_data=True,
     )


