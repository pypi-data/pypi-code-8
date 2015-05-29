from glob import glob
from setuptools import setup, find_packages
setup(name = 'worch-g4lbne',
      version = '0.0.2',
      description = 'Worch/waf tools and features for building G4LBNE.',
      author = 'Brett Viren',
      author_email = 'brett.viren@gmail.com',
      license = 'GPLv2',
      url = 'http://github.com/brettviren/worch-g4lbne',
      namespace_packages = ['worch'],
      packages = ['worch','worch.g4lbne'],
      install_requires = [l for l in open("requirements.txt").readlines() if l.strip()],
#      data_files = [('share/worch/config/examples', glob('examples/*.cfg')),],
      data_files = [
          ('share/worch/config/g4lbne', glob('config/*.cfg')),
          ('share/worch/patches/g4lbne', glob('patches/*.patch')),
          ('share/worch/wscripts/g4lbne', ['wscript']),
      ],
)
