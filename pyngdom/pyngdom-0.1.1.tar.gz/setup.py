
import os
from distutils.core import setup

from pyngdom import __version__

f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
long_description = f.read()
f.close()

setup(
    name='pyngdom',
    version=__version__,
    packages=['pyngdom'],
    author='Alvaro Leiva',
    author_email='aleivag@gmail.com',
    url='https://github.com/Epi10/pyngdom',
    download_url='https://github.com/Epi10/pyngdom/releases/tag/%s' % __version__,
    classifiers=[
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Topic :: System :: Monitoring"
    ],
    keywords=['monitoring', 'rum', 'pingdom'],
    description='A simple pingdom API interface for read RUM information',
    long_description=long_description,
    license='MIT'
)
