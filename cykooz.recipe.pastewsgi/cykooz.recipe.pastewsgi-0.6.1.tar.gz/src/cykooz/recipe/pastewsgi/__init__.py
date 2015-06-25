# cykooz.recipe.pastewsgi
# Copyright (C) 2014 Cykooz
import os
import stat

from zc.recipe.egg.egg import Eggs


WRAPPER_TEMPLATE = '''\
import sys
sys.path[0:0] = [
    %(syspath)s,
]
%(environ)s
%(initialization)s
from paste.deploy import loadapp
application = loadapp("config:%(config)s")
'''


class Recipe(object):
    """Buildout recipe: tranchitella.recipe.wsgi:default"""

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        self.options['eggs'] += '\nPasteDeploy'
        self.script_name = options.get('script-name', self.name)
        self.target = options.get('target', '')

    def install(self):
        egg = Eggs(self.buildout, self.options['recipe'], self.options)
        requirements, ws = egg.working_set()
        path = [pkg.location for pkg in ws]
        extra_paths = self.options.get('extra-paths', '')
        extra_paths = extra_paths.split()
        path.extend(extra_paths)
        environ = self.options.get('environ', '')
        initialization = self.options.get('initialization', '')
        if environ:
            environ = ["os.environ['%s'] = '%s'" % tuple(s.strip() for s in i.split('=', 1))
                       for i in environ.splitlines() if '=' in i]
            environ.insert(0, 'import os')
            environ = '\n'.join(environ)
        output = WRAPPER_TEMPLATE % dict(
            config=self.options['config-file'], environ=environ,
            initialization=initialization,
            syspath=',\n    '.join(repr(p) for p in path))
        if not self.target:
            location = self.buildout['buildout']['bin-directory']
            self.target = os.path.join(location, self.script_name)

        f = open(self.target, "wt")
        try:
            f.write(output)
        finally:
            f.close()

        exec_mask = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        os.chmod(self.target, os.stat(self.target).st_mode | exec_mask)

        self.options.created(self.target)
        return self.options.created()

    def update(self):
        self.install()
