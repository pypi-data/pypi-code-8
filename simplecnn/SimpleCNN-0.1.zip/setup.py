try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'SimpleCNN',
    'author': 'Zhengxing Chen',
    'author_email': 'czxttkl@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['cnn'], 
    'name':"SimpleCNN"
}

setup(**config)