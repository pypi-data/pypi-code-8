import os
import webbrowser

from fabric.api import env
from fabric.api import lcd
from fabric.api import task
from fabric.api import hide
from fabric.api import local

from . import log
from . import utils


@task
def build():
    """build project documentation"""
    log.info("Building documentation for {package_name} version {version}".format(**env.nexiles))
    with lcd("docs"), hide("running", "stdout"):
        local("make html")


@task
@utils.Requires(build_dir=str, root_dir=str)
def package():
    """package project documentation"""
    log.info("Packaging documentation for {package_name} version {version}".format(**env.nexiles))
    with lcd("docs/_build/html"), hide("running"):
        local("tar czf {doc_package} .".format(**env.nexiles))


@task
@utils.Requires(dist_dir=str)
def dist():
    """distribute project documentation"""
    log.info("Distributing documentation for {package_name} version {version}".format(**env.nexiles))
    with hide("running"):
        log.info("   {}".format(os.path.basename(env.nexiles.doc_package)))
        local("cp {doc_package} {dist_dir}".format(**env.nexiles))


@task
@utils.Requires(root_dir=str)
def preview():
    """preview project documentation"""
    webbrowser.open("file://{root_dir}/docs/_build/html/index.html".format(**env.nexiles))


@task
@utils.Requires(doc_public_dir=str)
def publish():
    """publish project documentation"""

    if not os.path.exists(os.path.dirname(env.nexiles.doc_public_dir)):
        log.error("Public dir not accessible.")
        return

    local("mkdir -p {}".format(env.nexiles.doc_public_dir))
    with lcd("docs/_build/html"):
        local("rsync -rv * {doc_public_dir}".format(**env.nexiles))

# EOF
