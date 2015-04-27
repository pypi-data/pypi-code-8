import os
from setuptools import setup, find_packages

VERSION = '0.2.1'

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-geohashing',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django', 'requests', 'djangorestframework'],
    license='MIT License',
    description='Django app for working with XKCD geohashing data',
    long_description=README,
    author='Chuck Bassett',
    author_email='iamchuckb@gmail.com',
    keywords='geohashing xkcd django',
    classifiers=[
	'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
