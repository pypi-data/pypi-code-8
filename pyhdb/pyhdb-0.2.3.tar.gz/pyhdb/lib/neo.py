
# ./neo.sh open-db-tunnel -h hanatrial.ondemand.com -a p1941306070trial -u rh@ralph-heinkel.com -i ralhei1
import os
import re
import sys
import getpass
import ConfigParser
import pexpect

NEO_CMD = 'neo.sh'
NEO_INI = 'neo.ini'
NEO_INI_SECTION = 'neo'

NEO_OUTPUT_MAPPING = {
    'Host name': 'host',
    'User': 'user',
    'Password': 'password',
    'XXX': 'port'  # not part of neo's output, but put in here for completeness
}

# Compose regexes to match lines from neo and to extract parameters from there:
NEO_OUTPUT_REGEXES = {re.compile(r'\s*%s\s+:\s+(\w+)' % k): v for k, v in NEO_OUTPUT_MAPPING.iteritems()}


def open_tunnel(host=None, account=None, instance=None, user=None, passwd=None, ini_file=NEO_INI, verbose=False):
    vals = dict(host=host, account=account, instance=instance, user=user, passwd=passwd)
    cp = _load_neo_ini(vals, ini_file)
    if not cp.has_option(NEO_INI_SECTION, 'cmd'):
        cp.set('neo', 'cmd', NEO_CMD)

    hana_params = dict(cp.items(NEO_INI_SECTION))

    cmd = '%(cmd)s open-db-tunnel -h %(host)s -a %(account)s -u %(user)s -i %(instance)s' % hana_params
    child = pexpect.spawn(cmd, maxread=5000)
    # import sys; child.logfile = sys.stdout
    child.expect('Password for your user:')
    passwd = hana_params['passwd'] or getpass.getpass('HANA cloud platform password: ')
    child.sendline(passwd)

    child.expect('Tunnel opened')
    verbose and sys.stdout.write(child.after)

    hana_params = {'port': 30015}
    line = child.readline()
    while not line.startswith('This tunnel will close automatically'):
        verbose and sys.stdout.write(line)
        for regex, hana_param in NEO_OUTPUT_REGEXES.iteritems():
            m = regex.match(line)
            if m:
                hana_params[hana_param] = m.group(1)
                break
        line = child.readline()

    # make sure that all parameters have been found:
    assert set(NEO_OUTPUT_MAPPING.values()) == set(hana_params.keys()), \
        'Not all params retrieved from neo, got: %r' % hana_params
    verbose and sys.stdout.write(line)
    return NeoTunnel(child, hana_params, verbose)


class NeoTunnel(object):
    """Thin wrapper for a neo expect child process which implements a proper shutdown within the close() method"""
    def __init__(self, neo_expect_child, hana_params, verbose):
        self._neo_expect_child = neo_expect_child
        self._verbose = verbose
        # public attribute to obtain hana parameters
        self.hana_params = hana_params

    def close(self):
        child = self._neo_expect_child
        child.sendline('')
        child.expect('Confirm that you want to close the tunnel')
        child.sendline('y')
        try:
            child.expect('Tunnel closed', timeout=7)
            self._verbose and sys.stdout.write(child.after)  # print 'tunnel closed' message
        except pexpect.TIMEOUT:
            child.close(force=True)

    def interact(self):
        self._neo_expect_child.interact()

    def connect_hana(self):
        import pyhdb
        return pyhdb.connect(**self.hana_params)

    def __del__(self):
        try:
            self.close()
        except StandardError:
            pass


def _load_neo_ini(config_values, ini_file):
    fp = None
    prev_dir = None
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    while cur_dir != prev_dir:
        try:
            fp = open(os.path.join(cur_dir, ini_file))
        except IOError, msg:
            if 'No such file or directory' not in str(msg):
                # some other error, raise again:
                raise
            cur_dir, prev_dir = os.path.dirname(cur_dir), cur_dir
        else:
            break
    cp = ConfigParser.ConfigParser(defaults=config_values)
    if fp:
        cp.readfp(fp, ini_file)
    else:
        cp.add_section(NEO_INI_SECTION)

    for k, v in config_values.iteritems():
        if v:
            cp.set(NEO_INI_SECTION, k, v)
    return cp


def _write_hana_ini(hana_ini, config_values):
    hana_cp = ConfigParser.ConfigParser()
    hana_cp.add_section(section)
    for param, value in config_values.iteritems():
        hana_cp.set(section, param, value)
    hana_cp.write(open(hana_ini, 'w'))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Neo')
    parser.add_argument('neo_ini', nargs='?', default='neo.ini', help='Name of neo ini file. Default="neo.ini"')
    parser.add_argument('-o', dest='hana_ini', help='Name of hana ini file to be written"')
    parser.add_argument('-q', dest='quiet', default=False, action='store_true', help='Suppress verbose information"')
    args = parser.parse_args()
    section = 'hana'
    neotunnel = open_tunnel(ini_file=args.neo_ini, verbose=not args.quiet)
    if args.hana_ini:
        _write_hana_ini(args.hana_ini, neotunnel.hana_params)
        (not args.quiet) and sys.stdout.write('Wrote %s\n' % args.hana_ini)
    neotunnel.interact()
