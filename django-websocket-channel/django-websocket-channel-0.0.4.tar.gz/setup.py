import os
from setuptools import setup, find_packages
from websocket_channel import __version__

DESCRIPTION = 'Websocket support for Django using Redis'

CLASSIFIERS = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Programming Language :: Python :: 2.7',
]


def read(fname):
    readme_file = os.path.join(os.path.dirname(__file__), fname)
    return os.popen('[ -x "$(which pandoc 2>/dev/null)" ] && pandoc -t rst {0} || cat {0}'.format(readme_file)).read()
setup(
    name='django-websocket-channel',
    version=__version__,
    author='Neo hu',
    author_email='9656951@qq.com',
    description=DESCRIPTION,
    long_description=read('README.md'),
    url='https://github.com/neo-hu/django-websocket-channel',
    keywords=['django', 'websocket', 'redis'],
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    include_package_data=True,
    license = "MIT",
    install_requires=[
	'wsaccel',
        'setuptools',
        'redis',
        'gevent',
        'greenlet',
        'six',
    ],
    extras_require={
        'uwsgi': ['uWSGI>=1.9.20'],
        'wsaccel': ['wsaccel>=0.6.2'],
    }
)
