import io
import re
from setuptools import setup

init_py = io.open('gavagai/__init__.py').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", init_py))
metadata['doc'] = re.findall('"""(.+)"""', init_py)[0]

setup(
    name='Gavagai',
    packages=['gavagai'],
    version=metadata['version'],
    description=metadata['doc'],
    author=metadata['author'],
    author_email=metadata['email'],
    url=metadata['url'],
    keywords = ['text-analysis', 'api', 'nlp'], 
    license='The MIT License (MIT)',
    install_requires=[
        'requests>=2.7.0,<3.0',
        'urllib3',
        'ndg-httpsclient',
    ]
)