import os
import shlex
import subprocess


def exec_cmd(cmd, ignore_failure=False, cwd=None):
    """ Executes a command and returns output.

    >>> exec_cmd('echo hello!')
    'hello!\\n'
    """

    if isinstance(cmd, str):
        cmd = shlex.split(cmd)

    if cwd is not None:
        old_cwd = os.getcwd()
        os.chdir(cwd)

    try:
        output = subprocess.check_output(cmd)
    except Exception as e:
        if ignore_failure:
            return ''
        else:
            raise e
    else:
        return output.decode('utf-8')
    finally:
        if cwd is not None:
            os.chdir(old_cwd)
