import labbook, sys, os, os.path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


me = 'Harsha Krishnareddy'
memail = 'c0mpiler@outlook.com'
url = 'http://pypi.python.org/pypi/labbook'

setup (
    name='labbook',
    version=labbook.VERSION,
    zip_safe=True,
    description='Python package to work with labbook',
    long_description=open('README.md','r').read(),
    author=me,
    author_email=memail,
    maintainer=me,
    maintainer_email=memail,
    url=url,
    license='BSD',
    keywords=['template','labbook', 'empty', 'package', 'example'],
    packages=['labbook'],
    download_url=url,
    platforms=['Independant'],
    classifiers = [
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    test_suite='nose.collector',
    tests_require=['nose'],
    )
