#!/usr/bin/env python
#
# fabfile for goulash
#
# this file is a self-hosting fabfile, meaning it
# supports direct invocation with standard option
# parsing, including --help and -l (for listing commands).
#
# summary of commands/arguments:
#
#   * fab pypi_repackage: update this package on pypi
#
import os, sys

from fabric.colors import red
from fabric import api
from fabric.contrib.console import confirm

_ope = os.path.exists
_mkdir = os.mkdir
_expanduser = os.path.expanduser
_dirname = os.path.dirname

ldir = _dirname(__file__)

VERSION_DELTA = .01
PROJECT_NAME = 'goulash'
SRC_ROOT = os.path.dirname(__file__)
DOCS_URL = 'http://localhost:8000'
DOCS_ROOT = os.path.join(SRC_ROOT, 'docs')
DOCS_API_ROOT = os.path.join(DOCS_ROOT, 'api')
DOCS_SITE_DIR = os.path.join(DOCS_ROOT, 'site')

if os.getcwd()!=os.path.dirname(SRC_ROOT):
    os.chdir(SRC_ROOT)

def pypi_repackage():
    ldir = _dirname(__file__)
    print red("warning:") + (" by now you should have commited local"
                             " master and bumped version string")
    ans = confirm('proceed with pypi update in "{0}"?'.format(ldir))
    if not ans: return
    with api.lcd(ldir):
        with api.settings(warn_only=True):
            # in case this has never been done before
            api.local("git checkout -b pypi")
        api.local("git reset --hard master")
        api.local("python setup.py register -r pypi")
        api.local("python setup.py sdist upload -r pypi")

def version_bump():
    """ bump the version number """
    sandbox = {}
    version_file = os.path.join('goulash', 'version.py')
    err = 'version file not found in expected location: ' + version_file
    assert os.path.exists(version_file), err
    execfile(version_file, sandbox)
    current_version = sandbox['__version__']
    new_version = current_version + VERSION_DELTA
    with open(version_file, 'r') as fhandle:
        version_file_contents = [x for x in fhandle.readlines() if x.strip()]
    new_file = version_file_contents[:-1]+["__version__={0}".format(new_version)]
    new_file = '\n'.join(new_file)
    print red("warning:") + " version will be changed to {0}".format(new_version)
    print
    print red("new version file will look like this:\n")
    print new_file
    ans = confirm('proceed with version change?'.format(ldir))
    if not ans:
        print 'aborting.'
        return
    with open(version_file,'w') as fhandle:
        fhandle.write(new_file)
        print 'version has been rewritten.'

def show_docs():
    import addict
    from goulash.bin.docs import gen_docs
    gen_docs(addict.Dict(dir='.', project=PROJECT_NAME))
    #if 'docs' in os.listdir(DOCS_ROOT):
    import webbrowser
    if 'docs' in os.listdir(DOCS_ROOT):
        print red('.. found read-the-docs style documentation')
        with api.lcd('docs'):
            webbrowser.open(DOCS_URL)
            from goulash.bin.serv import run_server
            run_server(dir=DOCS_SITE_DIR)
    else:
        print red("Not sure what to do with this style of documentation")

if __name__ == '__main__':
    # a neat hack that makes this file a "self-hosting" fabfile,
    # ie it is invoked directly but still gets all the fabric niceties
    # like real option parsing, including --help and -l (for listing
    # commands). note that as of fabric 1.10, the file for some reason
    # needs to end in .py, despite what the documentation says.  see:
    # http://docs.fabfile.org/en/1.4.2/usage/fabfiles.html#fabfile-discovery
    #
    # the .index() manipulation below should make this work regardless of
    # whether this is invoked from shell as "./foo.py" or "python foo.py"
    from fabric.main import main as fmain
    patched_argv = ['fab', '-f', __file__,] + \
                   sys.argv[sys.argv.index(__file__)+1:]
    sys.argv = patched_argv
    fmain()
