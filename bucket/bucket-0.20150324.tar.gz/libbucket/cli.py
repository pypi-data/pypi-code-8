# -*- coding: utf-8; mode: python -*-

import sys
import os
import getpass
import logging
import webbrowser
import argparse
# import OpenSSL

logging.basicConfig()
logger = logging.getLogger('bucket')

from commodity.args import parser, args
from commodity.thread_ import SimpleThreadPool

import api
import exceptions as exc


default_pub_keyfile = '~/.ssh/id_rsa.pub'


def canceled():
    msg('-- canceled')
    sys.exit(1)


def msg(text, fd=None):
    fd = fd or args.stdout
    fd.write(str(text) + '\n')

# import math
# http://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
# def convertSize(size):
#     size_name = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
#     i = int(math.floor(math.log(size, 1024)))
#     p = math.pow(1024, i)
#     s = round(size / p, 2)
#     if (s > 0):
#         return '%s %s' % (s, size_name[i])
#     else:
#         return '0B'


def convert_size(bytes):
    k = float(bytes) / 1000
    return "{:.0f} KB".format(k)


class readable_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values

        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError(
                "readable_dir: '{0}' is not a valid path".format(prospective_dir))

        if os.access(prospective_dir, os.R_OK):
            setattr(namespace, self.dest, prospective_dir)
            return

        raise argparse.ArgumentTypeError(
            "readable_dir: '{0}' is not a readable dir".format(prospective_dir))


def repo2full_name(repo):
    if repo is None:
        repo = api.Repo.from_dir(args.manager).full_name

    if repo.count('/') != 1 or repo.endswith('/'):
        raise exc.WrongRepoPathFormat()

    owner, slug = repo.split('/')
    if not owner:
        if args.account is None:
            raise exc.OwnerRequired()

        owner = args.account.username

    return owner + '/' + slug


def get_repo():
    full_name = repo2full_name(args.repo)

    try:
        return api.Repo.from_remote(args.manager, full_name)

    except exc.BasicException:
        if not args.repo.startswith('/'):
            raise

        return get_alternate_repo(args.repo)


def get_alternate_repo(repo):
    full_name = repo2full_name(args.repo)
    owner, name = full_name.split('/')

    owners = [owner] + get_config_owners(owner)
    for owner in owners:
        try:
            return api.Repo.from_remote(args.manager, owner + '/' + name)
        except exc.BasicException:
            logger.info("trying {}: FAIL".format(full_name))

    raise exc.NoSuchRepo(full_name)


def get_config_owners(owner):
    try:
        accounts = args.ui.account.values()
    except KeyError:
        return []

    retval = []
    for account in accounts:
        if account.count(':') > 1:
            logger.warning("wrong account format: '%s'", account)

        retval.append(account.split(':')[0])

    if owner in retval:
        retval.remove(owner)

    return retval


def repo_info():
    repo = get_repo()

    for atr in 'full_name name description scm is_private size updated_on'.split():
        key = atr.replace('_', ' ') + ':'
        value = str(repo[atr])
        if not value.strip():
            continue

        msg("{:12} {}".format(key, value))


def repo_create():
    full_name = repo2full_name(args.repo)

    scm = 'git' if args.create_git else 'hg'

    if not args.create_yes:
        answer = raw_input("create '{}' ({}) repository? (Y/n): ".format(full_name, scm))
        if answer.lower() not in ['', 'y', 'yes']:
            canceled()

    else:
        msg("creating '{}' ({})".format(full_name, scm))

    args.manager.repo_create(full_name, scm=scm)

    if args.create_local:
        msg("pushing local content to '{}'".format(full_name))
        repo = api.Repo.from_dir(args.manager)
        repo.push(args.create_proto)


def confirm_irrecoverable_operation():
    answer = raw_input("This is an IRRECOVERABLE operation!!\nAre you sure? (write uppercase 'yes'): ")
    if answer != 'YES':
        canceled()


def repo_delete():
    full_name = repo2full_name(args.repo)

    if not args.delete_yes:
        confirm_irrecoverable_operation()

    msg("Deleting '{}'\n".format(full_name))
    args.manager.repo_delete(full_name)


def repo_ls():
    # FIXME: function
    if args.owner is None:
        if args.account.is_anonymous():
            raise exc.OwnerRequired()

        args.owner = args.account.username

    nrepos = args.manager.get_repo_amount(args.owner)
    msg("-- owner '{}' has {} repositories".format(args.owner, nrepos))

    names = args.manager.list_repo_names(args.owner, step=put_point)
    print

    if not any([args.ls_access, args.ls_scm, args.ls_size]):
        for i in names:
            msg(i)
        return

    item = u'{full_name}'
    if args.ls_access:
        item = u'{access:7} - ' + item

    if args.ls_scm:
        item = u'{scm:3} - ' + item

    total_size = 0
    if args.ls_size:
        item = u'{size:>13} - ' + item

    lines = []
    for repo in args.manager.names2repos(names):
        repodata = repo.as_dict()
        repodata['size'] = convert_size(repodata['size'])
        line = item.format(**repodata) + u'\n'
        lines.append(line)

        if args.ls_size:
            total_size += repo['size']

    for line in lines:
        args.stdout.write(line.encode('utf-8'))

    if args.ls_size:
        msg("\n-- total storage: {}".format(convert_size(total_size)))


def repo_clone():
    repo = get_repo()

    destdir = os.path.join(args.clone_destdir or os.path.join(os.getcwd()), repo.slug)

    msg("Clonning '{}' to '{}' ({}/{}) ".format(
        repo.full_name, destdir, repo.scm, args.clone_proto))

    if not repo.clone(args.clone_proto, destdir):
        msg("  repository already cloned, updating")


def relpath(name):
    retval = os.path.relpath(name)
    if retval.startswith('..'):
        return name

    return retval


def put_point():
    args.stderr.write('.')
    args.stderr.flush()


def repo_sync():
    def sync_single_repo(repo):
        destdir = os.path.join(args.clone_destdir or os.path.join(os.getcwd()), repo.slug)
        proto_info = "({}/{})".format(repo.scm, args.clone_proto)

        msg("Syncing {0:11} {1}".format(
            proto_info, repo.full_name, relpath(destdir)))

        try:
            repo.clone(args.clone_proto, destdir)
        except (exc.CloneError, exc.UnrelatedContent) as e:
            logger.error(e)

        # , OpenSSL.SSL.ZeroReturnError

    # FIXME: same as repo_ls
    owner = args.sync_owner
    if owner is None:
        if args.account.is_anonymous():
            raise exc.OwnerRequired()

        owner = args.account.username

    nrepos = args.manager.get_repo_amount(owner)
    msg("-- owner '{}' has {} repositories".format(owner, nrepos))
    msg("-- target directory is: '{}'".format(os.path.abspath(args.clone_destdir)))

    repos = args.manager.repo_list(owner, step=put_point)
    print
    # for repo in repos:
    #     sync_single_repo(repo)
    pool = SimpleThreadPool(10)
    pool.map(sync_single_repo, repos)


def repo_website():
    url = get_repo().webpage

    if args.site_settings:
        url += '/admin'

    msg("Openning '{}'".format(url))
    webbrowser.open(url)


def repo_status():
    bb_repos = []
    not_bb_repos = []
    not_repos = []

    for d in os.listdir(args.clone_destdir):
        put_point()

        path = os.path.join(args.clone_destdir, d)
        if not os.path.isdir(path):
            continue

        try:
            local_repo = api.Repo.from_dir(path)
            if local_repo.path:
                bb_repos.append(local_repo)
            else:
                not_bb_repos.append(local_repo)

        except exc.NoSuchRepo:
            not_repos.append(d)

    print

    for r in bb_repos:
        msg("+ {:<3} - {:<30} - {}".format(r.scm, os.path.split(r.dirname)[1], r.path))

    msg("\n -- Not bitbucket.org repos:")
    for r in not_bb_repos:
        msg("- {:<3} - {:<30} - {}".format(r.scm, os.path.split(r.dirname)[1], r.origin))

    msg('\n -- Not a repository:')
    for r in not_repos:
        msg(r)


def ssh_ls():
    msg("SSH public keys for user: %s" % args.account.username)
    key_summaries = args.manager.key_manager.list_key_summaries()
    if not key_summaries:
        msg("No keys found")
        return

    print str.join('\n', key_summaries)


def ssh_add():
    pk = args.manager.key_manager.add_key(args.ssh_keylabel, args.ssh_keyfile)
    msg('PK for the uploaded key: %s' % pk)


def ssh_del():
    args.manager.key_manager.delete_key_by_label(args.ssh_keylabel)


## PARSER ##


def setup_parser():
    parser.add_argument('--account', '-a',
                        help='account in the form user[:pass] or config-key', type=str)
    parser.add_argument('--config', '-c',
                        help='process config file')
    parser.add_argument('--verbosity', '-v', action='count', default=0,
                        help='verbosity level')

    commands = parser.add_subparsers(dest='command')

    setup_parser_ls(commands)
    setup_parser_info(commands)
    setup_parser_create(commands)
    setup_parser_delete(commands)
    setup_parser_clone(commands)
    setup_parser_sync(commands)
    setup_parser_site(commands)
    setup_parser_status(commands)
    setup_parser_ssh(commands)


def setup_parser_ls(commands):
    subparser = create_subparser(commands, 'ls', func=repo_ls,
                                 help="list all repositories of the given owner")
    subparser.add_argument('owner', nargs='?',
                           help='Bitbucket repo owner [default:authenticated user]')

    subparser.add_argument('--size', '-s', dest='ls_size', action='store_true',
                           help='show repo size')
    subparser.add_argument('--access', '-a', dest='ls_access', action='store_true',
                           help='show repo access: public/private')
    subparser.add_argument('--scm', dest='ls_scm', action='store_true',
                           help='show scm: hg/git')


def setup_parser_info(commands):
    subparser = create_subparser(commands, 'info', func=repo_info,
                                 help='show detailed info about the given repository')
    subparser.add_argument('repo', nargs='?')


def setup_parser_create(commands):
    subparser = create_subparser(commands, 'create', func=repo_create,
                                 help="create a repository in bitbucket server")
    add_proto_args(subparser, 'create_proto')
    subparser.add_argument('repo')
    subparser.add_argument('--yes', '-y', dest='create_yes', action='store_true',
                           help="don't ask for confirmation")
    subparser.add_argument('--git', dest='create_git', action='store_true',
                           help='create a git repository')
    subparser.add_argument('--from-local', dest='create_local', action='store_true',
                           help="push current content to the created repo")

    # --hg
    # --public
    # --private
    # --desc
    # --clone


def setup_parser_delete(commands):
    subparser = create_subparser(commands, 'delete', func=repo_delete,
                                 help='delete de given repository')
    subparser.add_argument('repo')
    subparser.add_argument('--yes', '-y', dest='delete_yes', action='store_true',
                           help="don't ask for confirmation")


def add_proto_args(parser, dest):
    parser.add_argument('--https', dest=dest, action='store_const', const=api.PROTO_HTTPS,
                        help='use HTTPS to clone')
    parser.add_argument('--ssh', dest=dest, action='store_const', const=api.PROTO_SSH,
                        help='use SSH to clone')


def add_destdir_arg(parser):
    parser.add_argument(
        '--destdir', '-d', dest='clone_destdir', metavar='dirname',
        action=readable_dir,
        help='the directory where your repositories are')


def setup_parser_clone(commands):
    subparser = create_subparser(commands, 'clone', func=repo_clone,
                                 help="clone/update given repository")
    subparser.add_argument('repo', metavar='owner/repository',
                           help='repository to clone')
    add_proto_args(subparser, 'clone_proto')
    add_destdir_arg(subparser)


def setup_parser_sync(commands):
    subparser = create_subparser(commands, 'sync', func=repo_sync,
                                 help='clone/update a bunch of repositories')
    add_proto_args(subparser, 'clone_proto')
    add_destdir_arg(subparser)
    subparser.add_argument('--owner', '-o', dest='sync_owner',
                           help="sync all 'owner' repositories")


def setup_parser_site(commands):
    subparser = create_subparser(commands, 'site', func=repo_website,
                                 help="open bitbucket webpage for the repository")
    subparser.add_argument('repo', nargs='?')
    subparser.add_argument('--settings', '-s', dest="site_settings", action="store_true",
                           help="open settings page")


def setup_parser_status(commands):
    subparser = create_subparser(commands, 'st', func=repo_status,
                                 help="show status for your repository bunch")
    add_destdir_arg(subparser)


def setup_parser_ssh(commands):
    p = create_subparser(commands, 'ssh-ls', func=ssh_ls,
                         help='List your account SSH keys')

    p = create_subparser(commands, 'ssh-add', func=ssh_add,
                         help='Upload a SSH key to your account')
    p.add_argument('ssh_keylabel', metavar='keylabel',
                   help='the user-visible label on the key')
    p.add_argument('ssh_keyfile', metavar='keyfile', nargs='?',
                   type=argparse.FileType('r'),
                   help="public key file path [default: '{}']".format(
                       default_pub_keyfile))

    p = create_subparser(commands, 'ssh-del', func=ssh_del,
                         help='Delete a SSH key by label')
    p.add_argument('ssh_keylabel', metavar='keylabel',
                   help='key label. Run ssh-ls')


def create_subparser(root, name, func, help=""):
    cmd = root.add_parser(name, help=help)  # , argument_default=argparse.SUPPRESS)
    cmd.set_defaults(func=func)
    return cmd


def parse_args(argv=None, ns=None, stdout=None):
    argv = argv or sys.argv[1:]
    if isinstance(argv, (str, unicode)):
        argv = argv.split()

    load_config_file(argv)

    try:
        parser.parse_args(argv, ns)
    except argparse.ArgumentTypeError as e:
        logger.error(e)
        sys.exit(1)

    args.stdout = stdout or sys.stdout
    args.stderr = sys.stderr
    setup_verbosity()

    args.clone_proto = args.get('clone_proto') or api.PROTO_HTTPS

    args.account = setup_account(args.account)
    logger.info("Authenticated as: %s", args.account.username)
    args.manager = api.RepoManager(args.account)

    keyfile = os.path.expanduser(default_pub_keyfile)
    if os.path.exists(keyfile):
        args.ssh_keyfile = file(keyfile)


def load_config_file(argv):
    auxp = argparse.ArgumentParser(add_help=False)
    auxp.add_argument('--config', '-c', default=os.path.expanduser('~/.bucket'))
    values, pos = auxp.parse_known_args(argv)

    if not os.path.isfile(values.config):
        logger.error("bad file: %s", values.config)
    else:
        parser.load_config_file(values.config)


def setup_verbosity():
    try:
        level = [logging.WARNING, logging.INFO, logging.DEBUG][args.verbosity]
    except IndexError:
        level = logging.DEBUG

    logger.setLevel(level)
    if args.verbosity:
        print "logger level is:", logging.getLevelName(level)


def get_password(username):
    return getpass.getpass("{0}'s password: ".format(username))


def setup_account(account):
    if account is None:
        return api.Account()

    account = account.strip(':')
    nfields = account.count(':') + 1

    if nfields > 2:
        raise Exception("account argument ({}) wrong format: 'user:pass'".format(account))

    if nfields == 2:
        username, password = account.split(':')
    else:
        username = account
        password = get_password(account)

    return api.Account(username, password)


setup_parser()


def run():
    try:
        args.func()
        msg('-- ok')
    except exc.BasicException as e:
        print e

        if not args.verbosity:
            print "Try 'bucket -v'"
        sys.exit(1)
