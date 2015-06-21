#!/usr/bin/env python3

"""\
Format and print wetlab protocols stored as text files in git repositories.

Usage:
    wet_copy [options] <protocols>...

Arguments:
    <protocols>...
        The path to one or more protocols to print.  You can specify python 
        scripts (with arguments) as protocols by providing a space-separated 
        command line like so: wet_copy 'pcr.py 59 35'

Options:
    -d, --dry-run
        Print the formatted protocol, but don't send it to the printer.

Printed out protocols are nice because they can be easily carried around lab 
during an experiment, annotated in real time, and ultimately taped into a lab 
notebook.  Digital protocols stored as text files in git repositories are nice 
as well, because they can be updated and modified without losing any 
information.  This script helps manage the process of printing out and keeping 
track of digital protocols.

To use this program, start by the adding protocols you use to a git repository.  
Then use the wet_copy command to print out copies of your protocols formatted 
with all the information needed to recover the original digital protocol (e.g. 
a repository URL and a commit hash), enough space to make annotations in the 
margins, and lines showing where to cut so the protocol can be taped into a lab 
notebook.  The wet_copy command won't let you print protocols that have any 
lines wider than 53 characters (otherwise the margin will be too small) or that 
have any uncommitted changes (otherwise the original protocol won't be 
recoverable.)
"""

import os
import subprocess
import shlex
import docopt

page_width = 68
page_height = 50
content_width = 53
content_height = 48
margin_width = 78 - page_width

def main():
    args = docopt.docopt(__doc__)
    protocols = [format_protocol(x) for x in args['<protocols>']]
    print_protocols(protocols, dry_run=args['--dry-run'])

def run_command(command, cwd=None, error=None):
    if isinstance(command, str):
        command = shlex.split(command)
    try:
        return subprocess.check_output(command, cwd=cwd).strip().decode()
    except subprocess.CalledProcessError:
        if error is None:
            raise
        elif error == 'ok':
            pass
        else:
            print('Error: ' + error)

def format_protocol(protocol_path):
    """
    Read the given file and convert it into a nicely formatted protocol by 
    adding margins and a header.
    """

    protocol_path, *arguments = protocol_path.split()

    if not os.path.exists(protocol_path):
        print("Error: Protocol '{}' doesn't exist.".format(protocol_path))
        raise SystemExit

    # Figure out what commit is currently checked out and add that information 
    # to the top of the protocol.  Complain if there are any uncommitted 
    # changes.

    git_dir = run_command(
            'git rev-parse --show-toplevel',
            cwd=os.path.dirname(os.path.abspath(protocol_path)),
            error="'{}' not in a git repository.".format(protocol_path))

    protocol_relpath = os.path.relpath(protocol_path, git_dir)

    git_commit = run_command(
            'git log -n 1 --pretty=format:%H -- \'{}\''.format(protocol_relpath),
            cwd=git_dir,
            error="No commits found.")
    git_stale = protocol_relpath in run_command(
            'git ls-files --modified --deleted --others',
            cwd=git_dir)
    git_repo = run_command(
            'git config --get remote.origin.url',
            cwd=git_dir,
            error='ok') or git_dir

    if git_stale:
        print("Error: '{}' has uncommitted changes.".format(protocol_path))
        print()
        subprocess.call(shlex.split('git status'), cwd=git_dir)
        raise SystemExit

    # Create a header containing information about where the digital form of 
    # this protocol can be found.
    
    protocol = [ # (no fold)
            'file: {}'.format(protocol_relpath)[:page_width],
            'repo: {}'.format(git_repo)[:page_width],
            'commit: {}'.format(git_commit),
            '',
    ]

    # If the given path refers to a python script, run that script to get the 
    # protocol.  Otherwise just read the file.

    if protocol_path.endswith('.py'):
        stdout = subprocess.check_output([protocol_path] + arguments)
        lines = stdout.decode().split('\n')
    else:
        if arguments:
            print("Error: Specified arugments to non-script protocol '{}'.".format(protocol_path))
            raise SystemExit
        with open(protocol_path) as file:
            lines = file.readlines()

    # Make sure none of the lines are too long to fit in the notebook.

    for lineno, line in enumerate(lines, 1):
        line = line.rstrip()
        if line.startswith('vim:'):
            continue
        if len(line) > content_width:
            print("Error: line {} is more than {} characters long.".format(
                lineno, content_width))
            raise SystemExit
        protocol.append(line)

    # Remove trailing blank lines.

    while not protocol[-1].strip():
        protocol.pop()

    # Add a margin on the left, so that the pages can be stapled together 
    # naturally.

    left_margin = ' ' * margin_width + '│ '
    return '\n'.join(left_margin + line for line in protocol)

def print_protocols(protocols, dry_run=False):
    """
    Print out the given protocols.

    If more than one protocol is sent to the printer, each protocol will be 
    printed on its own page.  It's also possible for a single protocol to span 
    multiple pages.  If dry_run=True, the protocols will be simply printed to 
    the terminal instead of being sent to the printer.
    """

    if dry_run:
        if len(protocols) > 1:
            for protocol in protocols:
                print(' ' * margin_width + '┌' + '─' * (page_width + 1))
                print(protocol)
                print(' ' * margin_width + '└' + '─' * (page_width + 1))
        else:
            print(protocols[0])
    else:
        from subprocess import Popen, PIPE
        form_feed = ''
        lpr = Popen(shlex.split('lpr -o sides=one-sided'), stdin=PIPE)
        lpr.communicate(input=form_feed.join(protocols).encode())


if __name__ == '__main__':
    main()



