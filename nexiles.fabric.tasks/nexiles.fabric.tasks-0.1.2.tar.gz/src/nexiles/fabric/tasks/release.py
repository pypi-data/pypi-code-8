import os

from fabric.api import env
from fabric.api import task
from fabric.api import local

from . import log
from . import utils

@task
@utils.Requires(version=str, package_name=str, doc_package=str)
def github():
    """Release on github"""
    local("github-release release -u nexiles -r {0} --tag v{1} --name '{0} -- v{1}'".format(env.nexiles.package_name, env.nexiles.version))
    local("github-release upload -u nexiles -r {0} --tag v{1} --name documentation --file {2}".format(env.nexiles.package_name, env.nexiles.version, env.nexiles.doc_package))

@task
@utils.Requires(public_source=bool)
def pypi():
    """Release on the python package index (PUBLIC SOURCE RELEASE)"""
    if not env.nexiles.public_source:
        log.error("This package is not allowed on pypi.   Talk to SE if you think that's wrong.")
        return

    local("python setup.py clean register sdist upload")