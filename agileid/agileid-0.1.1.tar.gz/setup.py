from setuptools import setup


setup(
    name='agileid',
    packages=['agileid'],
    version='0.1.1',
    description="Generate and manage AgileID identifiers",
    url='https://github.com/kurttheviking/agileid-py',
    author='Kurt Ericson',
    author_email='kurttheviking@outlook.com',
    license='ISC',
    download_url='https://github.com/kurttheviking/agileid-py/tarball/v0.1.0',
    keywords=['agileid', 'short objectid', 'encode objectid'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    install_requires=[
        "pymongo >= 2.7.2"
    ]
)
