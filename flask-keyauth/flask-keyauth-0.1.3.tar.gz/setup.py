try:
    from setuptools import setup

except:
    from distutils.core import setup
import sys

setup(
    name='flask-keyauth',
    version='0.1.3',
    requires=['flask','pycrypto'],
    url='http://www.github.com/jsevilleja/flask-keyauth',
    include_package_data=True,
    license='MIT',
    author='Joel Sevilleja',
    author_email='joel@jsevilleja.org',
    description='A module to simplify working with KEY auth in Flask apps',
    packages = ["flask_keyauth"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
