from setuptools import setup

setup(
    name='django-deserializer',
    packages=('deserializer',),
    author='C. Paschalides',
    author_email='already.late@gmail.com',
    license='WTFPL',
    version=0.1,
    install_requires=(
        'Django',
    ),
    tests_require=(),
    test_suite='runtests',
    zip_safe=False,
    classifiers=(
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: Freely Distributable'
    ),
)
