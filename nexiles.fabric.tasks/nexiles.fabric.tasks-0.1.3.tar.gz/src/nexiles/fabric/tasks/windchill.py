import os
import glob
import json
import zipfile
import hashlib
import datetime
import contextlib

from fabric.api import env
from fabric.api import lcd
from fabric.api import task
from fabric.api import hide
from fabric.api import local
from fabric.api import execute
from fabric.api import settings

from nexiles.tools.api import get_api

from . import log
from . import utils
from . import environment

__all__ = ["setup_classpath"]

# We rely on these environment vars
env.nexiles.update(
    WT_HOST     = os.environ.get("WT_HOST"),
    WT_HOME     = os.environ.get("WT_HOME"),
    WTUSER      = os.environ.get("WTUSER"),
    WTPASS      = os.environ.get("WTPASS"),
    JYTHON_HOME = os.environ.get("JYTHON_HOME"),
)


if env.nexiles.WT_HOME:
    if not os.path.exists(env.nexiles.WT_HOME):
        log.warning("The path for WT_HOME is not accessible: {}", env.nexiles.WT_HOME)

    env.nexiles.update(
        WT_CODEBASE = os.path.join(env.nexiles.WT_HOME, "codebase"),
        WT_SRCLIB   = os.path.join(env.nexiles.WT_HOME, "src", "lib"),
        WT_WEB_INF  = os.path.join(env.nexiles.WT_HOME, "codebase", "WEB-INF")
    )


def api():
    """api() -> nexiles tools api object

    Get the nexiles tools api object."""
    return get_api(env.nexiles.WT_HOST, env.nexiles.WTUSER, env.nexiles.WTPASS)

##############################################################################
# Public Helpers
##############################################################################


def setup_classpath():
    """setup_classpath() -> None

    Sets up CLASSPATH to contain needed JAR files for compiling Windchill
    projects.
    """

    # collect all jars
    codebase_jars = glob.glob(os.path.join(env.nexiles.WT_CODEBASE, "*.jar"))
    webinf_jars = glob.glob(os.path.join(env.nexiles.WT_WEB_INF, "lib", "*.jar"))
    srclib_jars = glob.glob(os.path.join(env.nexiles.WT_SRCLIB, "*.jar"))

    # set the classpath
    all_jars = [env.nexiles.WT_CODEBASE, env.nexiles.WT_SRCLIB] + codebase_jars + webinf_jars + srclib_jars
    classpath = os.environ["CLASSPATH"] = ":".join(all_jars)
    return classpath



##############################################################################
# Tasks
##############################################################################

@task
@utils.Requires(WT_HOME=str, WT_HOST=str, WTUSER=str, WTPASS=str)
def dump_env():
    """Print windchill specific environment."""
    execute(environment.dump)


@task
@utils.Requires(WT_HOME=str)
def classpath():
    """Print CLASSPATH used to build."""
    cp = setup_classpath()
    log.info("CLASSPATH={}".format(cp))


# EOF
