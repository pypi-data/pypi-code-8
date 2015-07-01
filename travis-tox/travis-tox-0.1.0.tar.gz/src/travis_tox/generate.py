from __future__ import unicode_literals, print_function

from tox._config import parseconfig

def generate_tox_config(fileobj):
    def print_(text):
        print(text, file=fileobj)

    print_('language: python')
    print_('python: 3.4')
    print_('env:')
    for env in parseconfig(None, 'tox').envlist:
        print_('  - TOX_ENV={env}'.format(env))
    print_('install:')
    print_('  - pip install tox')
    print_('script:')
    print_('  - tox -e $TOX_ENV')
