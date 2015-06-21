#!/usr/bin/env python

# Git pre-commit hook that enforces code consistency in a team environment.
#
# Based on Bob Gilmore's <https://github.com/bobgilmore/githooks> work
# under the MIT License.
#
# Arthur Burkart (artburkart@gmail.com)
from codecs import open
from lib.checker_results import CheckerResults
from lib.checker import Checker
import os
import re
import shutil
from subprocess import check_output, CalledProcessError
import sys
import toml

res = CheckerResults()

# Regex matches the file path and the file's associated diff from git diff
filepath_regex = r"\+\+\+ b\/(.*)\n@@.*"
changes_regex = r"([\s\S]*?)(?:diff|$)"
REGEXP = "{}{}".format(filepath_regex, changes_regex)


def findfile(name, cwd, results):
    """findfile autodiscovers files by name that can be
    located in the current working dir or a parent dir"""
    cwd = os.path.abspath(cwd or os.getcwd())
    filename = "{}/{}".format(os.path.abspath(cwd), name)
    if results.get(filename):
        return results.get(filename)
    if os.path.isfile(filename):
        results[filename] = filename
        return filename
    parent = os.path.abspath("{}/..".format(cwd))
    if cwd in ["/", "//"]:
        results[filename] = None
        return None
    return findfile(name, parent, results)


def morph_opts(iteritem):
    name, opts = iteritem
    opts["key"] = name
    return opts


# http://stackoverflow.com/questions/12791997/how-do-you-do-a-simple-chmod-x-from-within-python/30463972#30463972
def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0444) >> 2
    os.chmod(path, mode)


def install(top_lvl, file_or_dir):
    file_or_dir = top_lvl + file_or_dir
    oldhook = file_or_dir + "Old"

    # Technically, the pythonic way would be for me
    # to make a whole bunch of exceptions here, but
    # I also want my code to be legible, so I didnt'
    if os.path.isfile(oldhook):
        os.remove(file_or_dir + "Old")
    elif os.path.isdir(oldhook):
        shutil.rmtree(file_or_dir + "Old")

    # If the file or directory exists, then make a backup
    if os.path.isfile(file_or_dir) or os.path.isdir(file_or_dir):
        shutil.move(file_or_dir, file_or_dir + "Old")

    # Create a new hooks folder
    os.makedirs(file_or_dir)

    # Create new pre-commit file
    newfile = file_or_dir + "/pre-commit"
    with open(newfile, mode="w+", encoding="utf-8") as pre_commit:
        pre_commit.write("#!/usr/bin/env bash\nexec gitpatrol\n")

    make_executable(newfile)
    print "Install successful."
    exit(0)


def main():
    # Directory where repo's .git folder lives
    try:
        top_lvl = check_output("git rev-parse --show-toplevel".split()).strip()
    except CalledProcessError:
        exit(1)

    # If we're installing, then do the installation magic
    if (len(sys.argv) == 2 and sys.argv[1] == 'install'):
        install(top_lvl, "/.git/hooks")

    # If there are no changes to any of the files, then there is no
    # reason to run gitpatrol
    full_diff = check_output("git diff --cached --".split()).strip()
    if (len(full_diff) == 0):
        print "No files have changed."
        exit(1)

    # Path to gitpatrol.toml file
    confpath = findfile("gitpatrol.toml", top_lvl, {})

    config = {}
    if confpath:
        with open(confpath) as conffile:
            config = toml.loads(conffile.read())

    # Build opts from the gitpatrol.toml
    optslist = map(morph_opts, config.get("checkers", {}).iteritems())

    # Iterate through all diffs
    diff_list = re.findall(REGEXP, full_diff)
    for (filepath, diff) in diff_list:
        # TODO(arthurb): If possible, pull out the line number
        # Get the bit that changed
        changed = "\n".join(
            (ln[1:] for ln in diff.split("\n") if ln.startswith("+")))

        # Update all options and then record a checker of each set of options
        for opts in optslist:
            opts.update({
                "filepath": filepath,
                "changes": changed,
                "directory": os.path.dirname(filepath)
            })
            res.record(Checker(opts))

    if res.has_errors or res.disabled:
        print res
        sys.exit(1)
    sys.exit(0)
