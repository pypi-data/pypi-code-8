from setuptools import setup, find_packages

setup(
    name = 'bootstrap_vi',
    version = '0.0.4',
    py_modules=['bootstrap_vi'],
    install_requires = [],
    author = 'Tyghe Vallard',
    author_email = 'vallardt@gmail.com',
    description = 'Bootstrap virtualenv without pip or easy_install',
    license = 'MIT',
    keywords = 'bootstrap, virtualenv',
    url = 'https://github.com/necrolyte2/bootstrap_vi',
    entry_points = {
        'distutils.commands': [
            #'bootstrap_virtualenv = bootstrap_vi:BootstrapVI'
            'bootstrap_virtualenv = bootstrap_vi:BootstrapVI'
        ],
        'console_scripts': [
            'bootstrap_vi = bootstrap_vi:main'
        ]
    },
    tests_require = [
        'mock',
        'unittest2',
        'tempdir'
    ],
    setup_requires = [
        'nose'
    ],
)
