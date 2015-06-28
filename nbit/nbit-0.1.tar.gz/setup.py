'''
NBit: Build tool for node.js projects

Note that "python setup.py test" invokes pytest on the package. With appropriately
configured setup.cfg, this will check both xxx_test modules and docstrings.

Copyright 2015, Valeria Lepina.
Licensed under MIT.
'''
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


version = "0.1"

setup(name="nbit",
      version=version,
      description="Build tool for node.js projects",
      long_description=open("README.md").read(),
      classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python'
      ],
      keywords="node nodejs js node.js build bootstrap-project google-closure-compiler",
      author="Valeria Lepina",
      author_email="divergence082@gmail.com",
      url="https://github.com/divergence082/NBit",
      license="MIT",
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=False,
      tests_require=['pytest'],
      cmdclass={
          'test': PyTest
      },
      install_requires=[],
      entry_points={
        'console_scripts': ['nbit=nbit.nbit:main']
      }
)
