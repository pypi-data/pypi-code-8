import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='great-sitemap-search',
    version='0.2',
    install_requires = [
        'Django',
        'Whoosh',
        'beautifulsoup4',
        'lxml',
    ],
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A really simple search backend for your site based on a crawler that scanns all pages in sitemap.xml',
    long_description=README,
    url='http://www.webkrafts.net/',
    author='Michael Schmidt',
    author_email='ms@webkrafts.net',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
