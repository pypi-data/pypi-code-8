from distutils.core import setup
setup(
    name = "valection",
    packages = ["valection"],
    version = "0.1.1",
    description = "Sampler for validation",
    author = "Chris Cooper",
    author_email = "chris.cooper@oicr.on.ca",
    url = "http://oicr.on.ca/",
    # download_url = "http://chardet.feedparser.org/download/python3-chardet-1.0.1.tgz",
    keywords = ["validation", "selection", "sampling"],
    classifiers = [
         "Programming Language :: Python",
         "Programming Language :: Python :: 3",
         "Intended Audience :: Science/Research",
         "License :: OSI Approved :: GNU General Public License (GPL)",
         ],
    long_description = """\
Valection - Sampler for validation (version 0.1.1)
--------------------------------------------------

Valection can be used in various ways to sample the outputs of competing algorithims or
parameterizations, and fairly assess their performance against each other.

The sampling will be distributed over the calls common to all, many, few, and single callers.

This version has been tested with Python 3.4.1, 3.3.0, and 2.7.6.

"""
)
