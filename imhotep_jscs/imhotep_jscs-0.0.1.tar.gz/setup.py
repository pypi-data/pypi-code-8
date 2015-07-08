import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='imhotep_jscs',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/justinabrahms/imhotep_jscs',
    license='MIT',
    install_requires=['imhotep>=0.4.0'],
    tests_require=['mock', 'pytest'],
    author='Justin Abrahms',
    author_email='justin@abrah.ms',
    description='An imhotep plugin for jscs validation',
    entry_points={
        'imhotep_linters': [
            '.js = imhotep_jscs.plugin:JSCS'
        ],
    },
    cmdclass={'test': PyTest},
)
