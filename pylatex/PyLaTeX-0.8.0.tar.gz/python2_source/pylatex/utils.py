# -*- coding: utf-8 -*-
u"""
    pylatex.utils
    ~~~~~~~

    This module implements some simple functions with all kinds of
    functionality.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from __future__ import absolute_import
import os.path
import shutil
import tempfile


_latex_special_chars = {
    u'&':  ur'\&',
    u'%':  ur'\%',
    u'$':  ur'\$',
    u'#':  ur'\#',
    u'_':  ur'\_',
    u'{':  ur'\{',
    u'}':  ur'\}',
    u'~':  ur'\textasciitilde{}',
    u'^':  ur'\^{}',
    u'\\': ur'\textbackslash{}',
    u'\n': ur'\\',
    u'-':  ur'{-}',
    u'\xA0': u'~',  # Non-breaking space
}

_tmp_path = os.path.abspath(
    os.path.join(
        tempfile.gettempdir(),
        u"pylatex"
    )
)


def escape_latex(s):
    u"""Escape characters that are special in latex.

    Sources:
        * http://tex.stackexchange.com/a/34586/43228
        * http://stackoverflow.com/a/16264094/2570866

        :param s:

        :type s: str

        :return:
        :rtype: str
    """

    return u''.join(_latex_special_chars.get(c, c) for c in s)


def fix_filename(path):
    u"""Latex has problems if there are one or more points in the filename,
    thus 'abc.def.jpg' will be changed to '{abc.def}.jpg

        :param filename:

        :type filename: str

        :return:
        :rtype: str
    """

    path_parts = path.split(u'/')
    dir_parts = path_parts[:-1]

    filename = path_parts[-1]
    file_parts = filename.split(u'.')

    if len(file_parts) > 2:
        filename = u'{' + u'.'.join(file_parts[0:-1]) + u'}.' + file_parts[-1]

    dir_parts.append(filename)
    return u'/'.join(dir_parts)


def dumps_list(l, escape=False, token=u'\n'):
    u"""Dumps a list that can contain anything.

        :param l:
        :param escape:
        :param token:

        :type l: list
        :type escape: bool
        :type token: str

        :return:
        :rtype: str
    """

    return token.join(_latex_item_to_string(i, escape) for i in l)


def _latex_item_to_string(i, escape=False):
    u"""Uses the render method when possible, otherwise uses str.

        :param i:
        :param escape:

        :type i: object
        :type escape: bool

        :return:
        :rtype: str
    """

    if hasattr(i, u'dumps'):
        return i.dumps()
    elif escape:
        return unicode(escape_latex(i))

    return unicode(i)


def bold(s):
    u"""Returns the string bold.

    Source: http://stackoverflow.com/a/16264094/2570866

        :param s:

        :type s: str

        :return:
        :rtype: str
    """

    return ur'\textbf{' + s + u'}'


def italic(s):
    u"""Returns the string italicized.

    Source: http://stackoverflow.com/a/16264094/2570866

        :param s:

        :type s: str

        :return:
        :rtype: str
    """

    return ur'\textit{' + s + u'}'


def verbatim(s, delimiter=u'|'):
    u"""Returns the string verbatim.

        :param s:
        :param delimiter:

        :type s: str
        :type delimiter: str

        :return:
        :rtype: str
    """

    return ur'\verb' + delimiter + s + delimiter


def make_temp_dir():
    u"""Creates the tmp directory if it doesn't exist."""

    if not os.path.exists(_tmp_path):
        os.makedirs(_tmp_path)
    return _tmp_path


def rm_temp_dir():
    u"""Removes the tmp directory."""

    if os.path.exists(_tmp_path):
        shutil.rmtree(_tmp_path)
