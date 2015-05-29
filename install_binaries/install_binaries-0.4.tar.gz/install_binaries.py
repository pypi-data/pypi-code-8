"""
install_binaries - Install binaries to the same place Python puts scripts.

For more info, see README.md
"""

import os
from stat import ST_MODE
from setuptools.dist import assert_string_list
from distutils.core import Command
from distutils import log


class install_binaries(Command):
    # Brief (40-50 characters) description of the command
    description = "Installs binaries to the same place Python puts scripts."

    # List of option tuples: long name, short name (None if no short
    # name), and help string.
    user_options = []

    def initialize_options(self):
        self.install_dir = None
        self.binaries = None

    def finalize_options(self):
        # We want to install to the same place as 'install_scripts',
        # because presumably that will be on the PATH.
        self.set_undefined_options('install',
                                   ('install_scripts', 'install_dir'))
        self.binaries = self.distribution.install_binaries

    def run(self):
        self.mkpath(self.install_dir)
        self.outfiles = []
        log.info("install_binaries: ensuring mode is a+rx")
        for binary in self.binaries:
            if not os.path.exists(binary):
                self.warn(
                    '  %s seems not to exist - is it in your MANIFEST.in?'
                    % binary)

            # Install the file (self.copy_file handles dry_run)
            path = os.path.join(self.install_dir, os.path.basename(binary))
            self.copy_file(binary, path)
            self.outfiles.append(path)

            if self.dry_run:
                log.info("  changing mode of %s +rx", path)
            else:
                old_mode = os.stat(path)[ST_MODE]
                mode = (old_mode | 0o555) & 0o7777

                if old_mode & 0o0555 == 0o0555:
                    log.info("  mode of %s is already %o, leaving alone",
                             path, old_mode % 0o10000)
                else:
                    log.info("  changing mode of %s to %o", path, mode)
                    os.chmod(path, mode)

    def get_inputs(self):
        return self.distribution.install_binaries or []

    def get_outputs(self):
        return self.outfiles or []


def handle_install_binaries(dist, attr, value):
    "Handles the install_binaries= setup() keyword arg"

    assert_string_list(dist, attr, value)

    script_args = ''.join(getattr(dist, 'script_args', []))

    if 'install' in script_args:
        if not ('single-version-externally-managed' in script_args
                or getattr(dist, 'single_version_externally_managed', 0)
                or getattr(dist, 'old_and_unmanageable', 0)):
            #
            # If none of those options are set, setuptools will run
            # easy_install.  easy_install, in turn, will install as an egg, and
            # doesn't run its sub_commands, so we can't install our binaries
            # (without much hackery).
            #
            # pip sets single_version_externally_managed.
            #

            log.warn('Warning: "easy_install" and "setup.py install" are'
                     ' unlikely to install binaries correctly')
            log.warn('Run "pip install <package or directory>" instead')

    from setuptools.command.install import install
    install.sub_commands.append(
        ('install_binaries', lambda *a: True))
