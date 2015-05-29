# stevedore/example/setup.py
from setuptools import setup, find_packages
import re
from pip.req import parse_requirements
import uuid


VERSION = open('VERSION').read().replace('\n', '')
ROOT_INCLUDE = ['requirements.txt', 'VERSION', 'LICENSE.txt']


def get_url(ir):
    if hasattr(ir, 'url'): return ir.url
    if ir.link is None: return
    return ir.link.url

requirements = parse_requirements('requirements.txt', session=uuid.uuid1())
install_requires = [str(ir.req) for ir in requirements if not get_url(ir)]

setup(
    name='nekbot.protocols.telegram',
    namespace_packages = ['nekbot.protocols'],
    version=VERSION,

    description='Telegram Protocol for Nekbot, a modular multiprotocol bot.',

    author='Nekmo',
    author_email='contacto@nekmo.com',

    url='https://bitbucket.org/Nekmo/nekbot.protocols.telegram',
    
    download_url='https://bitbucket.org/Nekmo/nekbot.protocols.telegram/get/default.tar.gz',

    classifiers=[
        'Natural Language :: Spanish',
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Topic :: Communications :: Chat',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
        'Topic :: Communications :: Conferencing',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    platforms=['linux'],

    scripts=[],
    
    provides=['nekbot.protocols.telegram',
              ],
    
    install_requires=install_requires,

    packages=['nekbot', 'nekbot.protocols', 'nekbot.protocols.telegram'],
    include_package_data=True,

    keywords=['nekbot', 'bot', 'telegram', 'chat'],
    
    dependency_links=[
        'https://bitbucket.org/luckydonald/pytg2/get/master.zip#egg=pytg2',
    ],

    entry_points={
        'nekbot.protocols': [
            'telegram = nekbot.protocols.telegram:Telegram',
        ],
    },
        
    package_data = {'': ROOT_INCLUDE},

    zip_safe=False,
)