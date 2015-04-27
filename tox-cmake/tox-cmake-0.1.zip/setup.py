# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


with open('README.rst', 'rb') as stream:
    readme = stream.read().decode('utf-8')


setup(
    name='tox-cmake',
    author='Andre Caron',
    author_email='andre.l.caron@gmail.com',
    description=readme,
    license='http://opensource.org/licenses/MIT',
    keywords='tox cmake',
    url='',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: C++',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
    ],

    version='0.1',
    platforms=['win32'],

    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tox-cmake = tox_cmake.cli:main',
         ],
    },
)
