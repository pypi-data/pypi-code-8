#!/usr/bin/env python
# -*- coding: utf-8 -*-

import appdirs
import os
import os.path
import sys
import json
import subprocess
import shutil
import socket
import re


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
    return subprocess.check_output(cmd.split())[:-1]


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
    process = subprocess.Popen(['less'], stdin=subprocess.PIPE)
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
    subprocess.Popen(editor.split() + files, cwd=cwd).wait()


def branch_to_db(branch):
    return branch[:20]


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
   help [CMD]
       prints this help, or the help of the
       provided command.
    """,
    "start": """
   start [args]
       [Re]start the Odoo server on port 8069
       with a db named with the current git
       branch. It will create a database
       with demo data if it doesn't exist.

       [args] will be passed to the odoo
       server command line.

       Ex: ook start -i stock
       -> Start odoo and install the stock
          module
    """,
    "reset": """
   reset [args]
       Restart the server with a new database

       [args] will be passed to the odoo
       server command line at restart.
    """,
    "stop": """
   stop
       Stops the current server.
    """,
    "log": """
   log
       Prints the last 20 commits in a readable
       format.
    """,
    "find": """
   find PATTERN
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
    """,
    "edit": """
   edit PATTERN
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
    """,
    "grep": """
   grep PATTERN [in FINDPATTERN]
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
    """,
    "try": """
   try BRANCH [args]
       Launches a Odoo server with the code found
       in the branch BRANCH, without changing the
       current branch of the repository.

       Odoo servers launched with 'try' are not
       affected by the start / stop / reset commands

       The databases created by try are recycled after
       a while

       [args] will be passed to the odoo
       server command line at restart.

       Ex: ook try 8.0-fixes-mat -i website
       -> Create an instance for the 8.0-fixes-mat
          branch and install the website module

       If no branch is specified, it will try the
       last fetched branch.

       Ex: ook fetch fix mat
           ook try -i website
       -> Tries the branch selected in the fetch.
    """,
    "path": """
   path
       Prints the path to the odoo server directory
    """,
    "fetch": """
   fetch BRANCH_PATTERN
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
   switch BRANCH_PATTERN
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
    """,
    "branch": """
   branch
       Prints the current branch of the odoo repository
    """,
    "git": """
   git [git command]
       Executes the git command in the odoo repository.
       Ex: cd /var/log; ook git status
       -> Prints git's status.
    """,
    "config": """
   config [key] [value]
       Prints the content of the Ook config file.

       [key] Prints the value associated with key
       in the Ook config file.

       [key] [value]
       Sets the Ook config option 'key' to 'value'
    """,
    "alias": """
   alias ALIAS CMD:
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
   todo [TASK]:
       Add the string TASK at the top of the todolist.

       Ex: ook todo save the world.

       If no TASK is specified, print the todolist.

       Ex: ook todo
       ->  [TODO]  0: save the world.
           [TODO]  1: pump up the jam.

       See 'ook help done' for marking tasks as done.
    """,

    "done": """
   done [TASK_IDS]:
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


HELP = "\n".join([
    "Usage: ook [COMMAND]",
    "".join(CMD_HELP.values()),
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
        print CMD_HELP[args[1]]
    else:
        print "Unknown command", args[1]
        print "Type 'ook help' to see the command list"


def cmd_log():
    opexec("git log --oneline -n 20")


def cmd_port():
    print find_port()


def cmd_branch():
    print '"' + odoo_branch() + '"'


def cmd_git(args):
    opexec(" ".join(args))


def cmd_ook():
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


def cmd_stop():
    pid = get_config("server_pid")
    if pid and pid > 0:
        pexec("pkill -TERM -P " + str(pid))
        set_config("server_pid", -1)


def cmd_dropdb():
    branch = odoo_branch()
    cmd_stop()
    pexec('dropdb ' + branch)


def cmd_start(args):
    path = odoo_path_or_crash()
    opath = path + "/odoo.py"
    branch = odoo_branch()

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

    set_config("server_pid", os.getpid())

    cmd = opath + " start -d " + branch + " " + " ".join(args)

    return subprocess.Popen(cmd.split(), cwd=path).wait()


def tmp_export(branch):
    path = odoo_path_or_crash()

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

    if len(trials) > 3:
        print "Cleaning up old exports... "
        for trial in trials[:-3]:
            if os.path.exists(trial['path']):
                shutil.rmtree(trial['path'])
            pexec('dropdb ' + trial['db'])
        trials = trials[-3:]

    set_config('tmps', trials)

    if os.path.exists(try_path):
        shutil.rmtree(try_path)
    os.makedirs(try_path)

    print "Exporting branch", branch, "to /tmp ..."
    os.system("cd " + path + "; git archive " + branch + " | tar -x -C " + try_path)


def cmd_try(args):
    path = odoo_path_or_crash()
    print args
    if len(args) < 2 or args[1][0] == '-':
        branches = get_config('fetched', False)
        oargs = args[1:]
    else:
        branches = cmd_fetch(['fetch', args[1]])
        oargs = args[2:]

    if not branches:
        sys.exit("No branch to try. Provide a branch or do a 'ook fetch'")

    branch = branches[0]["branch"]

    try_path = '/tmp/' + branch
    try_db = "try-" + branch
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

    cmd = opath + " start -d " + try_db + " --xmlrpc-port=" + port + " " + " ".join(oargs)

    return subprocess.Popen(cmd.split(), cwd=path).wait()


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
        path = odoo_path_or_crash()
        args = args[1:]
        if len(args) == 1:
            results = rexec('find ' + path + ' -iname ' + '*' + args[0] + '*')
        else:
            pattern = '*' + "*".join(args) + '*'
            results = rexec('find ' + path + ' -iwholename ' + pattern)

        results = iselect(results.split())
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
            pathspec = args[index+1:]
            args = args[:index]
            pattern = '.*' + '.*'.join(args) + '.*'
            pathspec = '*' + '*'.join(pathspec) + '*'
            results = orexec('git grep --no-color --basic-regexp --full-name ' + pattern + ' -- ' + pathspec)
        else:
            pattern = '.*' + '.*'.join(args) + '.*'
            results = orexec('git grep -w --no-color --basic-regexp --full-name ' + pattern)

        if not results:
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
            text = r[sep+1:]
            if path not in files:
                files[path] = [text]
            else:
                files[path].append(text)

        select = ""
        for path in files:
            abspath = os.path.join(opath, path)
            select += "<s>" + abspath + '\n'
            for line in files[path][:20]:
                try:
                    select += line + '\n'
                except:
                    continue
            if len(files[path]) > 20:
                select += '...\n'
            select += '\n'

        process = subprocess.Popen(['iselect', '-m'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
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

            if repo == 'local':
                continue

            print "Fetching", branch, "from", repo, "..."
            otexec('git fetch ' + repo + ' ' + branch + ':' + branch)
            otexec('git branch ' + branch)
            rvalues.append({"repo": repo, "branch": branch})

        set_config('fetched', rvalues)

        return rvalues


def cmd_switch(args):
    if len(args) < 2:
        branches = get_config('fetched', False)
    else:
        branches = cmd_fetch(args)

    if not branches:
        sys.exit("No branch to switch to. Please provide one, or use 'ook fetch'")

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

    if len(args) == 1:
        if 'todo' not in todos and 'done' not in todos:
            print "Nothing to do !"
        else:
            if 'todo' in todos:
                for i, todo in enumerate(todos['todo']):
                    print RED + "[TODO]" + COLOR_END + " {:>2}: ".format(str(i)) + todo
            if 'todo' in todos and 'done' in todos:
                print BLUE + ' ---- ' + COLOR_END
            if 'done' in todos:
                for i, done in enumerate(todos['done']):
                    print GREEN + "[DONE]" + COLOR_END + " {:>2}: ".format(str(i)) + done
                    if i >= 6:
                        break
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
            alias[index:index+1] = args[1:]
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
        args = cmd_alias(args)

    if args[0] == "help":
        cmd_help(args)
    elif args[0] == "log":
        cmd_log()
    elif args[0] == "git":
        cmd_git(args)
    elif args[0] == "path":
        cmd_path()
    elif args[0] == "test":
        print rexec("git rev-parse --abbrev-ref HEAD")
    elif args[0] == "find":
        cmd_find(args)
    elif args[0] == "edit":
        cmd_edit(args)
    elif args[0] == "grep":
        cmd_grep(args)
    elif args[0] == "config":
        cmd_config(args)
    elif args[0] == "branch":
        cmd_branch()
    elif args[0] == "try":
        cmd_try(args)
    elif args[0] == "start":
        cmd_start(args)
    elif args[0] == "dropdb":
        cmd_reset(args)
    elif args[0] == "reset":
        cmd_reset(args)
    elif args[0] == "stop":
        cmd_stop()
    elif args[0] == "fetch":
        cmd_fetch(args)
    elif args[0] == "switch":
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
    cmd_main(sys.argv[1:])


if __name__ == "__main__":
    main()

