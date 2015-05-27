from setuptools import setup, find_packages

PACKAGE = "excel2sql"
NAME = "excel2sql"
DESCRIPTION = "convert *.excel to *.sql file"
AUTHOR = "orange.lihai"
AUTHOR_EMAIL = "orange.lihai@gmail.com"
URL = ""
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    # long_description=read("README.rst"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=find_packages(exclude=["tests.*", "tests"]),
    # package_data=find_package_data(PACKAGE, only_in_packages=False),
    classifiers=[
        "Development Status :: 3 - Alpha",
        # "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        # "Operating System :: OS Independent",
        "Programming Language :: Python",
        # "Framework :: Django",
    ],
    zip_safe=False,
)