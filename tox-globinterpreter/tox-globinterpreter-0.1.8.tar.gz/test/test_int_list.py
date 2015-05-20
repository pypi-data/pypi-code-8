

from textwrap import dedent
from tox_globinterpreter import InterpreterList


def test_write_interpreter_list_1(tmpdir, monkeypatch):
    monkeypatch.chdir(tmpdir)
    with InterpreterList('rd1.lst') as il:
        il._first_interpreter = False
        il.write('/usr/local/bin/python2.7')
    assert open('rd1.lst').read().rstrip() == dedent("""\
    v 1
    p python2.7 /usr/local/bin/python2.7
    e
    """).rstrip()

def test_write_interpreter_list_2(tmpdir, monkeypatch):
    # file with newline
    monkeypatch.chdir(tmpdir)
    with InterpreterList('rd2.lst') as il:
        il._first_interpreter = False
        il.write('/usr/local/bin/python2.7')
        il.write('/usr/lo\ncal/bin/python3.4')
    assert open('rd2.lst').read().rstrip() == dedent("""\
    v 1
    p python2.7 /usr/local/bin/python2.7
    p python3.4 /usr/lo
      cal/bin/python3.4
    e
    """).rstrip()

def test_read_interpreter_list_1(tmpdir, monkeypatch):
    monkeypatch.chdir(tmpdir)
    with open('wr01.lst' , 'w') as fp:
        fp.write(dedent("""\
        v 1
        g bla*.*
        p python2.7 /usr/local/bin/python2.7
        p python2.5 /usr/loc
          al/bin/python2.5
        e
        """))  # format agains eol scrubbing editors
    for idx, interpreter in enumerate(InterpreterList('wr01.lst')):
        if idx == 0:
            assert interpreter.key == 'python2.7'
            assert interpreter.path == '/usr/local/bin/python2.7'
        if idx == 1:
            assert interpreter.key == 'python2.5'
            assert interpreter.path == '/usr/loc\nal/bin/python2.5'


