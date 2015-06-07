
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'secret_details',
    'author': 'Eran Zimbler',
    'url': 'https://github.com/srgrn/secrets_details',
    'author_email': 'eran@zimbler.net',
    'version': '0.2.1',
    'install_requires': ['pyOpenSSL'],
    'packages': ['secrets_details'],
    'scripts': ['bin/ProvExplorer','bin/CertificateExpirationChecker'],
    'name': 'secret_details'
}

setup(**config)
