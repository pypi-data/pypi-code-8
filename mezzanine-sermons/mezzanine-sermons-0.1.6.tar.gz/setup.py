import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='mezzanine-sermons',
    version='0.1.6',
    packages=['mezzanine_sermons'],
    include_package_data=True,
    license='BSD License',
    description='A simple mezzanine app which facilitates the management and playing of sermons',
    long_description=README,
    url='https://github.com/philipsouthwell/mezzanine-sermons',
    author='Philip Southwell',
    author_email='phil@zoothink.com',
    keywords=['django', 'mezzanine'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

