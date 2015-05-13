from setuptools import setup

setup(
    name = 'spaceapi',
    version = '0.1.2',
    description = 'Download and archive Space API data',
    author = 'Thomas Levine',
    author_email = '_@thomaslevine.com',
    url = 'http://dada.pink/spaceapi',
    entry_points = {'console_scripts': ['spaceapi = spaceapi:main']},
    license = 'AGPL',
    packages = ['spaceapi'],
    install_requires = [
        'requests>=2.3.0',
        'vlermv>=1.3.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.4',
    ],
)
