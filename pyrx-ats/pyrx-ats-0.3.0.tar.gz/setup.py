from setuptools import setup

readme = open('readme.md').read()
setup(name='pyrx-ats',
      version='0.3.0',
      #author='Philip Schleihauf, ATS Advanced Telematic Systems',
      license='GPLv2',
      description='Rx schema and validation system, with added error messages',
      long_description=readme,
      url='https://github.com/advancedtelematic/pyrx',
      py_modules=['pyrx'])
