from setuptools import setup
import sys

install_requires = []
if sys.version_info < (3, 4):
    install_requires.append('pathlib')
tests_require = ['pytest']

setup(
    version='0.0.0',
    description='A toolset for working with HFSS files',
    long_description=(open('README.md').read()),
    url='http://git.arrc.ou.edu/pier3595/hfss-lib',
    name='hfsslib',
    author='Cody Piersall',
    author_email='codypi@ou.edu',
    classifiers=[
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    packages=['hfsslib'],
    install_requires=install_requires,
    tests_require=tests_require,
)
