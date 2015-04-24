# -*- coding: utf-8 -*-
"""
This module contains the tool of pretaweb.agls
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0.5'

long_description = '\n'.join([
    read('README.rst'),
    read('CHANGES.rst'),
    read('pretaweb', 'agls', 'README.rst'),
    read('CONTRIBUTORS.rst'),
])

tests_require = ['zope.testing', 'Products.PloneTestCase']

setup(name='pretaweb.agls',
      version=version,
      description="This package injects AGLS meta tags into Plone page.",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          'Framework :: Plone',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
      ],
      keywords='plone agls metadata',
      author='Dylan Jay',
      author_email='software@pretaweb.com',
      url='https://github.com/pretaweb/pretaweb.agls',
      download_url = 'https://github.com/pretaweb/pretaweb.agls/tarball/1.0.5',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pretaweb', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'plone.app.z3cform',
                        'collective.z3cform.keywordwidget',
                        'z3c.jbot'
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      test_suite='pretaweb.agls.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
