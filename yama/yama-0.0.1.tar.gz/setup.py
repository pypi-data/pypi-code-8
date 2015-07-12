import os
from setuptools import setup, find_packages

REQUIREMENTS = os.path.join(os.path.dirname(__file__), 'requirements.txt')
REQUIREMENTS = open(REQUIREMENTS, 'r').read().splitlines()

setup(
    name='yama',
    version='0.0.1',
    description='simple process monitoring',
    url='https://github.com/ftzeng/yama',
    author='Francis Tseng (@frnsys)',
    license='MIT',
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    entry_points='''
        [console_scripts]
        yama=yama.cli:cli
    ''',
)