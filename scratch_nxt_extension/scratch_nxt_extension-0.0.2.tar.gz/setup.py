#import ez_setup
#ez_setup.use_setuptools() 

from setuptools import setup, find_packages
 
setup(
    name = 'scratch_nxt_extension',
    packages = find_packages(),
    py_modules = ['nxtbrick'],
    scripts = ['scratch_nxt_helper'],
    install_requires = ['flask', 'nxt-python', 'lightblue'],
    package_data = {
        '': ['COPYING.txt', 'LICENSE', 'README.md', 'setup.cfg']
    },
    version = '0.0.2',
    description = 'Provides a http helper app to allow Scratch 2 to control a LEGO NXT brick',
    author='Chris Proctor',
    author_email='chris.proctor@gmail.com',
    url='http://mrproctor.net/scratch',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Topic :: Education'
    ]
)
