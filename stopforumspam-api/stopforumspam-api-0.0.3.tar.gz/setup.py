from setuptools import setup, find_packages
import os

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Internet :: WWW/HTTP :: Site Management'
]

packages = find_packages()

setup(name="stopforumspam-api",
      description="Basic interface for Stop Forum Spam API",
      long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
      author="Stephen Paulger",
      author_email="stephen.paulger@newspeak.org.uk",
      version="0.0.3",
      packages=packages,
      classifiers=CLASSIFIERS,
      include_package_data=True
)
