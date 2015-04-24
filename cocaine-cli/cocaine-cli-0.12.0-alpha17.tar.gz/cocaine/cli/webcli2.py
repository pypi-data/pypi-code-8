import json
import collections
import click
import getpass
from os.path import expanduser, join, isfile
import os
import re
import sys

from pprint import pprint

import collections

import requests

from config_reader import ProjectReader, VersionReader

from cocaine.cli.util import make_archive

try:
    from io import BytesIO  # py3
except ImportError:
    from cStringIO import StringIO as BytesIO  # py2

import logging
log = logging.getLogger()
log.setLevel(logging.INFO)

AUTH_FILE = join(expanduser("~"), ".cocaine-pipelinerc")
PROJECT_FILE = './project.json'

NO_AUTH_COMMANDS = ("login", "init")
NO_CONFIG_COMMANDS = ("login", "init", "reschedule", "task", "status", "clusters_info", "clusters_create")

BASE = None
TOKEN = None
USER = None
DEBUG = False

CONFIG = collections.OrderedDict()

API_VERSION = (0, 0, 7)

headers = {'content-type': 'application/json'}


class MyGroup(click.Group):

    def __init__(self, commands=None, **kwargs):
        super(MyGroup, self).__init__(commands=commands, **kwargs)

        self.commands = commands or collections.OrderedDict()
    
    def list_commands(self, ctx):
        return list(self.commands)

b = ""
def blank():
    global b
    b += " "
    return b

def _command_need_auth(cmd):
    return not cmd in NO_AUTH_COMMANDS

def _command_need_config(cmd):
    return not cmd in NO_CONFIG_COMMANDS

def _load_auth(ctx):
    global BASE
    global TOKEN
    global DEBUG
    if not isfile(AUTH_FILE):
        return False
    try:
        rc_file = file(AUTH_FILE)
        data = json.load(rc_file)
        rc_file.close()
        if (re.search(r'^https?://[^:/]+(?::\d+)$', data["base"])):
            BASE = data["base"]
        else:
            click.echo('Base url broken. Please, use cocaine login with correct arguments (url ex. http://some.host:1234)')
            ctx.abort()
        TOKEN = data["token"]

        if "debug" in data:
            DEBUG = data["debug"]
            
        return True
    except (ValueError, KeyError):
        click.echo('Please, use `coke login` first!')
        ctx.abort()

def _check_api_version(ctx):
    r = requests.get(BASE+"/version/", params={"debug": DEBUG})
    if (r.status_code >= 400):
        ctx.abort("Can't check API version")
    parsed_api_version = r.text.split(".")
    for level in xrange(3): # TODO use xrange(2) after 0.1 version
        if (int(parsed_api_version[level]) < API_VERSION[level]):
            ctx.abort("Client API version doesn't match that of the server. Please, update your client using `pip install cocaine-cli`.")

def _fill_config(name, version, profile, main, user):
    #title
    CONFIG["name"] = name
    #version
    CONFIG["version"] = version
    #members
    CONFIG["members"] = CONFIG.get("members", {})
    u_name_default = USER or getpass.getuser()
    if not user:
        while click.confirm("Add user to config?", default=False):
            u_name = click.prompt("User name", default=u_name_default)
            u_roles = click.prompt("User roles", default="admin, developer")
            CONFIG["members"][u_name] = u_roles.replace(" ", "").split(",")
        if not len(CONFIG["members"]):
            CONFIG["members"][u_name_default] = ("admin", "developer")
    else:
        for u_rule in user:
            CONFIG["members"][u_rule[0]] = u_rule[1].replace(" ", "").split(",")

    #clusters
    #TODO get /clusters from API
    CONFIG["clusters"] = {
        "testing": _gen_cluster_cnf("testing", main, profile),
        "production": _gen_cluster_cnf("production", main, profile)
    }


def _gen_cluster_cnf(name, slave, profile):
    return {
        "profile": profile,
        "manifest": {
            "slave": slave,
            "environment": {
                "YANDEX_ENVIRONMENT": name
            }
        }
    }

def handle_streaming_response(r):
    print "response", r
    print "headers", r.headers
    status = 0
    for ch in r.iter_lines(chunk_size=1):
        logging.debug("got chunk %s"%ch)
        try:
            r = json.loads(ch)
            if "error" in r and r["error"]:
                status = 2
                print r["message"]

                if DEBUG:
                    print r["traceback"]
            else:
                if "b64" in r and r["b64"]:
                    m = r["message"].decode("base64")
                else:
                    m = r["message"]
                print m
        except Exception:
            print ch
    if status != 0:
        sys.exit(status)


@click.group(cls=MyGroup)
@click.pass_context
@click.option('sets', '--set', nargs=2, multiple=True, required=False,
              metavar="<k.e.y> <val>",
              help="override or provide corresponding fields of ./project.json")
@click.option('--no-config', "--nc", is_flag=True,
              help="don't load ./project.json (to manage projects other than current)")
@click.option('--save', is_flag=True,
              help="store --set fields to ./project.json")
@click.option('--debug', is_flag=True,
              help="spew more logs")
def cli(ctx, debug, nc, sets, save):
    """DON'T PANIC.

    Deliver your project to the public cloud with steps listed below
    in the Commands section.

    Or take your time and get acquainted with their --help messages.
    """
    global DEBUG
    global CONFIG


    DEBUG = debug
    if _command_need_config(ctx.invoked_subcommand) and not nc: #no_config
        try:
            with open(PROJECT_FILE, 'r') as prj_file:
                CONFIG = json.load(prj_file, object_pairs_hook=collections.OrderedDict)
        except (ValueError, IOError) as e:
            click.echo('Can`t load %s' % PROJECT_FILE)
            click.echo(e)
            click.echo('You can use `coke init` command to make a default one, then modify it and try again.')
            ctx.abort()
    else:
        CONFIG = collections.OrderedDict()

    for s in sets:
        path = s[0].split(".")
        last_path = path.pop()
        item = CONFIG
        for section in path:
            if not section in item:
                item[section] = {}
            item = item[section]
        item[last_path] = s[1]

    if save:
        with file(PROJECT_FILE, "w") as prj_file:
            json.dump(CONFIG, prj_file, indent=2)


    if _command_need_auth(ctx.invoked_subcommand):
        if _load_auth(ctx):
            _check_api_version(ctx)


@cli.command(short_help="set and verify a cloud API entry point and an auth token")
@click.option('--url', required=True, metavar="URL", help="API server base url")
@click.option('--token', metavar="AUTH_TOKEN", type=click.STRING)
def login(ctx):
    "set and verify a cloud API entry point and an auth token"
    pass

@cli.group(cls=MyGroup, name=blank())
def _separator(ctx):
    pass


@cli.group(cls=MyGroup,
           short_help=
           """initialize a new ./project.json file with defaults and blanks
           please, 8<---- tweak generated project.json to suit to your needs
           """)
def init():

    pass

@cli.command()
@click.option('--name', prompt="Project title", default=CONFIG.get("name"), required=True)
@click.option('--version', prompt="Project version", default=CONFIG.get("version"), required=True)
@click.option('--profile', prompt="Cocaine profile", default="docker-norepo", required=True)
@click.option('--main', prompt="Executable file", required=True)
@click.option('--user', nargs=2, multiple=True)
@click.option('--yes', is_flag=True)
def init(name, version, profile, main, user, yes):
    "initialize a new project.json file in cwd with defaults and blanks"

    # use project_name, version_tag, main, user
    # generate profile, manifest, clusters (testing, production)
    # save to ./project.json

    _fill_config(name, version, profile, main, user)

    click.echo(json.dumps(CONFIG, indent=2))
    if yes or click.confirm("Save?", default=True, show_default=True):
        with file(PROJECT_FILE, "w") as prj_file:
            json.dump(CONFIG, prj_file, indent=2)
    

@cli.group(cls=MyGroup, name=blank())
def _separator():
    pass

@cli.command(cls=MyGroup, short_help="create a new cloud project described in ./project.json")
@click.option('--force', '-f', is_flag=True,
              help="force an update of the existing project")
def create(force, **kwargs):
    "create a new project in a cloud described in ./project.json"

    params={
        "force":force,
        "token": TOKEN,
        "debug": DEBUG
    }

    project_def = ProjectReader.read(CONFIG)

    missing_fields = [f for f in ("name", "members", "clusters")
                      if f not in CONFIG]
    if len(missing_fields):
        click.echo("The config must have '%s' fields!" % absent_fields)
        raise click.Abort()

    print "creating project:"
    pprint(project_def)
    
    r = requests.post(BASE+"/create/",
                      headers=headers,
                      params=params,
                      data=json.dumps(project_def, indent=2))
    handle_streaming_response(r)


@cli.group(cls=MyGroup, name=blank())
def _separator(ctx):
    pass


@cli.command(short_help="push an app version to the cloud, then build it")
@click.option('--force', '-f', is_flag=True,
              help="force an update of the existing version")
@click.option('--no-build', '-n', is_flag=True,
              help="don't schedule build of a container")
@click.option('--no-docker', is_flag=True,
              help="don't use docker conteinerization")
@click.option('--increment', '-i', is_flag=True,
              help="increment version in package.json")
@click.option('--version', '-v', help="set version in package.json")
def push(force, no_build, no_docker, increment,  version, **kwargs):
    "push an app version to the cloud, then build it"
    
    new_version = version
    old_version = CONFIG.get("version", "0-0-0")

    # build_docker_image = True
    # archive = not no_docker

    # if build_docker_image and not archive:
    #     click.echo("-a required for --build-docker-image")
    #     raise click.Abort()
    
    if increment and version:
        click.echo("options -i and -v are mutually exclusive")
        pass
    elif increment:
        cocs_suffix = re.search(r'-cocaine-(\d+)?$', old_version)

        if cocs_suffix:
            try:
                new_version_patch = str(int(cocs_suffix.group(1)) + 1)
            except ValueError:
                click.echo("Please update version in project.json manually")
                pass
            new_version = re.sub(r'\d+$', new_version_patch, old_version)
        else:
            new_version = old_version + "-cocaine-1"
            
        CONFIG["version"] = new_version

    if new_version:
        with open(PROJECT_FILE, "w") as prj_file:
            json.dump(CONFIG, prj_file, indent=2)
        logging.info("incrementing version from %s to %s" % (old_version, new_version))

    params={"force":force,
            "no-build":no_build,
            "token": TOKEN,
            "sync": True,
            "debug": DEBUG}

    version_def  = VersionReader.read(CONFIG)

    missing_fields = [f for f in ("name", "version", "clusters")
                      if f not in CONFIG]
    if len(missing_fields):
        click.echo("The config must have '%s' fields!" % missing_fields)
        raise click.Abort()

    archive = True
    
    if CONFIG.get("source"):
        s = CONFIG.get("source")
        if isinstance(s, dict) and s.get("type") == "docker":
            archive = False

    if not archive:
        assert not no_docker, "can't upload source.type==docker with no-docker option"

        r = requests.post(BASE+"/push/",
                          headers=headers,
                          params=params,
                          data=json.dumps(version_def, indent=2),
                          stream=True)
        handle_streaming_response(r)

    else:
        key = "%(name)s_%(version)s"%(version_def)

        version_def["source"] = {
            "namespace": "app-archive",
            "key": key,
            "tags": ("APP_ARCHIVE",),
            "type": "archive"
        }

        if not no_docker:
            version_def["source"]["do_build"] = True


        logging.info("creating archive")

        tarball = make_archive(".")

        logging.info("uploading archive")

        files = {"archive": ("archive.tar", BytesIO(tarball), "application/octet-stream", {})}

        r = requests.post(BASE+"/app-archive",
                          data={"key": key},
                          params={"debug": DEBUG},
                          files=files)

        logging.info("server response %s", r.text)

        logging.info("upload done")

        logging.info("pushing and building version")

        r = requests.post(BASE+"/push/",
                          headers=headers,
                          params=params,
                          data=json.dumps(version_def, indent=2),
                          stream=True)
        handle_streaming_response(r)
        

@cli.command(short_help="deploy an alredy built version to the <target> cluster")
@click.option('-u', is_flag=True,
              help="undeploy version from cluster")
@click.argument("target", metavar="<target>")
def deploy(target, u, **kwargs):
    "deploy an alredy built version to the <target> cluster"

    event = "deploy"

    if u:
        event = "undeploy"

    missing_fields = [f for f in ("name", "version")
                      if f not in CONFIG]
    if len(missing_fields):
        click.echo("The config must have '%s' fields!" % fields)
        raise click.Abort()

    r = requests.post(BASE+"/%s/%s/"%(event,target),
                      data = json.dumps(CONFIG, indent=2),
                      params = { "sync": True,
                                 "token": TOKEN,
                                 "debug": DEBUG },
                      stream = True)

    handle_streaming_response(r)


@cli.command(short_help="balance a load between versions at the <target> cluster")
@click.argument("target", metavar="<target>")
def balance(target, **kwargs):
    """
    balance load between versions at the <target> cluster

    looks up routing info in your project.json, updates
    cluster configuration for the project, and performs
    a corresponding balance task.
    """

    bad_routing_msg = """
  To update routing with 'balance' command, you should have 'routing' section for particular cluster configured:
  "clusters": {
    "%s": {
      "routing": {
        "<project_name>_<versionA>": 100,
        "<project_name>_<versionB>": 200
      }
    }
  }
""" % target
    
    missing_fields = [f for f in ("name", "version")
                      if f not in CONFIG]
    if len(missing_fields):
        click.echo("The config must have '%s' fields!" % missing_fields)
        raise click.Abort()

    try:
        routing = CONFIG.get("clusters").get(target).get("routing")
    except (TypeError, KeyError, AttributeError) as err:
        click.echo(bad_routing_msg)
        raise click.Abort(err)
    else:
        if not isinstance(routing, dict):
            click.echo(bad_routing_msg)
            raise click.Abort()

    r = requests.post(BASE+"/balance/%s/"%target,
                      data = json.dumps(CONFIG, indent=2),
                      params = { "sync": True,
                                 "token": TOKEN,
                                 "debug": DEBUG},
                      stream = True)

    handle_streaming_response(r)


@cli.command(name="deliver", short_help="perform all three of the above steps with one command")
@click.option('--increment', '-i', is_flag=True,
              help="increment version in package.json")
@click.option('--version', '-v', help="set version in package.json")
@click.option('--no-docker', is_flag=True,
              help="don't use docker conteinerization")
@click.argument("target", metavar="<target>")
def deliver(increment,  version, no_docker, target, **kwargs):
    """
    perform all three of the above steps with one command

    pushes, deploys to <target> cluster and configures routing
    with one route, pointing to version it pushed with weight of 10
    """
    force = False

    new_version = version
    old_version = CONFIG.get("version", "0-0-0")

    if increment and version:
        click.echo("options -i and -v are mutually exclusive")
        pass
    elif increment:
        cocs_suffix = re.search(r'-cocaine-(\d+)?$', old_version)

        if cocs_suffix:
            try:
                new_version_patch = str(int(cocs_suffix.group(1)) + 1)
            except ValueError:
                click.echo("Please update version in project.json manually")
                pass
            new_version = re.sub(r'\d+$', new_version_patch, old_version)
        else:
            new_version = old_version + "-cocaine-1"
            
        CONFIG["version"] = new_version

    if new_version:
        with open(PROJECT_FILE, "w") as prj_file:
            json.dump(CONFIG, prj_file, indent=2)
        logging.info("incrementing version from %s to %s" % (old_version, new_version))

    params={"force":False,
            "no-build":False,
            "token": TOKEN,
            "sync": True,
            "debug": DEBUG}

    params["autorelease_to"] = target

    version_def  = VersionReader.read(CONFIG)

    missing_fields = [f for f in ("name", "version", "clusters")
                      if f not in CONFIG]
    if len(missing_fields):
        click.echo("The config must have '%s' fields!" % missing_fields)
        raise click.Abort()

    archive = True
    
    if CONFIG.get("source"):
        s = CONFIG.get("source")
        if isinstance(s, dict) and s.get("type") == "docker":
            archive = False

    if not archive:

        assert not no_docker, "can't upload source.type==docker with no-docker option"
        
        r = requests.post(BASE+"/push/",
                          headers=headers,
                          params=params,
                          data=json.dumps(version_def, indent=2),
                          stream=True)
        handle_streaming_response(r)

    else:
        key = "%(name)s_%(version)s"%(version_def)

        version_def["source"] = {
            "namespace": "app-archive",
            "key": key,
            "tags": ("APP_ARCHIVE",),
            "type": "archive"
        }

        if not no_dokcer:
            version_def["source"]["do_build"] = True

        logging.info("creating archive")

        tarball = make_archive(".")

        logging.info("uploading archive")

        files = {"archive": ("archive.tar", BytesIO(tarball), "application/octet-stream", {})}

        r = requests.post(BASE+"/app-archive",
                          data={"key": key},
                          params={"debug": DEBUG},
                          files=files)

        logging.info("server response %s", r.text)

        logging.info("upload done")

        logging.info("pushing and building version")

        r = requests.post(BASE+"/push/",
                          headers=headers,
                          params=params,
                          data=json.dumps(version_def, indent=2),
                          stream=True)
        handle_streaming_response(r)


@cli.group(cls=MyGroup, name=blank())
def _separator(ctx):
    pass

@cli.group(cls=MyGroup)
def show(ctx):
    "inspect various minutae and statuses"
    pass

@cli.group(cls=MyGroup, name=blank())
def _separator(ctx):
    pass


@cli.group(cls=MyGroup)
def task():
    "tasks-related subcommands"
    pass


@task.command()
@click.argument("task-id")
def status(task_id):
    "display status for given task-id"
    pass

@task.command()
@click.argument("task-id")
def retry(task_id):
    "retry task with task-id"
    pass


@cli.group(cls=MyGroup)
def project():
    "manage project configuration"
    pass

@cli.group(cls=MyGroup)
def version():
    "manage version configuration"
    pass

@cli.group(name=blank())
def _separator():
    pass
    
@cli.group(name=blank(), short_help="have to be a platform admin to do this:")
def _separator():
    pass
    
@cli.group(cls=MyGroup, short_help="manage cloud clusters")
def cluster():
    "manage cloud clusters (you have to be a platform admin to do this)"
    pass

@cli.group(cls=MyGroup, short_help="manage global users")
def user():
    "manage global users"
    pass

@cli.group(cls=MyGroup, name=blank())
def _separator():
    pass
    

@cli.command()
@click.argument("task-id")
def status(task_id):
    "<task-id> prints status of the task"
    r = requests.get(BASE+"/status/%s/"%task_id, params={"debug": DEBUG})
    handle_streaming_response(r)
    #print r.text


@cli.command()
@click.argument("task_id")
def task_restart(task_id):
    "restart given task"
    r = requests.post(BASE+"/task/%s/restart/"%task_id,
                      params = { "sync": True,
                                 "token": TOKEN,
                                 "debug": DEBUG},
                      stream = True)

    handle_streaming_response(r)

@cli.command()
def show():
    "show project status"

    project_id = CONFIG['name']

    r = requests.get(BASE+"/project/%s/" % project_id, params={"debug": DEBUG})
    print r.text
    if r.status_code != 200:
        sys.exit(2)

@cli.command()
def clusters_info():
    "dump cluster configuration"

    r = requests.get(BASE+"/clusters/", params={"debug": DEBUG})
    print r.text
    if r.status_code != 200:
        sys.exit(2)

@cli.command()
@click.option('-s', '--src', required=True, help="path to a file, formatted compatible to the output of `clusters_info`")
@click.option('-u', '--update', is_flag=True, default=False)
def clusters_create(src, update):
    with file(src, "r") as configs_file:
        configs = configs_file.read()
        click.echo(configs)
        if click.confirm("File is correct?", default=False):
            r = requests.post(BASE+"/clusters/", params={
                "debug": DEBUG,
                "update": update,
                "token": TOKEN
            }, data=configs)
            handle_streaming_response(r)

@cli.group(cls=MyGroup, name=blank())
def _separator(ctx):
    pass
    

if __name__ == "__main__":
    cli()
