import os
import sys

from distutils.core import setup, Extension


if 'JAVA_HOME' not in os.environ:
    raise ValueError('JAVA_HOME not defined in environment')


java_home = os.environ['JAVA_HOME']


def java_directory_containing(filename):
    for root, dirs, files in os.walk(java_home):
        for file in files:
            if file == 'jni.h':
                return root

    print('Unable to find {}'.format(filename))
    sys.exit(1)


java_include = java_directory_containing('jni.h')
java_server = java_directory_containing('libjvm.so')


pyhdfs = Extension('pyhdfs',
        sources=['src/pyhdfs.c'],
        include_dirs=['src', java_include],
        libraries=['hdfs'],
        library_dirs=['lib'],
        runtime_library_dirs=[java_server],
        )

setup(name='python-hdfs',
        version='0.3',
        author='Deng Zhiping, Joshua Downer',
        author_email='joshua.downer@gmail.com',
        description="Python wrapper for libhdfs",
        long_description=(open('README').read()),
        url="https://github.com/jdowner/libpyhdfs",
        license="Apache License 2.0",
        platforms=["GNU/Linux"],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Operating System :: Unix',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            'Topic :: System :: Filesystems',
            'Topic :: Utilities',
            ],
        ext_modules=[pyhdfs],
        )
