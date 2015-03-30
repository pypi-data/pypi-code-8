import os
import re

import rdoupdate.core

from action import Action, Arg
from conf import cfg, cfg_files
import exception
import guess
from rdopkg.actionmods import copr as _copr
from rdopkg.actionmods import kojibuild
from rdopkg.actionmods import nightly
from rdopkg.actionmods import pushupdate
from rdopkg.actionmods import query as _query
from rdopkg.actionmods import rdoinfo
from rdopkg.actionmods import reqs
from rdopkg.actionmods import reviews
from rdopkg.actionmods import update as _update
from utils import log
from utils.cmd import run, git
from utils import specfile
import helpers


ACTIONS = [
    Action('fix', help="change .spec file without introducing new patches",
           steps=[
               Action('get_package_env'),
               Action('update_spec'),
               Action('edit_spec'),
               Action('commit_distgit_update'),
               Action('final_spec_diff'),
           ]),
    Action('patch',
           help="introduce new patches to the package",
           optional_args=[
               Arg('patches_branch', shortcut='-p', metavar='REMOTE/BRANCH',
                   help="remote git branch containing patches"),
               Arg('local_patches_branch', shortcut='-P', metavar='LOCAL_BRANCH',
                   help="local git branch containing patches"),
               Arg('local_patches', shortcut='-l', action='store_true',
                   help="don't reset local patches branch, use it as is"),
           ],
           steps=[
               Action('get_package_env'),
               Action('ensure_patches_branch'),
               Action('reset_patches_branch'),
               Action('check_new_patches'),
               Action('update_spec'),
               Action('commit_distgit_update'),
               Action('update_patches', const_args={'amend': True}),
               Action('final_spec_diff'),
           ]),
    Action('new_version', help="update package to new upstream version",
           optional_args=[
               Arg('new_version', positional=True, nargs='?',
                   help="version (git tag) to update to"),
               Arg('patches_branch', shortcut='-p', metavar='REMOTE/BRANCH',
                   help="remote git branch containing patches"),
               Arg('local_patches_branch', shortcut='-P', metavar='LOCAL_BRANCH',
                   help="local git branch containing patches"),
               Arg('local_patches', shortcut='-l', action='store_true',
                   help="don't reset local patches branch, use it as is"),
               Arg('bump_only', shortcut='-b', action='store_true',
                   help="only bump .spec to new version a la rpmdev-bumpspec"),
               Arg('no_diff', shortcut='-d', action='store_true',
                   help="don't show git/requirements diff"),
               Arg('no_new_sources', shortcut='-n', action='store_true',
                   help="don't run `fedpkg new-sources`"),
           ],
           steps=[
               Action('get_package_env'),
               Action('new_version_setup'),
               Action('ensure_patches_branch'),
               Action('diff'),
               Action('rebase_patches', steps=[
                   Action('reset_patches_branch'),
                   Action('rebase_patches_branch'),
               ]),
               Action('update_spec'),
               Action('get_source'),
               Action('new_sources'),
               Action('commit_distgit_update'),
               Action('update_patches', const_args={'amend': True}),
               Action('final_spec_diff'),
           ]),
    Action('rebase',
           help="rebase our downstream patches on upstream ones",
           required_args=[
               Arg('upstream_branch',
                   help="remote git branch to rebase on"),
           ],
           optional_args=[
               Arg('patches_branch', shortcut='-p', metavar='REMOTE/BRANCH',
                   help="remote git branch containing downstream patches"),
               Arg('local_patches_branch', shortcut='-P', metavar='LOCAL_BRANCH',
                   help="local git branch containing downstream patches"),
               Arg('local_patches', shortcut='-l', action='store_true',
                   help="don't reset local patches branch, use it as is"),
               Arg('lame_patches', shortcut='-d', nargs='+',
                   help=("list of patches that don't change the code but "
                         "cause conflicts while building, e.g setup.cfg")),
           ],
           steps=[
               Action('get_package_env'),
               Action('ensure_patches_branch'),
               Action('reset_patches_branch'),
               Action('rebase_nightly'),
               Action('get_upstream_patches'),
               Action('update_spec'),
               Action('commit_distgit_update'),
               Action('update_patches', const_args={'amend': True}),
               Action('final_spec_diff'),
           ]),
    Action('reqdiff', atomic=True, help="show diff of requirements.txt",
           steps=[
               Action('get_package_env'),
               Action('get_diff_range'),
               Action('reqdiff'),
           ],
           optional_args=[
               Arg('diff_range', positional=True, nargs='*', metavar='VERSION',
                   help="no args: diff between current and upstream; "
                        "1 arg: diff between current and supplied revision; "
                        "2 args: diff between 1st and 2nd supplied revisions"),
               ],
           ),
    Action('update', atomic=True, help="submit RDO update",
           optional_args=[
               Arg('update_file', positional=True, nargs='?',
                   metavar='UPDATE_FILE',
                   help="UPDATE_FILE to submit (default: %s)" % _update.UPFILE),
               Arg('update_repo', shortcut='-u',
                   help="remote rdo-update repo to submit to"),
               Arg('no_check_available', shortcut='-a', action='store_true',
                   help="don't check build availability")
           ]),
    Action('list_updates', atomic=True, help="list pending RDO updates",
           optional_args=[
               Arg('update_repo', shortcut='-u',
                   help="remote rdo-update repo to check updates from"),
               Arg('local_update_repo', shortcut='-l',
                   help="local rdo-update repo to check updates from"),
               Arg('include_reviews', shortcut='-r', action='store_true',
                   help="include updates under review (slow)"),
               Arg('reviews_only', shortcut='-R', action='store_true',
                   help="only list updates under review (slow)"),
               Arg('verbose', shortcut='-v', action='store_true',
                   help="print status messages"),
           ]),
    Action('update_patches', atomic=True,
           help="update patches from -patches branch",
           steps=[
               Action('get_package_env'),
               Action('update_patches'),
           ],
           optional_args=[
               Arg('amend', shortcut='-a', action='store_true',
                   help="amend previous commit"),
               Arg('local_patches_branch', shortcut='-P', metavar='LOCAL_BRANCH',
                   help="local git branch containing patches"),
           ]),
    Action('coprbuild', atomic=True, help="build package in copr-jruzicka",
           steps=[
               Action('get_package_env'),
               Action('build_prep'),
               Action('copr_check'),
               Action('make_srpm'),
               Action('copr_upload'),
               Action('copr_build'),
           ],
           optional_args=[
               Arg('release', shortcut='-r',
                   help="OpenStack release (havana, icehouse, ...)"),
               Arg('dist', shortcut='-d',
                   help="target distribution (fedora-20, epel-7, ...)"),
               Arg('update_file', shortcut='-f', metavar='UPDATE_FILE',
                   help=("Dump build to UPDATE_FILE (default: %s)"
                   % _update.UPFILE)),
               Arg('no_update_file', shortcut='-F', action='store_true',
                   help="Don't dump build to an update file."),
               Arg('skip_build', shortcut='-s', action='store_true',
                   help="Skip the actual build and package upload. "
                        "Useful for generating update files."),
               Arg('fuser', shortcut='-u',
                   help="Fedora user to upload srpm as to fedorapeople.org"),
           ]),
    Action('kojibuild', atomic=True, help="build package in koji",
           steps=[
               Action('get_package_env'),
               Action('build_prep'),
               Action('koji_build'),
               ],
           optional_args=[
               Arg('update_file', shortcut='-f', metavar='UPDATE_FILE',
                   help=("Dump build to UPDATE_FILE (default: %s)"
                         % _update.UPFILE)),
               Arg('no_update_file', shortcut='-F', action='store_true',
                   help="Don't dump build to an update file."),
               Arg('skip_build', shortcut='-s', action='store_true',
                   help="Skip the actual build. "
                        "Useful for generating update files."),
               ]),
    Action('mockbuild', atomic=True, help="do a mock build",
           steps=[
               Action('get_package_env'),
               Action('fedpkg_mockbuild'),
           ]),
    Action('amend', atomic=True,
           help="amend last commit and recreate commit message"),
    Action('squash', atomic=True,
           help="squash HEAD into HEAD~ using HEAD~ commit message"),
    Action('get_source', atomic=True, help="fetch source archive"),
    Action('push_updates',
           help="(special) push package updates to repos",
           required_args=[
               Arg('update_repo_path', help="path to rdo-update repo"),
               Arg('dest_base', help="destination repo path base"),
           ],
           optional_args=[
               Arg('files', shortcut='-f', nargs='+', metavar='FILE',
                   help=("only push selected update file(s)"
                         " (relative to update-repo-path)"),
               ),
               Arg('overwrite', shortcut='-w', action='store_true',
                   help="overwrite existing packages"),
               Arg('debug', action='store_true',
                   help=('debug mode: break into shell on individual update '
                         'error')),
           ],
           steps=[
               Action('upush_setup_env'),
               Action('upush_download_packages'),
               Action('upush_sanity_check'),
               Action('upush_sign'),
               Action('upush_push'),
               Action('upush_summary'),
               Action('upush_cleanup'),
           ]),
    Action('pkgenv', atomic=True, help="show detected package environment",
           steps=[
               Action('get_package_env'),
               Action('show_package_env'),
           ]),
    Action('conf', atomic=True, help="show rdopkg configuration"),
    Action('info', atomic=True, help="show information about RDO packaging",
           optional_args=[
               Arg('pkgs', positional=True, nargs='*', metavar='ATTR:REGEX',
                   help="show info about packages with ATTR matching REGEX"),
               Arg('force_fetch', shortcut='-f', action='store_true',
                   help="force fetch of info repo"),
               ]),
    Action('query', atomic=True, help="query RDO and distribution repos for "
                                      "available package versions",
           optional_args=[
               Arg('filter', positional=True, metavar='RELEASE(/DIST)',
                   help="RDO release(/dist) to query (see `rdopkg info`)"),
               Arg('package', positional=True, metavar='PACKAGE',
                   help="package name to query about"),
               Arg('verbose', shortcut='-v', action='store_true',
                   help="print status during queries"),
           ]),
]


FEDPKG = ['fedpkg']


def get_package_env(version=None, release=None,
                    patches_branch=None, local_patches_branch=None):
    branch = git.current_branch()
    if branch.endswith('-patches'):
        branch = branch[:-8]
        if git.branch_exists(branch):
            log.info("This looks like -patches branch. Assuming distgit branch: "
                    "%s" % branch)
            git.checkout(branch)
        else:
            raise exception.InvalidUsage(
                why="This action must be run on a distgit branch.")
    args = {
        'package': guess.package(),
        'branch': branch,
    }
    if not release:
        release = guess.osrelease(branch, default='')
        if release:
            args['release'] = release
    osdist = guess.osdist()
    if osdist == 'RHOS':
        log.info("RHOS package detected.")
        args['fedpkg'] = ['rhpkg']
    if not patches_branch:
        patches_branch = guess.patches_branch(branch, pkg=args['package'],
                                              osdist=osdist)
    args['patches_branch'] = patches_branch
    if not local_patches_branch:
        args['local_patches_branch'] = patches_branch.partition('/')[2]
    if not version:
        spec = specfile.Spec()
        version, _ = spec.get_patches_base(expand_macros=True)
        if not version:
            version = spec.get_tag('Version', expand_macros=True)
        args['version'] = version
    return args


def show_package_env(package, version,
                     branch, patches_branch, local_patches_branch,
                     release=None):
    def _putv(title, val):
        print("{t.bold}{title}{t.normal} {val}"
              .format(title=title, val=val, t=log.term))

    osdist = guess.osdist()
    print
    _putv('Package:', package)
    _putv('Version:', version)
    _putv('OS dist:', osdist)
    print
    _putv('Dist-git branch:      ', branch)
    _putv('Local patches branch: ', local_patches_branch)
    _putv('Remote patches branch:', patches_branch)
    print
    if osdist == 'RDO':
        _putv('RDO release guess:', release or 'unknown')
        print


def conf():
    if cfg_files:
        log.info("Following config files were read:")
        helpers.print_list(cfg_files)
    else:
        log.info("No rdopkg config files found, using default config:")
    log.info("")
    for item in cfg.items():
        log.info("%s: %s" % item)


def new_version_setup(new_version=None):
    args = {}
    if not new_version:
        ub = guess.upstream_branch()
        if not git.ref_exists('refs/remotes/%s' % ub):
            msg=("Upstream branch not found: %s\n"
                 "Can't guess latest version.\n\n"
                 "a) provide new version (git tag) yourself\n"
                 "   $ rdopkg new-version 1.2.3\n\n"
                 "b) add upstream git remote:\n"
                 "   $ git remote add -f upstream GIT_URL\n"
                 % ub)
            raise exception.CantGuess(msg=msg)
        new_version = git.get_latest_tag(ub)
        args['new_version'] = new_version
        log.info("Latest version detected from %s: %s" % (ub, new_version))
    args['changes'] = ['Update to upstream %s' % new_version]
    args['new_patches_base'] = new_version
    spec = specfile.Spec()
    rpm_version = spec.get_tag('Version')
    new_rpm_version, new_milestone = specfile.version_parts(new_version)
    args['new_rpm_version'] = new_rpm_version
    if new_milestone:
        args['new_milestone'] = new_milestone
    if rpm_version != new_rpm_version:
        if new_milestone:
            args['new_release'] = '0.1'
        else:
            args['new_release'] = '1'
    return args


def ensure_patches_branch(patches_branch=None, local_patches=False,
                          bump_only=False):
    if local_patches or bump_only:
        return
    if not patches_branch:
        raise exception.CantGuess(
            what='remote patches branch',
            why="Specify with --patches-branch or use --local-patches")
    if not git.ref_exists('refs/remotes/%s' % patches_branch):
        raise exception.ConfigError(
            what=("remote patches branch '%s' not found. \n\n"
                  "Specify with -p/--patches-branch, use -l/--local-patches, "
                  "or skip patches branch operations with -b/--bump-only" %
                  patches_branch))


def diff(version, new_version, bump_only=False, no_diff=False):
    if bump_only or no_diff:
        return
    git('--no-pager', 'diff', '--stat', '%s..%s' % (version, new_version),
        direct=True)
    try:
        reqdiff(version, new_version)
    except Exception:
        pass
    raw_input("Press <Enter> to continue after you inspected the diff. ")


def get_diff_range(diff_range=None, patches_branch=None, branch=None):
    version, new_version = None, None
    if diff_range:
        n = len(diff_range)
        if n > 2:
            raise exception.InvalidUsage(why="diff only supports one or two "
                                             "positional parameters.")
        if n == 2:
            version, new_version = diff_range
        else:
            new_version = diff_range[0]
    if not version:
        if not patches_branch:
            if not branch:
                branch = guess.current_branch()
            patches_branch = guess.patches_branch(branch)
        if not git.ref_exists('refs/remotes/%s' % patches_branch):
            msg=("Patches branch not found: %s\n"
                 "Can't guess current version.\n\n"
                 "a) provide git tags/refs yourself a la:\n"
                 "   $ rdopkg reqdiff 1.1.1 2.2.2\n\n"
                 "b) add git remote with expected patches branch"
                 % patches_branch)
            raise exception.CantGuess(msg=msg)
        version = git.get_latest_tag(branch=patches_branch)
    if not new_version:
        upstream_branch = guess.upstream_branch()
        new_version = git.get_latest_tag(branch=upstream_branch)
    return {
        'version': version,
        'new_version': new_version
    }


def reqdiff(version, new_version):
    fmt = "\n{t.bold}requirements.txt diff{t.normal} between " \
          "{t.bold}{old}{t.normal} and {t.bold}{new}{t.normal}:"
    log.info(fmt.format(t=log.term, old=version, new=new_version))
    rdiff = reqs.reqdiff_from_refs(version, new_version)
    reqs.print_reqdiff(*rdiff)


def _ensure_branch(branch):
    if not branch:
        return
    if git.current_branch() != branch:
        git.checkout(branch)


def _reset_branch(branch, remote_branch):
    if git.branch_exists(branch):
        git('update-ref', 'refs/heads/%s' % branch,
            'refs/remotes/%s' % remote_branch)
    else:
        git.create_branch(branch, remote_branch)


def _is_same_commit(ref1, ref2):
    h1 = git('rev-parse', ref1, log_cmd=False)
    h2 = git('rev-parse', ref2, log_cmd=False)
    return h1 and h1 == h2


def fetch_all():
    git('fetch', '--all', direct=True)


def reset_patches_branch(local_patches_branch, patches_branch,
                         local_patches=False, bump_only=False):
    if local_patches or bump_only:
        return
    _reset_branch(local_patches_branch, remote_branch=patches_branch)


def rebase_patches_branch(new_version, local_patches_branch,
                          patches_branch=None, local_patches=False,
                          bump_only=False):
    if bump_only:
        return
    git.checkout(local_patches_branch)
    git('rebase', new_version, direct=True)
    if local_patches or not patches_branch:
        return
    if _is_same_commit(local_patches_branch, patches_branch):
        log.info("%s is up to date, no need for push." % patches_branch)
        return
    try:
        remote, branch = git.remote_branch_split(patches_branch)
        helpers.confirm("Push %s to %s / %s (with --force)?" % (
            local_patches_branch, remote, branch))
        git('push', '--force', remote,
            '%s:%s' % (local_patches_branch, branch))
        # push the tag
        git('push', '--force', remote, new_version)
    except exception.UserAbort:
        pass


def check_new_patches(version, local_patches_branch, local_patches=False,
                      patches_branch=None, changes=None):
    if not changes:
        changes = []
    if local_patches:
        head = local_patches_branch
    else:
        if not patches_branch:
            raise exception.RequiredActionArgumentNotAvailable(
                action='check_new_patches', arg='patches_branch')
        head = patches_branch
    spec = specfile.Spec()
    n_patches = spec.get_n_patches() + spec.get_n_excluded_patches()
    patches = git.get_commit_subjects(version, head)
    if n_patches > 0:
        patches = patches[0:-n_patches]
    if not patches:
        log.warn("No new patches detected in %s." % head)
        helpers.confirm("Do you want to continue anyway?", default_yes=False)
    changes.extend(patches)
    return {'changes': changes}


def get_upstream_patches(version, local_patches_branch,
                         patches_branch=None, upstream_branch=None,
                         new_milestone=None):
    patches = git("log", "--cherry-pick", "--pretty=format:\%s",
                  "%(remote)s...%(local)s" % {'remote': patches_branch,
                                              'local': local_patches_branch})
    changes = [p.strip().replace('\\', '')
               for p in patches.split('\n') if p != '']

    if not changes:
        log.warn("No new patches detected in %s." % local_patches_branch)
        helpers.confirm("Do you want to continue anyway?", default_yes=False)

    n_patches = len(changes)
    changes.insert(0, ("Rebase %s changes from %s" %
                       (n_patches, upstream_branch)))
    args = {'changes': changes}
    if n_patches > 0:
        if new_milestone:
            new_milestone += '.p%d' % n_patches
        else:
            new_milestone = 'p%d' % n_patches
        args['new_milestone'] = new_milestone
    return args


def update_spec(branch=None, changes=None,
                new_rpm_version=None, new_release=None,
                new_milestone=None, new_patches_base=None):
    if not changes:
        changes = []
    _ensure_branch(branch)
    spec = specfile.Spec()
    if new_rpm_version:
        old_version = spec.get_tag('Version')
        if specfile.has_macros(old_version):
            log.info('Version contains macro - not touching that.')
        else:
            spec.set_tag('Version', new_rpm_version)
    if new_release is not None:
        if spec.recognized_release():
            spec.set_release(new_release, milestone=new_milestone)
        else:
            log.info('Custom Release format detected - assuming custom milestone management.')
            spec.set_release(new_release)
    else:
        spec.bump_release(milestone=new_milestone)
    if new_patches_base:
        if new_patches_base == new_rpm_version:
            new_patches_base = None
        changed = spec.set_patches_base_version(new_patches_base)
        if not changed:
            log.info("Macro detected in patches_base - not touching that.")
    spec.new_changelog_entry(user=guess.user(), email=guess.email(),
                             changes=changes)
    spec.save()


def get_source(bump_only=False):
    if bump_only:
        return
    source_urls = specfile.Spec().get_source_urls()
    # So far, only Source0 is a tarball to download
    source_url = source_urls[0]
    source_fn = os.path.basename(source_url)
    if os.path.isfile(source_fn):
        log.info("%s already present" % source_fn)
        return
    try:
        helpers.download_file(source_url)
    except exception.CommandFailed:
        raise exception.ActionRequired(
            msg="Failed to download source tarball. Please update Source0 in "
                ".spec file.", rerun=True)


def new_sources(branch=None, fedpkg=FEDPKG, no_new_sources=False,
                bump_only=False):
    _ensure_branch(branch)
    if bump_only:
        return
    if no_new_sources:
        log.info("skipping `%s new-sources` as requested." % fedpkg[0])
        return
    if not os.path.isfile('sources'):
        log.info("'sources' file not found, skipping `%s new-sources`" %
                 fedpkg[0])
        return
    sources = specfile.Spec().get_source_fns()
    cmd = fedpkg + ['new-sources'] + sources
    run(*cmd, direct=True)


def _commit_message(changes=None):
    if not changes:
        _, changes = specfile.Spec().get_last_changelog_entry(strip=True)
        if not changes:
            raise exception.IncompleteChangelog()
    msg = re.sub(r'\s+\(.*\)\s*$', '', changes[0])
    fixed_rhbzs = set()
    for change in changes:
        for m in re.finditer(r'rhbz#(\d+)', change):
            fixed_rhbzs.add(m.group(1))
    if fixed_rhbzs:
        rhbzs_str = "\n".join(map(lambda x: "Resolves: rhbz#%s" % x,
                                  fixed_rhbzs))
        msg += "\n\n%s" % rhbzs_str
    if len(changes) > 1:
        changes_str = "\n".join(map(lambda x: "- %s" % x, changes))
        msg += "\n\nChangelog:\n%s" % changes_str
    return msg


def commit_distgit_update(branch=None, new_version=None):
    _ensure_branch(branch)
    msg = _commit_message()
    git('commit', '-a', '-F', '-', input=msg, print_output=True)


def amend():
    msg = _commit_message()
    git('commit', '-a', '--amend', '-F', '-', input=msg, print_output=True)
    print("")
    git('--no-pager', 'log', '--name-status', 'HEAD~..HEAD', direct=True)


def update_patches(branch, local_patches_branch,
                   version=None, new_version=None, amend=False,
                   bump_only=False):
    if bump_only:
        return
    tag = new_version or version
    if not tag:
        raise exception.RequiredActionArgumentNotAvailable(
            action='update_patches',
            arg='version or new_version')
    _ensure_branch(local_patches_branch)
    patches = git.get_commits(tag, local_patches_branch)
    n_patches = len(patches)
    _ensure_branch(branch)
    spec = specfile.Spec()
    spec.sanity_check()
    n_excluded = spec.get_n_excluded_patches()

    pfns = spec.get_patch_fns()
    for pfn in pfns:
        git('rm', '--ignore-unmatch', pfn)

    if n_excluded > 0:
        patches = patches[:-n_excluded]
    log.info("\n{t.bold}{n} patches{t.normal} on top of {t.bold}{tag}{t.normal}"
             ", {t.bold}{ne}{t.normal} excluded".format(
        t=log.term, n=n_patches, tag=tag, ne=n_excluded))

    if patches:
        start_commit = patches[-1][0]
        for hsh, title in patches:
            log.info("%s  %s" % (hsh, title))

        rng = git.rev_range(start_commit + '~', local_patches_branch)
        o = git('format-patch', '--no-renames', '--no-signature', '-N', rng)
        pfns = git._parse_output(o)
        spec.set_new_patches(pfns)
        for pfn in pfns:
            git('add', pfn)

    spec.save()
    if git.is_clean():
        log.info('No new patches.')
        return
    msg = 'Updated patches from ' + local_patches_branch
    git('commit', '-a', '-m', msg)
    if amend:
        git.squash_last()


def squash():
    git.squash_last()


def final_spec_diff(branch=None):
    _ensure_branch(branch)
    print("Important distgit changes:")
    spec = specfile.Spec()
    git('--no-pager', 'diff', 'HEAD~..HEAD', '--', spec.fn, direct=True)
    print("")
    git('--no-pager', 'log', '--name-status', 'HEAD~..HEAD', direct=True)
    print("\nRequested distgit update finished, see last commit.")


def edit_spec():
    raise exception.ActionRequired(
        msg="Edit .spec file as needed and describe changes in changelog.")


def update(update_file=None, update_repo=None, no_check_available=False):
    check_avail = not no_check_available
    if not update_repo:
        update_repo = cfg['RDO_UPDATE_REPO']
    repo = _update.UpdateRepo(cfg['HOME_DIR'], update_repo)

    if update_file:
        if not os.path.isfile(update_file):
            raise exception.UpdateFileNotFound(path=update_file)
    else:
        update_file = _update.UPFILE
        if not os.path.isfile(update_file):
            raise exception.UpdateFileNotFound(
                msg="Default update file not found: %s\n\n"
                    "Use `kojibuild` and `coprbuild` actions to create it."
                    % update_file)
    repo.init()
    repo.submit_existing_update(update_file, check_availability=check_avail)
    if update_file == _update.UPFILE:
        log.info("Removing default update file after successful update: %s"
                 % _update.UPFILE)
        os.remove(update_file)


def list_updates(update_repo=None, local_update_repo=None,
                 include_reviews=False, reviews_only=False, verbose=False):
    if reviews_only and (include_reviews or update_repo or local_update_repo):
        raise exception.ConfigError(
            what="-R/--reviews-only is exclusive with other options.")
    if update_repo and local_update_repo:
        raise exception.ConfigError(
            what="-u/--update-repo and -l/--local-update-repo are exclusive.")

    if local_update_repo:
        base_dir, repo_name = os.path.split(local_update_repo)
    if not local_update_repo and not update_repo:
        update_repo = cfg['RDO_UPDATE_REPO']
    list_merged = True
    list_reviews = False
    if include_reviews:
        list_reviews = True
    if reviews_only:
        list_merged = False
        list_reviews = True

    if list_reviews:
        uinfos = reviews.get_updates_info(verbose=verbose)
        uinfos_dict = {'__reviews__': uinfos}
        _update.pretty_print_uinfos_dict(uinfos_dict)

    if list_merged:
        if local_update_repo:
            repo = _update.UpdateRepo(local_repo_path=local_update_repo,
                                      verbose=verbose)
        else:
            repo = _update.UpdateRepo(base_path=cfg['HOME_DIR'],
                                      url=update_repo, verbose=verbose)
        repo.init(force_fetch=True)
        repo.pretty_print_updates()


def fedpkg_mockbuild(branch=None, fedpkg=FEDPKG):
    if not branch:
        branch = guess.current_branch(default=None)
    cmd = list(fedpkg) + ['mockbuild']
    if fedpkg[0] == 'rhpkg':
        cmd += ['--root', 'epel-6-x86_64']
    run(*cmd, direct=True)


def _upush_check_updates(update_files, update_fails):
    if not update_files:
        raise exception.ActionGoto(goto=['upush_summary'])


def upush_setup_env(update_repo_path, dest_base, files=None, debug=False):
    if not os.path.isdir(update_repo_path):
        raise exception.NotADirectory(path=update_repo_path)
    pusher = pushupdate.UpdatePusher(update_repo_path, dest_base, debug=debug)
    if not os.path.isdir(pusher.ready_path()):
        raise exception.NotADirectory(path=pusher.ready_path())
    if files:
        pusher.update_files = files
        pusher.ready_dir = ''
    else:
        if not pusher.get_update_files():
            raise exception.ActionFinished(msg="No pending updates.")
    log.info("Initializing update push environment...")
    pusher.init_env()
    return {'update_files': pusher.update_files,
            'update_fails': pusher.fails,
            'temp_path': pusher.temp_path,
            'ready_dir': pusher.ready_dir}


def upush_download_packages(update_repo_path, dest_base, update_files,
                            update_fails, temp_path, debug=False):
    _upush_check_updates(update_files, update_fails)
    pusher = pushupdate.UpdatePusher(update_repo_path,
                                     dest_base,
                                     update_files=update_files,
                                     fails=update_fails,
                                     temp_path=temp_path,
                                     debug=debug)
    log.info("Downloading packages to push...")
    pusher.download_packages()
    return {'update_files': pusher.update_files,
            'update_fails': pusher.fails}


def upush_sanity_check(update_repo_path, dest_base, update_files, update_fails,
                       temp_path, overwrite=False, debug=False):
    _upush_check_updates(update_files, update_fails)
    pusher = pushupdate.UpdatePusher(update_repo_path,
                                     dest_base,
                                     update_files=update_files,
                                     fails=update_fails,
                                     temp_path=temp_path,
                                     overwrite=overwrite,
                                     debug=debug)
    pusher.check_collision()
    return {'update_files': pusher.update_files,
            'update_fails': pusher.fails}


def upush_sign(update_repo_path, dest_base, update_files, update_fails,
               temp_path, debug=False):
    _upush_check_updates(update_files, update_fails)
    pusher = pushupdate.UpdatePusher(update_repo_path,
                                     dest_base,
                                     update_files=update_files,
                                     fails=update_fails,
                                     temp_path=temp_path,
                                     debug=debug)
    pusher.sign_packages()
    return {'update_files': pusher.update_files,
            'update_fails': pusher.fails}


def upush_push(update_repo_path, dest_base, update_files, update_fails,
               temp_path, overwrite=False, debug=False):
    _upush_check_updates(update_files, update_fails)
    pusher = pushupdate.UpdatePusher(update_repo_path,
                                     dest_base,
                                     update_files=update_files,
                                     fails=update_fails,
                                     temp_path=temp_path,
                                     overwrite=overwrite,
                                     debug=debug)
    need_sync = pusher.push_packages()
    return {'update_files': pusher.update_files,
            'update_fails': pusher.fails,
            'need_sync': need_sync}


def upush_summary(update_repo_path, dest_base, update_files, update_fails,
                  temp_path, need_sync=None, debug=False):
    pusher = pushupdate.UpdatePusher(update_repo_path,
                                     dest_base,
                                     update_files=update_files,
                                     fails=update_fails,
                                     temp_path=temp_path,
                                     debug=debug)
    pusher.print_summary()
    if need_sync:
        log.success("Updated trees (might need sync):")
        helpers.print_list(map(os.path.basename, need_sync), nl_after=True)
        log.info(log.term.warn(
            "Don't forget to push changes to update repo:"))
        log.info(update_repo_path)
        log.info('')


def upush_cleanup(update_repo_path, dest_base, temp_path, debug=False):
    log.info("Cleaning up update push environment: %s" % temp_path)
    pusher = pushupdate.UpdatePusher(update_repo_path, dest_base,
                                     temp_path=temp_path,
                                     debug=True)
    pusher.clean_env()


def rebase_nightly(upstream_branch, local_patches_branch, branch=None,
                   lame_patches=None):
    log.info("Rebasing upstream %s" % upstream_branch)
    nightly.rebase_nightly(upstream_branch,
                           lame_patches=lame_patches,
                           patches_branch=local_patches_branch,
                           distgit_branch=branch)


def build_prep(update_file=None, no_update_file=False):
    if update_file and no_update_file:
        raise exception.InvalidUsage(
            why="Using both -f and -F doesn't make sense.")
    if not update_file and not no_update_file:
        return {'update_file': _update.UPFILE}


def make_srpm(package, dist=None, fedpkg=FEDPKG):
    cmd = list(fedpkg)
    if dist:
        dname, _, drls = dist.partition('-')
        if dname == 'epel' and drls:
            cmd += ['--dist', 'el' + drls]
    cmd.append('srpm')
    out = run(*cmd)
    m = re.search(r'/([^/\\]+\.src.rpm)\b', out)
    if not m:
        raise exception.CommandOutputParseError(tool=cmd[0], output=out)
    srpm = m.group(1)
    if not os.path.isfile(srpm):
        raise exception.FileNotFound(path=srpm)
    return {'srpm': srpm}


def copr_check(release=None, dist=None):
    osdist = guess.osdist()
    if osdist == 'RHOS':
        helpers.confirm("Look like you're trying to build RHOS package in "
                        "public copr.\nProceed anyway?")
    if not release:
        raise exception.CantGuess(
            what='release',
            why="Specify with -r/--release")

    if not dist:
        builds = guess.builds(release=release)
        for dist_, src in builds:
            if src.startswith('copr/jruzicka'):
                dist = dist_
                log.info("Autodetected dist: %s" % dist)
                break
        if not dist:
            raise exception.CantGuess(
                what='dist',
                why="Specify with -d/--dist")
        return {'dist': dist}


def copr_upload(srpm, fuser=None, skip_build=False):
    if not fuser:
        fuser = guess.fuser()
    if skip_build:
        log.info("Skipping SRPM upload due to -s/--skip-build")
        url = _copr.fpo_url(srpm, fuser)
    else:
        url = _copr.upload_fpo(srpm, fuser)
    return {'srpm_url': url}


def _show_update_entry(build):
    log.info("")
    fmt = "{t.bold}Entry for{t.normal} {t.cmd}rdopkg update{t.normal}:\n\n{s}"
    log.info(fmt.format(t=log.term, s=build.as_yaml_item()))


def copr_build(srpm_url, release, dist, package, version,
               update_file=None, copr_owner='jruzicka', skip_build=False):
    if skip_build:
        log.info("\nSkipping copr build due to -s/--skip-build")
    else:
        copr = _copr.RdoCoprs()
        copr_name = _copr.rdo_copr_name(release, dist)
        repo_url = copr.get_repo_url(release, dist)
        web_url = copr.get_builds_url(release, dist)
        log.info("\n{t.bold}copr:{t.normal} {owner} / {copr}\n"
                 "{t.bold}SRPM:{t.normal} {srpm}\n"
                 "{t.bold}repo:{t.normal} {repo}\n"
                 "{t.bold}web: {t.normal} {web}".format(
                 owner=copr_owner,
                 copr=copr_name,
                 srpm=srpm_url,
                 repo=repo_url,
                 web=web_url,
                 t=log.term))
        copr.new_build(srpm_url, release, dist, watch=True)
    build = rdoupdate.core.Build(id=_copr.copr_fetcher_id(srpm_url),
                                 repo=release,
                                 dist=dist,
                                 source='copr-jruzicka')
    _show_update_entry(build)
    if update_file:
        _update.dump_build(build, update_file)


def koji_build(update_file=None, skip_build=False):
    if skip_build:
        log.info("\nSkipping koji build due to -s/--skip-build")
        fcmd = kojibuild.get_fedpkg_commands()
        build_id = fcmd.nvr
    else:
        if git.branch_needs_push():
            helpers.confirm("It seems local distgit branch needs push. Push "
                            "now?")
        git('push')
        build_id = kojibuild.new_build()
    build = kojibuild.guess_build(build_id)
    _show_update_entry(build)
    if update_file:
        _update.dump_build(build, update_file)


def info(pkgs=None, info_repo=None, force_fetch=False, verbose=False):
    if not info_repo:
        info_repo = cfg['RDOINFO_REPO']
    inforepo = rdoinfo.get_default_inforepo()
    inforepo.init(force_fetch=force_fetch)
    if pkgs:
        filters = {}
        for pf in pkgs:
            attr, sep, rex = pf.partition(':')
            if not sep:
                # filter by name by default
                attr = 'name'
                rex = pf
            filters[attr] = rex
        inforepo.print_pkgs(filters)
    else:
        inforepo.print_summary()
        print
        print("Supply regex filter(s) to list package details, e.g.:\n{t.cmd}"
              "    rdopkg info nova\n"
              "    rdopkg info conf:client maintainers:jruzicka\n"
              "    rdopkg info '.*'"
              "{t.normal}".format(t=log.term))


def query(filter, package, verbose=False):
    r = _query.query_rdo(filter, package, verbose=verbose)
    if not r:
        log.warn('No distrepos information in rdoinfo for %s' % filter)
        return
    if verbose:
        print('')
    _query.pretty_print_query_results(r)
