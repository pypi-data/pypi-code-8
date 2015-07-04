u"""Terminal client for paperwork.py"""

from __future__ import with_statement
from __future__ import absolute_import
from . import models
from .utils import fuzzy_find
import os
import sys
import logging
import argparse
import tempfile
from io import open

if unicode(sys.version[0]) < u'3':
    input = raw_input

LOGGER = logging.getLogger(__name__)

PW = models.Paperwork(raw_input(u'Host: '))
if not PW.authenticated:
    print u'User/password not valid or host not reachable.'
    sys.exit()

SEP_NOTE_ATTACH = u' to '
SEP_NOTE_NB = u' in '


def download():
    u"""Fills Paperwork instance with information from server."""
    PW.download()


def update():
    u"""Synchronizes local and remote information."""
    PW.update()


def print_all():
    u"""Prints notebook and notes in alphabetical order."""
    for notebook in PW.get_notebooks():
        print notebook.title
        for note in notebook.get_notes():
            print u"- {}".format(note.title)
            for attachment in note.attachments:
                print u"-- {}".format(attachment.title)


def split(args, splitter):
    u"""Splits string with splitter and returns the resulting strings,

    if the splitter is in the string. If not None and the string is returned.
    :type args: str
    :type splitter: str
    :rtype: list or None and str
    """
    if splitter in args:
        return args.split(splitter, 1)
    else:
        return None, args


def split_args(args):
    u"""Splits sring into attachment, note and notebook string.

    :type args: str
    :rtype: list
    """
    attachment, args = split(args, SEP_NOTE_ATTACH)
    note, notebook = split(args, SEP_NOTE_NB)
    return attachment, note, notebook


def split_and_search_args(args):
    u"""Parses attachment, note and notebook.

    Returns a list of three items with [attachment, note, notebook]
    :type args: str
    :param bool search: If true the method searches for objects and
        returns them instead of strings.
    :rtype: list
    """
    attachment, note, notebook = split_args(args)
    notebook = fuzzy_find(notebook, PW.notebooks)
    if note:
        note = fuzzy_find(note, notebook.notes)
    if attachment:
        attachment = fuzzy_find(attachment, note.attachments)
    return attachment, note, notebook


def prompt(text, important=False):
    u"""Prompts user for confirmation.

    :type text: str
    :param bool important: If true the default answer is false.
    :rtype: bool
    """
    answers = (u'y', u'Y', u'yes', u'Yes', u'YES')
    text += u' y/N' if important else u' Y/n'
    if not important:
        answers += (u'',)
    answer = raw_input(text + u' ')
    if answer in answers:
        return True
    return False


def edit(title):
    u"""Edit note with title.

    :type title: str
    """
    note = split_and_search_args(title)[1]
    LOGGER.info(u'Getting $EDITOR')
    editor = os.environ.get(u'EDITOR')

    tmpfile = tempfile.NamedTemporaryFile()

    LOGGER.info(u'Writing content to temporary file')
    with open(tmpfile, u'w') as f:
        f.write(note.content)

    LOGGER.info(u'Launching system editor')
    os.system(u"{} '{}'".format(editor, tmpfile.name))

    LOGGER.info(u'Reading contents of temporary file')
    with open(tmpfile, u'r') as f:
        note.content = f.read()

    LOGGER.info(u'Removing temporary file')
    tmpfile.close()

    LOGGER.info(u'Updating remote note')
    note.update()


def delete(args):
    u"""Delete note, notebook or attachment, depending on input.

    :type args: str
    """
    attachment, note, notebook = split_and_search_args(args)
    if attachment:
        if prompt(u'Delete attachment {} to {} in {}?'.format(
                attachment.title, note.title, notebook.title)):
            attachment.delete()
    elif note:
        if prompt(u'Delete note {} in {}?'.format(
                note.title, notebook.title)):
            note.delete()
    else:
        if prompt(u'Delete notebook {}?'.format(notebook.title)):
            PW.delete_notebook(notebook)


def move(args):
    u"""Move a note to another notebook.

    :type args: str
    """
    # splits off the new notebook at the end first, so it
    # doesn't mess with the split_args function
    args, notebook = split(args, u' to ')
    notebook = fuzzy_find(notebook, PW.notebooks)
    note = split_and_search_args(args)[1]
    if prompt(u'Move note {} to {}?'.format(note.title, notebook.title)):
        note.move_to(notebook)


def create(args):
    u"""Creates note or notebook, depending on input.

    :type args: str
    """
    if SEP_NOTE_NB in args:
        note, notebook = split_args(args)[1:]
        notebook = fuzzy_find(notebook, PW.notebooks)
        if prompt(u'Create note {} in {}?'.format(note, notebook.title)):
            notebook.create_note(note)
    else:
        if prompt(u'Create notebook {}?'.format(args)):
            PW.create_notebook(args)


def tags():
    u"""Lists tags."""
    for tag in PW.get_tags():
        print tag.title


def tag(args):
    u"""Create a tag or tag a note with a tag, depending on input.

    :type args: str
    """
    if u' with ' in args:
        # Again, split tag before
        args, tag = split(args, u' with ')
        tag = fuzzy_find(tag, PW.tags)
        note = split_and_search_args(args)[1]
        if prompt(u'Tag note {} with {}?'.format(note.title, tag.title)):
            note.add_tags([tag])
    else:
        if prompt(u'Create tag {}?'.format(args)):
            PW.add_tag(args)


def tagged(tag_title):
    u"""Print notes tagged with tag.

    :type tag_title: str
    """
    tag = fuzzy_find(tag_title, PW.tags)
    print u'Notes tagged with {}'.format(tag.title)
    for note in tag.notes:
        print note.title


def upload(args):
    u"""Uploads a file as attacment to a note.

    :type args: str
    """
    filepath, note, notebook = split_args(args)
    notebook = fuzzy_find(notebook, PW.notebooks)
    note = fuzzy_find(note, notebook.notes)
    note.upload_file(filepath)


def print_help():
    u"""Prints commands and their usage to terminal."""
    print u"""The commands are self-explanatory.
Notes, tags and notebooksare chosen through a fuzzy search.

update                                      Pushes local changes to the remote host
ls                                          List notebooks and notes
edit $note                                  edit note
delete $notebook                            delete notebook
delete $note in $notebook                   delete note in notebook
delete $attachment to $note in $notebook    Delete attachment to note in notebook
upload $filepath to $note in $notebook      Upload file at $filepath as attachment to note in notebook
move $note to $notebook                     move note to notebook
create $note in $notebook                   create note in notebook
create $notebook                            create notebook
tags                                        list tags
tag $note with $tag                         tag note with tag
tag $tag                                    create $tag
tagged $tag                                 print notes tagged with $tag
exit                                        exit application
"""


CMD_DICT = {
    u'update': update,
    u'ls': print_all,
    u'edit': edit,
    u'delete': delete,
    u'move': move,
    u'create': create,
    u'tags': tags,
    u'tag': tag,
    u'tagged': tagged,
    u'help': print_help,
    u'upload': upload
    }


def main():
    u"""Main function for terminal client.

    Awaits user input and executes the functions.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        u"-v", u"--verbose", help=u"verbose output", action=u"store_true")
    parser.add_argument(
        u"--threading", help=u"enable multi-threading", action=u"store_true")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.threading:
        models.use_threading = True

    download()

    cmd = raw_input(u'>')
    while cmd != u'exit':
        LOGGER.info(cmd)
        cmd, args = split(cmd, u' ')
        if cmd and cmd in CMD_DICT:
            CMD_DICT[cmd](args)
        elif args in CMD_DICT:
            CMD_DICT[args]()
        else:
            LOGGER.info(u'Invalid command')
            print u'{} {} unknown'.format(cmd, args)
        cmd = raw_input(u'>')

if __name__ == u"__main__":
    main()
