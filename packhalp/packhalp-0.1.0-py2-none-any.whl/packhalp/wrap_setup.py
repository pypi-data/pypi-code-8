#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Runs a setup.py command (eg. bdist_wheel) with a customized version number.

The use-case is adding a CI (eg. jenkins) BUILD_NUMBER to the version number
specified in setup() calls, so that we can automatically build and publish new
distributions without having to update/commit/push any file for small projects
that don't have strong release management requirements.

Note that any version number referenced inside the target package won't be
affected (think module.__version__) and thus won't match the distribution
version.

For example, if we have "setup(..., version='1.0.7', ...)" in setup.py and run
"BUILD_NUMBER=19 wrap_setup.py setup.py bdist_wheel", the resulting wheel file
will have version 1.0.7.post19

If BUILD_NUMBER does not exist the suffix will be .dev0

We do this by parsing the target setup.py file and injecting a call to our
wrap_version function in place of the version keyword value in the setup()
call.
"""

import ast
import os
import sys


def wrap_version(version):
    build = os.getenv('BUILD_NUMBER')
    if build is None:
        version_suffix = '.dev0'
    else:
        version_suffix = '.post' + build
    return version + version_suffix


def run_patched_setup_command(args):
    # read setup.py and patch the version arg
    filename = args[0]
    with open(filename, 'r') as fp:
        tree = ast.parse(fp.read(), filename)
    expr_list = [ i.value for i in tree.body if isinstance(i, ast.Expr) ]
    call_list = [ i for i in expr_list if isinstance(i, ast.Call) ]
    setup_call = [ i for i in call_list if i.func.id == 'setup' ][0]
    version = [ i for i in setup_call.keywords if i.arg == 'version' ][0]
    # insert our call to wrap_version
    previous_value = version.value
    func = ast.Name(id='wrap_version', ctx=ast.Load(),
                    lineno=previous_value.lineno,
                    col_offset=previous_value.col_offset)
    version.value = ast.Call(func=func,
                             args=[version.value], keywords=[],
                             lineno=previous_value.lineno,
                             col_offset=previous_value.col_offset)
    # compile the patched AST and run
    patched_code = compile(tree, filename, 'exec')
    sys.argv = args
    exec(patched_code)


if __name__ == '__main__':
    run_patched_setup_command(sys.argv[1:])
