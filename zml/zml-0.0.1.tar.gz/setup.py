from distutils.core import setup
setup(
    name = "zml",
    packages = ["zml"],
    version = "0.0.1",
    description = "zero markup language",
    author = "Christof Hagedorn",
    author_email = "team@zml.org",
    url = "http://www.zml.org/",
    download_url = "http://www.doonx.org/download/zml-0.0.1.gz",
    keywords = ["zml", "zero", "markup", "language", "template", "templating"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.2",
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description = """\
zml - zero markup language
-------------------------------------

Features
 - zero markup templates
 - lean code
 - clean syntax
 - extensible
 - namespaces

This version requires Python 3 or later.
"""
)
