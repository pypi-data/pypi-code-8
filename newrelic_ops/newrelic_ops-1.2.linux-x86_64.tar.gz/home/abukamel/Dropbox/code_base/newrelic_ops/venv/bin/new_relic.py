#!/home/abukamel/Dropbox/code_base/newrelic_ops/venv/bin/python
import begin
import sys
import logging
import salt.config
import salt.client
from newrelic_ops import newrelic as newrelic


@begin.start(auto_convert=True)
@begin.logging
def main(install=False, key=''):
    if not install:
        logging.error('Try -h/--help option for usage info!')
        sys.exit(1)
    else:
        if not key:
            logging.error('Please provide newrelic license key via --key option')
            sys.exit(1)
        caller = newrelic.salt_init()
        if 'redhat' in caller.sminion.functions['grains.get']('os_family').lower():
            newrelic.install_redhat(key)
            sys.exit(0)
        if 'debian' in caller.sminion.functions['grains.get']('os_family').lower():
            newrelic.install_debian(key)
            sys.exit(0)
        else:
            newrelic.install_linux(key)
            sys.exit(0)
