
import os
from textwrap import dedent

from tox_globinterpreter import GlobInterpreterPlugin

class Option:
    scan = True


class Cfg:
    def __init__(self, option):
        self.option = option


def test_scan_executables(tmpdir, monkeypatch):
    monkeypatch.chdir(tmpdir)
    monkeypatch.delenv('TOX_INTERPRETER_GLOBS', raising=False)
    exe_paths = [
        'bin/python2.7',
        'bin/python2.6',
        'bin/python3.4',
        'bin/python3.3',
    ]
    os.mkdir('bin')
    for file_name in exe_paths:
        with open(file_name, 'w') as fp:
            fp.write('test')
    os.mkdir('config')
    os.environ['XDG_CONFIG_HOME'] = os.path.abspath('config')
    gip = GlobInterpreterPlugin()
    opt = Option()
    opt.args = ['bin/python2.?', 'bin/python3.?']
    opt.help = False
    cfg = Cfg(opt)
    try:
        gip.tox_configure(cfg)
    except SystemExit as e:
        if e.code != 1:
            raise
    cwd = os.getcwd()
    assert open('config/tox/interpreters.lst').read().strip() == dedent("""\
    v 1
    # Original pattern used:
    g bin/python2.? bin/python3.?
    # Interpreters found:
    p python2.6 {0}/bin/python2.6
    p python2.7 {0}/bin/python2.7
    p python3.3 {0}/bin/python3.3
    p python3.4 {0}/bin/python3.4
    e
    """.format(cwd)).strip()
    print('loading....')
    gip = GlobInterpreterPlugin()
    print(gip._il._interpreters)
    for ver in '2.6 2.7 3.3 3.4'.split():
        base_python = "python" + ver
        assert gip._tox_get_python_executable(base_python) == \
               '{0}/bin/python{1}'.format(cwd, ver)
