from setuptools import setup, find_packages
import os

version = '0.10.0'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n' +
    read('js', 'cropper', 'test_cropper.txt')
    + '\n' +
    read('CHANGES.txt'))

setup(
    name='js.cropper',
    version=version,
    description="Fanstatic packaging of Cropper",
    long_description=long_description,
    classifiers=[],
    keywords='',
    author='Fanstatic Developers',
    author_email='fanstatic@googlegroups.com',
    license='BSD',
    packages=find_packages(),namespace_packages=['js'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'fanstatic',
        'setuptools',
        ],
    entry_points={
        'fanstatic.libraries': [
            'cropper = js.cropper:library',
            ],
        },
    )
