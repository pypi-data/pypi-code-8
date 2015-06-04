# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='django-rgallery',
    version='1.8.0',  # New branch adapted to Django 1.8
    author=u'Oscar M. Lage Guitian',
    author_email='info@oscarmlage.com',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['rgallery/templates',
                       'rgallery/static',
                       'rgallery/management']},
    url='http://bitbucket.org/r0sk/django-rgallery',
    license='BSD licence, see LICENSE file',
    description='Yet another Django Gallery App',
    zip_safe=False,
    long_description=open('README.rst').read(),
    install_requires=[
        "Django < 1.9",
        "Pillow",
        "exifread",
        "django-braces",
        "django-rmixins",
        "sorl-thumbnail == 11.12.1b",  # this version fixes the problem
                                       # importing simplejson from django
        "django_compressor",
        "dropbox",
        "django-taggit",
        "BeautifulSoup",
    ],
    keywords="django application gallery",
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
