from setuptools import setup, find_packages

name = 'siblings'
__version__ = "Undefined"
for line in open('{}/__init__.py'.format(name)):
    if (line.startswith('__version__')):
        exec (line.strip())

setup(
    name=name,
    version=__version__,
    author='Adrian Altenhoff',
    author_email='adrian.altenhoff@inf.ethz.ch',
    description="Siblings is a code base to compute homologs between genomes and make them "
                "publicly available through a REST api",
    url='http://siblings.ch',
    packages=find_packages(),
    package_data={'siblings': ['test/*.h5']},
    install_requires=['numpy', 'tables>=3.1', 'future', 'pyzmq'],
    license='MPL 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='bioinformatics homology homologs Smith-Waterman resource REST',
    extras_require={
        'REST': ['tornado'],
        'WORKER': ['pyopa', 'pyzmq'],
        'BROKER': ['pyzmq']},
    dependency_links=['git@cbrg-git.ethz.ch/pyopa'],
    scripts=['bin/start_worker.py',
             'bin/start_broker.py',
             'bin/start_scheduler.py'],
)
