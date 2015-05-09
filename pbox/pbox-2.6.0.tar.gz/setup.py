#!/usr/bin/env python
# --------------------------------------------------------------------------------------------------------------
from setuptools import setup
import os, sys, shutil
import pbox as module

# --------------------------------------------------------------------------------------------------------------
# Cleaning up build directory:
# --------------------------------------------------------------------------------------------------------------

def clean_up():
    
    if os.path.exists('dist'):
        shutil.rmtree('dist')
        
    if os.path.exists('{}.egg-info'.format(module.__name__)):
        shutil.rmtree('{}.egg-info'.format(module.__name__))
    
    if os.path.exists('README.md'):
        os.remove('README.md')
        
    if os.path.exists('README.txt'):
        os.remove('README.txt')
        
    if os.path.exists('MANIFEST.in'):
        os.remove('MANIFEST.in')
        
    if os.path.exists('setup.cfg'):
        os.remove('setup.cfg')
    
    if os.path.exists('LICENSE.txt'):
        os.remove('LICENSE.txt')


if len(sys.argv) > 1 and sys.argv[1] == 'cleanup':
    
    sys.stdout.write('\nCleaning up build folder for module \'{}\'...\n\n'.format(module.__name__))
    sys.stdout.write('Folder contents before cleaning:\n{}\n'.format('-' * 60))
    sys.stdout.write('{}\n\n'.format(os.system('ls -l')))
    
    clean_up()
    
    sys.stdout.write('Folder contents after cleaning:\n{}\n'.format('-' * 60))
    sys.stdout.write('{}\n\n'.format(os.system('ls -l')))
    sys.stdout.write('{0}\nDone!\n{0}\n\n'.format('-' * 60))
    exit()

# --------------------------------------------------------------------------------------------------------------
# Creating README.md, README.txt, MANIFEST.in, setup.cfg and LICENSE.txt files:
# --------------------------------------------------------------------------------------------------------------

if not os.path.exists('README.md'):
    with open('README.md', 'w') as outfile:
        outfile.write(module._readme)

if not os.path.exists('README.txt'):
    with open('README.txt', 'w') as outfile:
        outfile.write(module.__doc__)
       
if not os.path.exists('MANIFEST.in'):        
    with open('MANIFEST.in', 'w') as outfile:
        outfile.write(module._manifest)

if not os.path.exists('setup.cfg'):        
    with open('setup.cfg', 'w') as outfile:
        outfile.write(module._setup_cfg)
        
if not os.path.exists('LICENSE.txt'):
    os.system('curl -L http://www.gnu.org/licenses/lgpl.txt >> LICENSE.txt')
          
# --------------------------------------------------------------------------------------------------------------
# Creating Module Setup:
# --------------------------------------------------------------------------------------------------------------

setup(
    # Module Name:
    name = module.__name__,
    
    # Module Version:
    version = module.__version__,
    
    # Module Repository:
    url = module.__url__,
    download_url = module._download_url,
    
    # Module Author Info:
    author = module.__author__,
    author_email = module.__email__,
     
    # Module packages to include:
    packages = module._packages,
    
    # Module info:
    description = module._info,
    long_description = module._more_info,
    keywords = module._keywords,
    classifiers = module._classifiers,
    include_package_data = True,
    
    # License Agreement:
    license = module.__license__,
    
    # Install Requirements:
    install_requires = module._requires,
    
    # Compatible Platforms:
    platforms = module._platforms,
    )

# --------------------------------------------------------------------------------------------------------------
#  END
# --------------------------------------------------------------------------------------------------------------
