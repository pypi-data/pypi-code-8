from setuptools import setup, find_packages

setup(
    name='mdx_anchors_away',
    version='1.0.0',
    description='Add anchor tags and icons to all headers',
    author='Marco Ceppi',
    author_email='marco@ceppi.net',
    url='https://github.com/marcoceppi/mdx_anchors_away',
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
