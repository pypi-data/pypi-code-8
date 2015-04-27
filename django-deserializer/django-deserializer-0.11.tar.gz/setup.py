from setuptools import setup

setup(
    name='django-deserializer',
    packages=('deserializer',),
    author='C. Paschalides',
    author_email='already.late@gmail.com',
    description='A Django Mixin capable of deserializing a request\'s body into python data structures.',
    url='https://github.com/stargazer/django-deserializer/',
    license='WTFPL',
    version=0.11,
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
