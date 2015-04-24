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
        build_dir = os.path.join(self.source_dir, 'build', 'html')
        dest_dir = self.dest_dir

        script = []
        script.append('rm  -fr {}'.format(dest_dir))
        script.append('rm  -fr {}'.format(build_dir))
        script.append('mkdir -p {}'.format(dest_dir))

        script.append('cd {}'.format(self.source_dir))
        script.append('make html')

        script.append('cp -r {}/* {}'.format(build_dir, dest_dir))

        with open(self.script_path, 'w') as f:
            f.write('\n'.join(script))
        os.chmod(self.script_path, 0o777)

        return self.script_path

    update = install
