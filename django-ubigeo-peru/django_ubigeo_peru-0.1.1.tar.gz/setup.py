# -*- coding: utf-8 -*-

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django_ubigeo_peru',
    version='0.1.1',
    license='GPL v.3',
    description='Django app para aplicaciones que requieran usar los ubigeos del Perú.',
    long_description=read('README.md'),
    author='Miguel Angel Cumpa Asuña',
    author_email='themiseck.rock@gmail.com',
    url = 'https://bitbucket.org/micky_miseck/django-ubigeo-peru',
    download_url = 'https://bitbucket.org/micky_miseck/django-ubigeo-peru/get/master.tar.gz',
    keywords = ['ubigeo', 'peru',],
    packages = ['ubigeo'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    include_package_data=True,
    zip_safe=False,
)
