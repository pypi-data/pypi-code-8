from setuptools import setup, find_packages

version = '1.2'

long_description = '\n'.join([
    open("README.rst").read(),
    open("CHANGELOG.rst").read(),
])

setup(
    name='elementtreewriter',
    version=version,
    description="XML writer for elementtree with sane namespace support.",
    long_description=long_description,
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: XML',
    ],
    keywords='xml elementtree',
    author='Martin Raspe, Jens Klein',
    author_email='hertzhaft@biblhertz.it, jens@bluedynamics.com',
    url='',
    license='D-FSL - German Free Software License',
    include_package_data=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=True,
    install_requires=[
        'elementtree'
    ],
)
