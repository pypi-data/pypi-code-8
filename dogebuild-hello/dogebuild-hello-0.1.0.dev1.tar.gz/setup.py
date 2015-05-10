from setuptools import setup, find_packages

setup(
    name='dogebuild-hello',
    version='0.1.0.dev1',
    description='Hello world plugin for dogebuild',
    author='Kirill Sulim',
    author_email='kirillsulim@gmail.com',
    license='MIT',
    url='https://github.com/dogebuild/dogebuild-hello',
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
    keywords='dogebuild builder helloworld',
)
