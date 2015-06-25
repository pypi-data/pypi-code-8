import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from django.test import TestCase
from django.conf import settings
from django.utils import autoreload
from sassy_coffee import compilers, utils

class SassyCoffeeTest(TestCase):

    _mtimes = {}
    _win = (sys.platform == 'win32')

    root = None
    if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
        root = settings.STATIC_ROOT
    else:
        path = None
        if hasattr(settings, 'PROJECT_PATH') and settings.PROJECT_PATH:
            path = settings.PROJECT_PATH
        else:
            path = settings.BASE_DIR
        root = os.path.join(path, 'static')

    def test_autoreload(self):
        formats_to_compile = [format.lower() for format in getattr(settings, 'DJANGO_SASSY_COFFEE_FORMATS', list())]

        c = autoreload.code_changed

        def code_changed():

            for format in formats_to_compile:
                format = '*.%s' % format
                files = utils.locate_folders_to_monitor(format)

                for folder in files:
                    stat = os.stat(folder)
                    mtime = stat.st_mtime

                    if self._win:
                        mtime -= stat.st_ctime
                    if folder not in self._mtimes:
                        self._mtimes[folder] = mtime
                        continue
                    if mtime != self._mtimes[folder]:
                        self._mtimes = {}
                        return True
            return c()

        if code_changed():
            compilers.compile_files()

        new_file = open('%s/app/sass/new.sass' % self.root, 'w')
        new_file.write('@import base.sass')
        new_file.close()

        if code_changed():
            compilers.compile_files()

    def tearDown(self):
        if os.path.exists('%s/app/sass/new.sass' % self.root):
            os.remove('%s/app/sass/new.sass' % self.root)

        if os.path.exists('%s/app/css/new.css' % self.root):
            os.remove('%s/app/css/new.css' % self.root)
