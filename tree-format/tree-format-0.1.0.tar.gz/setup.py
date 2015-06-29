from setuptools import setup, find_packages

setup(
    name='tree-format',
    version='0.1.0',
    description='Generate nicely formatted trees',
    author='Jonathan M. Lange',
    author_email='jml@mumak.net',
    url='https://github.com/jml/tree-format',
    platforms='any',
    packages=find_packages('.'),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
