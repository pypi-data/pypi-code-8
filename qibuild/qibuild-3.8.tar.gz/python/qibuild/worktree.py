## Copyright (c) 2012-2015 Aldebaran Robotics. All rights reserved.
## Use of this source code is governed by a BSD-style license that can be
## found in the COPYING file.
import os
import sys
import difflib

from qisys import ui
import qisys.command
import qisys.worktree
import qibuild.build
import qibuild.build_config
import qibuild.deps
import qibuild.project


class BuildWorkTree(qisys.worktree.WorkTreeObserver):
    """ Stores a list of projects that can be built using CMake

    """
    def __init__(self, worktree):
        self.worktree = worktree
        self.root = self.worktree.root
        self.build_config = qibuild.build_config.CMakeBuildConfig(self)
        self.build_projects = list()
        self._load_build_projects()
        worktree.register(self)

    @property
    def dot_qi(self):
        return self.worktree.dot_qi

    @property
    def qibuild_cfg(self):
        return self.build_config.qibuild_cfg

    @property
    def qibuild_xml(self):
        """ Path to <worktree>/.qi/qibuild.xml
        Will be created if it does not exist

        """
        config_path = os.path.join(self.dot_qi, "qibuild.xml")
        if not os.path.exists(config_path):
            with open(config_path, "w") as fp:
                fp.write("<qibuild />\n")
        return config_path

    @property
    def toolchain(self):
        """ The toolchain to use """
        return self.build_config.toolchain

    @property
    def default_config(self):
        """ The default config to use """
        return self.build_config.default_config

    def generate_sourceme(self):
        """ Generate a sourceme file to help running binaries using
        libraries from the build projects and the toolchain packages

        """
        subdir = self.build_config.build_directory(prefix="")
        to_make = os.path.join(self.dot_qi, subdir)
        qisys.sh.mkdir(to_make)
        sourceme = os.path.join(to_make, "sourceme")
        env = self.get_env(extend_os_environ=False)
        with open(sourceme, "w") as fp:
            to_write = "# autogenerated by qibuild. Do not edit.\n"
            for key, value in env.iteritems():
                to_write += 'export %s="%s"\n'%  (key, value)
            fp.write(to_write)
        return sourceme


    def get_env(self, extend_os_environ=True):
        """ Get an environment dictionary to help running binaries
        using libraries from the build projects and the toolchain
        packages

        """
        if extend_os_environ:
            res = os.environ.copy()
        else:
            res = dict()
        if os.name == 'nt':
            dlls_paths = self._get_dll_paths()
            res["PATH"] = ";".join(dlls_paths) + ";" + os.environ["PATH"]
        else:
            lib_paths = self._get_lib_paths()
            if sys.platform.startswith("linux"):
                res["LD_LIBRARY_PATH"] = os.path.pathsep.join(lib_paths)
            if sys.platform == "darwin":
                res["DYLD_LIBRARY_PATH"] = os.path.pathsep.join(lib_paths)
                res["DYLD_FRAMEWORK_PATH"] = os.path.pathsep.join(
                        self._get_framework_paths())
        if self.toolchain:
            python_package = self.toolchain.get_package("python", raises=False)
            if python_package:
                res["PYTHONHOME"] = python_package.path
        return res

    def _get_lib_paths(self):
        res = list()
        for project in self.build_projects:
            res.append(os.path.join(project.sdk_directory, "lib"))
        if self.toolchain:
            for package in self.toolchain.packages:
                res.append(os.path.join(package.path, "lib"))
        return res

    def _get_framework_paths(self):
        res = list()
        if self.toolchain:
            for package in self.toolchain.packages:
                res.append(package.path)
        return res

    def _get_dll_paths(self):
        res = list()
        for project in self.build_projects:
            res.append(os.path.join(project.sdk_directory, "bin"))
        if self.toolchain:
            for package in self.toolchain.packages:
                res.append(os.path.join(package.path, "bin"))
        return res

    def get_known_profiles(self):
        """ Parse the remote profiles (coming from qisrc sync), and the
        local profiles (written in .qi/qibuild.xml). Return a dict
        name -> list of tuple (key, value)

        """
        res = dict()
        remote_xml = os.path.join(self.root, ".qi", "manifests",
                                  "default", "manifest.xml")
        if os.path.exists(remote_xml):
            res = qibuild.profile.parse_profiles(remote_xml)
        local_xml = self.qibuild_xml
        local_profiles = qibuild.profile.parse_profiles(local_xml)
        res.update(local_profiles)
        return res

    def get_build_project(self, name, raises=True):
        """ Get a :py:class:`.BuildProject` given its name """
        for build_project in self.build_projects:
            if build_project.name == name:
                return build_project
        if raises:
            mess = ui.did_you_mean("No such qibuild project: %s" % name,
                                   name, [x.name for x in self.build_projects])
            raise BuildWorkTreeError(mess)

    def on_project_added(self, project):
        """ Called when a new project has been registered """
        self._load_build_projects()

    def on_project_removed(self, project):
        """ Called when a build project has been removed """
        self._load_build_projects()

    def on_project_moved(self, project):
        self._load_build_projects()

    def _load_build_projects(self):
        """ Create BuildProject for every buildable project in the
        worktree

        """
        self.build_projects = list()
        for wt_project in self.worktree.projects:
            build_project = new_build_project(self, wt_project)
            if build_project:
                self.check_unique_name(build_project)
                self.build_projects.append(build_project)

    def configure_build_profile(self, name, flags):
        """ Configure a build profile for the worktree """
        qibuild.profile.configure_build_profile(self.qibuild_xml,
                                                name, flags)

    def remove_build_profile(self, name):
        """ Remove a build profile for this worktree """
        qibuild.profile.remove_build_profile(self.qibuild_xml, name)

    def set_default_config(self, name):
        """ Set the default toolchain for this worktree """
        qibuild_cfg = qibuild.config.QiBuildConfig()
        qibuild_cfg.read(create_if_missing=True)
        qibuild_cfg.set_default_config_for_worktree(self.root, name)
        qibuild_cfg.write()

    def set_active_config(self, active_config):
        """ Set the config to use for this worktree
        Should match a build config name

        """
        self.build_config.set_active_config(active_config)

    def check_unique_name(self, new_project):
        for project in self.build_projects:
            if project.name == new_project.name:
                raise Exception("""\
Found two projects with the same name ({project.name})
In:
* {project.path}
* {new_project.path}
""".format(project=project, new_project=new_project))




def new_build_project(build_worktree, project):
    """ Cerate a new BuildProject from a worktree project.
    Return None if there is no BuildProject here

    """
    if not os.path.exists(project.qiproject_xml):
        return None
    tree = qisys.qixml.read(project.qiproject_xml)
    root = tree.getroot()
    if root.get("version") == "3":
        qibuild_elem = root.find("qibuild")
        if qibuild_elem is None:
            return None
    else:
        # qibuild2 used to check for a CMakeLists.txt
        cmake_lists = os.path.join(project.path, "CMakeLists.txt")
        if not os.path.exists(cmake_lists):
            return None
        qibuild_elem = root

    name = qibuild_elem.get("name")
    if not name:
        return None

    build_project = qibuild.project.BuildProject(build_worktree, project)
    build_project.name = name
    build_project.version = qibuild_elem.get("version", "0.1")
    qibuild.deps.read_deps_from_xml(build_project, qibuild_elem)

    return build_project


class BuildWorkTreeError(Exception):
    pass

class BadProjectConfig(Exception):
    def __str__(self):
        return """
Incorrect configuration detected for project in {0}
{1}
""".format(*self.args)
