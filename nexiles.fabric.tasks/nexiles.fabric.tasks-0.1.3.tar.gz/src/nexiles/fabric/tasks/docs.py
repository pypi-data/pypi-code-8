import os
import webbrowser

from fabric.api import env
from fabric.api import lcd
from fabric.api import task
from fabric.api import local

from . import log
from . import utils


@task
def build():
    """build project documentation"""
    with lcd("docs"):
        local("make html")


@task
@utils.Requires(doc_package=str)
def package():
    """package project documentation"""
    with lcd("docs/_build/html"):
        local("tar czf {doc_package} .".format(**env.nexiles))


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
