from setuptools import setup, find_packages
import re

ld_md				= open('README.md').read()

try:
  import pandoc
  pandoc.core.PANDOC_PATH	= '/usr/bin/pandoc'

  ld_md				= re.sub("\(\*.*\*\)", "", ld_md, re.M)

  doc				= pandoc.Document()
  doc.markdown			= ld_md
  ld				= doc.rst
except:
  ld				= ld_md

setup(
  name='ebscopy',
  version='0.0.4.dev1',
  author='Jesse Jensen',
  author_email='jjensen@ebsco.com',
  url='https://github.com/jessejensen/ebscopy',
  license='GNUv3',
  packages=find_packages(),
  include_package_data=True,
  description='Official Python wrapper for the EBSCO Discovery Service (EDS) API',
  long_description=ld,
  install_requires=[
			'requests',
			'datetime',
			'logging',
			'nose',
  ],
  package_data = {
  },
)


