try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'SimpleCNN',
    'author': 'Zhengxing Chen',
    'author_email': 'czxttkl@gmail.com',
    'install_requires': ['nose'],
    'packages': ['simplecnn'], 
    'name':"SimpleCNN"
}

setup(**config)