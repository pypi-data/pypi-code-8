from setuptools import setup
import sys

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

setup(
    name="mr-monkeypatch",
    version="0.0.3",
    license='http://www.apache.org/licenses/LICENSE-2.0',
    description="A monkey patching library for python",
    author='phoeagon',
    author_email='admin@phoeagon.info',
    url='https://github.com/phoeagon/monkeypatch-python',
    download_url='https://github.com/phoeagon/monkeypatch-python/tarball/0.0.3',
    packages = ['monkeypatch'],
    package_dir = {'monkeypatch': 'src'},
    test_suite = 'monkeypatch.monkeypatch_test',
    package_data={
        'monkeypatch': ['README', 'LICENSE']
    },
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    long_description="""Provide dynamic method name resolution and routing
    simulates monkey patching in Ruby.""",
)
