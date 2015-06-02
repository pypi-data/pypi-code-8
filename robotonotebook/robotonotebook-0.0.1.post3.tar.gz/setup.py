# Thanks, Stephen https://groups.google.com/d/msg/mezzanine-users/bdqjepkhtzc/dG0xl9qx4kEJ
# and Hynek https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
import os

from setuptools import setup, find_packages
from robotonotebook import __version__ as version

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='robotonotebook',
    version=version,
    description='A Mezzanine CMS theme intended for publishing a personal blog with a minimalist design typeset with the Roboto typeface.',
    long_description=(read('README.md') + '\n\n' +
                      read('AUTHORS.md') + '\n\n' +
                      read('HISTORY.md')),
    url='https://github.com/hypertexthero/mezzanine-robotonotebook/',
    license='MIT',
    author = 'Simon Griffee',
    author_email = 'simongriffee@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['Mezzanine'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)