# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='django-rmixins',
    version='0.0.1',
    author=u'Oscar M. Lage Guitian',
    author_email='info@oscarmlage.com',
    packages=find_packages(),
    include_package_data=True,
    url='http://bitbucket.org/r0sk/django-rmixins',
    license='BSD licence, see LICENSE file',
    description='Yet another django mixins compilation',
    zip_safe=False,
    long_description=open('README.rst').read(),
    keywords="django mixins",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
