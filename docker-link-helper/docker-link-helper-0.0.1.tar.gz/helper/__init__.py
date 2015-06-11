#!/usr/bin/env python
from __future__ import print_function
import argparse
import os
import re
import collections
import sys

__author__ = 'tback'

CHEVRON_MARKER = lambda x: '<{0}>'.format(x)
NOP_MARKER = lambda x: x
PIPE_MARKER = lambda x: '|{0}|'.format(x)
VAR_MARKER = lambda x: '${0}'.format(x)


def replace_many(string, replacements, marker_function=NOP_MARKER):
    """
    :param string:
    :param replacements:
    :return:
    http://stackoverflow.com/a/6117124

    >>> replace_many('A_XX A B XAX', {'A': 'a', 'B': 'b'})
    'a_XX a b XaX'

    >>> replace_many('A_XX <A><B> XAX', {'A': 'a', 'B': 'b'}, CHEVRON_MARKER)
    'A_XX ab XAX'

    """
    # use these three lines to do the replacement
    rep = dict((re.escape(marker_function(k)), v) for k, v in replacements.items())
    pattern = re.compile("|".join(x for x in rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], string)


def file_replace(paths, variables):
    """
    :param variables:
    :param paths:
    :return:

    >>> import tempfile, os
    >>> fd, name = tempfile.mkstemp()
    >>> os.write(fd, b'A_XX <A><B> XAX')
    15
    >>> os.close(fd)
    >>> file_replace((name, ), {'A': 'a', 'B': 'b'})
    >>> with open(name) as f:
    ...     f.read()
    'A_XX ab XAX'
    >>> os.remove(name)


    >>> import tempfile, os
    >>> fd, name = tempfile.mkstemp()
    >>> os.write(fd, b'A_XX <A><B> XAX')
    15
    >>> os.close(fd)
    >>> file_replace(name, {'A': 'a', 'B': 'b'})
    >>> with open(name) as f:
    ...     f.read()
    'A_XX ab XAX'
    >>> os.remove(name)

    """
    if type(paths) is str:
        paths = (paths, )

    for path in paths:
        with open(path, 'r+') as file:
            content = file.read()
            s = replace_many(content, variables, CHEVRON_MARKER)
            file.seek(0)
            file.write(s)
            file.truncate()


def get_links(environment):
    """
    :param environment:
    :return:

    >>> get_links({'MYSQL_PROTO': 'tcp'}) == set(())
    True


    >>> get_links(test_env()) == set(('HIGHWAY', 'MYSQL', 'SPHINX',  'REDIS'))
    True
    """
    candidates = collections.defaultdict(set)

    for k, v in environment.items():
        prefix, unused, unused = k.partition('_')
        unused, unused, suffix = k.rpartition('_')
        if suffix not in ('PROTO', 'ADDR', 'PORT'):
            continue

        candidates[prefix].add(suffix)

    links = []
    for p, suffixes in candidates.items():
        if suffixes.issuperset(set(('PROTO', 'ADDR', 'PORT'))):
            links.append(p)

    return set(links)


def get_link_vars(links, environment):
    """
    :param links:
    :param environment:
    :return:
    >>> get_link_vars( \
            ('MYSQL', ), \
            { \
                "REDIS_PORT_6379_TCP_PROTO": "tcp", \
                "MYSQL_1_PORT_3306_TCP": "tcp://172.17.0.2:3306", \
                "MYSQL_ENV_MYSQL_DATABASE": "highway", \
                "HOSTNAME": "f32ac6d8d1df", \
                "MYSQL_ENV_MYSQL_ROOT_PASSWORD": "foo", \
                "REDIS_ENV_REDIS_DOWNLOAD_SHA1": "45f134113fb3d75b8c37f7968e46565a70800091", \
            } \
       ) == { \
          "MYSQL_1_PORT_3306_TCP": "tcp://172.17.0.2:3306", \
          "MYSQL_ENV_MYSQL_DATABASE": "highway", \
          "MYSQL_ENV_MYSQL_ROOT_PASSWORD": "foo", \
       }
    True
    """
    link_vars = {}
    for key, value in environment.items():
        prefix, _, _ = key.partition('_')
        if prefix in links:
            link_vars[key] = value
    return link_vars


def test_env():
    return {
        "SPHINX_PORT_9306_TCP_PORT": "9306",
        "REDIS_ENV_REDIS_DOWNLOAD_URL": "http://download.redis.io/releases/redis-2.8.20.tar.gz",
        "REDIS_PORT_6379_TCP_PROTO": "tcp",
        "MYSQL_1_PORT_3306_TCP": "tcp://172.17.0.2:3306",
        "MYSQL_ENV_MYSQL_DATABASE": "highway",
        "HOSTNAME": "f32ac6d8d1df",
        "MYSQL_ENV_MYSQL_ROOT_PASSWORD": "foo",
        "REDIS_ENV_REDIS_DOWNLOAD_SHA1": "45f134113fb3d75b8c37f7968e46565a70800091",
        "MYSQL_1_ENV_MYSQL_USER": "highway",
        "HIGHWAY_SPHINX_1_PORT_9306_TCP_PORT": "9306",
        "MYSQL_1_ENV_PERCONA_VERSION": "5.5.43-rel37.2-1.wheezy",
        "HIGHWAY_MYSQL_1_PORT_3306_TCP_ADDR": "172.17.0.2",
        "MYSQL_1_PORT_3306_TCP_PROTO": "tcp",
        "SPHINX_PORT_9306_TCP_ADDR": "172.17.0.3",
        "REDIS_1_PORT_6379_TCP": "tcp://172.17.0.1:6379",
        "SPHINX_PORT_9306_TCP_PROTO": "tcp",
        "REDIS_1_PORT_6379_TCP_PORT": "6379",
        "REDIS_NAME": "/highway_fpm_1/redis",
        "MYSQL_ENV_PERCONA_VERSION": "5.5.43-rel37.2-1.wheezy",
        "HIGHWAY_SPHINX_1_PORT_9306_TCP_PROTO": "tcp",
        "MYSQL_1_PORT_3306_TCP_PORT": "3306",
        "HIGHWAY_MYSQL_1_ENV_MYSQL_DATABASE": "highway",
        "HIGHWAY_MYSQL_1_PORT_3306_TCP": "tcp://172.17.0.2:3306",
        "REDIS_1_PORT": "tcp://172.17.0.1:6379",
        "REDIS_PORT_6379_TCP_ADDR": "172.17.0.1",
        "LS_COLORS": "",
        "SPHINX_1_PORT_9306_TCP": "tcp://172.17.0.3:9306",
        "HIGHWAY_REDIS_1_PORT": "tcp://172.17.0.1:6379",
        "REDIS_1_PORT_6379_TCP_PROTO": "tcp",
        "MYSQL_PORT_3306_TCP_PORT": "3306",
        "HIGHWAY_SPHINX_1_PORT": "tcp://172.17.0.3:9306",
        "REDIS_1_ENV_REDIS_DOWNLOAD_SHA1": "45f134113fb3d75b8c37f7968e46565a70800091",
        "MYSQL_1_ENV_PERCONA_MAJOR": "5.5",
        "REDIS_1_NAME": "/highway_fpm_1/redis_1",
        "REDIS_PORT_6379_TCP_PORT": "6379",
        "HIGHWAY_REDIS_1_ENV_REDIS_DOWNLOAD_URL": "http://download.redis.io/releases/redis-2.8.20.tar.gz",
        "HIGHWAY_REDIS_1_PORT_6379_TCP_PROTO": "tcp",
        "MYSQL_PORT_3306_TCP": "tcp://172.17.0.2:3306",
        "MYSQL_1_ENV_MYSQL_ROOT_PASSWORD": "foo",
        "SPHINX_PORT_9306_TCP": "tcp://172.17.0.3:9306",
        "MYSQL_ENV_MYSQL_USER": "highway",
        "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "PWD": "/var/www",
        "SPHINX_1_PORT_9306_TCP_ADDR": "172.17.0.3",
        "MYSQL_ENV_PERCONA_MAJOR": "5.5",
        "HIGHWAY_MYSQL_1_ENV_MYSQL_USER": "highway",
        "HIGHWAY_MYSQL_1_ENV_MYSQL_PASSWORD": "bar",
        "HIGHWAY_MYSQL_1_NAME": "/highway_fpm_1/highway_mysql_1",
        "REDIS_PORT_6379_TCP": "tcp://172.17.0.1:6379",
        "HIGHWAY_REDIS_1_NAME": "/highway_fpm_1/highway_redis_1",
        "MYSQL_ENV_MYSQL_PASSWORD": "bar",
        "HIGHWAY_MYSQL_1_PORT": "tcp://172.17.0.2:3306",
        "REDIS_1_ENV_REDIS_VERSION": "2.8.20",
        "SPHINX_1_PORT_9306_TCP_PORT": "9306",
        "MYSQL_1_ENV_MYSQL_DATABASE": "highway",
        "HIGHWAY_MYSQL_1_PORT_3306_TCP_PORT": "3306",
        "HIGHWAY_REDIS_1_ENV_REDIS_DOWNLOAD_SHA1": "45f134113fb3d75b8c37f7968e46565a70800091",
        "HIGHWAY_REDIS_1_ENV_REDIS_VERSION": "2.8.20",
        "SHLVL": "1",
        "HOME": "/root",
        "REDIS_PORT": "tcp://172.17.0.1:6379",
        "HIGHWAY_REDIS_1_PORT_6379_TCP": "tcp://172.17.0.1:6379",
        "SPHINX_NAME": "/highway_fpm_1/sphinx",
        "MYSQL_NAME": "/highway_fpm_1/mysql",
        "MYSQL_PORT_3306_TCP_PROTO": "tcp",
        "HIGHWAY_SPHINX_1_PORT_9306_TCP": "tcp://172.17.0.3:9306",
        "HIGHWAY_REDIS_1_PORT_6379_TCP_PORT": "6379",
        "SPHINX_1_PORT_9306_TCP_PROTO": "tcp",
        "HIGHWAY_MYSQL_1_ENV_PERCONA_VERSION": "5.5.43-rel37.2-1.wheezy",
        "affinity:container=": "d62c4f28416295507bb34e31d0b2f8e8326e5718a0d58210da50e58ad4d60657",
        "MYSQL_PORT_3306_TCP_ADDR": "172.17.0.2",
        "SPHINX_1_PORT": "tcp://172.17.0.3:9306",
        "MYSQL_1_PORT": "tcp://172.17.0.2:3306",
        "HIGHWAY_SPHINX_1_NAME": "/highway_fpm_1/highway_sphinx_1",
        "HIGHWAY_MYSQL_1_PORT_3306_TCP_PROTO": "tcp",
        "REDIS_ENV_REDIS_VERSION": "2.8.20",
        "HIGHWAY_MYSQL_1_ENV_PERCONA_MAJOR": "5.5",
        "REDIS_1_PORT_6379_TCP_ADDR": "172.17.0.1",
        "LESSOPEN": "| /usr/bin/lesspipe %s",
        "SPHINX_1_NAME": "/highway_fpm_1/sphinx_1",
        "MYSQL_1_NAME": "/highway_fpm_1/mysql_1",
        "HIGHWAY_MYSQL_1_ENV_MYSQL_ROOT_PASSWORD": "foo",
        "HIGHWAY_REDIS_1_PORT_6379_TCP_ADDR": "172.17.0.1",
        "MYSQL_1_PORT_3306_TCP_ADDR": "172.17.0.2",
        "SPHINX_PORT": "tcp://172.17.0.3:9306",
        "MYSQL_PORT": "tcp://172.17.0.2:3306",
        "LESSCLOSE": "/usr/bin/lesspipe %s %s",
        "HIGHWAY_SPHINX_1_PORT_9306_TCP_ADDR": "172.17.0.3",
        "REDIS_1_ENV_REDIS_DOWNLOAD_URL": "http://download.redis.io/releases/redis-2.8.20.tar.gz",
        "MYSQL_1_ENV_MYSQL_PASSWORD": "bar",
        "_": "/usr/bin/env",
    }


def parse_args():
    parser = argparse.ArgumentParser(
        description='Search for occurrences of docker links and replace them by their value'
    )
    parser.add_argument('-l', '--link', dest='links', default=[], action='append', help='mandatory links')
    parser.add_argument('-s', '--show', action='store_true', help='show values of docker links')
    parser.add_argument('-t', '--test_env', action='store_true', help='use static test environment')
    parser.add_argument('files', nargs='+', help='search for links in these files')
    return parser.parse_args()


def get_env(test_environment):
    if test_environment:
        return test_env()
    return os.environ


def main():
    args = parse_args()
    if args.run_tests:
        import doctest
        doctest.testmod()
        sys.exit(0)

    env = get_env(args.test_env)
    if args.show:
        for key, value in get_link_vars(get_links(env), env).items():
            print('{key}={value}'.format(key=key, value=value))
        sys.exit(0)
    required_links = set(x.upper() for x in args.links)
    links = get_links(env)
    missing_links = required_links - links
    if missing_links:
        print('Link(s) to {0} not present. Quitting'.format(', '.join(missing_links)), file=sys.stderr)
        sys.exit(1)

    env_links = get_links(env)
    link_vars = get_link_vars(env_links, env)
    file_replace(args.files, link_vars)

if __name__ == '__main__':
    main()
