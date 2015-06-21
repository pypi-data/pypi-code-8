#!/usr/bin/env python3

import distutils.core

# Uploading to PyPI
# =================
# The first time only:
# $ python setup.py register -r pypi
#
# Every version bump:
# $ git tag <version>; git push
# $ python setup.py sdist upload -r pypi

version = '1.1'
distutils.core.setup(
        name='wet_copy',
        version=version,
        author='Kale Kundert',
        author_email='kale@thekunderts.net',
        url='https://github.com/kalekundert/wet_copy',
        download_url='https://github.com/kalekundert/wet_copy/tarball/'+version,
        license='GPLv3',
        description="Format and print wetlab protocols stored as text files in git repositories.",
        long_description=open('README.rst').read(),
        keywords=['print', 'scientific', 'protocols'],
        py_modules=['wet_copy'],
        install_requires=[
            'docopt==0.6.2',
        ],
        entry_points = {
            'console_scripts': ['wet_copy=wet_copy:main'],
        },

)
