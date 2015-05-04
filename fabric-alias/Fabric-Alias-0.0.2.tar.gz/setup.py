from setuptools import setup, find_packages

install_requires = ['fabric']
version = '0.0.2'
name = 'fabric_alias'
short_description = 'fabric_alias is a plugin for fabric when using fabfile.'
long_description = """\

"""


setup(
    name='Fabric-Alias',
    author='Hiroyuki Ishii',
    packages=find_packages(),
    install_requires=install_requires,
    version=version,
    description=short_description,
    long_description=long_description,
    # classifiers=classifiers,
    # keywords=['',],
    # url='',
)
