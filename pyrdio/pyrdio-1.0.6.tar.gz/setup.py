from setuptools import setup, find_packages

requires = [
    'oauth2'
]

setup(
    name='pyrdio',
    version='1.0.6',
    description='A simple Python wrapper for Rdio\'s API',
    url='https://github.com/rcrdclub/pyrdio',
    author='Hery Ratsimihah',
    license='MIT',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ),
    keywords='rdio library',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=requires
)