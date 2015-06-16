"""
Portfolio

Command line tool

bluebook -c project_name

"""

import os
import argparse
import pkg_resources
import portfolio

PACKAGE = portfolio
CWD = os.getcwd()
SKELETON_DIR = "app_templates"
APPLICATION_DIR = "%s/application" % CWD
APPLICATION_DATA_DIR = "%s/data" % APPLICATION_DIR
APPLICATION_UPLOAD_DIR = "%s/uploads" % APPLICATION_DATA_DIR

def get_project_dir_path(project_name):
    return "%s/%s" % (APPLICATION_DIR, project_name)

def copy_resource(src, dest):
    """
    To copy package data to destination
    """
    dest = (dest + "/" + os.path.basename(src)).rstrip("/")
    if pkg_resources.resource_isdir(PACKAGE.__name__, src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        for res in pkg_resources.resource_listdir(__name__, src):
            copy_resource(src + "/" + res, dest)
    else:
        if os.path.splitext(src)[1] not in [".pyc"]:
            with open(dest, "wb") as f:
                f.write(pkg_resources.resource_string(__name__, src))


def create_project(project_name, template="default"):
    """
    Create the project
    """

    project_dir = get_project_dir_path(project_name)

    run_tpl = pkg_resources.resource_string(__name__, '%s/run.py' % (SKELETON_DIR))
    init_py_tpl = pkg_resources.resource_string(__name__, '%s/init.py' % (SKELETON_DIR))
    propel_tpl = pkg_resources.resource_string(__name__, '%s/propel.yml' % (SKELETON_DIR))
    config_tpl = pkg_resources.resource_string(__name__, '%s/config.py' % (SKELETON_DIR))
    model_tpl = pkg_resources.resource_string(__name__, '%s/model.py' % (SKELETON_DIR))
    manage_tpl = pkg_resources.resource_string(__name__, '%s/manage.py' % (SKELETON_DIR))

    run_file = "%s/run_%s.py" % (CWD, project_name)
    requirements_txt = "%s/requirements.txt" % CWD
    propel_yml = "%s/propel.yml" % CWD
    config_py = "%s/config.py" % APPLICATION_DIR
    model_py = "%s/model.py" % APPLICATION_DIR
    manage_py = "%s/manage.py" % CWD

    dirs = [
        APPLICATION_DIR,
        APPLICATION_DATA_DIR,
        APPLICATION_UPLOAD_DIR,
        project_dir
    ]
    for dir in dirs:
        if not os.path.isdir(dir):
            os.makedirs(dir)

    files = [
        ("%s/__init__.py" % APPLICATION_DIR, init_py_tpl),
        ("%s/__init__.py" % CWD, "# Portfolio"),
        (config_py, config_tpl),
        (model_py, model_tpl),
        (run_file, run_tpl.format(project_name=project_name)),
        (requirements_txt, "%s==%s" % (PACKAGE.NAME, PACKAGE.__version__)),
        (propel_yml, propel_tpl),
        (manage_py, manage_tpl)
    ]
    for file in files:
        if not os.path.isfile(file[0]):
            with open(file[0], "wb") as f:
                f.write(file[1])

    copy_resource("%s/%s/" % (SKELETON_DIR, template), project_dir)


def main():

    _description = "%s %s" % (PACKAGE.NAME, PACKAGE.__version__)
    parser = argparse.ArgumentParser(description=_description)
    parser.add_argument("-c", "--create", help="To create a new project."
                             " [ie: portfolio -c www]")

    arg = parser.parse_args()
    print(_description)
    if arg.create:
        project_name = arg.create
        template = "default"
        create_project(project_name, template)
        print("Created project: %s'" % project_name)
        print("To launch server run 'run_%s.py'" % project_name)

