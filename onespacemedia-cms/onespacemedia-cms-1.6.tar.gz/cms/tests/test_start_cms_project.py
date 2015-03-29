from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from ..bin.start_cms_project import (Output, git, make_executable, query_yes_no,
                                     configure_apps, main)

import mock
from mock import call
import os
from StringIO import StringIO
import sys


class TestStartCMSProject(TestCase):

    def setUp(self):
        # Redirect STDOUT so we can capture the `print`.
        self.orig_stdout = sys.stdout
        self.stdout = StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        sys.stdout = self.orig_stdout

    def test_output_info(self):
        Output().info('Foo')
        self.assertEqual(self.stdout.getvalue().strip(), '[\x1b[92mINFO\x1b[0m] Foo')

    def test_output_warn(self):
        # Redirect STDOUT so we can capture the `print`.
        Output().warn('Foo')
        self.assertEqual(self.stdout.getvalue().strip(), '[\x1b[93mWARN\x1b[0m] Foo')

    @mock.patch('cms.bin.start_cms_project.subprocess')
    def test_git(self, mock_subprocess):
        git('status')
        mock_subprocess.check_call.assert_called_with(['git', 'status'])

    @mock.patch('cms.bin.start_cms_project.os')
    def test_make_executable(self, mock_os):
        make_executable('test.png')
        mock_os.stat.assert_called_with('test.png')
        mock_os.chmod.assert_called()

    @mock.patch('cms.bin.start_cms_project.sys')
    @mock.patch('__builtin__.raw_input', return_value='y')
    def test_query_yes_no(self, mock_raw_input, mock_sys):
        query_yes_no('Foo')
        mock_raw_input.assert_called_with()
        mock_sys.stdout.write.assert_called_with('Foo [Y/n] ')

        query_yes_no('Foo', None)
        mock_raw_input.assert_called_with()
        mock_sys.stdout.write.assert_called_with('Foo [y/n] ')

        query_yes_no('Foo', 'yes')
        mock_raw_input.assert_called_with()
        mock_sys.stdout.write.assert_called_with('Foo [Y/n] ')

        query_yes_no('Foo', 'no')
        mock_raw_input.assert_called_with()
        mock_sys.stdout.write.assert_called_with('Foo [y/N] ')

        with self.assertRaises(ValueError):
            query_yes_no('Foo', 'foo')

        with mock.patch('cms.bin.start_cms_project.sys') as mock_sys:
            with mock.patch('__builtin__.raw_input', side_effect=['foo', 'y']) as mock_raw_input:
                query_yes_no('Foo')
                mock_raw_input.assert_called_with()

                self.assertListEqual(mock_sys.stdout.write.call_args_list, [
                    call('Foo [Y/n] '),
                    call("Please respond with 'yes' or 'no' (or 'y' or 'n').\n"),
                    call('Foo [Y/n] ')
                ])

        with mock.patch('__builtin__.raw_input', return_value='') as mock_raw_input:
            query_yes_no('Foo', 'no')
            mock_raw_input.assert_called_with()
            mock_sys.stdout.write.assert_called_with('Foo [Y/n] ')

    def test_configure_apps(self):
        os_paths = [
            '/tmp/apps/temp/',
            '/tmp/settings/base.py',
            '/tmp/settings/base.py',
            '/tmp/apps/temp/people/',
            '/tmp/apps/temp/people/apps/people/',
            '/tmp/apps/',
            '/tmp/apps/people/models.py',
            '/tmp/apps/people/models.py',
            '/tmp/apps/temp/people/apps/people/',
            '/tmp/templates/',
        ]

        os_walk = [
            ('/tmp/apps/temp/people', ['apps', 'templates'], ['.gitignore']),
            ('/tmp/apps/temp/people/apps', ['people'], []),
            ('/tmp/apps/temp/people/apps/people', ['migrations', 'templatetags', 'tests'], ['__init__.py', 'admin.py', 'models.py', 'urls.py', 'views.py']),
            ('/tmp/apps/temp/people/apps/people/migrations', [], ['0001_initial.py', '__init__.py']),
            ('/tmp/apps/temp/people/apps/people/templatetags', [], ['__init__.py', 'people.py']),
            ('/tmp/apps/temp/people/apps/people/tests', [], ['__init__.py', 'test_models.py']),
            ('/tmp/apps/temp/people/templates', ['people'], []),
            ('/tmp/apps/temp/people/templates/people', ['includes'], ['person_detail.html', 'person_list.html', 'team_detail.html', 'team_list.html']),
            ('/tmp/apps/temp/people/templates/people/includes', [], ['people_list.html'])
        ]

        files = [
            SimpleUploadedFile('base.py', '{{ project_name }}'),
            SimpleUploadedFile('base.py', '{{ project_name }}'),
            SimpleUploadedFile('models.py', '{{ project_name }}'),
            SimpleUploadedFile('models.py', '')
        ]

        with mock.patch('cms.bin.start_cms_project.os'), \
                mock.patch('cms.bin.start_cms_project.os.walk', return_value=os_walk) as mock_os_walk, \
                mock.patch('cms.bin.start_cms_project.os.path.join', side_effect=os_paths) as mock_os_path_join, \
                mock.patch('cms.bin.start_cms_project.subprocess.check_call') as mock_check_call, \
                mock.patch('cms.bin.start_cms_project.shutil.move') as mock_shutil_move, \
                mock.patch('cms.bin.start_cms_project.shutil.rmtree') as mock_shutil_rmtree, \
                mock.patch('__builtin__.open', side_effect=files) as mock_open:
            configure_apps('/tmp', {'people': True, 'jobs': False}, 'foo')

        self.assertListEqual(mock_os_walk.call_args_list, [
            call('/tmp/apps/temp/people/'),
        ])

        self.assertListEqual(mock_os_path_join.call_args_list, [
            call('/tmp', 'apps', 'temp'),
            call('/tmp', 'settings', 'base.py'),
            call('/tmp', 'settings', 'base.py'),
            call('/tmp/apps/temp/', 'people'),
            call('/tmp/apps/temp/people/', 'apps', 'people'),
            call('/tmp', 'apps'),
            call('/tmp', 'apps', 'people', 'models.py'),
            call('/tmp', 'apps', 'people', 'models.py'),
            call('/tmp/apps/temp/people/', 'templates', 'people'),
            call('/tmp', 'templates')
        ])

        self.assertListEqual(mock_check_call.call_args_list, [
            call([
                'git',
                'clone',
                'git://github.com/onespacemedia/cms-people.git',
                '/tmp/apps/temp/people/',
                '-q'
            ])
        ])

        self.assertListEqual(mock_shutil_move.call_args_list, [
            call('/tmp/apps/temp/people/apps/people/', '/tmp/apps/'),
            call('/tmp/apps/temp/people/apps/people/', '/tmp/templates/')
        ])

        self.assertListEqual(mock_shutil_rmtree.call_args_list, [
            call('/tmp/apps/temp/')
        ])

        self.assertListEqual(mock_open.call_args_list, [
            call('/tmp/settings/base.py'),
            call('/tmp/settings/base.py', 'w'),
            call('/tmp/apps/people/models.py', 'r'),
            call('/tmp/apps/people/models.py', 'w')
        ])

        self.assertEqual(self.stdout.getvalue().strip(), '[\x1b[92mINFO\x1b[0m] Installed people app')

        # Try to break things.
        self.stdout = StringIO()
        sys.stdout = self.stdout

        os_paths = [
            '/tmp/apps/temp/',
            '/tmp/settings/base.py',
            '/tmp/settings/base.py',
            '/tmp/settings/base.py',
            '/tmp/settings/base.py',
        ]

        files = [
            SimpleUploadedFile('base.py', '{{ project_name }}'),
            SimpleUploadedFile('base.py', '{{ project_name }}'),
            SimpleUploadedFile('base.py', '{{ project_name }}'),
            SimpleUploadedFile('base.py', '{{ project_name }}'),
        ]

        with mock.patch('cms.bin.start_cms_project.os'), \
                mock.patch('cms.bin.start_cms_project.os.path.join', side_effect=os_paths) as mock_os_path_join, \
                mock.patch('cms.bin.start_cms_project.shutil.rmtree') as mock_shutil_rmtree, \
                mock.patch('__builtin__.open', side_effect=files) as mock_open:
            configure_apps('/tmp', {'people': True, 'jobs': False, 'faqs': False}, 'foobar')
            self.assertEqual(self.stdout.getvalue().strip(), 'Error:')

    def _test_main_func(self, with_or_without):
        self.stdout = StringIO()
        sys.stdout = self.stdout

        sys.argv = [
            '',
            'foo',
            '/tmp',
            '--{}-people'.format(with_or_without)
        ]

        files = [
            SimpleUploadedFile('base.py', '"usertools",\n""'),
            SimpleUploadedFile('base.py', ''),
            SimpleUploadedFile('change_list.html', ''),
            SimpleUploadedFile('server.json', ''),
            open(os.devnull, 'w'),
        ]

        with mock.patch('os.makedirs') as mock_os_makedirs, \
                mock.patch('cms.bin.start_cms_project.management') as mock_django_core_management, \
                mock.patch('cms.bin.start_cms_project.query_yes_no', return_value=True) as mock_query_yes_no, \
                mock.patch('cms.bin.start_cms_project.make_executable') as mock_make_executable, \
                mock.patch('cms.bin.start_cms_project.configure_apps') as mock_configure_apps, \
                mock.patch('cms.bin.start_cms_project.subprocess.call') as mock_call, \
                mock.patch('__builtin__.open', side_effect=files) as mock_open:
            main()

            self.assertListEqual(mock_os_makedirs.call_args_list, [
                call('/tmp'),
                call('/tmp/foo/templates/admin/auth/user')
            ])

            self.assertListEqual(mock_django_core_management.call_args_list, [

            ])

            self.assertListEqual(mock_query_yes_no.call_args_list, [
                # call('Would you like the people module?'),
                call('Would you like the jobs module?'),
                call('Would you like the FAQs module?')
            ])

            if with_or_without == 'with':
                self.assertListEqual(mock_configure_apps.call_args_list, [
                    call('/tmp/foo', {'faqs': True, 'jobs': True, 'people': True}, 'foo')
                ])
            elif with_or_without == 'without':
                self.assertListEqual(mock_configure_apps.call_args_list, [
                    call('/tmp/foo', {'faqs': True, 'jobs': True, 'people': False}, 'foo')
                ])

            self.assertListEqual(mock_make_executable.call_args_list, [
                call('/tmp/manage.py')
            ])

            self.assertListEqual(mock_open.call_args_list, [
                call('/tmp/foo/settings/base.py'),
                call('/tmp/foo/settings/base.py', 'w'),
                call('/tmp/foo/templates/admin/auth/user/change_list.html', 'w+'),
                call('/tmp/foo/server.json', 'w+'),
                call('/dev/null', 'w')
            ])

            self.assertEqual(
                mock_call.call_args_list[0][0][0],
                ['npm', 'install', '-g', 'bower', 'gulp']
            )

            self.assertEqual(
                mock_call.call_args_list[1][0][0],
                ['npm', 'install']
            )

            self.assertEqual(
                mock_call.call_args_list[2][0][0],
                ['gulp', 'initialise']
            )

            self.assertEqual(
                mock_call.call_args_list[3][0][0],
                ['gulp', 'styles']
            )

            self.assertEqual(
                self.stdout.getvalue().strip(),
                '[\x1b[93mWARN\x1b[0m] Usertools is not installed\n[\x1b[92mINF'
                'O\x1b[0m] Installing bower and gulp\n[\x1b[92mINFO\x1b[0m] Ins'
                'talling npm dependancies\n[\x1b[92mINFO\x1b[0m] Running gulp\n'
                '[\x1b[92mINFO\x1b[0m] CMS project created'
            )

    def test_main_func(self):
        self._test_main_func('with')
        self._test_main_func('without')

    def test_main_func_exceptions(self):
        # Now test exceptions.
        sys.argv = [
            '',
            'foo',
            '/tmp',
            '--with-people',
            '--without-people'
        ]

        with mock.patch('os.makedirs', side_effect=OSError) as mock_os_makedirs, \
                mock.patch('cms.bin.start_cms_project.management.call_command') as mock_call_command, \
                self.assertRaises(SystemExit):
            main()

        self.assertListEqual(mock_os_makedirs.call_args_list, [
            call('/tmp')
        ])

        self.assertListEqual(mock_call_command.call_args_list, [
            call(
                'startproject',
                'foo',
                '/tmp',
                extensions=['py', 'txt', 'conf', 'gitignore', 'md', 'css', 'js', 'json'],
                user=os.getlogin(),
                # Did someone say 'clunky'?
                template=os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../project_template')),
                project_slug='foo'
            )
        ])

        self.assertEqual(
            self.stdout.getvalue().strip(),
            'You cannot use --with-people and --without-people together.'
        )
