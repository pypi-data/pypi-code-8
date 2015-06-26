# -*- coding: utf-8 -*-
# (c) 2015 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
import os
from unittest.case import TestCase
from mock import MagicMock, patch
from bright_fabric.tasks import pylint
from tests.util import ArgumentCaptor, OverrideFabricConfig


class TaskTests(TestCase):

    test_data_path = os.path.join('tests', 'test_data', 'tasks')

    py_in_path = [
        'one.py',
        os.path.join('subdir', 'two.py')
    ]

    def setUp(self):
        self.mock_fabric_api = MagicMock()

    @patch('bright_fabric.tasks.local')
    def test_pylint_runs_without_ignores_by_default(self, mock_local):
        pylint()
        captor = ArgumentCaptor()
        mock_local.assert_called_with(captor)
        self.assertTrue(all([
            captor.argument.startswith('flake8'),
            '--ignore' not in captor.argument,
        ]))

    @patch('bright_fabric.tasks.local')
    def test_pylint_runs_flake_with_ignores_if_configured(self, mock_local):
        with OverrideFabricConfig(pylint_ignore_errors=['E591', 'E100']):
            pylint()
            captor = ArgumentCaptor()
            mock_local.assert_called_with(captor)
            self.assertTrue(all([
                captor.argument.startswith('flake8'),
                '--ignore=E591,E100' in captor.argument,
            ]))

    @patch('bright_fabric.tasks.local')
    def test_pylint_runs_flake_on_all_python_files_in_configured_folders(self, mock_local):
        with OverrideFabricConfig(pylint_dirs=[self.test_data_path]):
            pylint()
            captor = ArgumentCaptor()
            mock_local.assert_called_with(captor)
            self.assertTrue(captor.argument.startswith('flake8'))
            for file in self.py_in_path:
                self.assertIn(file, captor.argument)

    @patch('bright_fabric.tasks.local')
    def test_pylint_runs_flake_on_current_working_path_if_no_dirs_configured(self, mock_local):
        pylint()
        captor = ArgumentCaptor()
        mock_local.assert_called_with(captor)
        self.assertTrue(captor.argument.startswith('flake8'))
        self.assertIn(os.path.abspath('fabfile.py'), captor.argument)

    @patch('bright_fabric.tasks.local')
    def test_pylint_ignores_excluded_dirs(self, mock_local):
        with OverrideFabricConfig(pylint_exclude_dirs=['subdir']):
            pylint()
            captor = ArgumentCaptor()
            mock_local.assert_called_with(captor)
            self.assertTrue(captor.argument.startswith('flake8'))
            self.assertNotIn(
                os.path.abspath(
                    os.path.join(
                        self.test_data_path, 'subdir', 'two.py'
                    )
                ),
                captor.argument
            )
