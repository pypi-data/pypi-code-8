from distutils.core import setup, Extension

pyhdfs = Extension('pyhdfs',
        sources=['src/pyhdfs.c'],
        include_dirs=[
            'src',
            '/usr/lib/jvm/java-6-sun/include/',
            '/usr/lib/jvm/java-1.7.0-openjdk-1.7.0.79-2.5.5.0.fc20.x86_64/include',
            ],
        libraries=['hdfs'],
        library_dirs=['lib'],
        runtime_library_dirs=[
            '/usr/local/lib/pyhdfs',
            '/usr/lib/jvm/java-6-sun/jre/lib/i386/server',
            '/usr/lib/jvm/java-1.7.0-openjdk-1.7.0.79-2.5.5.0.fc20.x86_64/jre/lib/amd64/server',
            ],
        )

setup(name='python-hdfs',
        version='0.2',
        author='Deng Zhiping, Joshua Downer',
        author_email='joshua.downer@gmail.com',
        description="Python wrapper for libhdfs",
        long_description=(open('README').read()),
        url="https://github.com/jdowner/libpyhdfs",
        license="Apache License 2.0",
        platforms=["GNU/Linux"],
        ext_modules=[pyhdfs],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Operating System :: Unix',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            'Topic :: System :: Filesystems',
            'Topic :: Utilities',
            ],
        )
