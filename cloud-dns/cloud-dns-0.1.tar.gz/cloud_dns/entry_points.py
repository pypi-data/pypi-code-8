
import argparse
import itertools
import logging
import os
import os.path as osp
import sys

from .config import (
    DEFAULT_CONFIG_PATH,
    GSDriver,
    GStorageKeybaseProfile,
    Profile,
    Profiles,
)

def config_pull(profile, bucket, identity, **kwargs):
    keybase_id = identity.split("://", 1)
    profile = GStorageKeybaseProfile(profile, GSDriver, bucket, keybase_id, **kwargs)
    profile.pull()

def config_push(profile, bucket, **kwargs):
    """Push encryted configuration of a profile on Google Storage

    :param profile: profile to push (a directory in ~/.config/cloud-dns/)
    :param bucket: the destination Google Storage bucket
    :param config_dir: absolute path to Cloud DNS root config dir
    (default ~/.config/cloud-dns)
    """
    profile = GStorageKeybaseProfile(profile, GSDriver, bucket, **kwargs)
    profile.push()

def update_etc_hosts_file(hostip_tuples, output_file=None):
    """Update specified nodes in /etc/hosts
    Previous content is not lost

    :param hostip_tuples: generator of tuple (host, ip)
    :param output_file: destination file, default is /etc/hosts
    """
    BEGIN_MARKUP = '# CloudDNS prelude - DO NOT REMOVE\n'
    END_MARKUP = '# CloudDNS epilogue - DO NOT REMOVE\n'
    output_file = output_file or '/etc/hosts'
    if not osp.isfile(output_file):
        with open(output_file, 'a'):
            os.utime(output_file, None)
    with open(output_file, 'r+') as etc_hosts:
        lines  = etc_hosts.readlines()
        etc_hosts.seek(0)
        etc_hosts.truncate(0)
        previous_content_replaced = False
        between_markups = False
        for line in lines:
            if not between_markups:
                if line == BEGIN_MARKUP:
                    between_markups = True
                etc_hosts.write(line)
            else:
                if line == END_MARKUP:
                    previous_content_replaced = True
                    for hosts, ip in hostip_tuples:
                        etc_hosts.write("{} {}\n".format(ip.ljust(15, ' '), ' '.join(hosts)))
                    between_markups = False
                    etc_hosts.write(line)
        if not previous_content_replaced:
            etc_hosts.write(BEGIN_MARKUP)
            for host, ip in hostip_tuples:
                etc_hosts.write("{} {}\n".format(ip.ljust(15, ' '), host))
            etc_hosts.write(END_MARKUP)

def etc_hosts_update(output_file=None, **kwargs):
    """Update /etc/hosts with all nodes available in configured projects

    :param output_file: destination file, default is /etc/hosts
    """
    update_etc_hosts_file(etc_hosts_generator(**kwargs), output_file)

def etc_hosts_generator(**kwargs):
    """Provides a generator of tuple (hosts, ip) for all nodes registered
    in the configured projects
    """
    generators = []
    for profile in Profiles(**kwargs).list():
        for project in profile.projects.values():
            generators.append(project.get_hostip_tuples())
    return itertools.chain(*generators)

def etc_hosts_list(**kwargs):
    """Print to standard output nodes available in all configured projects
    """
    for hosts, ip in etc_hosts_generator(**kwargs):
        print "{} {}".format(ip.ljust(15, ' '), ' '.join(hosts))


def cloud_dns(args=None):
    """cloud-dns entry point"""
    args = args or sys.argv[1:]
    from .version import version
    parser = argparse.ArgumentParser(
        description="DNS utilities on top of Apache libcloud"
    )
    parser.add_argument(
        '-V', '--version',
        action='version',
        version='%(proj)s ' + version
    )
    parser.add_argument(
        '-v', '--verbose',
        action='count',
        help='Verbose mode, -vv for more details, -vvv for 3rd-parties logs as well'
    )
    parser.add_argument(
        '-c', '--config-dir',
        help='Specify config root path [default: %(default)s]',
        dest='config_path',
        default=DEFAULT_CONFIG_PATH
    )
    subparsers = parser.add_subparsers(help='top commands')
    config_parser = subparsers.add_parser(
        'config',
        help='Manipulate DNS cloud configuration'
    )
    config_subparsers = config_parser.add_subparsers(help='config commands')
    config_push_parser = config_subparsers.add_parser(
        'push',
        help='Push configuration to Google Storage'
    )
    config_push_parser.add_argument('profile')
    config_push_parser.add_argument('bucket')
    config_push_parser.set_defaults(func=config_push)

    config_pull_parser = config_subparsers.add_parser(
        'pull',
        help='Retrieve latest configuration from Google Storage'
    )
    config_pull_parser.add_argument('profile')
    config_pull_parser.add_argument('bucket')
    config_pull_parser.add_argument(
        "identity",
        help='Keybase signature to use to decrypt configuration, for instance: github://tristan0x'
    )

    etc_hosts_parser = subparsers.add_parser(
        'etc-hosts',
        help='Manipulate DNS cloud configuration'
    )
    etc_hosts_subparsers = etc_hosts_parser.add_subparsers(help='etc-hosts commands')
    etc_hosts_update_parser = etc_hosts_subparsers.add_parser(
        "update",
        help='Required super-user privileges'
    )
    etc_hosts_update_parser.add_argument(
        '-o', '--ouput',
        dest='output_file',
        default='/etc/hosts',
        help='Output file [default: %(default)s]'
    )
    etc_hosts_update_parser.set_defaults(func=etc_hosts_update)
    etc_hosts_list_parser = etc_hosts_subparsers.add_parser(
        "list",
        help="List nodes in /etc/hosts format"
    )
    etc_hosts_list_parser.set_defaults(func=etc_hosts_list)

    config_pull_parser.set_defaults(func=config_pull)
    args = parser.parse_args(args)
    log_level = logging.WARN
    third_parties_log_level = logging.WARN
    if args.verbose:
        if args.verbose > 1:
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO
        if args.verbose >= 3:
            third_parties_log_level = logging.INFO
    logging.basicConfig(level=log_level)
    for logger in [
        'boto',
        'gnupg',
        'oauth2client',
        'oauth2_client',
        'requests',
    ]:
        logging.getLogger(logger).setLevel(third_parties_log_level)

    args.func(**vars(args))
