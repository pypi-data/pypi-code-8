from setuptools import setup, find_packages
import sys, os

version = '0.2b'

setup(name='crackqcli',
      packages=['crackqcli'],
      download_url = 'https://github.com/vnik5287/Crackq/tarball/0.2b',
      version=version,
      description="Hashcrack Crackq command-line client",
      long_description="""\
Hashcrack Crackq command-line client for submitting hashes to the Crackq. Supported hash formats: NTLM, MD5, SHA1, WPA/WPA2, IPSec IKE MD5, DESCRYPT, MD5CCRYPT""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='hashcrack crackq password bruteforce hash NTLM MD5 SHAA1 WPA WPA2 DESCRYPT MD5CRYPT',
      author='Hashcrack',
      author_email='support@hashcrack.org',
      scripts=['crackqcli/crackqcli.py'],
      url='http://hashcrack.org',
      license='GPLv3',
      include_package_data=False,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
