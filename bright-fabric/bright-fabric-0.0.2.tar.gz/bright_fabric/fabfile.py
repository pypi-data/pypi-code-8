from fabric.api import local, settings
from fabric.context_managers import hide

from bright_fabric.fab import abs_path, find_files, jslint_file


def pylint():
    PEP8_CMD = 'pep8 --repeat --ignore=E501'
    PYFLAKES_CMD = 'pyflakes'

    all_files = \
        find_files(abs_path('apps'), ['py'], exclude_dirs=['migrations']) + \
        find_files(abs_path('apps_test'), ['py'], exclude_dirs=['migrations']) + \
        find_files(abs_path('fab'), ['py']) + \
        find_files(abs_path('project'), ['py'], exclude_dirs=['settings']) + \
        [abs_path('fabfile.py')]
    all_files_for_cmd = "'" + "' '".join(all_files) + "'"
    with settings(hide('aborts', 'running')):
        local('%s %s' % (PEP8_CMD, all_files_for_cmd))
        local('%s %s' % (PYFLAKES_CMD, all_files_for_cmd))


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
