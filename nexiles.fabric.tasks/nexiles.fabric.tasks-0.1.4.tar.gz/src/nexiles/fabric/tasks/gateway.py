import os
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


from . import log
from . import utils
from . import windchill


##############################################################################
# PRIVATE
##############################################################################


def get_package_env(which=None):
    """Return env for specific package"""
    if which is None:
        e = env.nexiles
    else:
        e = env.nexiles[which]

    return e


def generate_manifest(name, p, h=None):
    """ generate_manifest(name, p, h) -> mapping

    Generates a mapping used as the manifest file.

    :param name:      a dotted package name, as in setup.py
    :param p:         the zip file with package content.
    :param h:         optional hash function to use.
    :returns:         the path to the created manifest file.
    """
    if h is None:
        h = hashlib.sha256
    m = {}
    fh = m["files"] = {}
    order = []
    with zipfile.ZipFile(p) as zf:
        for fi in zf.filelist:
            order.append(fi.filename)

        hash_all = h()
        for fn in sorted(order):
            contents = zf.read(fn)
            hash_all.update(contents)
            fh[fn] = h(contents).hexdigest()

    m["name"] = name
    m["sum"]  = hash_all.hexdigest()
    m["date"] = datetime.datetime.now().isoformat()
    return m


def add_manifest(package, manifest, egg):
    manifest_resource = os.path.join(*package.import_name.split("."))
    manifest_resource = os.path.join(manifest_resource, "resources", "manifest.json")
    with zipfile.ZipFile(egg, "a") as zf:
        zf.writestr(manifest_resource, json.dumps(manifest))


def get_package_name(package, customer=None, python="2.7"):
    """ returns the egg filename (without the fs path),
        e.g. nexiles.gateway.appservice-1.0.0-py2.7-customer.egg
    """
    if customer:
        return "{}-{}-py{}-{}.egg".format(
            package.import_name,
            package.version,
            python,
            customer
        )
    return "{}-{}-py{}.egg".format(
        package.import_name,
        package.version,
        python
    )


def get_package_eggs(package):
    out = []
    for customer in package.customers:
        out.append(os.path.join(env.nexiles.build_dir, get_package_name(package, customer=customer)))
    return out


@contextlib.contextmanager
def licensed_package(package, customer):
    """"""

    with file(package.license_module, "w") as f:
        f.write("""# -*- coding: utf-8 -*-
LICENSE = {
   "customer_id": "%s",
   "key":         "%s"
}
""" % (customer, package.urn))
        log.info("   Generated license module for {}".format(customer))

    yield

    log.info("   Removed license module for {}".format(customer))

    with hide("running"):
        local("git checkout {}".format(package.license_module))

    egg_name          = os.path.join(env.nexiles.build_dir, get_package_name(package))
    egg_name_customer = os.path.join(env.nexiles.build_dir, get_package_name(package, customer=customer))

    with hide("running"):
        local("mv {} {}".format(egg_name, egg_name_customer))

    log.info("   Adding package manifest to {} for {}.".format(egg_name_customer, customer))
    manifest = generate_manifest(package.package_name, egg_name_customer)
    add_manifest(package, manifest, egg_name_customer)

    package.setdefault("built_eggs", []).append(egg_name_customer)


def get_gw_module_dist_root_dir(package):
    ""
    return os.path.join(env.nexiles.dist_root, "nexiles.gateway.services", package.import_name.split(".")[-1])

##############################################################################
# Tasks
##############################################################################


@task
@utils.Requires(build_dir=str)
def list_eggs(which=None):
    """List gateway module eggs to be built."""
    package = get_package_env(which)
    eggs = get_package_eggs(package)
    for egg in eggs:
        log.info(egg)


@task
@utils.Requires(build_dir=str, dist_root=str)
def dist_eggs(which=None):
    """Copy built eggs to dist dir."""
    package = get_package_env(which)
    eggs = get_package_eggs(package)

    root = get_gw_module_dist_root_dir(package)
    dist = os.path.join(root, "{package_name}-{version}".format(**package))
    package["dist_dir"] = dist
    with hide("running"):
        local("mkdir -p {}".format(dist))

    log.info("Distributing {} version {}".format(which, package.version))
    for egg in eggs:
        log.info("   {}".format(os.path.basename(egg)))
        with hide("running"):
            local("cp {} {}".format(egg, dist))


@task
@utils.Requires(build_dir=str, WT_HOME=str, WT_HOST=str, WTUSER=str, WTPASS=str, JYTHON_HOME=str)
def build_eggs(which=None):
    """Build gateway module."""
    package = get_package_env(which)
    if which is None:
        which = env.nexiles.package_name

    log.info("Building {} version {}".format(which, package.version))

    windchill.setup_classpath()

    for customer in package.customers:
        with licensed_package(package, customer):
            with lcd(package.package_dir), hide("running", "stdout"):
                log.info("   Building {} for {}".format(package.package_name, customer))
                local("jython setup.py bdist_egg --exclude-source-files -d {}".format(env.nexiles.build_dir))

    log.info("Built eggs:")
    for p in package.built_eggs:
        log.info("   {}".format(p))

# EOF
