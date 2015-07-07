from os import path, chdir, environ
from sys import stdout, stderr, exit, argv, platform
from subprocess import call, check_output

PYTHONBUILD_DIR = path.dirname(path.realpath(__file__))

def python_build(*args):
    environment_vars = environ
    if platform == "darwin":
        osx_version = check_output(["sw_vers", "-productVersion"]).replace('\n', '')
        if osx_version in ["10.9", "10.10"]:
            environment_vars.update({"CFLAGS": "-I$(xcrun --show-sdk-path)/usr/include"})
    pyenv_build_bin = path.join(PYTHONBUILD_DIR, "bin", "python-build")
    call([pyenv_build_bin] + list(args), env=environment_vars)

def run():
    python_build(*argv[1:])
