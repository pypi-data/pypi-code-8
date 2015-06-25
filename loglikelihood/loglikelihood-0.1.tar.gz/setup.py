from setuptools import setup

"""
Build & setup script.
    build (with symlink for dev): python setup.py develop
    build (source distribution): python setup.py sdist
    install (from here): python setup.py install
    upload to pip: python setup.py sdist upload
    install (from pip): pip install loglikelihood
"""
setup(
    name='loglikelihood',
    version='0.1',
    description=(
        'A library for python to implement the \'Log Likelihood\'' +
        ' and \'Root Log Likelihood\' algorithms.'
    ),
    url='https://github.com/Tom-Davidson/logLikelihood',
    author='Tom Davidson',
    author_email='tom@davidson.me.uk',
    license='MIT',
    packages=['loglikelihood'],
    zip_safe=False
)
