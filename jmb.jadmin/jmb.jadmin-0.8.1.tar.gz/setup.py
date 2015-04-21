# http://www.28lines.com/?p=8
import os
import re
from setuptools import setup, find_packages
from setuptools.command.test import test

f = open('docs/index.rst')
long_description = f.read()
f.close()


class TestRunner(test):
    def run(self, *args, **kwargs):
        if self.distribution.install_requires:
            self.distribution.fetch_build_eggs(
                self.distribution.install_requires)
        if self.distribution.tests_require:
            self.distribution.fetch_build_eggs(
                self.distribution.tests_require)
        from jmb.jadmin.tests.runtests import runtests
        runtests()


def get_data_files(*args, **kwargs):

    EXT_PATTERN = kwargs.get('ext') or '\.(html|js|txt|css|po|mo|jpg|png|gif|ico)'

    data_dict = {}
    for pkg_name in args:
        data_files = []
        for dirpath, dirnames, filenames in os.walk(pkg_name.replace('.', '/')):
            rel_dirpath = re.sub("^" + pkg_name + '/', '',  dirpath)
            # Ignore dirnames that start with '.'
            for i, dirname in enumerate(dirnames):
                if dirname.startswith('.'): del dirnames[i]
            if filenames:
                data_files += [os.path.join(rel_dirpath, f) for f in filenames
                               if re.search(EXT_PATTERN, f)]
        data_dict[pkg_name] = data_files
    return data_dict

v = file(os.path.join(os.getcwd(), 'jmb', 'jadmin', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(v.read()).group(1)
v.close()

setup(
    name='jmb.jadmin',
    version=VERSION,
    description='jumbo admin', 
    long_description=long_description,
    author='ThunderSystems',
    url='https://bitbucket.org/jumboteam/jmb.jadmin',
    author_email='dev@thundersystems.it',
    packages=find_packages(exclude=['tests', 'tests.*']),
    platforms='any',
    zip_safe=False,
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Framework :: Django',
    ],
    test_suite = "jmb.jadmin.tests",
    cmdclass={"test": TestRunner},
    install_requires = [
        'setuptools',
        'Django>=1.4.3',
        'pyquery',
        'jmb.filters',
    ],
    namespace_packages = ['jmb'],    
    package_data=get_data_files('jmb.jadmin')
)

