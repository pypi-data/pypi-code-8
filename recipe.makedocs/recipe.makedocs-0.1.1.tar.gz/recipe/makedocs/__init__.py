# -*- coding: utf-8 -*-
"""Recipe sphinx docs builder"""

import os
import sys

import zc.buildout


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options

        self.bin_dir = self.buildout['buildout']['bin-directory']
        self.buildout_dir = self.buildout['buildout']['directory']

        script_name = options.get('script-name', name)
        self.script_path = os.path.join(self.bin_dir, script_name)

        self.source_dir = os.path.join(self.buildout_dir, options.get('source-dir', 'docs'))
        self.dest_dir = os.path.join(self.buildout_dir, options.get('dest-dir', 'media'))

    def install(self):
        """Installer"""
        script = _script.format(source_dir=self.source_dir,
                                dest_dir=self.dest_dir,
                                pypath=self.buildout[self.buildout['buildout']['python']]['executable'])

        with open(self.script_path, 'w') as f:
            f.write(script)
        os.chmod(self.script_path, 0o777)

        return self.script_path

    update = install


_script = '''#! {pypath}

import os
import shutil
import subprocess


def makedocs():
    build_dir = os.path.join('{source_dir}', 'build', 'html')
    dest_dir = '{dest_dir}'

    if os.path.isdir(dest_dir):
        shutil.rmtree(dest_dir)

    if os.path.isdir(build_dir):
        shutil.rmtree(build_dir)

    subprocess.call('make html', cwd='{source_dir}', shell=True)
    shutil.copytree(build_dir, dest_dir)


makedocs()
'''
