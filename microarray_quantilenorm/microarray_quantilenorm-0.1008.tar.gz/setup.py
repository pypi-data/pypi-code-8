from setuptools import setup

setup(
    name='microarray_quantilenorm',
    version=0.1008,
    url='http://github.com/githubuser8392/microarray-quantilenorm/',
    license='GNU General Public License v2',
    author='githubuser8392',
    install_requires=['Matplotlib>=1.4.3',
                      'Scipy>=0.15.1'],
    author_email='pypi@account.neomailbox.ch',
    description='Quantile normalization of microarray data.',
    platforms='any',
    scripts = ['microarray_quantilenorm/mq'],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )
