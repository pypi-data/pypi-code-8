from setuptools import setup, find_packages

setup(
    name='digimat.ipcamera',
    version='0.1.2',
    description='Digimat IP Camera',
    namespace_packages=['digimat'],
    author='Frederic Hess',
    author_email='fhess@splust.ch',
    license='PSF',
    packages=find_packages('src'),
    package_dir = {'':'src'},
    install_requires=[
        #'pil',
        'setuptools'
    ],
    dependency_links=[
        ''
    ],
    zip_safe=False)
