# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='django-rblog',
    version='1.8.0',  # New branch adapted to Django 1.8
    author=u'Oscar M. Lage Guitian',
    author_email='r0sk10@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='http://bitbucket.org/r0sk/django-rblog',
    license='BSD licence, see LICENSE file',
    description='Yet another Django Blog App',
    zip_safe=False,
    long_description=open('README.rst').read(),
    install_requires=[
        "Django < 1.9",
        "Pygments",
        "BeautifulSoup",
        "Pillow",
        "django-braces",
        "django-rmixins",
        "django-tinymce",
        "django-filebrowser-no-grappelli",
        "django-taggit",
        "django_compressor",
        "sorl-thumbnail == 11.12.1b",  # this version fixes the problem
                                       # importing simplejson from django
        "elementtree==1.2.7-20070827-preview",
        "disqus-python",
        "django-disqus",
    ],
    keywords="django application blog",
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
