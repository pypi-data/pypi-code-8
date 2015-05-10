from setuptools import setup, find_packages

setup(
    name='dogebuild-fpc',
    version='0.1.0.dev1',
    description='Free Pascal Compiler plugin for dogebuild',
    author='Kirill Sulim',
    author_email='kirillsulim@gmail.com',
    url='https://github.com/dogebuild/dogebuild-fpc',
    packages=find_packages(include=[
        'dogebuild*',
      ]),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
    ],
    keywords='dogebuild builder fpc pascal',
)
