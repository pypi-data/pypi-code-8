from setuptools import setup, find_packages


setup(
    name='ReactiPy',

    version='0.0.6',

    description='Compiles React Components server side using python \n '
                'Documentation: https://github.com/logandhead/reactipy',

    long_description=open('DESCRIPTION').read(),

    # The project's main homepage.
    url='https://github.com/logandhead/ReactiPy',

    # Author details
    author='Logan Head',
    author_email='logandhead@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[

        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',
    ],

    # What does your project relate to?
    keywords='react jsx compile react.js reactjs facebook',
    packages=find_packages(),
    package_data={'': ['*.json', '*.js']},
    install_requires=['nodeenv==0.13.1'],


)