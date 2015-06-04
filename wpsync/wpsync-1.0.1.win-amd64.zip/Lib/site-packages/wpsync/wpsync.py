#!/usr/bin/python
#  _       ______  _____
# | |     / / __ \/ ___/__  ______  _____
# | | /| / / /_/ /\__ \/ / / / __ \/ ___/
# | |/ |/ / ____/___/ / /_/ / / / / /__
# |__/|__/_/    /____/\__, /_/ /_/\___/
#                    /____/
#
# Copyright (C) 2015 Henrique Dias <hacdias@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import json
import tempfile
import subprocess
import shutil
import re


class Composer:
    def __init__(self):
        self.main = 'composer.json'
        self.lock = 'composer.lock'
        self.json = json.loads(open(self.main).read())
        self.folder = 'vendor'
        self.__check_folder()

    def __check_folder(self):
        if 'config' in self.json:
            if 'vendor-dir' in self.json['config']:
                self.folder = self.json['config']['vendor-dir']

        self.folder = os.path.normpath(self.folder)

    def update(self):
        if os.path.isfile(self.lock):
            os.remove(self.lock)

        if os.path.isdir(self.folder):
            shutil.rmtree(self.folder)

        subprocess.call('composer install', shell=True)


class Bower:
    def __init__(self):
        self.main = 'bower.json'
        self.cnf = '.bowerrc'
        self.json = json.loads(open(self.main).read())
        self.folder = 'bower_components'
        self.config = ''
        self.__check_folder()

    def __check_folder(self):
        if os.path.isfile(self.cnf):
            self.config = json.loads(open(self.cnf).read())

            if 'directory' in self.config:
                self.folder = self.config['directory']

        self.folder = os.path.normpath(self.folder)

    def update(self):
        if os.path.isdir(self.folder):
            shutil.rmtree(self.folder)

        subprocess.call('bower install', shell=True)


class Git:
    def __init__(self):
        self.commit = ''
        self.tag = ''

    def update(self):
        subprocess.call("git add -A", shell=True)

        if self.tag is not '':
            subprocess.call("git tag " + self.tag, shell=True)

        if self.commit is '':
            print("You haven't mentioned the commit message.")
            exit(1)

        subprocess.call("git commit -m '" + self.commit + "'", shell=True)

        subprocess.call("git push", shell=True)
        subprocess.call("git push --tags", shell=True)
        return


class Svn:
    def __init__(self):
        self.commit = ''
        self.tag = ''

    def update(self):
        if self.tag is not '':
            repo = os.getcwd()
            trunk = os.path.join(repo, 'trunk')
            tags = os.path.join(repo, 'tags')
            new_tag = os.path.join(tags, self.tag)
            shutil.copytree(trunk, new_tag)

        if self.commit is '':
            print("You haven't mentioned the commit message.")
            exit(1)

        subprocess.call("svn add * --force", shell=True)
        subprocess.call("svn commit -m '" + self.commit + "'", shell=True)


class Plugin:
    def __init__(self):
        self.plugin_file = 'plugin.php'
        self.plugin_file_content = ''
        self.readme_file = 'readme.txt'
        self.readme_file_content = ''
        self.old_version = []
        self.new_version = []
        self.the_version = ''
        self.index = 2
        self.version_control = 'git'
        self.wordpress_svn = ''
        self.ignore_files = []

    def update(self):
        self.__get_plugin_file_content()
        self.__get_readme_content()
        self.__get_current_version()
        self.__get_new_version()

        try:
            input("Confirm you want to update your plugin to v" + self.the_version)
        except SyntaxError:
            pass

        self.__change_version_files()
        self.__update_this_repo()
        self.__update_wordpress_repo()

    def __get_current_version(self):
        match = re.search("Version:[ \t]*[\d+\.]+\d", self.plugin_file_content)

        if match is None:
            print("We can't understand the version of your plugin :(")
            exit(1)

        version = match.group(0)
        version = re.search("[\d+\.]+\d", version).group(0)
        version = version.split('.')

        self.old_version = list(map(int, version))

    def __get_plugin_file_content(self):
        self.plugin_file_content = open(self.plugin_file, 'r').read()

    def __get_readme_content(self):
        self.readme_file_content = open(self.readme_file, 'r').read()

    def __get_new_version_helper(self):
        if (self.new_version[self.index] + 1) > 9 and self.index != 0:
            self.new_version[self.index] = 0
            self.index -= 1
            self.__get_new_version_helper()
        else:
            self.new_version[self.index] += 1

    def __get_new_version(self):
        # get the version index to update
        # major.minor[.build[.revision]]
        # default is build
        index_list = {
            'major': 0,
            'minor': 1,
            'build': 2,
            'revision': 3
        }

        self.index = index_list[self.index]
        self.new_version = self.old_version
        self.__get_new_version_helper()

        self.new_version = list(map(str, self.new_version))
        self.the_version = '.'.join(self.new_version)

    def __change_version_files(self):
        plugin_search = 'Version:[ \t]*[\d+\.]+\d'
        plugin_replace = 'Version: ' + self.the_version

        self.plugin_file_content = re.sub(plugin_search, plugin_replace, self.plugin_file_content)

        with open(self.plugin_file, 'w') as fs:
            fs.write(self.plugin_file_content)

        readme_search = 'Stable tag:[ \t]*[\d+\.]+\d'
        readme_replace = 'Stable tag: ' + self.the_version

        self.readme_file_content = re.sub(readme_search, readme_replace, self.readme_file_content)

        with open(self.readme_file, 'w') as fs:
            fs.write(self.readme_file_content)

    def __update_this_repo(self):
        if self.version_control == 'svn':
            svn = Svn()
            svn.tag = 'v' + self.the_version
            svn.commit = 'v' + self.the_version
            svn.update()
            return

        # in case of being git
        git = Git()
        git.tag = 'v' + self.the_version
        git.commit = 'v' + self.the_version
        git.update()

    def __update_wordpress_repo(self):
        # save the path where we're working and creates a temporary one
        main_path = os.getcwd()
        temp_path = tempfile.mkdtemp()

        # set the files to ignore
        ignore_files = shutil.ignore_patterns(*self.ignore_files)

        # changes the working path to the temporary path
        os.chdir(temp_path)

        subprocess.call('svn checkout ' + self.wordpress_svn + ' .', shell=True)

        trunk = os.path.join(temp_path, 'trunk')
        temporary_content = os.path.join(temp_path, 'contents_temp')

        # copy the new plugin files to the temporary_folder, ignoring some files
        shutil.copytree(main_path, temporary_content, False, ignore_files)

        # replace the current 'trunk' folder with the new contents
        shutil.rmtree(trunk)
        shutil.move(temporary_content, trunk)

        svn = Svn()
        svn.commit = 'v' + self.the_version
        svn.tag = self.the_version
        svn.update()

        # return to the first working path
        os.chdir(main_path)

        # remove the temporary folder
        shutil.rmtree(temp_path, True)


def main():
    config_file = 'wpsync.json'

    if not os.path.isfile(config_file):
        print('There is no configuration file.')
        exit(1)

    config = json.loads(open(config_file).read())

    if 'plugin' not in config:
        print('You have problems in the configuration file.')
        exit(1)

    if 'wordpress-svn' not in config:
        print("You haven't defined the WordPress SVN link.")
        exit(1)

    if 'trunk' in config['wordpress-svn']:
        print('Please remove "trunk" from the SVN link.')
        exit(1)

    if os.path.isfile('composer.json'):
        composer = Composer()
        composer.update()

    if os.path.isfile('bower.json'):
        bower = Bower()
        bower.update()

    plugin = Plugin()
    plugin.plugin_file = config['plugin']['main'] if 'main' in config['plugin'] else 'plugin.php'
    plugin.index = config['increase'] if 'increase' in config else 'build'

    if os.path.isdir('.svn'):
        plugin.version_control = 'svn'

    plugin.wordpress_svn = config['wordpress-svn']

    if 'ignore' in config:
        plugin.ignore_files = config['ignore']

    plugin.update()

    try:
        input("Press any key to continue...")
    except SyntaxError:
        pass
