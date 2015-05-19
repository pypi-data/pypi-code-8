import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "commonwealth",
    version = "0.0.0",
    author = "James Brewer",
    author_email = "james@jamesbrewer.io",
    description = "Community as a Platform",
    license = "MIT",
    keywords = "community platform",
    url = "https://github.com/brwr/Commonwealth",
    packages=['commonwealth', 'tests'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: Django :: 1.8",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Topic :: Education",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
)