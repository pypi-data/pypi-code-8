#!/usr/bin/env python
import os

extra_link_args = []
## For a windows build you should use the following
## extra_link_args = ["-static-libgfortran","-static-libgcc"]


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def configuration(parent_package='', top_path=None, package_path='Lib'):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('pyssm', parent_package, top_path, package_path)
    ## to get the required libraries, we use the atlas configuration
    ## information
    atlas_config_data = config.get_info('atlas')

    config.add_extension('filter',
                         ['Src/filter.f'],
             library_dirs=atlas_config_data['library_dirs'],
             libraries=atlas_config_data['libraries'],
			 extra_link_args=extra_link_args
                         )
    config.add_extension('filterreg',
                         ['Src/filterreg.f'],
             library_dirs=atlas_config_data['library_dirs'],
             libraries=atlas_config_data['libraries'],
             extra_link_args=extra_link_args
                         )
    config.add_extension('unifilter',
                         ['Src/univariate.f'],
             library_dirs=atlas_config_data['library_dirs'],
             libraries=atlas_config_data['libraries'],
             extra_link_args=extra_link_args
                         )
    config.add_data_files(
        'examples/example_spline.py',
        'examples/example_ssm_ar1_reg.py',
        'examples/example_ssm_trendcycle2.py',
        'data/farmb.txt',
        'data/motorcycle.txt',
        'doc/pyssm.pdf')
    return config

if __name__ == "__main__":
    from numpy.distutils.core import setup
    setup(configuration=configuration,
          version='1.1a2',
          url='https://bitbucket.org/christophermarkstrickland/pyssm',
          description = "A Python package for analysis of time series using linear Gaussian state space models.",
          long_description=read("README.rst"),
          author = "Christopher Strickland",
          author_email = 'christopher.strickland@qut.edu.au',
          license = "GNU GPLv3",
          maintainer = "Robert Denham",
          maintainer_email = "rjadenham@gmail.com",
          bugtrack_url='https://bitbucket.org/christophermarkstrickland/pyssm/issues'
        )





