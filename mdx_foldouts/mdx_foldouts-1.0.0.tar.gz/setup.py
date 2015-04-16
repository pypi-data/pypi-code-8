from setuptools import setup, find_packages

setup(
    name='mdx_foldouts',
    version='1.0.0',
    description='Ability to model callouts in Markdown',
    author='Marco Ceppi',
    author_email='marco@ceppi.net',
    url='https://github.com/marcoceppi/mdx_foldouts',
    packages=find_packages(),
    include_package_data = True,
    install_requires = ['setuptools', 'markdown'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
