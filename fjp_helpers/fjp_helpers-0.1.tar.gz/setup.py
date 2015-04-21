try:
    from setuptools import setup
except:
    from distutils.core import setup

config = {
    'description': 'A collection of helper functions used to solve different equations.',
    'author': 'Dakota St. Laurent',
    'url': 'https://github.com/Poulin-Research-Group',
    'download_url': 'https://github.com/Poulin-Research-Group/helpers',
    'author_email': 'fpoulin@uwaterloo.ca',
    'version': '0.1',
    'install_requires': ['mpi4py'],
    'packages': ['helpers'],
    'name': 'fjp_helpers'
}

setup(**config)
