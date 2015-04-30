
# ./neo.sh open-db-tunnel -h hanatrial.ondemand.com -a p1941306070trial -u rh@ralph-heinkel.com -i ralhei1
import os
import getpass
import ConfigParser
import pexpect

NEO_SH = 'neo.sh'
NEO_INI = 'neo.ini'
NEO_INI_SECTION = 'neo'


def connect(host=None, account=None, instance=None, user=None, passwd=None):
    vals = locals()
    cp = _load_neo_ini(vals)
    if not cp.get(NEO_INI_SECTION, 'cmd'):
        cp.set('neo', 'cmd', NEO_SH)

    params = dict(cp.items(NEO_INI_SECTION))

    cmd = '%(cmd)s open-db-tunnel -h %(host)s -a %(account)s -u %(user)s -i %(instance)s' % params
    child = pexpect.spawn(cmd, maxread=5000)
    child.expect('Password for your user:')
    passwd = params['passwd'] or getpass.getpass('HANA cloud platform password: ')
    child.sendline(passwd)

    child.expect('Tunnel opened')
    b_output = child.before
    a_output = child.aftercd
    print '---'
    print b_output
    print '---'
    print a_output
    print '------'
    child.expect('Host name\d+: \w+\r\n')
    print 'hostline', child.after


    child.interact()


def _load_neo_ini(config_values):
    fp = None
    prev_dir = None
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    while cur_dir != prev_dir:
        try:
            fp = open(os.path.join(cur_dir, NEO_INI))
        except IOError, msg:
            if 'No such file or directory' not in str(msg):
                # some other error, raise again:
                raise
            cur_dir, prev_dir = os.path.dirname(cur_dir), cur_dir
        else:
            break
    cp = ConfigParser.ConfigParser(defaults=config_values)
    if fp:
        cp.readfp(fp, NEO_INI)
    else:
        cp.add_section(NEO_INI_SECTION)
    for k, v in config_values.iteritems():
        if v:
            cp.set(NEO_INI_SECTION, k, v)
    return cp


if __name__ == '__main__':
    connect()
