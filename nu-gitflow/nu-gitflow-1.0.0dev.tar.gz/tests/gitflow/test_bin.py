#
# This file is part of `gitflow`.
# Copyright (c) 2010-2011 Vincent Driessen
# Copyright (c) 2012-2013 Hartmut Goebel
# Copyright (c) 2015 Christian Assing
# Distributed under a BSD-like license. For full terms see the file LICENSE.txt
#

import sys
import re
from io import StringIO

from unittest2 import TestCase

import gitflow
from gitflow.core import GitFlow, Repo
from gitflow.exceptions import (NoSuchBranchError, NoSuchRemoteError,
                                AlreadyInitialized, NotInitialized,
                                BaseNotOnBranch)

from tests.helpers import (copy_from_fixture, remote_clone_from_fixture,
                           sandboxed, fake_commit)
from tests.helpers.factory import create_git_repo

__copyright__ = "2010-2011 Vincent Driessen; 2012-2013 Hartmut Goebel; 2015 Christian Assing"
__license__ = "BSD"


def run_git_flow(*argv, **kwargs):
    capture = kwargs.get('capture', False)
    _argv, sys.argv = sys.argv, ['git-flow'] + list(argv)
    _stdout = sys.stdout
    try:
        if not capture:
            gitflow.bin.main()
        else:
            sys.stdout = StringIO()
            gitflow.bin.main()
            return sys.stdout.getvalue()
    finally:
        sys.stdout = _stdout
        sys.argv = _argv


class TestCase(TestCase):

    def assert_argparse_error(self, expected_regexp, func, *args, **kwargs):
        _stderr, sys.stderr = sys.stderr, StringIO()
        try:
            self.assertRaises(SystemExit, func, *args, **kwargs)
            msg = sys.stderr.getvalue()
            if expected_regexp:
                expected_regexp = re.compile(expected_regexp)
                if not expected_regexp.search(str(msg)):
                    raise self.failureException('"%s" does not match "%s"' % (expected_regexp.pattern, msg))
        finally:
            sys.stderr = _stderr


class TestVersionCommand(TestCase):

    def test_version(self):
        stdout = run_git_flow('version', capture=1)
        self.assertEqual(gitflow.__version__ + '\n', stdout)


class TestStatusCommand(TestCase):

    @copy_from_fixture('sample_repo')
    def test_version(self):
        stdout = run_git_flow('status', capture=1)
        self.assertItemsEqual([
            '  devel: 2b34cd2',
            '  feat/even: e56be18',
            '* feat/recursion: 54d59c8',
            '  stable: 296586b',
        ], stdout.splitlines())


class TestInitCommand(TestCase):

    @sandboxed
    def test_init_defaults(self):
        run_git_flow('init', '--defaults')
        gitflow = GitFlow('.').init()
        self.assertEquals('origin', gitflow.origin_name())
        self.assertEquals('master', gitflow.master_name())
        self.assertEquals('develop', gitflow.develop_name())
        self.assertEquals('feature/', gitflow.get_prefix('feature'))
        self.assertEquals('release/', gitflow.get_prefix('release'))
        self.assertEquals('hotfix/', gitflow.get_prefix('hotfix'))
        self.assertEquals('support/', gitflow.get_prefix('support'))
        self.assertEquals('', gitflow.get_prefix('versiontag'))

    @sandboxed
    def test_init_accepting_defaults(self):
        text = u'\n' * 8
        _stdin, sys.stdin = sys.stdin, StringIO(text)
        try:
            run_git_flow('init')
        finally:
            sys.stdin = _stdin
        gitflow = GitFlow('.').init()
        self.assertEquals('origin', gitflow.origin_name())
        self.assertEquals('master', gitflow.master_name())
        self.assertEquals('develop', gitflow.develop_name())
        self.assertEquals('feature/', gitflow.get_prefix('feature'))
        self.assertEquals('release/', gitflow.get_prefix('release'))
        self.assertEquals('hotfix/', gitflow.get_prefix('hotfix'))
        self.assertEquals('support/', gitflow.get_prefix('support'))
        self.assertEquals('', gitflow.get_prefix('versiontag'))

    @sandboxed
    def test_init_custom(self):
        text = u'\n'.join(['my-remote', 'stable', 'devel',
                           'feat/', 'rel/', 'hf/', 'sup/', 'ver'])
        _stdin, sys.stdin = sys.stdin, StringIO(text)
        try:
            run_git_flow('init')
        finally:
            sys.stdin = _stdin
        gitflow = GitFlow('.').init()
        self.assertEquals('my-remote', gitflow.origin_name())
        self.assertEquals('stable', gitflow.master_name())
        self.assertEquals('devel', gitflow.develop_name())
        self.assertEquals('feat/', gitflow.get_prefix('feature'))
        self.assertEquals('rel/', gitflow.get_prefix('release'))
        self.assertEquals('hf/', gitflow.get_prefix('hotfix'))
        self.assertEquals('sup/', gitflow.get_prefix('support'))
        self.assertEquals('ver', gitflow.get_prefix('versiontag'))

    @sandboxed
    def test_init_custom_accepting_some_defaults(self):
        text = u'\n'.join(['my-remote', '', 'devel',
                           'feat/', '', '', 'sup/', 'v'])
        _stdin, sys.stdin = sys.stdin, StringIO(text)
        try:
            run_git_flow('init')
        finally:
            sys.stdin = _stdin
        gitflow = GitFlow('.').init()
        self.assertEquals('my-remote', gitflow.origin_name())
        self.assertEquals('master', gitflow.master_name())
        self.assertEquals('devel', gitflow.develop_name())
        self.assertEquals('feat/', gitflow.get_prefix('feature'))
        self.assertEquals('release/', gitflow.get_prefix('release'))
        self.assertEquals('hotfix/', gitflow.get_prefix('hotfix'))
        self.assertEquals('sup/', gitflow.get_prefix('support'))
        self.assertEquals('v', gitflow.get_prefix('versiontag'))

    @copy_from_fixture('custom_repo')
    def test_init_fails_if_already_initialized(self):
        self.assertRaises(AlreadyInitialized, run_git_flow, 'init')

    @copy_from_fixture('custom_repo')
    def test_init_force_defaults_succeeds_if_already_initialized(self):
        run_git_flow('init', '--defaults', '--force')
        gitflow = GitFlow('.').init()
        # these are the values already defined in custom_repo
        self.assertEquals('origin', gitflow.origin_name())
        self.assertEquals('production', gitflow.master_name())
        self.assertEquals('master', gitflow.develop_name())
        self.assertEquals('f-', gitflow.get_prefix('feature'))
        self.assertEquals('rel-', gitflow.get_prefix('release'))
        self.assertEquals('hf-', gitflow.get_prefix('hotfix'))
        self.assertEquals('supp-', gitflow.get_prefix('support'))
        self.assertEquals('v', gitflow.get_prefix('versiontag'))

    @copy_from_fixture('custom_repo')
    def test_init_existing_repo_fails_on_non_existing_master_branch(self):
        text = u'\n'.join(['', 'stable', '', '', '', '', '', ''])
        _stdin, sys.stdin = sys.stdin, StringIO(text)
        try:
            self.assertRaises(NoSuchBranchError, run_git_flow, 'init', '--force')
        finally:
            sys.stdin = _stdin

    @copy_from_fixture('custom_repo')
    def test_init_existing_repo_fails_on_non_existing_develop_branch(self):
        text = u'\n'.join(['', '', 'workinprogress', '', '', '', '', ''])
        _stdin, sys.stdin = sys.stdin, StringIO(text)
        try:
            self.assertRaises(NoSuchBranchError, run_git_flow, 'init', '--force')
        finally:
            sys.stdin = _stdin

    @copy_from_fixture('custom_repo')
    def test_init_force_succeeds_if_already_initialized(self):
        # NB: switching master and develop
        text = u'\n'.join(['my-remote', 'master', 'production',
                           'feat/', 'rel/', 'hf/', 'sup/', 'ver'])
        _stdin, sys.stdin = sys.stdin, StringIO(text)
        try:
            run_git_flow('init', '--force')
        finally:
            sys.stdin = _stdin
        gitflow = GitFlow('.').init()
        self.assertEquals('master', gitflow.master_name())
        self.assertEquals('production', gitflow.develop_name())

    @sandboxed
    def test_init_fails_if_develop_name_equals_master_name(self):
        text = u'\n'.join(['', 'mainbranch', 'mainbranch'])
        _stdin, sys.stdin = sys.stdin, StringIO(text)
        try:
            self.assertRaisesRegexp(SystemExit, ".*branches should differ.*",
                                    run_git_flow, 'init')
        finally:
            sys.stdin = _stdin

    @remote_clone_from_fixture('sample_repo')
    def test_init_with_master_existing_remote_but_not_local(self):
        rsc0 = self.remote.branches['stable'].commit
        text = u'\n'.join(['my-remote', 'stable', 'devel',
                           'feat/', 'rel/', 'hf/', 'sup/', 'ver'])
        _stdin, sys.stdin = sys.stdin, StringIO(text)
        try:
            run_git_flow('init', '--force')
        finally:
            sys.stdin = _stdin
        rsc1 = self.remote.branches['stable'].commit
        lsc1 = self.repo.branches['stable'].commit
        self.assertEqual(rsc0, rsc1)
        self.assertEqual(rsc1, lsc1)

    # These tests need a repo with only branches `foo` and `bar`
    # or other names not selected for defaults
    # :todo: give no master branch name (or white-spaces)
    # :todo: give no develop branch name (or white-spaces)
    @remote_clone_from_fixture('sample_repo')
    def test_subcommands_requiring_initialized_repo(self):
        def assert_system_exit(*args):
            self.assertRaisesRegexp(
                SystemExit, 'repo has not yet been initialized for git-flow',
                run_git_flow, 'feature', *args)

        def assert_not_initialized(*args):
            self.assertRaises(NotInitialized,
                              run_git_flow, 'feature', *args)
        assert_not_initialized('start', 'xxx')
        assert_not_initialized('finish', 'recursion')
        assert_not_initialized('publish', 'recursion')
        assert_not_initialized('track', 'recursion')
        assert_not_initialized('diff', 'recursion')
        assert_not_initialized('rebase', 'recursion')
        assert_not_initialized('pull', 'even')


class TestFeature(TestCase):

    @copy_from_fixture('sample_repo')
    def test_feature_list(self):
        stdout = run_git_flow('feature', 'list', capture=1)
        expected = [
            '  even',
            '* recursion'
        ]
        self.assertEqual(stdout.splitlines(), expected)

    @copy_from_fixture('sample_repo')
    def test_feature_list_verbose(self):
        stdout = run_git_flow('feature', 'list', '--verbose', capture=1)
        expected = [
            '  even      (based on latest devel)',
            '* recursion (based on latest devel)'
        ]
        self.assertEqual(stdout.splitlines(), expected)

    @copy_from_fixture('sample_repo')
    def test_feature_list_verbose_rebased(self):
        self.repo.refs['devel'].checkout()
        fake_commit(self.repo, 'A commit on devel')
        stdout = run_git_flow('feature', 'list', '--verbose', capture=1)
        expected = [
            '  even      (may be rebased)',
            '  recursion (may be rebased)'
        ]
        self.assertEqual(stdout.splitlines(), expected)

    @sandboxed
    def test_feature_list_verbose_no_commits(self):
        repo = create_git_repo(self)
        GitFlow(repo).init()
        repo.create_head('feature/wow', 'HEAD')
        stdout = run_git_flow('feature', 'list', '--verbose', capture=1)
        expected = [
            '  wow (no commits yet)'
        ]
        self.assertEqual(stdout.splitlines(), expected)

    @copy_from_fixture('sample_repo')
    def test_feature_list_verbose_ff(self):
        self.repo.create_head('devel', 'feat/recursion', force=1)
        self.repo.refs['devel'].checkout()
        fake_commit(self.repo, 'A commit on devel')
        stdout = run_git_flow('feature', 'list', '--verbose', capture=1)
        expected = [
            '  even      (may be rebased)',
            '  recursion (is behind devel, may ff)'
        ]
        self.assertEqual(stdout.splitlines(), expected)

    # --- feature start ---

    @copy_from_fixture('sample_repo')
    def test_feature_start(self):
        run_git_flow('feature', 'start', 'wow-feature')
        self.assertIn('feat/wow-feature', Repo().branches)

    @copy_from_fixture('sample_repo')
    def test_feature_start_alt_base(self):
        run_git_flow('feature', 'start', 'wow-feature', 'devel')
        self.assertIn('feat/wow-feature', Repo().branches)

    # feature branch is not required to start at `develop`, rethink this
    # @copy_from_fixture('sample_repo')
    # def test_feature_start_wrong_alt_base_raises_error(self):
    # self.repo.refs['stable'].checkout()
    #      fake_commit(self.repo, 'A fake commit on stable')
    # self.assertRaises(BaseNotOnBranch,
    # run_git_flow, 'feature', 'start', 'wow', 'stable')

    @copy_from_fixture('sample_repo')
    def test_feature_start_empty_name(self):
        self.assert_argparse_error('must not by empty',
                                   run_git_flow, 'feature', 'start', '')
        self.assert_argparse_error('must not by empty',
                                   run_git_flow, 'feature', 'start', '', 'devel')

    @copy_from_fixture('sample_repo')
    def test_feature_start_no_name(self):
        self.assert_argparse_error(None,
                                   run_git_flow, 'feature', 'start')

    # --- feature finish ---

    @remote_clone_from_fixture('sample_repo')
    def test_feature_finish(self):
        GitFlow('.').init()
        run_git_flow('feature', 'finish', 'recursion')
        self.assertNotIn('feat/recursion', Repo().branches)

    @copy_from_fixture('sample_repo')
    def test_feature_finish_current(self):
        GitFlow('.').init()
        run_git_flow('feature', 'finish')
        self.assertNotIn('feat/recursion', Repo().branches)

    @copy_from_fixture('sample_repo')
    def test_feature_finish_empty_prefix(self):
        GitFlow('.').init()
        run_git_flow('feature', 'checkout', 'even')
        run_git_flow('feature', 'finish', '')
        self.assertNotIn('feat/even', Repo().branches)

    @copy_from_fixture('sample_repo')
    def test_feature_finish_prefix(self):
        GitFlow('.').init()
        run_git_flow('feature', 'finish', 'e')
        self.assertNotIn('feat/even', Repo().branches)

    @copy_from_fixture('sample_repo')
    def test_feature_finish_rebase(self):
        gitflow = GitFlow('.').init()
        gitflow.develop().checkout()
        fake_commit(gitflow.repo, 'A commit on devel')
        run_git_flow('feature', 'finish', 'even', '--rebase')
        self.assertNotIn('feat/even', Repo().branches)
        self.assertTrue(gitflow.develop().commit.message.startswith('Finished feature even.\n'))
        # :todo: think about some other test to see if it really worked

    # :todo: test-cases for `feature finish --rebase` w/ conflict

    @copy_from_fixture('sample_repo')
    def test_feature_finish_keep(self):
        GitFlow('.').init()
        run_git_flow('feature', 'finish', 'even', '--keep')
        self.assertIn('feat/even', Repo().branches)

    # :todo: test-cases for `feature finish --fetch`
    # :todo: test-cases for `feature finish --force-delete`

    # --- feature publish ---

    @remote_clone_from_fixture('sample_repo')
    def test_feature_publish(self):
        GitFlow('.').init()
        run_git_flow('feature', 'start', 'wow')
        run_git_flow('feature', 'publish', 'wow')
        self.assertIn('feat/wow', Repo().remotes['my-remote'].refs)

    @remote_clone_from_fixture('sample_repo')
    def test_feature_publish_current(self):
        GitFlow('.').init()
        run_git_flow('feature', 'start', 'wow')
        run_git_flow('feature', 'publish')
        self.assertIn('feat/wow', Repo().remotes['my-remote'].refs)

    @remote_clone_from_fixture('sample_repo')
    def test_feature_publish_empty_prefix(self):
        GitFlow('.').init()
        run_git_flow('feature', 'start', 'wow')
        run_git_flow('feature', 'publish', '')
        self.assertIn('feat/wow', Repo().remotes['my-remote'].refs)

    @remote_clone_from_fixture('sample_repo')
    def test_feature_publish_prefix(self):
        GitFlow('.').init()
        run_git_flow('feature', 'start', 'wow')
        run_git_flow('feature', 'publish', 'w')
        self.assertIn('feat/wow', Repo().remotes['my-remote'].refs)

    # --- feature track ---

    @remote_clone_from_fixture('sample_repo')
    def test_feature_track(self):
        GitFlow('.').init()
        run_git_flow('feature', 'track', 'even')

    @remote_clone_from_fixture('sample_repo')
    def test_feature_track_name_is_required(self):
        GitFlow('.').init()
        self.assert_argparse_error(None,
                                   run_git_flow, 'feature', 'track')
        self.assert_argparse_error('must not by empty',
                                   run_git_flow, 'feature', 'track', '')

    # --- feature diff ---

    @copy_from_fixture('sample_repo')
    def test_feature_diff(self):
        run_git_flow('feature', 'diff', 'recursion')

    @copy_from_fixture('sample_repo')
    def test_feature_diff_current(self):
        run_git_flow('feature', 'diff')

    @copy_from_fixture('sample_repo')
    def test_feature_diff_empty_prefix(self):
        run_git_flow('feature', 'diff', '')

    @copy_from_fixture('sample_repo')
    def test_feature_diff_prefix(self):
        run_git_flow('feature', 'diff', 'rec')

    # --- feature rebase ---

    @copy_from_fixture('sample_repo')
    def test_feature_rebase(self):
        run_git_flow('feature', 'rebase', 'recursion')

    @copy_from_fixture('sample_repo')
    def test_feature_rebase_current(self):
        run_git_flow('feature', 'rebase')

    @copy_from_fixture('sample_repo')
    def test_feature_rebase_empty_prefix(self):
        run_git_flow('feature', 'rebase', '')

    @copy_from_fixture('sample_repo')
    def test_feature_rebase_prefix(self):
        run_git_flow('feature', 'rebase', 'rec')

    # --- feature  checkout ---

    @copy_from_fixture('sample_repo')
    def test_feature_checkout(self):
        run_git_flow('feature', 'checkout', 'even')

    @copy_from_fixture('sample_repo')
    def test_feature_checkout_current(self):
        self.assert_argparse_error(None,
                                   run_git_flow, 'feature', 'checkout')

    @copy_from_fixture('sample_repo')
    def test_feature_checkout_empty_prefix(self):
        self.assert_argparse_error('must not by empty',
                                   run_git_flow, 'feature', 'checkout', '')

    @copy_from_fixture('sample_repo')
    def test_feature_checkout_prefix(self):
        run_git_flow('feature', 'checkout', 'rec')

    # --- feature pull ---

    @remote_clone_from_fixture('sample_repo')
    def test_feature_pull(self):
        GitFlow('.').init()
        run_git_flow('feature', 'pull', 'my-remote', 'even')

    @remote_clone_from_fixture('sample_repo')
    def test_feature_pull_empty_remote_raises_error(self):
        GitFlow('.').init()
        self.assert_argparse_error('must not by empty',
                                   run_git_flow, 'feature', 'pull', '', 'even')

    @remote_clone_from_fixture('sample_repo')
    def test_feature_pull_nonexisting_remote_raises_error(self):
        GitFlow('.').init()
        self.assertRaises(NoSuchRemoteError,
                          run_git_flow, 'feature', 'pull', 'some-remote', 'even')

    @remote_clone_from_fixture('sample_repo')
    def test_feature_pull_name_is_required(self):
        GitFlow('.').init()
        self.assertRaises(NoSuchBranchError, run_git_flow, 'feature', 'pull', 'my-remote')
        self.assertRaises(NoSuchBranchError, run_git_flow, 'feature', 'pull', 'my-remote', '')


class TestRelease(TestCase):

    @copy_from_fixture('release')
    def test_release_list(self):
        stdout = run_git_flow('release', 'list', capture=1)
        expected = [
            '  1.0'
        ]
        self.assertEqual(stdout.splitlines(), expected)

    @copy_from_fixture('release')
    def test_release_list_verbose(self):
        stdout = run_git_flow('release', 'list', '--verbose', capture=1)
        expected = [
            '  1.0 (based on latest devel)'
        ]
        self.assertEqual(stdout.splitlines(), expected)

    # --- release start ---

    @copy_from_fixture('sample_repo')
    def test_release_start(self):
        run_git_flow('release', 'start', '1.1')
        self.assertIn('rel/1.1', Repo().branches)

    @copy_from_fixture('sample_repo')
    def test_release_start_alt_base(self):
        run_git_flow('release', 'start', '1.1', 'devel')
        self.assertIn('rel/1.1', Repo().branches)

    @copy_from_fixture('sample_repo')
    def test_release_start_wrong_alt_base_raises_error(self):
        self.repo.refs['stable'].checkout()
        fake_commit(self.repo, 'A fake commit on stable')
        self.assertRaises(BaseNotOnBranch,
                          run_git_flow, 'release', 'start', 'wow', 'stable')

    @copy_from_fixture('release')
    def test_release_start_empty_name(self):
        self.assert_argparse_error('must not by empty',
                                   run_git_flow, 'release', 'start', '')

    @copy_from_fixture('release')
    def test_release_start_no_name(self):
        self.assert_argparse_error(None,
                                   run_git_flow, 'release', 'start')

    # --- release finish ---

    @copy_from_fixture('release')
    def test_release_finish(self):
        gitflow = GitFlow('.').init()
        gitflow.checkout('release', '1.0')
        run_git_flow('release', 'finish', '1.0')
        self.assertNotIn('rel/1.0', Repo().branches)

    @copy_from_fixture('release')
    def test_release_finish_current(self):
        gitflow = GitFlow('.').init()
        gitflow.checkout('release', '1.0')
        run_git_flow('release', 'finish')
        self.assertNotIn('rel/1.0', Repo().branches)

    @copy_from_fixture('release')
    def test_release_finish_empty_prefix(self):
        gitflow = GitFlow('.').init()
        gitflow.checkout('release', '1.0')
        run_git_flow('release', 'finish', '')
        self.assertNotIn('rel/1.0', Repo().branches)

    @copy_from_fixture('release')
    def test_release_finish_prefix(self):
        gitflow = GitFlow('.').init()
        gitflow.checkout('release', '1.0')
        # release finish requires a name, not a prefix
        self.assertRaises(NoSuchBranchError,
                          run_git_flow, 'release', 'finish', '1')

    # :todo: test-cases for `release finish --rebase`
    # :todo: test-cases for `release finish --fetch`
    # :todo: test-cases for `release finish --keep`
    # :todo: test-cases for `release finish --force-delete`

    # --- release publish ---

    @remote_clone_from_fixture('sample_repo')
    def test_release_publish(self):
        GitFlow('.').init()
        run_git_flow('release', 'start', '1.1')
        run_git_flow('release', 'publish', '1.1')
        self.assertIn('rel/1.1', Repo().remotes['my-remote'].refs)

    @remote_clone_from_fixture('sample_repo')
    def test_release_publish_current(self):
        GitFlow('.').init()
        run_git_flow('release', 'start', '1.1')
        run_git_flow('release', 'publish')
        self.assertIn('rel/1.1', Repo().remotes['my-remote'].refs)

    @remote_clone_from_fixture('sample_repo')
    def test_release_publish_empty_prefix(self):
        GitFlow('.').init()
        run_git_flow('release', 'start', '1.1')
        run_git_flow('release', 'publish', '')
        self.assertIn('rel/1.1', Repo().remotes['my-remote'].refs)

    @remote_clone_from_fixture('sample_repo')
    def test_release_publish_prefix(self):
        GitFlow('.').init()
        run_git_flow('release', 'start', '1.1')
        self.assertRaises(NoSuchBranchError,
                          run_git_flow, 'release', 'publish', '1')

    # --- release track ---

    @remote_clone_from_fixture('release')
    def test_release_track(self):
        GitFlow('.').init()
        run_git_flow('release', 'track', '1.0')

    @remote_clone_from_fixture('sample_repo')
    def test_release_track_name_is_required(self):
        GitFlow('.').init()
        self.assert_argparse_error(None,
                                   run_git_flow, 'release', 'track')
        self.assert_argparse_error('must not by empty',
                                   run_git_flow, 'release', 'track', '')

    # --- unsupported `release` subcommands ---

    def test_release_diff_is_no_valid_subcommand(self):
        self.assert_argparse_error("invalid choice: 'diff'",
                                   run_git_flow, 'release', 'diff')

    def test_release_rebase_is_no_valid_subcommand(self):
        self.assert_argparse_error("invalid choice: 'rebase'",
                                   run_git_flow, 'release', 'rebase')

    def test_release_checkout_is_no_valid_subcommand(self):
        self.assert_argparse_error("invalid choice: 'checkout'",
                                   run_git_flow, 'release', 'checkout')

    def test_release_pull_is_no_valid_subcommand(self):
        self.assert_argparse_error("invalid choice: 'pull'",
                                   run_git_flow, 'release', 'pull')


class TestHotfix(TestCase):

    @copy_from_fixture('sample_repo')
    def test_hotfix_list(self):
        self.repo.create_head('hf/2.3', 'HEAD')
        stdout = run_git_flow('hotfix', 'list', capture=1)
        expected = [
            '  2.3'
        ]
        self.assertEqual(stdout.splitlines(), expected)

    @copy_from_fixture('sample_repo')
    def test_hotfix_list_verbose(self):
        self.repo.create_head('hf/2.3', 'HEAD')
        stdout = run_git_flow('hotfix', 'list', '--verbose', capture=1)
        expected = [
            '  2.3 (based on latest stable)'
        ]
        self.assertEqual(stdout.splitlines(), expected)

    @copy_from_fixture('release')
    def test_hotfix_list_verbose_tagged(self):
        run_git_flow('release', 'finish', '1.0')
        run_git_flow('hotfix', 'start', '1.0.1')
        fake_commit(self.repo, 'Hotfix commit.')
        stdout = run_git_flow('hotfix', 'list', '--verbose', capture=1)
        expected = [
            '* 1.0.1 (based on v1.0)'
        ]
        self.assertEqual(stdout.splitlines(), expected)

    # --- hotfix start ---

    @copy_from_fixture('sample_repo')
    def test_hotfix_start(self):
        run_git_flow('hotfix', 'start', 'wow-hotfix')
        self.assertIn('hf/wow-hotfix', Repo().branches)

    @copy_from_fixture('sample_repo')
    def test_hotfix_start_alt_base(self):
        run_git_flow('hotfix', 'start', 'wow-hotfix', 'stable')
        self.assertIn('hf/wow-hotfix', Repo().branches)

    @copy_from_fixture('sample_repo')
    def test_hotfix_start_wrong_alt_base_raises_error(self):
        self.assertRaises(BaseNotOnBranch,
                          run_git_flow, 'hotfix', 'start', 'wow-feature', 'devel')

    @copy_from_fixture('sample_repo')
    def test_hotfix_start_empty_name(self):
        self.assert_argparse_error('must not by empty',
                                   run_git_flow, 'hotfix', 'start', '')

    @copy_from_fixture('sample_repo')
    def test_hotfix_start_no_name(self):
        self.assert_argparse_error(None,
                                   run_git_flow, 'hotfix', 'start')

    # --- hotfix finish ---

    @remote_clone_from_fixture('sample_repo')
    def test_hotfix_finish(self):
        GitFlow('.').init()
        run_git_flow('hotfix', 'start', 'fast')
        self.assertIn('hf/fast', Repo().branches)
        run_git_flow('hotfix', 'finish', 'fast')
        self.assertNotIn('hf/fast', Repo().branches)

    @copy_from_fixture('sample_repo')
    def test_hotfix_finish_current(self):
        GitFlow('.').init()
        run_git_flow('hotfix', 'start', 'fast')
        run_git_flow('hotfix', 'finish')
        self.assertNotIn('hf/fast', Repo().branches)

    @copy_from_fixture('sample_repo')
    def test_hotfix_finish_empty_prefix(self):
        GitFlow('.').init()
        run_git_flow('hotfix', 'start', 'fast')
        run_git_flow('hotfix', 'finish', '')
        self.assertNotIn('hf/fast', Repo().branches)

    @copy_from_fixture('sample_repo')
    def test_hotfix_finish_prefix(self):
        GitFlow('.').init()
        run_git_flow('hotfix', 'start', 'fast')
        self.assertRaises(NoSuchBranchError,
                          run_git_flow, 'hotfix', 'finish', 'f')

    # :todo: test-cases for `hotfix finish --rebase`
    # :todo: test-cases for `hotfix finish --fetch`
    # :todo: test-cases for `hotfix finish --keep`
    # :todo: test-cases for `hotfix finish --force-delete`

    # --- hotfix publish ---

    @remote_clone_from_fixture('sample_repo')
    def test_hotfix_publish(self):
        GitFlow('.').init()
        run_git_flow('hotfix', 'start', 'wow')
        run_git_flow('hotfix', 'publish', 'wow')
        self.assertIn('hf/wow', Repo().remotes['my-remote'].refs)

    @remote_clone_from_fixture('sample_repo')
    def test_hotfix_publish_current(self):
        GitFlow('.').init()
        run_git_flow('hotfix', 'start', 'wow')
        run_git_flow('hotfix', 'publish')
        self.assertIn('hf/wow', Repo().remotes['my-remote'].refs)

    @remote_clone_from_fixture('sample_repo')
    def test_hotfix_publish_empty_prefix(self):
        GitFlow('.').init()
        run_git_flow('hotfix', 'start', 'wow')
        run_git_flow('hotfix', 'publish', '')
        self.assertIn('hf/wow', Repo().remotes['my-remote'].refs)

    @remote_clone_from_fixture('sample_repo')
    def test_hotfix_publish_prefix(self):
        GitFlow('.').init()
        run_git_flow('hotfix', 'start', 'wow')
        self.assertRaises(NoSuchBranchError,
                          run_git_flow, 'hotfix', 'publish', 'w')

    # --- unsupported `hotfix` subcommands ---

    def test_hotfix_track_is_no_valid_subcommand(self):
        self.assert_argparse_error("invalid choice: 'track'",
                                   run_git_flow, 'hotfix', 'track')

    def test_hotfix_diff_is_no_valid_subcommand(self):
        self.assert_argparse_error("invalid choice: 'diff'",
                                   run_git_flow, 'hotfix', 'diff')

    def test_hotfix_rebase_is_no_valid_subcommand(self):
        self.assert_argparse_error("invalid choice: 'rebase'",
                                   run_git_flow, 'hotfix', 'rebase')

    def test_hotfix_checkout_is_no_valid_subcommand(self):
        self.assert_argparse_error("invalid choice: 'checkout'",
                                   run_git_flow, 'hotfix', 'checkout')

    def test_hotfix_pull_is_no_valid_subcommand(self):
        self.assert_argparse_error("invalid choice: 'pull'",
                                   run_git_flow, 'hotfix', 'pull')


class TestSupport(TestCase):

    @copy_from_fixture('sample_repo')
    def test_support_list(self):
        self.repo.create_head('supp/1.0-22', 'HEAD')
        stdout = run_git_flow('support', 'list', capture=1)
        expected = [
            '  1.0-22'
        ]
        self.assertEqual(stdout.splitlines(), expected)

    @copy_from_fixture('sample_repo')
    def test_support_list_verbose(self):
        self.repo.create_head('supp/1.0-22', 'HEAD')
        stdout = run_git_flow('support', 'list', '--verbose', capture=1)
        expected = [
            '  1.0-22 (based on latest stable)'
        ]
        self.assertEqual(stdout.splitlines(), expected)

    @copy_from_fixture('release')
    def test_support_list_verbose_tagged(self):
        run_git_flow('release', 'finish', '1.0')
        run_git_flow('support', 'start', '1.0-22')
        fake_commit(self.repo, 'Support commit.')
        stdout = run_git_flow('support', 'list', '--verbose', capture=1)
        expected = [
            '* 1.0-22 (based on v1.0)'
        ]
        self.assertEqual(stdout.splitlines(), expected)

    # --- support start ---

    @copy_from_fixture('sample_repo')
    def test_support_start(self):
        run_git_flow('support', 'start', 'wow-support')
        self.assertIn('supp/wow-support', Repo().branches)

    @copy_from_fixture('sample_repo')
    def test_support_start_alt_base(self):
        run_git_flow('support', 'start', 'wow-support', 'stable')
        self.assertIn('supp/wow-support', Repo().branches)

    @copy_from_fixture('sample_repo')
    def test_support_start_wrong_alt_base_raises_error(self):
        self.assertRaises(BaseNotOnBranch,
                          run_git_flow, 'support', 'start', 'wow-support', 'devel')

    @copy_from_fixture('sample_repo')
    def test_support_start_empty_name(self):
        self.assert_argparse_error('must not by empty',
                                   run_git_flow, 'support', 'start', '')

    @copy_from_fixture('sample_repo')
    def test_support_start_no_name(self):
        self.assert_argparse_error(None,
                                   run_git_flow, 'support', 'start')

    # --- unsupported `support` subcommands ---

    def test_support_publish_is_no_valid_subcommand(self):
        self.assert_argparse_error("invalid choice: 'finish'",
                                   run_git_flow, 'support', 'finish')

    def test_support_track_is_no_valid_subcommand(self):
        self.assert_argparse_error("invalid choice: 'track'",
                                   run_git_flow, 'support', 'track')

    def test_support_diff_is_no_valid_subcommand(self):
        self.assert_argparse_error("invalid choice: 'diff'",
                                   run_git_flow, 'support', 'diff')

    def test_support_rebase_is_no_valid_subcommand(self):
        self.assert_argparse_error("invalid choice: 'rebase'",
                                   run_git_flow, 'support', 'rebase')

    def test_support_checkout_is_no_valid_subcommand(self):
        self.assert_argparse_error("invalid choice: 'checkout'",
                                   run_git_flow, 'support', 'checkout')

    def test_support_pull_is_no_valid_subcommand(self):
        self.assert_argparse_error("invalid choice: 'pull'",
                                   run_git_flow, 'support', 'pull')
