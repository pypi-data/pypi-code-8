from fabric.api import local, settings
from fabric.context_managers import hide
from fabric.state import env

from bright_fabric.util import abs_path, find_files, jslint_file


def pylint():
    """
    Validates the code layout for all python files in configured paths using flake8

    You can customise how this command is run by setting the following parameters
    in the fabric configuration (either through a config file or in env)

    pylint_ignore_errors: Set codes to ignore in a list (eg ['E500', 'E501'])
    pylint_dirs: Set dirs to search for python files in (defaults to current dir)
    pylint_exclude_dirs: Set dirs exclude when searching for python files to lint

    """
    flake8_command = 'flake8'

    ignore_errors = env.get('pylint_ignore_errors')

    if ignore_errors:
        flake8_command += ' --ignore=%s' % ','.join(ignore_errors)

    dirs = env.get('pylint_dirs', ['.'])

    exclude_dirs = env.get('pylint_exclude_dirs', [])

    all_files = []

    for dir in dirs:
        all_files += find_files(abs_path(dir), ['py'], exclude_dirs=exclude_dirs)

    all_files_for_cmd = "'" + "' '".join(all_files) + "'"
    with settings(hide('aborts', 'running')):
        local('%s %s' % (flake8_command, all_files_for_cmd))


def jslint():
    """
    We're using jslint-reporter:
        https://github.com/FND/jslint-reporter

    You'll need to install Node.js to run `fab jslint`:
        https://github.com/joyent/node/wiki/Installation

    To updgrade jslint use:
        `node tool/jslint-wrapper.js --upgrade`
    """

    with settings(warn_only=True):
        JS_ROOT = abs_path('static/js')
        SNIPPETS_ROOT = abs_path('templates/snippets')

        for filename in find_files(JS_ROOT, ['js'], exclude_dirs=['lib']):
            jslint_file(filename)
        # There are some JavaScript snippets in that get included into the
        # template HTML, so they have to be under templates/ not static/js/
        for filename in find_files(SNIPPETS_ROOT, ['js']):
            jslint_file(filename)
