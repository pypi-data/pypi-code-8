# Copyright 2015, Kevin Carter.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example Usage:
>>> from cloudlib import package_installer
>>> packages_dict = {
...     'apt': {
...         'packages': [
...             'someDebianPackageName'
...         ],
...     },
...     'yum': {
...         'packages': [
...             'someRHELPackageName'
...         ]
...     }
... }
>>> installer = package_installer.PackageInstaller(
...     packages_dict=packages_dict
... )
>>> installer.install()
"""

import platform

from cloudlib import shell
from cloudlib import logger


def distro_check():
    """Return a string containing the distro package manager."""
    distro_data = platform.linux_distribution()
    distro = [d.lower() for d in distro_data if d.isalpha()]

    if any(['ubuntu' in distro, 'debian' in distro]) is True:
        return 'apt'
    elif any(['centos' in distro, 'redhat' in distro]) is True:
        return 'yum'
    elif any(['suse' in distro]) is True:
        return 'zypper'
    else:
        raise AssertionError(
            'Distro [ %s ] is unsupported.' % distro
        )


class PackageInstaller(object):

    def __init__(self, packages_dict, log_name=__name__):
        """Install packages on a local Linux Operating System.

        :param packages_dict: ``dict``
        :param log_name: ``str`` This is used to log against an existing log
                                 handler.
        """
        self.log = logger.getLogger(log_name)
        self.shell = shell.ShellCommands(log_name=log_name)

        self.distro = None
        self.packages_dict = packages_dict

        self.install_process = {
            'apt': "apt-get update && apt-get"
                   " -o Dpkg::Options:='--force-confold'"
                   " -o Dpkg::Options:='--force-confdef'"
                   " -y install %s",
            'yum': "yum -y instaall %s",
            'zypper': "zypper -n install %s"
        }
        self.install_string = None

    def _installer(self, package_list, install_string=None):
        """Install operating system packages for the system.

        :param: package_list: ``list``
        :param install_string: ``str``
        """
        packages = ' '.join(package_list)

        if install_string is None:
            self.install_string = self.install_process[self.distro] % packages
        else:
            self.install_string = install_string

        output, outcome = self.shell.run_command(command=self.install_string)

        if outcome is False:
            raise IOError(output)

    def install(self):
        """Install packages from the packages_dict."""
        self.distro = distro_check()
        package_list = self.packages_dict.get(self.distro)
        self._installer(package_list=package_list.get('packages'))
