"""
Copyright @ 2015 Atlassian Pty Ltd

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup
from setuptools.command.install import install
# To use a consistent encoding
from codecs import open
from os import path, system

here = path.abspath(path.dirname(__file__))


class OverloadInstall(install):
    def run(self):
        install.run(self)
        system('mandb')

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    cmdclass={'install': OverloadInstall},
    name='crowd_pam',
    # cmdclass = {'build_manpage': build_manpage}
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.1',

    description='A PAM module for authenticating with Atlassian Crowd',
    long_description=long_description,

    # The project's main homepage.
    url='https://bitbucket.org/sam_caldwell/pip-crowd-pam',

    # Author details
    author="""Sam Caldwell (Atlassian)
   Brendan Shaklovitz (Atlassian)
   Zach Boody (Atlassian)
   Cassonra Taylor (Atlassian)""",
    author_email='cst-dev@atlassian.com',

    # Choose your license
    license='Apache Software License',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration :: Authentication/Directory',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7'
    ],

    # What does your project relate to?
    keywords='atlassian crowd sso authentication pam',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['crowd_pam'],
    package_dir={'crowd_pam': 'module'},

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['requests', 'Crowd>=0.9.0,<0.9.1'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
    },
    scripts=['scripts/crowd_pam_configure.py'],

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    data_files=[
        ('/etc/pam.d/', ['data/etc/pam.d/common-account']),
        ('/etc/pam.d/', ['data/etc/pam.d/common-auth']),
        ('/etc/pam.d/', ['data/etc/pam.d/common-password']),
        ('/etc/pam.d/', ['data/etc/pam.d/common-session']),
        ('/etc/pam.d/', ['data/etc/pam.d/common-session-noninteractive']),
        ('/lib/security/', ['module/crowd_pam.py']),
        ('/usr/share/pam-configs/', ['data/usr/share/pam-configs/pam_config_python']),
        ('/usr/local/man/man8/', ['data/man/crowd_pam.8']),
        ('/etc/', ['data/etc/crowd_pam.conf'])


    ],
    package_data={'crowd_pam': ['data']},
)
