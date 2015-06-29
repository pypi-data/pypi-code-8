"""
Purpose: provide functions with the same parametrizations as found in CRAN,
but implemented by parametrizing Pandas, StatsModels, SciKit Learn, Matplotlib,
and other Python's stable libraries.
"""

from cran import settings
import pandas as pd
import os, git, sys, imp

if settings.CRAN_LOCAL not in os.sys.path:
    os.sys.path.append(settings.CRAN_LOCAL)

if not os.path.isdir(settings.CRAN_LOCAL):
    os.system('mkdir '+settings.CRAN_LOCAL)

if not os.path.isdir(os.path.join(settings.CRAN_LOCAL,'library')):
    os.system('mkdir '+os.path.join(settings.CRAN_LOCAL,'library'))

if not os.path.isfile(os.path.join(settings.CRAN_LOCAL,'library/__init__.py')):
    os.system('touch '+os.path.join(settings.CRAN_LOCAL,'library/__init__.py'))

def install_packages(package,
                     repos=settings.CRAN_REPOS,
                     lib=settings.CRAN_LOCAL):

    if isinstance(package, basestring):
        remote = os.path.join(repos, package)
        local = os.path.join(os.path.join(lib, 'library'), package)
        if os.path.exists(local):
            git.cmd.Git(local).pull()
            return git.Repo(local)
        else:
            return git.Repo.clone_from(remote, local)
    else:
        pass

def library(package,
            lib_loc=settings.CRAN_LOCAL):
    if isinstance(package, basestring):
        module = imp.load_source(package, os.path.join(lib_loc, '/library/'))
        setattr(sys.modules[__name__], package, module)

def max(it):
    if isinstance(it, pd.DataFrame):
        return it.values.max()
    else:
        pass


