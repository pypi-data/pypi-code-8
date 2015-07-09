#!/usr/bin/env python

import os
import versioneer
from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup


def get_requirements(filename):
    if not os.path.exists(filename):
        return []

    install_reqs = parse_requirements(filename, session=PipSession())
    return [str(ir.req) for ir in install_reqs]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]
    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(name='django-mgsub',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='Subscribe Mailgun mailing lists from Django',
      long_description=README,
      author='Ferrix Hovi',
      author_email='ferrix@codetry.fi',
      install_requires=get_requirements('requirements.txt'),
      tests_require=get_requirements('development.txt'),
      packages=['mgsub'],
      package_data=get_package_data('mgsub'),
      include_package_data=True,
      zip_safe=False,
      url='https://github.com/codetry/mgsub/',
      license='MIT License',
      classifiers=[
          'Environment :: Web Environment',
          'Framework :: Django',
          'Framework :: Django :: 1.8',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'License :: OSI Approved :: MIT License',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ],
      )
