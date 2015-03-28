#!/home/abukamel/Dropbox/code_base/newrelic_ops/venv/bin/python2
import begin
import sys
import logging
import salt.config
import salt.client


def salt_init():
    opts = salt.config.apply_minion_config()
    opts['file_client'] = 'local'
    caller = salt.client.Caller(mopts=opts)
    return caller


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
        caller = salt_init()
        info = dict(
            newrelic_url='http://download.newrelic.com/pub/newrelic/el5/i386/newrelic-repo-5-3.noarch.rpm',
            newrelic_package='newrelic-sysmond',
            newrelic_license_cmd=r"nrsysmond-config --set license_key='%(l_key)s'"
            % {'l_key': key},
            newrelic_start_cmd=r"/etc/init.d/newrelic-sysmond restart",
            newrelic_chkconfig_cmd='chkconfig newrelic-sysmond on')
        logging.info(caller.sminion.functions['pkg.install'](sources=[
            {'repo': info['newrelic_url']}
        ]))
        logging.info(caller.sminion.functions['pkg.install'](
            info['newrelic_package'],
            require=[{'pkg': info['newrelic_url']}]))
        logging.info(
            caller.sminion.functions['cmd.run'](info['newrelic_license_cmd']))
        logging.info(
            caller.sminion.functions['cmd.run'](info['newrelic_start_cmd']))
        logging.info(
            caller.sminion.functions['cmd.run'](info['newrelic_chkconfig_cmd'])
        )
