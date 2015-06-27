""" Setup for django-future-staticfiles """

from setuptools import setup, find_packages

from django_future_staticfiles import __version__


setup(
    name="django-future-staticfiles",
    version=__version__,
    description="Backport of Django staticfiles storages from Django 1.7+ to "
                "earlier Django 1.6",
    long_description=open("README.rst", 'rb').read().decode('utf-8'),
    license="MIT",
    author="David Sanders",
    author_email="dsanders11@ucsbalum.com",
    url="https://github.com/dsanders11/django-future-staticfiles/",
    keywords="django staticfiles future",
    packages=find_packages(exclude=("tests", "test_project")),
    install_requires=[
        "Django >= 1.6"
    ],
    test_suite="runtests.run_tests",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Utilities",
    ]
)
