#!/usr/bin/env python
# -*- coding: utf-8 -*-

import appdirs
import os
import os.path
import sys
import json
import glob
import subprocess
import shutil
import socket
import re


odoo_server = None


def pexec(cmd):
    """ executes shell command cmd with the output
        printed in the parent shell. Returns when the
        command has finished.
    """
    os.system(cmd)


def rexec(cmd):
    """ executes shell command cmd with the output
        returned as a string when the command has
        finished.
    """
    try:
        output = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        return exc.output[:-1]
    else:
        return output[:-1]


def opexec(cmd):
    """ same as pexec() but with current working
        directory set to the odoo server path
    """
    path = odoo_path_or_crash()
    process = subprocess.Popen(cmd.split(), cwd=path)
    return process.wait() == 0


def otexec(cmd):
    """ executes the command cmd with the odoo
        server path as current working dir.
        All output is hidden. Returns True if the
        call exited successfully, False otherwise.
    """
    path = odoo_path_or_crash()
    process = subprocess.Popen(cmd.split(), cwd=path,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.wait() == 0


def orexec(cmd):
    """ same as rexec() but with current working
        directory set to the odoo server path
    """
    path = odoo_path_or_crash()
    process = subprocess.Popen(cmd.split(), cwd=path, stdout=subprocess.PIPE)
    return process.communicate()[0][:-1]


def less(string):
    process = subprocess.Popen(['less', '-R'], stdin=subprocess.PIPE)
    process.communicate(input=string)
    process.wait()


def is_port_taken(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    return result == 0


def find_port(start=8069):
    for port in range(start, start + 10):
        if not is_port_taken(port):
            return port
    return None


def iselect(list):
    if len(list) <= 1:
        return list
    else:
        result = rexec('iselect -a -m ' + ' '.join(list))
        if result:
            return result.split('\n')
        else:
            return []


def edit(files, cwd='/'):
    editor = get_config('editor', 'vim -p')
    if not _cmd_exists(editor.split()[0]):
        print 'Editor not found: ' + editor.split()
        print 'You can either install the editor or configure another one.'
        print 'Ex: ook config editor emacs'
        sys.exit(1)
    subprocess.Popen(editor.split() + files, cwd=cwd).wait()


def branch_to_db(branch):
    return branch


def dblist():
    l = [el.split() for el in rexec('psql -l').split('\n')]
    return [el[0] for el in l if len(el) > 3]


def ignored(path):
    path = path.strip()
    return path.endswith('.pyc') or path.endswith('.po')


# FIXME: use gitpython ?
def git_status():
    status = {
        'untracked': [],
        'modified': [],
        'removed': [],
        'ignored': [],
    }

    path = odoo_path_or_crash()
    stat = orexec('git status --porcelain')
    if not stat:
        return status

    stat = [[line[0:2], os.path.join(path, line[3:])] for line in stat.split('\n')]
    for s in stat:
        if s[0] == '??':
            status['untracked'].append(s[1])
        elif s[0] == '!!':
            status['ignored'].append(s[1])
        else:
            if os.path.exists(s[1]):
                status['modified'].append(s[1])
            else:
                status['removed'].append(s[1])

    return status


#   +============================+
#   |        HELP STRINGS        |
#   +============================+


PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
COLOR_END = '\033[0m'


def clr(c, txt):
    return c + txt + COLOR_END


CMD_HELP = {
    "help": """
ook help [CMD]
       prints this help, or the help of the
       provided command.
    """,
    "install": """
ook install
       install the non-python dependencies. This
       command must be run as the administrator.

       Ex: sudo ook install
    """,
    "start": """
ook start [args]
       [Re]start the Odoo server on port 8069
       with a db named with the current git
       branch. It will create a database
       with demo data if it doesn't exist.

       [args] will be passed to the odoo
       server command line.

       Ex: ook start -i stock
       -> Start odoo and install the stock
          module

       ALIAS: 'x'
    """,
    "reset": """
ook reset [args]
       Restart the server with a new database

       [args] will be passed to the odoo
       server command line at restart.
    """,
    "stop": """
ook stop
       Stops the current server.
    """,
    "dropdb": """
ook dropdb
       Drops the database named with current branch.
    """,
    "status": """
ook status
       Shows the status of the current branch.

       ALIAS: 'st'
    """,
    "log": """
ook log
       Prints the last 20 commits in a readable
       format.
    """,
    "find": """
ook find PATTERN
       Finds files in the repository that
       contains PATTERN in their filename.

       Ex: ook find .js
       -> Lists all javascript files in Odoo

       If multiple space separated patterns are
       provided, it will search for paths that
       contains the patterns in matching order.

       Ex: ook find web/ src .xml
       -> Lists all client side templates inside
          the 'web/' module

        ALIAS: 'f'
    """,
    "edit": """
ook edit PATTERN
       Find files using PATTERN, and edit them
       in your favorite editor. See the help for
       the 'find' command to see how PATTERN
       works.

       The default configuration is to open the
       selected files in vim tabs. The editor is
       specified in the 'editor' config.

       Type 'ook config editor' to check what's
       your current editor.

       Type 'ook config editor PATH ARGS' to
       change the current editor.

       Ex: ook config editor vim -O
       -> sets the current editor to VIM and
          open files in vertical splits.

       If no PATTERN is provided, the last
       edited files will be re-opened

       ALIAS: 'e'
    """,
    "grep": """
ook grep PATTERN [in FINDPATTERN]
       Find and edit files that contain PATTERN
       in one or more lines.

       Ex: ook grep ActionManager
       -> Find files containing 'ActionManager'

       Ex: ook grep ActionManager extend
       -> Find files containing 'ActionManager'
          followed by 'extend' on the same line

       It is possible to restrict the inspected
       files with a pattern. The pattern works
       exactly the same as in the 'ook find'
       command, and must be specified after a
       'in' token.

       Ex: ook grep ActionManager in .js
       -> Find files containing 'ActionManger'
          with '.js' in their path

       Ex: ook grep ActionManager in web/ .js
       -> Find files containing 'ActionManager'
          in javascript files in the web/ module

       After files have been found, you have
       the possibility to edit them in your text
       editor. See the 'ook edit' help for more
       information.

       ALIAS: 'ack', 'g'
    """,
    "try": """
ook try [BRANCH] [ARGS]
       Duplicates the code of the current branch or
       of the selected branch BRANCH in a temporary
       directory, then launches a odoo instance on
       that codebase.

       The current repository is not touched, and the
       currently running servers are kept alive.

       Odoo servers launched with 'try' are not
       affected by the start / stop / reset commands

       The databases created by try are recycled after
       a while

       [ARGS] will be passed to the odoo server.

       Ex: ook try
       -> Create an instance for the current branch

       Ex: ook try 8.0-fixes-mat -i website
       -> Create an instance for the 8.0-fixes-mat
          branch and install the website module
    """,
    "test": """
ook test [BRANCH] [ARGS]
       Starts python unit tests on the code found in
       the current branch, or on branch BRANCH.
       The code is exported before the tests are
       started so that you can keep working while the
       tests are running.

       Only committed changes are tested.

       The databases created by test are recycled after
       a while

       [ARGS] will be passed to the odoo
       server command line at startup.

       Ex: ook test
       -> Run tests on current branch.

       Ex: ook test 8.0-fixes-mat
       -> Create an instance for the 8.0-fixes-mat
          branch and test all modules

    """,
    "path": """
ook path
       Prints the path to the odoo server directory
    """,
    "fetch": """
ook fetch BRANCH_PATTERN
       Searches for remote branch matching the branch
       pattern, and makes them available as a local
       branch. You can then use 'ook try BRANCH_NAME'
       or 'git checkout BRANCH_NAME', etc.

       Ex: ook fetch fix mat
       -> Find all remote branches containing 'fix'
          and 'mat' in that order, then lets you fetch
          them

    """,
    "switch": """
ook switch BRANCH_PATTERN
       Searches for local branches matching the branch
       pattern, and lets you checkout one of them.

       Ex: ook switch pos fva
       -> List all local branches containing 'pos' and
          'fva' and lets you checkout one of them.

       If no pattern is provided, it will switch to
       the last fetched branch.

       Ex: ook fetch fix mat
           ook switch
       -> Switches to the branch selected in the fetch

       ALIAS: 'sw', 'checkout', 'co'
    """,
    "branch": """
ook branch
       Prints the current branch of the odoo repository
    """,
    "git": """
ook git [git command]
       Executes the git command in the odoo repository.
       Ex: cd /var/log; ook git status
       -> Prints git's status.
    """,
    "config": """
ook config [key] [value]
       Prints the content of the Ook config file.

       [key] Prints the value associated with key
       in the Ook config file.

       [key] [value]
       Sets the Ook config option 'key' to 'value'
    """,
    "alias": """
ook alias ALIAS CMD:
       Creates an alias named ALIAS for the ook command
       CMD. CMD can contain arguments for the aliased
       command. If further arguments are given when
       invoking the alias, they are appended to the
       alias.

       Ex: ook alias f find
       ->  ook f web/ .js

       If the alias contains the token ARGS, it will
       be replaced by the invocation arguments.

       Ex: ook alias css edit ARGS .css
       ->  ook css website/
           - Expands to "ook edit website/ .css"
    """,
    "todo": """
ook todo [TASK]:
       Add the string TASK at the top of the todolist.

       Ex: ook todo save the world.

       If no TASK is specified, print the todolist.

       Ex: ook todo
       ->  [TODO]  0: save the world.
           [TODO]  1: pump up the jam.

       See 'ook help done' for marking tasks as done.
    """,

    "done": """
ook done [TASK_IDS]:
       Mark the todo tasks with ids 'TASK_IDS' as done.

       Ex: ook todo
       ->  [TODO]  0: save the world.
           [TODO]  1: pump up the jam.
        -  ook done 0
        -  ook todo
       ->  [TODO]  0: pump up the jam.
            ----
           [DONE]  0: save the world.

       If no TASK_IDS are provided, print all the done
       tasks.
    """,
}


def fmt_help(cmd):
    help = CMD_HELP[cmd]
    help1 = help.split('\n')[1].split(' ')
    help2 = help.split('\n')[2:]
    out = ''
    out += help1[0] + ' ' + BOLD + help1[1] + COLOR_END
    if len(help1) > 2:
        out += ' ' + ' '.join(help1[2:]) + '\n'
    else:
        out += '\n'
    out += '\n'.join(help2) + '\n'
    return out


HELP = "\n".join([
    "",
    "Usage: ook [COMMAND]",
    "",
    "".join([fmt_help(help) for help in CMD_HELP.keys()]),
])


#   +============================+
#   |        CONFIG FILE         |
#   +============================+

def config_file_path():
    return os.path.join(appdirs.user_config_dir(), 'ook.json')


def config_file():
    path = config_file_path()
    if os.path.exists(path):
        return open(path, 'r+')
    else:
        return open(path, 'w+')


def set_config(key, value):
    with config_file() as config:
        contents = config.read()
        parsed = json.loads(contents if contents else "{}")
        parsed[key] = value
        config.seek(0)
        config.truncate(0)
        config.write(json.dumps(parsed, indent=4))


def get_config(key, default=None):
    with config_file() as config:
        contents = config.read()
        parsed = json.loads(contents if contents else "{}")
        return parsed.get(key, default)


#   +============================+
#   |      REPOSITORY INFO       |
#   +============================+


def odoo_branch():
    return orexec("git rev-parse --abbrev-ref HEAD")


def odoo_path():
    def is_path_repo(path):
        return ".git" in os.listdir(path)

    def is_path_odoo(path):
        return "openerp-server" in os.listdir(path)

    def get_odoo(path):
        if is_path_repo(path) and is_path_odoo(path):
            return path
        elif os.path.samefile(path, os.path.join(path, '..')):
            return None
        else:
            return get_odoo(os.path.abspath(os.path.join(path, "..")))

    path = get_odoo(os.getcwd())

    if path:
        set_config('path', path)
        return path

    path = get_config('path')
    if path and os.path.exists(path) and is_path_odoo(path):
        return path

    for path in ['~/odoo', '~/odoo/odoo', '~/code/odoo',
                 '~/projects/odoo', '~/Projects/odoo',
                 '~/Code/odoo/', "/opt/odoo"]:
        path = os.path.expanduser(path)
        if os.path.exists(path) and is_path_odoo(path) and is_path_repo(path):
            set_config('path', path)
            return path

    return None


def odoo_path_or_crash():
    path = odoo_path()
    if path:
        return path
    else:
        error = """
Could not find the odoo server directory.
Please type 'ook' from inside your odoo
server directory, its location will be
remembered.
"""
        sys.exit(error)

#   +============================+
#   |         COMMANDS           |
#   +============================+


def cmd_help(args):
    if len(args) < 2:
        less(HELP)
    elif args[1] in CMD_HELP.keys():
        print "\n" + fmt_help(args[1])[:-1]
    else:
        print "Unknown command", args[1]
        print "Type 'ook help' to see the command list"


def cmd_log():
    opexec("git log --oneline -n 20")


def cmd_port():
    print find_port()


def cmd_branch():
    print odoo_branch()


def cmd_git(args):
    opexec(" ".join(args))


def cmd_ook():
    if not _is_installed():
        print RED + "Installation not complete ... " + COLOR_END
        print "Type '" + UNDERLINE + "sudo ook install" + COLOR_END + "' to complete the installation."
        sys.exit(1)
    print ""
    print PURPLE + "      The Odoo Code Monkey Helper" + COLOR_END
    print "  Type '" + UNDERLINE + "ook help" + COLOR_END + "' to display the help"
    print
    print "\n".join([
        """                         .="=.          """,
        """                Ook!   _/.-.-.\\_     _  """,
        """                   \\  ( ( o o ) )    )) """,
        """                       |/  "  \\|    //  """,
        """       .-------.        \\'---'/    //   """,
        """      _|~~ ~~  |_       /`"'"`\\\\  ((    """,
        """    =(_|_______|_)=    / /_,_\\ \\\\  \\\\   """,
        """      |:::::::::|      \_\\_'__/ \\  ))  """,
        """      |:::::::[]|       /`  /`~\\  |//   """,
        """      |o=======.|      /   /    \\  /    """,
        """      `"'"'"'"'"`  ,--`,--'\\/\\    /     """,
        """                    '-- "--'  '--'      """,
        "",
    ])

EXTRA_WORDS = set(['EAN', 'EAN-13', 'EAN-8', 'nbsp', 'barcode',
                   'barcodes', 'UPC', 'UPC-A', 'UPC-E', 'Odoo', 'POS', 'CRM', 'MRP', 'PosBox',
                   'str', 'multi', 'div', 'textarea', 'kanban', 'px', 'ip', 'hostname',
                  'desc', 'resize', 'resized', 'login', 'API', 'TCP', 'lookup'])

EXTRA_WORDS = [w.lower() for w in EXTRA_WORDS]


def spell_check(path, content):
    process = subprocess.Popen(['aspell', '-l', 'en_US', '--encoding=utf-8', '--mode=html',
                                '--add-html-skip=t-name,t-esc,t-if,t-raw,t-foreach,t-as,t-set,content',
                                '-a'],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    result = process.communicate(input=content)[0][:-1]
    process.wait()
    result = result.split('\n')[1:]
    result = [r for r in result if len(r) and r[0] != '*']

    if not len(result):
        return None

    words = {}
    for line in result:
        line = line.split()
        word = line[1]
        if word.lower() not in EXTRA_WORDS and word not in words:
            words[word] = line[4:12]

    out = ''
    content = content.split('\n')
    for word in words:
        out += word + ' : ' + ' '.join(words[word]) + '\n'
        count = 0
        reg = re.compile("(?:^|\W)" + word + "(?:$|\W)")
        for i, line in enumerate(content):
            if reg.search(line):
                count += 1
                out += "{:>5}:".format(i) + " " + line + "\n"
            if count >= 8:
                out += " ...\n"
                break

    return out[:-1]


def py_path_check(path, content):
    path, file = os.path.split(path)
    path = path + '/'
    if file in ['__init__.py', '__openerp__.py']:
        return None
    if 'addons/' in path:
        if 'tests/' not in path and 'models/' not in path and 'controllers/' and 'wizard/' not in path:
            return "python files should be in 'models/', 'tests/' , 'wizard/' or 'controllers/'"
        if 'controllers/' in path and file != 'main.py':
            return "The controller file should be named 'main.py'"
    return None


def xml_path_check(path, content):
    path, file = os.path.split(path)
    path = path + '/'
    if 'addons/' not in path:
        return None
    if ('_demo' in file or '_data' in file) and 'data/' not in path:
        return "Demo and Data files should be in the 'data/' subdirectory."
    elif 'data/' in path and ('_demo' not in file and '_data' not in file):
        return "Demo and Data files should be suffixed with '_demo.xml' or '_data.xml'"
    elif '_security' in file and 'security/' not in path:
        return "Security files should be in the 'security/' subdirectory."
    elif 'security/' in path and '_security' not in file:
        return "Security files should be suffixed with '_security.xml'"
    elif ('_templates' in file or '_views' in file) and 'views/' not in path:
        return "Views and templates should be in the 'views/' subdirectory."
    elif 'views/' in path and ('_templates' not in file and '_views' not in file):
        return "Views and and templates should be suffixed with '_views.xml' or '_templates.xml'"
    elif 'static/src/xml/' not in path and 'views/' not in path and 'security/' not in path and 'data/' not in path:
        return "Xml files should be placed in the appropriate subfolder"


def code_spell_check(path, content):
    reg = re.compile("((?:'.*?[^']')|(?:\".*?[^\"]\"))")
    reg_css = re.compile("\s[.#<>]")
    content = content.split('\n')
    textchars = set(list("abcdefghijklmnopqrstuvwxyz0123456789:,. \t"))
    out = ""

    def textratio(txt):
        r = 0
        for c in txt:
            if c.lower() in textchars:
                r += 1.0
        ratio = r / float(len(txt))
        return ratio

    for line in content:
        strings = reg.findall(line)
        strings = [s[1:-1] for s in strings if ' ' in s]  # ignoring keywords
        strings = [s for s in strings if textratio(s) > 0.85]  # ignore code
        strings = [s for s in strings if s[0] not in ['.', '#', "<", ">"] and s[-1] not in ["<", ">"]]  # ignoring css and xml strings
        strings = [s for s in strings if not reg_css.search(s)]  # further ignoring
        strings = [s for s in strings if s != 'use strict']

        if strings:
            out += '\n'.join(strings) + '\n'

    if out:
        return spell_check(path, out)
    else:
        return None


PY_CHECKS = {
    "spell_check": spell_check,
    "code_spell_check": code_spell_check,
    "py_path_check": py_path_check,
    "xml_path_check": xml_path_check,
}


CHECKS = {
    ".xml": [
        {"ignore": "/lib/"},
        {"cmd": "xmllint --noout", "sev": "error", "msg": "Invalid XML File."},  # Fails if 'cmd' outputs
        {"regexp": "model=.*id=", "sev": "warn", "msg": "Put the 'id=' before 'model='"},
        {"py": "spell_check", "sev": "spell", "msg": "Spelling Mistakes."},
        {"py": "xml_path_check", "sev": "warn", "msg": "File Naming Recommendations."},
    ],
    ".js": [
        {"ignore": "\.min\.js$"},  # Regexp on the path will ignore file for further tests
        {"ignore": "\/lib\/"},
        {"regexp": "debugger", "sev": "error", "msg": "Debugger Directives."},  # Must not match a line
        {"regexp": "console\.log", "sev": "warn", "msg": "console.log()"},
        {"assert": "use strict", "sev": "error", "msg": 'Missing "use strict"'},  # Opposite of 'regexp'
        {"py": "code_spell_check", "sev": "spell", "msg": "Spelling Mistakes."},
        {"cmd": "jshint", "sev": "warn", "msg": "JSHint"},
    ],
    ".py": [
        {"ignore": "/lib/"},
        {"regexp": "(?:import.*pudb|import.*pdb|set_trace\(\))", "sev": "error", "msg": "Debugger Directives."},
        {"ignore": "__init__\.py"},
        {"regexp": "fields\.(?!.*help=)(?=.*\))", "sev": "warn", "msg": "Undocumented Fields."},
        {
            "cmd": "flake8 --exit-zero --ignore=W,E501,E301,E302,E123,E126,E127,E128,E265,E231",
            "sev": "warn",
            "msg": "PEP8",
        },
        {"py": "py_path_check", "sev": "warn", "msg": "File Naming Recommendations."},
        {"py": "code_spell_check", "sev": "spell", "msg": "Spelling Mistakes."},
    ],
}


def cmd_check(args):

    def search(regexp, text):
        r = re.compile(regexp)
        return r.search(text)

    def contents(path):
        with open(path, 'r') as f:
            return f.read()

    def print_stat(sev, path, msg=None):
        print {
            'ok': BLUE + '   OK:',
            'error': RED + 'ERROR:',
            'warn': PURPLE + ' WARN:',
            'spell': UNDERLINE + 'SPELL:',
        }[sev] + ' ' + path + ((' : ' + msg) if msg else '') + COLOR_END

    nowarn = 'error' in args
    if nowarn:
        args.remove('error')

    onlyspell = 'spell' in args
    if onlyspell:
        args.remove('spell')

    if len(args) == 1:
        paths = git_status()['modified']
    else:
        paths = find_paths(args)

    for path in paths:
        exts = [ext for ext in CHECKS if path.endswith(ext)]
        if not len(exts):
            continue
        if os.path.isdir(path):
            continue

        ext = exts[0]
        content = contents(path)
        tests = CHECKS[ext]
        ok = True
        checked = False

        for test in tests:
            if test.get('ignore') and search(test.get('ignore'), path):
                break
            if nowarn and test.get('sev') in ['warn', 'spell']:
                continue
            if onlyspell and test.get('sev', 'spell') != 'spell':
                continue
            if not onlyspell and test.get('sev') == 'spell':
                continue
            checked = True

            if test.get('cmd'):
                assert_cmd(test.get('cmd').split()[0])
                errors = rexec(test.get('cmd') + ' ' + path)
                if errors:
                    ok = False
                    print_stat(test.get('sev', 'error'), path, test.get('msg'))
                    print errors
            elif test.get('py'):
                errors = PY_CHECKS[test.get('py')](path, content)
                if errors:
                    ok = False
                    print_stat(test.get('sev', 'error'), path, test.get('msg'))
                    print errors
            elif test.get('regexp') or test.get('assert'):
                reg = re.compile(test.get('regexp') or test.get('assert'))
                lines = content.split('\n')
                valid = True
                out = ''
                for i, line in enumerate(lines):
                    if reg.search(line):
                        valid = False
                        out += "{:>5}: ".format(str(i)) + " " + line + "\n"
                if test.get('assert'):
                    valid = not valid
                if not valid:
                    ok = False
                    print_stat(test.get('sev', 'error'), path, test.get('msg'))
                    if out:
                        print out[:-1]
        if checked and ok:
            print_stat('ok', path)

DEPS = {
    "deps": ["git", "aspell", "iselect", "jshint", "xmllint", "npm"],  # Those commands should be available when installed
    "osx": {  # Packages to install on OSX
        "brew": ["git", "aspell", "node"],
        "port": ["iselect"],
        "npm": ["jshint"]
    },
    "linux": {  # Packages to install on Linux
        "apt-get": ["git", "aspell", "iselect", "libxml2-utils", "nodejs"],
        "npm": ["jshint"]
    }
}


def _cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE) == 0


def assert_cmd(cmd):
    if not _cmd_exists(cmd):
        sys.exit("Command not found: " + cmd)


def _missing_deps():
    return [dep for dep in DEPS["deps"] if not _cmd_exists(dep)]


def _is_installed():
    return len(_missing_deps()) == 0


def cmd_install():
    if _is_installed():
        print "Already installed."
        return
    if os.getuid() != 0:
        sys.exit("Please run this command as the administrator ( sudo ook install )")

    if sys.platform.startswith('linux'):
        if not _cmd_exists("apt-get"):
            print "Apt-Get not found; please install the following dependencies manually."
            print ' '.join(DEPS["linux"]["apt-get"])
            sys.exit(1)
        pexec("apt-get install " + ' '.join(DEPS["linux"]["apt-get"]))
        pexec("npm install -g " + ' '.join(DEPS["linux"]["npm"]))

    if sys.platform.startswith('darwin'):
        if not _cmd_exists("port"):
            print "MacPorts not found; please install macports and try again."
            print "https://www.macports.org/install.php"
            sys.exit(1)
        if not _cmd_exists("brew"):
            print "Homebrew not found; please install Homebrew and try again."
            print "http://brew.sh/"
            sys.exit(1)
        pexec("port install " + ' '.join(DEPS["osx"]["port"]))
        pexec("brew install " + ' '.join(DEPS["osx"]["brew"]))
        pexec("npm install -g " + ' '.join(DEPS["linux"]["npm"]))

    if not _is_installed():
        print RED + "Installation Errors." + COLOR_END
        print "The following packages could not be installed:"
        print " ".join(_missing_deps())
        sys.exit(1)
    else:
        print GREEN + "Installation complete." + COLOR_END


def cmd_status():
    path = odoo_path_or_crash()
    print "On repo", path
    opexec("git status")


def cmd_stop():
    pid = get_config("ook_pid")
    if pid and pid > 0:
        pexec("pkill -TERM -P " + str(pid))
        set_config("ook_pid", -1)
        set_config("server_pid", -1)


def cmd_dropdb():
    branch = odoo_branch()
    cmd_stop()
    print "Dropping database", branch
    pexec('dropdb ' + branch)


def cmd_start(args):
    global odoo_server
    path = odoo_path_or_crash()
    opath = path + "/odoo.py"
    branch = odoo_branch()
    cmd = args[0]

    if len(args) < 2:
        args = []
    else:
        args = args[1:]

    cmd_stop()

    print "Starting Odoo:"
    print "     Server: " + opath
    print "   Database: " + branch
    if len(args):
        print "       args: " + " ".join(args)
    print ""

    if branch not in dblist():
        rexec('createdb ' + branch)

    set_config("ook_pid", os.getpid())

    if cmd == 'startall':
        mpath = path + '/addons/*/__init__.py'
        modules = glob.glob(mpath)
        modules = set([os.path.basename(os.path.dirname(m)) for m in modules])
        modules = modules - set(['auth_ldap', 'document_ftp', 'hw_escpos', 'hw_proxy',
                                 'hw_scanner', 'base_gengo', 'website_gengo', 'website_instantclick'])
        modules = ",".join(list(modules))
        cmd = opath + " start -d " + branch + ' --db-filter="^' + branch + '$" -i ' + modules + " ".join(args)
    else:
        cmd = opath + " start -d " + branch + ' --db-filter="^' + branch + '$" ' + " ".join(args)

    odoo_server = subprocess.Popen(cmd.split(), cwd=path)
    set_config("server_pid", odoo_server.pid)

    return odoo_server.wait()


def tmp_export(branch):
    path = odoo_path_or_crash()
    maxtmps = get_config('maxtmps', 5)

    try_path = '/tmp/' + branch
    try_db = "tmp-" + branch_to_db(branch)

    trials = get_config('tmps', [])

    exists = False
    for trial in trials:
        if trial['path'] == try_path:
            exists = True
            break
    if not exists:
        trials.append({'path': try_path, 'db': try_db})

    if len(trials) > maxtmps:
        print "Cleaning up old exports... "
        for trial in trials[:-maxtmps]:
            if os.path.exists(trial['path']):
                shutil.rmtree(trial['path'])
            if trial['db'] in dblist():
                pexec('dropdb ' + trial['db'])
        trials = trials[-maxtmps:]

    set_config('tmps', trials)

    if os.path.exists(try_path):
        shutil.rmtree(try_path)
    os.makedirs(try_path)

    print "Exporting branch", branch, "to /tmp ..."
    os.system("cd " + path + "; git archive " + branch + " | tar -x -C " + try_path)


def cmd_try(args):
    global odoo_server
    path = odoo_path_or_crash()
    cmd = args[0]

    oargs = []
    for index, arg in enumerate(args):
        if arg[0] == '-':
            oargs = args[index:]
            args = args[:index]
            break

    if len(args) < 2:
        branch = odoo_branch()
    else:
        branches = cmd_fetch(['fetch'] + args[1:])
        if not branches:
            sys.exit("No branch selected.")
        branch = branches[0]["branch"]

    try_path = '/tmp/' + branch
    try_db = "tmp-" + branch
    tmp_export(branch)

    opath = try_path + '/odoo.py'

    port = find_port(8070)
    if not port:
        sys.exit('Could not find an available server port')
    else:
        port = str(port)

    print "Starting Odoo:"
    print "     Server: " + opath
    print "   Database: " + try_db
    print "       Port: " + port
    if len(oargs):
        print "       args: " + " ".join(oargs)
    print ""

    if cmd == 'test':
        mpath = path + '/addons/*/__init__.py'
        modules = glob.glob(mpath)
        modules = set([os.path.basename(os.path.dirname(m)) for m in modules])
        modules = modules - set(['auth_ldap', 'document_ftp', 'hw_escpos', 'hw_proxy',
                                 'hw_scanner', 'base_gengo', 'website_gengo', 'website_instantclick'])
        modules = ",".join(list(modules))

        if try_db in dblist():
            rexec("dropdb " + try_db)
            rexec("createdb " + try_db)

        cmd = opath + " start -d " + try_db + ' --db-filter="^' + try_db + '$" --xmlrpc-port=' + port
        cmd += ' --test-enable --stop-after-init --log-level=test --max-cron-threads=0'
        cmd += ' -i ' + modules
        cmd += ' ' + ' '.join(oargs)

    else:
        if try_db not in dblist():
            rexec("createdb " + try_db)

        cmd = opath + " start -d " + try_db + ' --db-filter="^' + try_db + '$" --xmlrpc-port=' + port + " " + " ".join(oargs)

    odoo_server = subprocess.Popen(cmd.split(), cwd=path)
    return odoo_server.wait()


def cmd_reset(args):
    cmd_dropdb()
    cmd_start(args)


def cmd_path():
    print odoo_path_or_crash()


def cmd_find(args):
    if len(args) < 2:
        print "Please provide a pattern to find"
        print CMD_HELP["find"]
    else:
        path = odoo_path_or_crash()
        pattern = '"*' + "*".join(args[1:]) + '*"'
        args = args[1:]
        if len(args) == 1:
            pexec('find ' + path + ' -iname ' + '*' + args[0] + '*')
        else:
            pattern = '*' + "*".join(args) + '*'
            pexec('find ' + path + ' -iwholename ' + pattern)


def find_paths(args):
    path = odoo_path_or_crash()
    args = args[1:]
    if len(args) == 1:
        if os.path.exists(args[0]):
            results = args[0]
        else:
            results = rexec('find ' + path + ' -iwholename ' + '*' + args[0] + '*')
    else:
        pattern = '*' + "*".join(args) + '*'
        results = rexec('find ' + path + ' -iwholename ' + pattern)

    results = [r for r in results.split() if not ignored(r)]

    if len(results) > 1:
        results = iselect(results)

    fresults = []

    def visit(root, dirname, names):
        for name in names:
            # print root, dirname, name
            path = os.path.join(dirname, name)
            if not ignored(path):
                fresults.append(path)

    for r in results:
        if os.path.isdir(r):
            os.path.walk(r, visit, r)
        else:
            fresults.append(r)

    return fresults


def cmd_edit(args):
    if len(args) < 2:
        results = get_config('edits', [])
        if len(results) >= 1:
            if len(results) == 1:
                ecwd = os.path.split(results[0])[0]
            else:
                ecwd = os.path.commonprefix(results)
                ecwd = os.path.split(ecwd)[0]
            edit(results, cwd=ecwd)
        else:
            print "Please provide a pattern to find files to edit"
            print CMD_HELP["edit"]
    else:
        results = find_paths(args)
        if len(results) >= 1:
            if len(results) == 1:
                ecwd = os.path.split(results[0])[0]
            else:
                ecwd = os.path.commonprefix(results)
                ecwd = os.path.split(ecwd)[0]
            set_config('edits', results)
            edit(results, cwd=ecwd)


def cmd_grep(args):
    if len(args) < 2:
        print "Please provide a grep pattern"
        print CMD_HELP["grep"]
    else:
        opath = odoo_path_or_crash()
        args = args[1:]
        if 'in' in args:
            index = args.index('in')
            pathspec = args[index + 1:]
            args = args[:index]
            pattern = '.*' + '.*'.join(args) + '.*'
            pathspec = '*' + '*'.join(pathspec) + '*'
            results = orexec('git --no-pager grep --no-color --basic-regexp --full-name ' + pattern + ' -- ' + pathspec)
        else:
            pattern = '.*' + '.*'.join(args) + '.*'
            results = orexec('git --no-pager grep -w --no-color --basic-regexp --full-name ' + pattern)

        if not results:
            print "No Results"
            return

        results = results.split('\n')

        files = {}

        for r in results:
            if len(r) > 1024:
                continue
            try:
                sep = r.index(':')
            except:
                continue

            path = r[:sep]
            text = r[sep + 1:]
            if ignored(path):
                continue
            if path not in files:
                files[path] = [text]
            else:
                files[path].append(text)

        select = ""
        count = 0
        for path in files:
            count += 1
            if count > 50:
                select += str(len(files) - 50) + ' MORE FILES ... ' + '\n'
                break
            abspath = os.path.join(opath, path)
            select += "#@[#s#]@#" + abspath + '\n'
            for line in files[path][:8]:
                try:
                    select += line + '\n'
                except:
                    continue
            if len(files[path]) > 8:
                select += '...\n'
            select += '\n'

        process = subprocess.Popen(['iselect', '-m', '-d', '#@[#,#]@#'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        result = process.communicate(input=select)[0][:-1]
        process.wait()

        if not result:
            return
        else:
            result = result.split('\n')
            set_config('edits', result)
        cwd = os.path.commonprefix(result)
        cwd = os.path.split(cwd)[0]
        edit(result, cwd=cwd)


def cmd_fetch(args):
    if len(args) < 2:
        print "Please provide the branch to fetch"
        print CMD_HELP["fetch"]
    else:
        if len(args) == 2:
            branch = args[1]
            if otexec('git rev-parse --verify ' + branch):
                print 'Found local branch', branch
                return [{"repo": "?", "branch": branch}]

        pattern = '.*' + '.*'.join(args[1:]) + '.*'
        pattern = re.compile(pattern)

        branches = orexec("git branch --list --no-color -a")
        if not branches:
            return

        matches = {}
        for branch in branches.split('\n'):
            branch = branch[2:]
            repo, branch = os.path.split(branch)

            if not repo:
                repo = 'local'

            if 'pull/' in repo:
                continue
            elif '/HEAD' in repo:
                continue
            elif not pattern.search(os.path.join(repo, branch)):
                continue

            if 'remotes/' in repo:
                repo = os.path.split(repo)[1]

            if repo not in matches:
                matches[repo] = [branch]
            else:
                matches[repo].append(branch)

        select = ""
        for repo in matches:
            select += repo.upper() + '\n'
            for branch in matches[repo]:
                select += "<s:" + repo + ';' + branch + ">" + branch + '\n'
            select += '\n'

        process = subprocess.Popen(['iselect', '-m'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        result = process.communicate(input=select)[0][:-1]
        process.wait()

        if not result:
            return []
        else:
            result = result.split('\n')

        rvalues = []
        for r in result:
            repo, branch = r.split(';')

            rvalues.append({"repo": repo, "branch": branch})

            if repo == 'local':
                continue

            print "Fetching", branch, "from", repo, "..."
            otexec('git fetch ' + repo + ' ' + branch + ':' + branch)
            otexec('git branch ' + branch)

        return rvalues


def cmd_switch(args):
    if len(args) < 2:
        branches = None
    else:
        branches = cmd_fetch(args)

    if not branches:
        sys.exit("No branch to switch to.")

    opexec('git checkout ' + branches[0]["branch"])


def cmd_config(args):
    if len(args) == 1:
        path = config_file_path()
        if os.path.exists(path):
            edit([path])
        else:
            print "Empty Configuration File"

    elif len(args) == 2:
        print get_config(args[1], "None")
    elif len(args) > 2:
        print "Setting", args[1], "to", ' '.join(args[2:])
        set_config(args[1], ' '.join(args[2:]))


def cmd_todo(args):
    todos = get_config("todo", {})

    def has(thing):
        return thing in todos and len(todos[thing]) > 0

    if len(args) == 1:
        if not has('todo') and not has('done'):
            print "Nothing to do !"
        else:
            print ""
            if has('todo'):
                for i, todo in enumerate(todos['todo']):
                    print RED + "[TODO]" + COLOR_END + " {:>2}: ".format(str(i)) + todo
            if has('todo') and has('done'):
                print BLUE + ' ---- ' + COLOR_END
            if has('done'):
                for i, done in enumerate(todos['done']):
                    print GREEN + "[DONE]" + COLOR_END + " {:>2}: ".format(str(i)) + done
                    if i >= 6:
                        break
            print ""
    elif len(args) > 1:
        task = " ".join(args[1:])
        if 'todo' not in todos:
            todos['todo'] = [task]
        else:
            todos['todo'].insert(0, task)
        set_config("todo", todos)


def cmd_done(args):
    todos = get_config("todo", {})
    if len(args) == 1:
        if 'done' in todos:
            for i, done in enumerate(todos['done']):
                print GREEN + "[DONE]" + COLOR_END + " {:>2}: ".format(str(i)) + done
    else:
        if 'todo' not in todos:
            return
        if 'done' not in todos:
            todos['done'] = []

        for i in args[1:]:
            i = int(i)
            if i < len(todos['todo']):
                todos['done'].insert(0, todos['todo'][i])
                todos['todo'][i] = None

        todos['todo'] = [x for x in todos['todo'] if x is not None]
        set_config("todo", todos)


def cmd_alias(args):
    aliases = get_config('alias', {})
    if args[0] in aliases:
        alias = aliases[args[0]]
        if 'ARGS' in alias:
            index = alias.index('ARGS')
            alias[index:index + 1] = args[1:]
            return alias
        else:
            return aliases[args[0]] + args[1:]
    else:
        return args


def cmd_set_alias(args):
    if len(args) < 3:
        print "Not enough arguments"
        print CMD_HELP["alias"]
    elif args[1] in CMD_HELP:
        print "Aliasing to built-in commands is not allowed"
        print CMD_HELP["alias"]
    else:
        aliases = get_config('alias', {})
        aliases[args[1]] = args[2:]
        set_config('alias', aliases)


def cmd_main(args):
    if len(args) == 0:
        cmd_ook()
        return
    else:
        if os.getuid() != 0:  # cmd_alias will create a config file. if it is launched as root, shit happens.
            args = cmd_alias(args)

    if args[0] in ["help", "--help", "-h"]:
        cmd_help(args)
    if args[0] == "install":
        cmd_install()
    elif args[0] == "status" or args[0] == 'st':
        cmd_status()
    elif args[0] == "check":
        cmd_check(args)
    elif args[0] == "log":
        cmd_log()
    elif args[0] == "git":
        cmd_git(args)
    elif args[0] == "path":
        cmd_path()
    elif args[0] == "find" or args[0] == 'f':
        cmd_find(args)
    elif args[0] == "edit" or args[0] == 'e':
        cmd_edit(args)
    elif args[0] in ["grep", "ack", "g"]:
        cmd_grep(args)
    elif args[0] == "config":
        cmd_config(args)
    elif args[0] == "configpath":
        print config_file_path()
    elif args[0] == "branch":
        cmd_branch()
    elif args[0] == "try" or args[0] == 'test':
        cmd_try(args)
    elif args[0] in ["start", "x", "startall"]:
        cmd_start(args)
    elif args[0] == "dropdb":
        cmd_dropdb()
    elif args[0] == "reset":
        cmd_reset(args)
    elif args[0] == "stop":
        cmd_stop()
    elif args[0] == "fetch":
        cmd_fetch(args)
    elif args[0] in ["switch", "sw", "checkout", "co"]:
        cmd_switch(args)
    elif args[0] == "port":
        cmd_port()
    elif args[0] == "todo":
        cmd_todo(args)
    elif args[0] == "done":
        cmd_done(args)
    elif args[0] == "alias":
        cmd_set_alias(args)
    else:
        print "Unknown command", args[0]
        print "Type 'ook help' to see the available commands"


#   +============================+
#   |           MAIN             |
#   +============================+

def main():
    try:
        cmd_main(sys.argv[1:])
    except KeyboardInterrupt:
        if odoo_server:
            odoo_server.kill()
            odoo_server.kill()
            odoo_server.terminate()
            odoo_server.terminate()  # Beating dead horses ... !
        sys.exit()


if __name__ == "__main__":
    main()

