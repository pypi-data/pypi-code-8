#!python
#-*- coding: UTF-8 -*-



import sys, os, inspect, shutil, subprocess

# this should be before any distutils command
# setup tools for bdist wheel
try:
  from setuptools import setup
  from setuptools import Command
except Exception, e:
  from distutils.core import setup
  from distutils.core import Command




from distutils.command.build import build as _build
from distutils.command.build_ext import build_ext as _build_ext
from distutils.command.sdist import sdist as _sdist
from distutils import log
from distutils.util import convert_path

from distutils.extension import Extension as _Extension 


# OSX
# python setup.py build_cmake --boostroot=~/Code/SoftwareWorkshop/sw_thirdparties/osx/boost_1_55_patched/ --additionaloptions=-DBoost_COMPILER=-clang-darwin42


# This variable will contain the location where we can build the project. This is a temporary location pointing
# to a predefined place. This can be overridden during the installation by the build command to take the build_temp
# variable given by the user.
cmake_build_location    = os.path.join(os.path.dirname(__file__), 'build', 'tmp_cmake')

# This variable contains the location where the binaries should be installed. This is replaced during the install_cmake command
# by the final location. When set, the cmake is reconfigured, which lead to a possible relinking after a build_cmake.
cmake_install_location  = os.path.join(os.path.dirname(__file__), 'yayi', 'bin')

# location where the cmake --build install will copy the binaries. 
cmake_install_location_cmake = os.path.join(os.path.dirname(__file__), 'yayi', 'bin')

# This variable contains the location of the source files of Yayi. For a "sdist", the variable is used to create a proper tarball
# by copying the real repository directory into this directory.   
# note: relative path does not work, pip might uncompress the sdist anywhere
yayi_src_files_location = os.path.abspath(os.path.join(os.path.dirname(__file__), 'yayi_src_cpp'))


def _get_version():
    """"Convenient function to get the version of this package"""
    import os
    
    ns = {}
    version_path = convert_path('yayi/version.py')
    if not os.path.exists(version_path):
        return None
    with open(version_path) as version_file:
        exec(version_file.read(), ns)

    return ns['__version__']


def _utils_copy_left_to_right(root_left, left, root_right, right):
    """Simple utility function for copying files from a left directory to a right directory. The copy
       does not overwrite files when the corresponding file has the same time stamp. The files on the right
       are removed accordingly to reflect any change on the left.
  
       :param (string) root_left: root location of the files in the left. 
       :param (list) left: list of file names, relative to `root_left`
       :param (string) root_right: root location of the files in the right. 
       :param (list) right: list of file names, relative to `root_right`
       :returns: None
    """
    
    from stat import ST_MTIME
  
    keep_file = lambda x, y:  os.path.exists(os.path.join(y, x)) and os.path.isfile(os.path.join(y, x))
    
    # keep only existing ones and files
    set_left = set((i for i in left if keep_file(i, root_left))) 
    set_right= set((i for i in right if keep_file(i, root_right)))
    left_only =  set_left - set_right
    right_only = set_right - set_left
  
    # removing right only, checking consistency first
    for f in right_only:
        file_to_remove = os.path.join(root_right, f)
        assert(os.path.exists(file_to_remove))
  
    nb_removed = 0
    for f in right_only:
        os.remove(os.path.join(root_right, f))
        nb_removed += 1
  
    # copying left only
    nb_copied = 0
    for f in left_only:
        destination = os.path.join(root_right, f)
        dirname = os.path.dirname(destination)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
    
        shutil.copyfile(os.path.join(root_left, f), destination)
        nb_copied += 1
  
  
    # for the others, check the date
    nb_replaced = 0
    for f in set_left & set_right:
        src = os.path.join(root_left, f)
        dst = os.path.join(root_right, f)
    
        if os.stat(src)[ST_MTIME] > os.stat(dst)[ST_MTIME]:
            shutil.copyfile(src, dst)
            nb_replaced += 1
  
    log.warn("[YAYI] sync %s -> %s", root_left, root_right)
    log.warn("[YAYI] - copied %d / removed (right) %d / replaced %d", nb_copied, nb_removed, nb_replaced) 
    
    pass


def _utils_get_all_files(directory, no_sub_dir = False):
  """Returns all the files contained in a directory, relatively to this directory. Some files
  and extensions are ignored in the list.
  
  :param (string) directory: the directory that should be parsed
  :param (boolean) no_sub_dir: indicate if the subdirectories should be parsed as well
  :returns: a list of files relative to `directory` (`directory` is not included in the file names)
  :rtype: list
  """
  
  files_to_ignore_lower_case = ['.ds_store', '.gitignore']
  
  filter = lambda x : x.lower() not in files_to_ignore_lower_case and \
                      os.path.splitext(x)[1].lower() != '.bak' and \
                      x.find('~') == -1
  file_list = []
  for root, dirlist, filelist in os.walk(directory, True):
    file_list += [os.path.join(root, f) for f in filelist if filter(f)]
    if no_sub_dir:
      break
  
  file_list = [os.path.abspath(f) for f in file_list]
  file_list = [os.path.relpath(f, os.path.abspath(directory)) for f in file_list]
  return file_list
    
class create_package_layout(Command):
    description = "Copy the necessary files from the repository layout for making a proper distribution layout"
    user_options = [
        ('from-original-repository', None, "Set to true for original repository setup")
    ]

    def initialize_options(self):
      pass
    
    def finalize_options(self):
      pass

    def run(self):
      
      destination_directory = yayi_src_files_location
      if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
      original_repository_base_directory = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)
      
      # this is the restriction of the original project repository in order to create a source distribution.
      # this should be edited if something new is added to the general repository layout.
      paths_to_copy = (('.', True),
                       ('cmake', False), 
                       ('core', False),
                       ('doc', False),
                       ('coreTests', False), # remove the data directory here
                       ('python', False),
                       ('plugins/external_libraries', False))

      # check if we are in our repository configuration
      for current_root, nosubdir in paths_to_copy:
        if not os.path.exists(os.path.join(original_repository_base_directory, current_root)):
          return
      
      for current_root, nosubdir in paths_to_copy:        
        srcdir = os.path.join(original_repository_base_directory, current_root)
        dstdir = os.path.join(destination_directory, current_root)
        left_file_list = _utils_get_all_files(srcdir, nosubdir)
        right_file_list = _utils_get_all_files(dstdir, nosubdir) if os.path.exists(dstdir) else []
      
        _utils_copy_left_to_right(srcdir, left_file_list, dstdir, right_file_list)

      

def cmake_configure(options):
  """Configuring CMake.
  
  This is the main function for configuring CMake on all platforms. It takes 
  """ 
  
  # cmake location
  cmake_path = yayi_src_files_location
  
  # build location
  build_location = cmake_build_location
  if not os.path.exists(build_location):
    os.makedirs(build_location)
  
  # is 64 bits interpreter?
  is_64bits = sys.maxsize > 2**32
  
  
  cmd = ['cmake']
  cmd+= options
  
  
  # multiplatform options: check if numpy is available?
  cmd += ['-DENABLE_NUMPY=True']
  
  
  # "installation" location: the proper installation is performed by cmake and not by the distutils. The distutils
  # propagate the installation path to cmake using the variable "cmake_install_location_cmake". This is determined by
  # the distutil target "install"
  install_location = cmake_install_location
  if(not install_location is None):
    
    # this is the commands for OSX.
    # this looks to work properly on a boost version that was installed with brew. The boost binaries
    # should have their soname set properly (full path) otherwise DYLD_LIBRARY_PATH is required at runtime 
    cmd+= [# directory where we will install the libraries
           #'-DCMAKE_INSTALL_PREFIX=%s' % os.path.abspath(os.path.join(install_location, 'yayi', 'bin')),#cmake_install_location_cmake,
           '-DYAYI_PYTHON_PACKAGE_LOCATION=%s' % os.path.abspath(os.path.join(os.path.dirname(__file__))),
           '-DYAYI_PYTHON_PACKAGE_INSTALLATION_DIR=%s' % os.path.abspath(install_location),
           ]

  # common to linux/osx
  if sys.platform in ["linux2"]:
    cmd += [
            # indicates the location where the libraries will be installed after the setup install command
            '-DCMAKE_INSTALL_RPATH=$ORIGIN/.' #%s' % os.path.abspath(install_location),
          ]

  
  # for OSX
  if sys.platform == "darwin":
    cmd+= [# indicates that the directory part will be replaced by @rpath, related to CMAKE_INSTALL_RPATH
           '-DCMAKE_MACOSX_RPATH=ON',
           ]

  
  # for linux
  if sys.platform == "linux2":
    
    # we use system libraries instead of the ones shipped with Yayi
    for option in ["DO_NOT_USE_YAYI_JPEG", "DO_NOT_USE_YAYI_ZLIB", "DO_NOT_USE_YAYI_LIBPNG", "DO_NOT_USE_YAYI_LIBTIFF"]:
      cmd += ['-D%s=True' % option]
      
      
  if sys.platform == 'win32':
    cmd = [cmd[0]] + ['-G', 'Visual Studio 12' + ' Win64' if is_64bits else ''] + cmd[1:]
  
  cmd+= [cmake_path]
  
  
  log.info('#' * 40)
  log.info('# CMake configuration')
  log.info('# - command is\n\t%s\n - running in path\n\t%s', ' '.join(cmd), os.path.abspath(build_location))
  config_proc = subprocess.Popen(cmd, cwd = build_location)
  config_proc.wait()



class build_cmake(Command):
    """Calls cmake to build Yayi"""
  
  
    description = "Build of Yayi using cmake"
    user_options = [
                    ('boostroot=', None, 'specifies the boost directory'),  # option with = because it takes an argument
                    ('additionaloptions=', None, 'additional cmake options'),
                    ]
  
    def initialize_options(self):
        self.boostroot = None
        self.additionaloptions = None
        self.build_temp = None
        self.build_lib = None
        self.build_platlib = None
        self.install_dir = None
  
    def finalize_options(self):
        self.set_undefined_options('build', ('build_temp', 'build_temp'), 
                                             ('build_lib', 'build_lib'),
                                             ('build_platlib', 'build_platlib')
                                             )
        self.set_undefined_options('install', ('install_lib', 'install_dir'))
        pass
    
    def run(self):
        global cmake_build_location
        global cmake_install_location
        cmake_build_location = os.path.abspath(os.path.join(os.path.dirname(__file__), self.build_temp))
        cmake_install_location = os.path.abspath(os.path.join(os.path.dirname(__file__), self.build_lib))
        cmake_install_prefix = os.path.abspath(self.install_dir)

        log.info('#' * 40)
        log.info('[YAYI] build_cmake\n'
                 '\tinside directory %s\n'\
                 '\tinstall to directory %s\n'\
                 '\tinstallPREFIX to directory %s', self.build_temp, self.build_lib, self.install_dir)
        
        # this layout should be there
        self.run_command('create_package_layout')
    
        options = []
        if not self.boostroot is None:
            options += ['-DBOOST_ROOT=' + os.path.abspath(os.path.expanduser(self.boostroot))]
        
        if not self.additionaloptions is None:
            options += [self.additionaloptions]
    
        cmake_configure(options)
    
        # now the version should be available
        if self.distribution.metadata.version is None:
            self.distribution.metadata.version = _get_version()
    

        # todo
        # check that the python library is compatible with the version of boost we have
        # which might be not the case for virtualenv like with exotic python +/- 
        # boost. In any case, boost-python and python should be coherent. 
        
        try:
            from multiprocessing import cpu_count
            cpu_count_ = cpu_count()
        except Exception, e:
            cpu_count_ = 1
          
        cmake_cmd = ['cmake', '--build', '.']
    
        # release on win32
        if sys.platform == "win32":
            cmake_cmd += ['--config', 'Release']
        
        # additional options: cpu for multithreaded builds
        if sys.platform == "win32":
            cmake_cmd += ['--', '/m:%d' % cpu_count_, '/v:m']
        else:
            cmake_cmd += ['--', '-j%d' % cpu_count_]
    
        # todo flush the cmake output into a file
        build_proc = subprocess.Popen(cmake_cmd, cwd=cmake_build_location)
        build_proc.wait()
        
        # build_proc = subprocess.Popen(['cmake', '--build', '.', '--', 'Doxygen'], cwd = cmake_build_location)
        # build_proc.wait()
        
        # build_proc = subprocess.Popen(['cmake', '--build', '.', '--', 'Sphinx'], cwd = cmake_build_location)
        # build_proc.wait()
    
    
        if(build_proc.returncode != 0):
            print '# build_cmake returned an error code', build_proc.returncode
            print '# stopping the commands'
            raise Exception('Error produced by build_cmake')

        log.info('#' * 40)
        log.info('[YAYI] build_cmake ok')
        
        
        # the installation procedure is copying yayi files into the python package tree, so it should be part of the
        # build itself
        log.info('#' * 40)
        log.info('[YAYI] build_cmake -- install the python package component')
        
        
        cmake_cmd = ['cmake', '--build', '.', '--target', 'PythonPackageSetup']
        if sys.platform == "win32":
            cmake_cmd += ['--config', 'Release'] # important otherwise the other version might get installed
            cmake_cmd += ['--', '/v:m']
    
        build_proc = subprocess.Popen(cmake_cmd, cwd=cmake_build_location)
        build_proc.wait()
        
        # consider, for installing one component only:
        # ${CMAKE_COMMAND} -DCOMPONENT=python_package_install_intermediate -P ${CMAKE_BINARY_DIR}/cmake_install.cmake
        
      
        if(build_proc.returncode != 0):
            log.error('[YAYI] build_cmake install returned an error code %d', build_proc.returncode)
            log.error('[YAYI] stopping the commands')
            raise Exception('Error produced by cmake "install" command, see logs for more information')    
    
        log.info('#' * 40)
        log.info('[YAYI] build_cmake -- install ok')

        pass # class build_cmake

    def get_outputs(self):
        """Returns the list of files generated by this specific build command"""
        global cmake_install_location
        # Apparently needed while undocumented. Note: should be able to run it in dry-run, which is now impossible
        log.warn('#' * 40 + " I am in get_outputs, build directory is " + self.build_temp)
        
        # here we retrieve the information from cmake itself.
        # todo: abstract the file that is read: this is the component that is installed, the python script
        # here should not know about that
        list_installed_files = []
        with open(os.path.join(self.build_temp, 'install_manifest_python_package_install_intermediate.txt'), 'r') as f:
            for l in f.readlines():
                list_installed_files.append(os.path.relpath(l.strip(), self.build_lib))
        #out_files = _utils_get_all_files(cmake_install_location)
        log.warn("returning %s", '\n\t'.join(list_installed_files))
        return list_installed_files

    # not needed as 'create_package_layout' is called from the run
    # sub_commands = Command.sub_commands #[('create_package_layout', None)] + 





#############################################
#
# Overrides of the regular distutils commands
# Needed in order to perform the commands in the right order and to capture
# some variables needed during the builds.

class ExtensionCMake(_Extension):
  
    def __init__(self, *args, **kwargs):
        _Extension.__init__(self, *args, **kwargs)




class build_ext(_build_ext):
    sub_commands = [('build_cmake', None)] + _build_ext.sub_commands
  
    def build_extension(self, ext):
        if(not isinstance(ext, ExtensionCMake)):
            return _Extension.build_extension(self, ext)
    
        # the 1 at the end construct the object always, even if not specified on 
        # the command line.
        build_cmake = self.get_finalized_command('build_cmake', 1)
        
        # for each of the cmake extensions, configure this one a bit
        # - name of the target
        # - build location
        # - install location, maybe run the tests
        
        # right now, doing this only stuff
        build_cmake.run()
        
        # now maybe extend the self.libraries
        
        pass

    def get_outputs(self):
    
        pruned_extension = [i for i in self.extensions if not isinstance(i, ExtensionCMake)]
        original = self.extensions
        self.extensions = pruned_extension
        
        r = _build_ext.get_outputs(self)
        
        self.extensions = original
        
        build_cmd = self.get_finalized_command('build_cmake')
        build_files = build_cmd.get_outputs()
        build_dir = getattr(build_cmd, 'build_platlib')
        
        return r + build_files





class sdist(_sdist):
    """Modified source distribution that installs create_package_layout as a dependent subcommand"""
    sub_commands = [('create_package_layout', None)] + _sdist.sub_commands
  
    def get_file_list(self):
        """Extends the file list read from the manifest with the sources of Yayi"""
    
        _sdist.get_file_list(self)
        src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), yayi_src_files_location))
        my_files = _utils_get_all_files(src_dir)
        my_files = [os.path.join(src_dir, x) for x in my_files]
        my_files = [os.path.relpath(x, os.path.abspath(os.path.dirname(__file__))) for x in my_files]
        self.filelist.extend(my_files)
        
        self.filelist.exclude_pattern('*.so', anchor = False)
        self.filelist.exclude_pattern('*.dylib', anchor = False)
        self.filelist.exclude_pattern('*.dll', anchor = False)
        self.filelist.exclude_pattern('*.lib', anchor = False)
    
        # anything platform specific that might be an extension        
        import imp
        for i in (_[0] for _ in imp.get_suffixes() if _[2] == imp.C_EXTENSION):
            self.filelist.exclude_pattern('*%s' % i, anchor = False)
    
        return




classifiers = [
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Developers',
  'Intended Audience :: Information Technology',
  'Intended Audience :: Science/Research',
  'Operating System :: MacOS :: MacOS X',
  'Operating System :: Microsoft :: Windows :: Windows NT/2000',
  'Operating System :: POSIX :: Linux',
  'Programming Language :: C++',
  'Programming Language :: Python :: 2.7',
  'Topic :: Scientific/Engineering :: Image Recognition',
  'Topic :: Scientific/Engineering :: Mathematics',
]

keywords = 'image processing', 'mathematical morphology', \
           'multidimensional images', 'multispectral images', \
           'image segmentation', 'erosion', 'dilation', \
           'opening', 'closing', 'hit-or-miss', 'connected components' 

cmdclass= { 'create_package_layout': create_package_layout,
            
            'build_ext': build_ext,
            'build_cmake': build_cmake,
            'sdist': sdist,
           }

setup(
  name          = 'yayi',
  version       = _get_version(),
  
  author = 'Raffi Enficiaud',
  author_email = 'raffi.enficiaud@free.fr',
  
  # cmake extension, mainly to declare this package as non-pure and to
  # intercept the cmake related options
  # if the name is a subpackage (yayi.sthg), it is not listed in the top_level.txt file
  ext_modules = [ExtensionCMake('yayi.bin', [])],
  
  url = 'http://raffi.enficiaud.free.fr',
  packages = ['yayi', 'yayi.extensions', 'yayi.tests'],
  package_data = { 'yayi': ['bin/*.*'] },
  classifiers = classifiers,
  keywords = keywords,
  license ='Boost Software License - Version 1.0 - August 17th, 2003',
  description = 'Yayi toolbox for image processing and mathematical morphology',
  long_description=open('README.txt').read(),
  cmdclass = cmdclass,
  #zip_safe = False, extensions already there
)

