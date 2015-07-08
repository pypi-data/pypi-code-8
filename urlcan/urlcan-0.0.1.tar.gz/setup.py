from distutils.core import setup

version = '0.0.1'

setup(name='urlcan',
    version=version,
    description="",
    py_modules=['urlcan'],
    install_requires=['six'],
    license='MIT License',
    author='Ilya Shalyapin',
    author_email='ishalyapin@gmail.com',
    url='http://github.com/un1t/urlcan',
    classifiers  = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
