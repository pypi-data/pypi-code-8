import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "sorbcrawler",
    version = "1.01",
    author = "sid-eload",
    author_email = "sideload3695@gmail.com",
    description = ("Crawls through sorb forum threads, and returns the top 10 posters and their post count"),
    license = "N/A",
    keywords = "sorb thread count post",
    url = "https://github.com/sid-eload/sorb-crawler",
    packages=['sorbcrawler'],
    install_requires=[
          'requests',
          'beautifulsoup4',
      ],
    scripts=['bin/sorbcrawler'],
    long_description=read('README.md'),
    zip_safe=False
)