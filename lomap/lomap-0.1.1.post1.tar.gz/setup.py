from setuptools import setup
from setuptools.command.install import install

class post_install(install):
    def run(self):

        install.run(self)

        import os
        import sys
        import subprocess
        import traceback
        from os.path import expanduser
        home_dir = expanduser("~")
        orig_stdout, orig_stderr = sys.stdout, sys.stderr
        sys.stdout = os.fdopen(0, 'w', 0)
        sys.stderr = os.fdopen(1, 'w', 0)
        try:
            output = subprocess.check_output('python -c "import os; os.chdir(\'%s\'); import lomap; print lomap.__file__"' % home_dir, shell=True).strip()
            assert(output)
            install_dir = os.path.dirname(output)
            exp_dir = os.path.join(install_dir, 'examples')
            print '\n###\n# LOMAP has been installed to %s.\n# To run the examples, copy the contents of %s\n# to a writable directory.\n###\n' % (install_dir, exp_dir)
        except Exception as ex:
            print '\n###\n# Installation of LOMAP failed! Please check error messages to see what went wrong.\n###\n'
            print "%s: Exception %s: %s" % (__name__, type(ex), ex)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, file=sys.stdout)
            exit(1)
        sys.stdout, sys.stderr = orig_stdout, orig_stderr

setup(
    name='lomap',
    version='0.1.1-1',
    description='LTL Optimal Multi-Agent Planner (LOMAP)',
    author='Alphan Ulusoy',
    author_email='alphan@bu.edu',
    url='http://hyness.bu.edu/lomap',
    packages=['lomap', 'lomap.algorithms', 'lomap.classes'],
    package_dir={'lomap': 'lomap'},
    package_data={'lomap': ['binaries/linux/*','binaries/mac/*','README','COPYING','third_party_sources/*','examples/ijrr2013/*', 'examples/ijrr2014_inc_syn/*', 'examples/ijrr2014_rec_hor/*']},
    license='GNU GPL',
    long_description=open('README').read(),
    install_requires=['networkx >= 1.6','pp >= 1.6.2','matplotlib >= 1.3.1','setuptools >= 1.1.6'],
    cmdclass={'install': post_install},
)
