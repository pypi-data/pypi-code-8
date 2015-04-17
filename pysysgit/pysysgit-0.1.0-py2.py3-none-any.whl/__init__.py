# -*- coding: utf-8 -*-

__author__ = 'Steven Willis'
__email__ = 'onlynone@gmail.com'
__version__ = '0.1.0'

import subprocess

__all__ = ["git", "CALL", "CHECK_CALL", "CHECK_OUTPUT"]

CALL = 'call'
CHECK_CALL = 'check_call'
CHECK_OUTPUT = 'check_output'

__sub_calls = {
    CALL: subprocess.call,
    CHECK_CALL: subprocess.check_call,
    CHECK_OUTPUT: subprocess.check_output
    }

__default_subprocess_kwargs = {
    'close_fds': True,
    'shell': False,
    }


def git(*args, **kwargs):
    """Execute git commands

    Args:
        *args: The positional arguments are used as arguments to the git
        command. For example, the following python code:

            git("commit", "--help")

        would execute:

            git commit --help

        f: One of CALL, CHECK_CALL, or CHECK_OUTPUT. Corresponds to the function
        from the subprocess module called to execute git. Defaults to CHECK_CALL

        **kwargs: The keyword arguments are passed through to the subprocess
        function as-is.

    Returns:
        Whatever is returned by the respective subprocess function. For example,
        f=CALL would return the returncode attribute, and f=CHECK_OUTPUT would
        return the content of stdout.

    Exmples:
        The following call:

            git("commit", "-m", "Commit Message", cwd="/path/to/repo")

        results in:

            subprocess.check_call(["git", "commit", "-m", "Commit Message"], cwd="/path/to/repo")

        And:

            git("checkout", "-b", "branch_name", f=CHECK_OUTPUT, cwd="/path/to/repo")

        results in:

            subprocess.check_output(["git", "checkout", "-b", "branch_name"], cwd="/path/to/repo")


    """

    f = kwargs.pop('f', CHECK_CALL)
    f = __sub_calls[f]

    full_args = ("git",) + tuple(args)

    full_kwargs = __default_subprocess_kwargs.copy()
    full_kwargs.update(kwargs)

    return f(full_args, **full_kwargs)

del subprocess
