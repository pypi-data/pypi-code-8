from setuptools import setup, find_packages
import trendy

setup(
    name='trendy',
    version=trendy.__version__,
    license='MIT',

    description='A library for interacting with Trend Deep Security API',
    long_description=open('README.md').read(),

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Networking',
        'Programming Language :: Python :: 2.7',
    ],

    packages=find_packages(exclude=['tests*']),

    install_requires=[
        "suds >= 0.4",
        "requests"
    ],

    tests_require=[
        'mock'
    ],

    test_suite='tests',
)