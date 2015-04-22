#!/usr/bin/env python

from __future__ import with_statement
import sys
import os
import imp
from setuptools import setup, find_packages


def get_version():
    " Get version & version_info without importing markdown.__init__ "
    path = os.path.join(os.path.dirname(__file__), 'markdown')
    fp, pathname, desc = imp.find_module('__version__', [path])
    try:
        v = imp.load_module('__version__', fp, pathname, desc)
        return v.version, v.version_info
    finally:
        fp.close()

version, version_info = get_version()


install_requirements = []

# sdist
if not 'bdist_wheel' in sys.argv:
    try:
        import importlib
    except ImportError:
        install_requirements.append('importlib>=1.0.3')

# bdist_wheel
extras_require = {
    # http://wheel.readthedocs.org/en/latest/#defining-conditional-dependencies
    ':python_version=="2.6"': ['importlib>=1.0.3'],
}


long_description = \
'''This is a Python implementation of John Gruber's Markdown_.
It is almost completely compliant with the reference implementation,
though there are a few known issues. See Features_ for information
on what exactly is supported and what is not. Additional features are
supported by the `Available Extensions`_.

Please note that this is the Python 2.6 support branch, the official package
is hosted at https://pythonhosted.org/Markdown/

.. _Markdown: http://daringfireball.net/projects/markdown/
.. _Features: https://pythonhosted.org/Markdown/index.html#Features
.. _`Available Extensions`: https://pythonhosted.org/Markdown/extensions/index.html

Support
=======

You may ask for help and discuss various other issues on the
`mailing list`_ and report bugs on the `bug tracker`_.

.. _`mailing list`: http://lists.sourceforge.net/lists/listinfo/python-markdown-discuss
.. _`bug tracker`: http://github.com/waylan/Python-Markdown/issues
'''


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    print('You probably want to also tag the version now:')
    print('  git tag -a %s -m "version %s"' % (version, version))
    print('  git push --tags')
    sys.exit()


setup(
    name='markdown-py26-support',
    version=version,
    url='https://pythonhosted.org/Markdown/',
    description='Python implementation of Markdown.',
    long_description=long_description,
    author='Manfred Stienstra, Yuri takhteyev and Waylan limberg',
    author_email='waylan.limberg [at] icloud.com',
    maintainer='Christopher Grebs',
    maintainer_email='cg@webshox.org',
    license='BSD License',
    packages=['markdown', 'markdown.extensions'],
    install_requires=install_requirements,
    extras_require=extras_require,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Communications :: Email :: Filters',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML'
    ]
)
