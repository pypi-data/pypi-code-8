import os
import pprint

__author__ = 'Lai Tash (lai.tash@yandex.ru)'


import shutil
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py


class BuildAutoDocCommandSphinx(build_py):

    def run(self):
        self.spawn(['sphinx-apidoc', '-feF',
                    '-H', self.distribution.get_name(),
                    '-V', self.distribution.get_version(),
                    '-A', self.distribution.get_author(),
                    '-o', 'build/doc', 'src'])
        os.chdir('build/doc')
        self.spawn(['make', 'html'])
        os.chdir('../../')
        self.copy_tree('build/doc/_build/html', 'doc/sphinx/html')
        shutil.rmtree('build')

class BuildAutoDocCommandEpydoc(build_py):

    def run(self):
        try:
            shutil.rmtree('doc/epydoc/html')
        except OSError:
            pass
        os.makedirs('doc/epydoc/html')
        self.spawn(['epydoc',
            '-v',
            '--docformat', 'restructuredtext en',
            '-o', 'doc/epydoc/html',
            '--name', self.distribution.get_name(),
            '--inheritance', 'listed',
            '--graph', 'all',
            'src/configwrapper'
        ])

setup(
    name = 'ConfigWrapper',

    author="Lai Tash",
    author_email='lai.tash@gmail.com',
    version='0.4.0',
    description="Schema support for ConfigParser",

    package_dir = {'': 'src/'},
    packages=find_packages('src'),


    cmdclass = {
        'document_sphinx': BuildAutoDocCommandSphinx,
        'document_epydoc': BuildAutoDocCommandEpydoc
    }
)

