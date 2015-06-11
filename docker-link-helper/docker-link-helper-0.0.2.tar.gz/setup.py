from setuptools import setup, find_packages

setup(
    name='docker-link-helper',
    version='0.0.2',
    url='https://github.com/tback/docker-link-helper',
    license='MIT',
    author='Till Backhaus',
    author_email='till@backha.us',
    description='Search for occurrences of docker links and replace them by their value',
    download_url='https://github.com/tback/docker-link-helper/tarball/0.0.2',
    packages=['helper'],
    keywords=['docker', 'environment-variable', 'docker link'],
    entry_points={
        'console_scripts': [
            'docker-link-helper=helper:main',
        ],
    }
)
