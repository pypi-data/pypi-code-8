import begin
import mechanize
import salt.config
import salt.client
import logging
import glob


def salt_init():
    opts = salt.config.apply_minion_config()
    opts['file_client'] = 'local'
    caller = salt.client.Caller(mopts=opts)
    return caller

@begin.logging
def install_redhat(key):
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

@begin.logging
def install_debian(key):
    caller = salt_init()
    info = dict(
        apt_repo_cmd = 'echo deb http://apt.newrelic.com/debian/ newrelic non-free >> /etc/apt/sources.list.d/newrelic.list',
        repo_trust_cmd = 'wget -O- https://download.newrelic.com/548C16BF.gpg | apt-key add -',
        apt_update_cmd = 'apt-get update',
        newrelic_package='newrelic-sysmond',
        newrelic_license_cmd=r"nrsysmond-config --set license_key='%(l_key)s'"
        % {'l_key': key},
        newrelic_start_cmd=r"/etc/init.d/newrelic-sysmond restart",
        newrelic_chkconfig_cmd='update-rc.d newrelic-sysmond defaults'
    )
    logging.info(
        caller.sminion.functions['pkg.install'](name='wget')
    )
    logging.info(
        caller.sminion.functions['cmd.run'](info['apt_repo_cmd']))
    logging.info(
        caller.sminion.functions['cmd.run'](info['repo_trust_cmd']))
    logging.info(
        caller.sminion.functions['cmd.run'](info['apt_update_cmd']))
    logging.info(caller.sminion.functions['pkg.install'](
        info['newrelic_package'],
        require=[{'cmd': info['apt_update_cmd']}]))
    logging.info(
        caller.sminion.functions['cmd.run'](info['newrelic_license_cmd']))
    logging.info(
        caller.sminion.functions['cmd.run'](info['newrelic_start_cmd']))
    logging.info(
        caller.sminion.functions['cmd.run'](info['newrelic_chkconfig_cmd'])
    )

@begin.logging
def install_linux(key):
    caller = salt_init()
    br = mechanize.Browser()
    br.open('http://download.newrelic.com/server_monitor/release/')
    info = dict(
        newrelic_url = br.find_link(text_regex='.*linux.*gz').absolute_url,
        newrelic_license_cmd=r"nrsysmond-config --set license_key='%(l_key)s'"
        % {'l_key': key},
    )
    logging.info(
        caller.sminion.functions['file.remove']('/usr/local/src/newrelic.tgz'))
    logging.info(
        caller.sminion.functions['file.remove']('/usr/local/src/newrelic.tar'))
    logging.info(
        caller.sminion.functions['cp.get_url'](dest='/usr/local/src/newrelic.tgz', path=info['newrelic_url']))
    logging.info(
        caller.sminion.functions['archive.gunzip']('/usr/local/src/newrelic.tgz'))
    logging.info(
        caller.sminion.functions['archive.tar']('xf', sources=[], tarfile='/usr/local/src/newrelic.tar', dest='/usr/local/src/'))
    logging.info(
        caller.sminion.functions['file.mkdir']('/etc/newrelic'))
    logging.info(
        caller.sminion.functions['file.mkdir']('/var/log/newrelic'))
    logging.info(
        caller.sminion.functions['cmd.run']('pkill -9 nrsysmond'))
    logging.info(
        caller.sminion.functions['file.copy'](src=glob.glob('/usr/local/src/newrelic-sysmond-*-linux')[0] + '/daemon/nrsysmond.x64', dst='/usr/local/bin/nrsysmond', remove_existing=True))
    logging.info(
        caller.sminion.functions['file.copy'](src=glob.glob('/usr/local/src/newrelic-sysmond-*-linux')[0] + '/scripts/nrsysmond-config', dst='/usr/local/bin/nrsysmond-config', remove_existing=True))
    logging.info(
        caller.sminion.functions['file.copy'](src=glob.glob('/usr/local/src/newrelic-sysmond-*-linux')[0] + '/nrsysmond.cfg', dst='/etc/newrelic/nrsysmond.cfg', remove_existing=True))
    logging.info(
        caller.sminion.functions['cmd.run'](info['newrelic_license_cmd']))
    logging.info(
        caller.sminion.functions['cmd.run']('/usr/local/bin/nrsysmond -c /etc/newrelic/nrsysmond.cfg'))
    
