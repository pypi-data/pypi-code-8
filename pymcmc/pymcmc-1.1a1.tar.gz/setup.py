#!/usr/bin/env python

## If you use the parallel option we found Ubuntu it is best to set the
## number of threads to the number of available cores. Performance can
## be really poor otherwise. This has not effected us when using other
## distros, so we are currently unsure why this occurs.
## For example on a 4 core machine for example is to set
## export OMP_NUM_THREADS=4
## You could of course use less cores.
## to add parallel stuff, simplest is to modify f2py flags in
## config_fc, using
## python setup.py config_fc --f77flags='-fopenmp ' --f90flags='-fopenmp ' install --home=/export/home/denhamrj/
## but see as well
## https://github.com/numpy/numpy/blob/master/doc/DISTUTILS.rst.txt#getting-extra-fortran-77-compiler-options-from-source
## Note you will have to delete the build directory if you have already built
## pymcmc without parallel flags.

## Some of the fortran files require atlas
## Most builds will use the available shared libraries
## but some need the static libraries.

#######################################################
#                                                     #
# Building under linux                                #
#                                                     #
#######################################################
## eg ubuntu

## first, get a working atlas
## note that if you use ubuntu, you might find some missing
## symlinks (see
# https://bugs.launchpad.net/ubuntu/+source/atlas/+bug/769180

# this works for ubuntu using libatlas-base-dev
# also libatlas3gf-sse
#atlas_libs = ['lapack_atlas', 'f77blas', 'cblas']

#atlas_libs = ['satlas']
#extra_link_args = []
#extra_compile_args = []
#libs = []
#atlas_libs = ['atlas','lapack','f77blas','cblas']
#library_dirs = ['/usr/lib/']
#library_dirs = ['/usr/local/atlas/lib/']


## you might need this if you aren't
## using gfortran as a fortran compiler
#libs = ['gfortran']

#library_dirs=["/usr/lib/sse2/atlas","/usr/lib/sse2/"]
#library_dirs=['/usr/lib64/atlas/']

#######################################################
#                                                     #
# Building under windows                              #
#                                                     #
#######################################################

## This is not easy, but basically, make sure you have
## blas, lapack installed with if possible ATLAS.
## Use gfortan as your compiler, using the mingw windows
## installer.

## Since you want this to be able to run on machines
## without gfortran installed, you will need to use
## the following extra link args:

# extra_link_args = ["-static-libgfortran","-static-libgcc"]

# ## give the location of the lapack/blas/ATLAS library
# library_dirs=["d:\\tmp\\pymcmc_win_install\\BUILDS\\lib\\"]
# atlas_libs = ['lapack','cblas','f77blas','atlas']
# libs = []

#######################################################
#                                                     #
# Building with non-standard ATLAS location           #
#                                                     #
#######################################################
## if you've built your own atlas and isn't in a standard
## location,
## eg, at work, our atlas is in
## libs = []
## extra_link_args = []
## extra_compile_args = []
## library_dirs=["/opt/sw/fw/rsc/SLES-11/atlas/3.8.4//lib/"]
## library_dirs = []
## library_dirs = ["/usr/lib/openblas-base/"]
## atlas_libs = ['atlas','lapack','f77blas','cblas']

#openblas
#atlas_libs = ['lapack', 'blas', 'openblas']


#######################################################
#                                                     #
# Building using Static atlas libraries...            #
#                                                     #
#######################################################
library_dirs=[]
ATLASLIB="/apps/atlas/3.11.11//lib/"
extra_compile_args=[]
extra_link_args=[""" {0}/liblapack.a {0}/libcblas.a \
 {0}/libf77blas.a {0}/libatlas.a \
 -lgfortran """.format(ATLASLIB) ]
atlas_libs = []
libs = []
def configuration(parent_package='', top_path=None, package_path='Lib'):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('pymcmc', parent_package, top_path, package_path)
    config.add_subpackage('standard', 'Lib/standard/')
    config.add_extension('stochsearch',
                         ['Src/stochsearch.f'],
                         library_dirs=library_dirs,
                         libraries=atlas_libs,
                         extra_link_args=extra_link_args,
                         extra_compile_args=extra_compile_args
                         )
    config.add_extension('reg_helper',
                         ['Src/reg_helper.f'],
                         libraries=atlas_libs,
                         library_dirs=library_dirs,
                         extra_link_args=extra_link_args,
                         extra_compile_args=extra_compile_args,
                         )
    config.add_extension('timeseriesfunc',
                         ['Src/timeseriesfunc.f'],
                         libraries=libs,
                         extra_link_args=extra_link_args,
                         extra_compile_args=extra_compile_args
                         )
    config.add_extension('wishart',
                         ['Src/wishart.f'],
                         libraries=atlas_libs,
                         library_dirs=library_dirs,
                         extra_link_args=extra_link_args,
                         extra_compile_args=extra_compile_args
                         )
    config.add_extension('mcmc_helper',
                         ['Src/mcmc_helper.f'],
                         libraries=atlas_libs,
                         library_dirs=library_dirs,
                         extra_link_args=extra_link_args,
                         extra_compile_args=extra_compile_args
                         )
    config.add_extension('random_mtar',
                         ['Src/random_mtar.f'],
                         libraries=atlas_libs,
                         library_dirs=library_dirs,
                         extra_link_args=extra_link_args,
                         extra_compile_args=extra_compile_args
                         )
    config.add_extension('random_mtar_ref',
                         ['Src/random_mtar_ref.f'],
                         libraries=atlas_libs,
                         library_dirs=library_dirs,
                         extra_link_args=extra_link_args,
                         extra_compile_args=extra_compile_args
                         )
    config.add_extension('loglinear',
                         ['Src/loglinear.f', 'Src/mlgam.f'],
                         libraries=atlas_libs + ["gomp"],
                         library_dirs=library_dirs,
                         extra_link_args=extra_link_args,
                         extra_compile_args=extra_compile_args
                         )
    config.add_extension('logit',
                         ['Src/logit.f'],
                         libraries=atlas_libs + ["gomp"],
                         library_dirs=library_dirs,
                         extra_link_args=extra_link_args,
                         extra_compile_args=extra_compile_args
                         )
    config.add_extension('mixture_model',
                         ['Src/mixture_model.f'],
                         libraries=atlas_libs + ["gomp"],
                         library_dirs=library_dirs,
                         extra_link_args=extra_link_args,
                         extra_compile_args=extra_compile_args
                         )
    config.add_extension('mix_logit_helper',
                         ['Src/mix_logit_helper.f90'],
                         libraries=atlas_libs + ["gomp"],
                         library_dirs=library_dirs,
                         extra_link_args=extra_link_args,
                         extra_compile_args=extra_compile_args
                         )
    config.add_data_files('examples/ex_loglinear.py',
                          'examples/ex_AR1.py',
                          'examples/ex_variable_selection.py',
                          'examples/loglinear.f',
                          'data/count.txt',
                          'data/yld2.txt',
                          'data/weeddata.txt',
                          'data/MVweeddata.txt',
                          'data/Nile.dat',
                          'data/OldFaithful.txt', 
                          'Lib/standard/GL-mixture_weights.txt',
                          'Lib/standard/GL-mixture_ssq.txt',
                          'Lib/standard/setup.py')
    return config

if __name__ == "__main__":
    from numpy.distutils.core import setup
    setup(
          version='1.1a1',
          description="""A python package for Bayesian estimation \
using Markov chain Monte Carlo""",
          author="Christopher Strickland",
          author_email='christopher.strickland@qut.edu.au',
          maintainer="Robert Denham",
          maintainer_email="rjadenham@gmail.com",
          license="GNU GPLv3",
          url="https://bitbucket.org/christophermarkstrickland/pymcmc",
          configuration=configuration)
