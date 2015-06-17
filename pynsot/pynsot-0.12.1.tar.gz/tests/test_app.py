# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Test the CLI app.
"""

import logging
import os
import pytest
import shlex
import tempfile

from pynsot.app import app
from pynsot.vendor import click
from pynsot.vendor.click.testing import CliRunner

from .fixtures import config


# Hard-code the app name as 'nsot' to match the CLI util.
app.name = 'nsot'


def test_site_id(config):
    runner = CliRunner()

    # Make sure it says site-id is required
    result = runner.invoke(app, shlex.split('devices list'))

    assert result.exit_code == 2
    expected_output = (
        'Usage: nsot devices list [OPTIONS]\n'
        '\n'
        'Error: Missing option "-s" / "--site-id".\n'
    )
    assert result.output == expected_output
