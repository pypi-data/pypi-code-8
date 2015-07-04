#
# -*- coding: utf-8 -*-

"""
Module sphinxcontrib.unicode_ids
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The Sphinx extension to allow HTML builder to use Non-ASCII identifiers

:copyright: © 2011-2015 Suzumizaki-Kimitaka(鈴見咲 君高, for additional works only)
:license: 2-clause BSD.

This module hacks :meth:`sphinx.environment.BuildEnvironment.resolve_toctree`.
And because of this, when used with Python 2(means not Python 3), just
cover characters included in the set of :code:`sys.getdefaultencoding()`,
not all of Unicode characters.

For Windows, you might create :file:`usercustomize.py` or
:file:`sitecustomize.py` to call :code:`sys.setdefaultencoding('mbcs')`.
See PEP 370 http://www.python.org/dev/peps/pep-0370/ to know where 
to place the script.
"""

#
# the imports below need to define alternate functions. copied from:
# environment.py
#

import os
import sys
from os import path
from docutils import nodes
from sphinx import addnodes
from sphinx.util \
    import url_re, get_matching_docs, docname_join, FilenameUniqDict, patfilter
# ^ Thanks for the information written at http://koyudoon.hatenablog.com/entry/20120126/1327529750

#
# to define new builder.
#
import sphinx.builders.html

#
# to support my_make_id() function
#
import re
import docutils

#
# to define alternate functions.
#
def to_unicode(s):
    """Get unicode object by decoding given string with filesystem encoding
    
    :param str s: the string, if unicode object is given, return this unmodified.
    :rtype: unicode
    :return: the string converted unicode type
    
    When the system encoding is not found, just return the parameter :code:`s`.
    This function is called Python 2 only.
    """
    if isinstance(s, str):
        # NOTE: I don't know how to perform with cygwin.
        if sys.platform == "windows":
            encoding = sys.getdefaultencoding()
        else:
            encoding = sys.getfilesystemencoding()
        if not encoding:
            return s
        return s.decode(encoding, "replace")
    return s

#
# alternate functions.
#

# ====================================================================
# alter 'docutils.nodes.make_id'
# ====================================================================

if len(u'\U0010FFFF') == 1:
    _unusable_characters_for_id = re.compile(u'[^0-9A-Za-z_\\-\u00a0-\U0010FFFF]')
else:
    _unusable_characters_for_id = re.compile(u'[^0-9A-Za-z_\\-\u00a0-\uFFFF]')

_unusable_prefixes = re.compile(u'^([0-9]|--)')

def my_make_id(s):
    """Return identifier without losing Unicode characters.

    :param str_or_unicode s: base string to make new identifier
    :rtype: unicode(Python 2), str(Python 3)
    :return: the new identifier string for patched Sphinx

    Defined to replace the function :meth:`docutils.nodes.make_id`.
    
    Currently, this function can't determine the return value will be used
    in HTML or CSS. Unusable characters will be replaced with :code:`_xhh`
    form where :code:`hh` is 2-digit hexadecimal lowercase.
    """
    if sys.version_info[0] <= 2:
        s = to_unicode(s.lower())
    s = u'-'.join(s.split()) # replace white spaces with hyphens.
    s = _unusable_characters_for_id.sub(lambda mo: u'_x{:02x}'.format(ord(mo.group())), s)
    if _unusable_prefixes.match(s):
        s = u'_' + s
    return s # we need unicode object, NOT str.

# ====================================================================
# alter 'sphinx.directives.other.TocTree.run'
# ====================================================================

from sphinx.util.nodes import explicit_title_re, set_source_info

def my_toctree_run(self):
    """Show non existing entries of toctree
    
    :param sphinx.directives.other.TocTree self: The instance object
    :rtype: list
    :return: list of the nodes made in this method
    
    Defined to replace the method :meth:`sphinx.directives.other.TocTree.run`

    Only :code:`%r` following are replaced with :code:`%s` to avoid unreadable string.
    """
    env = self.state.document.settings.env
    suffixes = env.config.source_suffix
    glob = 'glob' in self.options
    caption = self.options.get('caption')
    if caption:
        self.options.setdefault('name', nodes.fully_normalize_name(caption))

    ret = []
    # (title, ref) pairs, where ref may be a document, or an external link,
    # and title may be None if the document's title is to be used
    entries = []
    includefiles = []
    all_docnames = env.found_docs.copy()
    # don't add the currently visited file in catch-all patterns
    all_docnames.remove(env.docname)
    for entry in self.content:
        if not entry:
            continue
        if glob and ('*' in entry or '?' in entry or '[' in entry):
            patname = docname_join(env.docname, entry)
            docnames = sorted(patfilter(all_docnames, patname))
            for docname in docnames:
                all_docnames.remove(docname)  # don't include it again
                entries.append((None, docname))
                includefiles.append(docname)
            if not docnames:
                ret.append(self.state.document.reporter.warning(
                    'toctree glob pattern %r didn\'t match any documents'
                    % entry, line=self.lineno))
        else:
            # look for explicit titles ("Some Title <document>")
            m = explicit_title_re.match(entry)
            if m:
                ref = m.group(2)
                title = m.group(1)
                docname = ref
            else:
                ref = docname = entry
                title = None
            # remove suffixes (backwards compatibility)
            for suffix in suffixes:
                if docname.endswith(suffix):
                    docname = docname[:-len(suffix)]
                    break
            # absolutize filenames
            docname = docname_join(env.docname, docname)
            if url_re.match(ref) or ref == 'self':
                entries.append((title, ref))
            elif docname not in env.found_docs:
                ret.append(self.state.document.reporter.warning(
                    u'toctree contains reference to nonexisting '
                    u'document %s' % docname, line=self.lineno))
                env.note_reread()
            else:
                all_docnames.discard(docname)
                entries.append((title, docname))
                includefiles.append(docname)
    subnode = addnodes.toctree()
    subnode['parent'] = env.docname
    # entries contains all entries (self references, external links etc.)
    subnode['entries'] = entries
    # includefiles only entries that are documents
    subnode['includefiles'] = includefiles
    subnode['maxdepth'] = self.options.get('maxdepth', -1)
    subnode['caption'] = caption
    subnode['glob'] = glob
    subnode['hidden'] = 'hidden' in self.options
    subnode['includehidden'] = 'includehidden' in self.options
    subnode['numbered'] = self.options.get('numbered', 0)
    subnode['titlesonly'] = 'titlesonly' in self.options
    set_source_info(self, subnode)
    wrappernode = nodes.compound(classes=['toctree-wrapper'])
    wrappernode.append(subnode)
    self.add_name(wrappernode)
    ret.append(wrappernode)
    return ret

def setup(app):
    """Extend the Sphinx as we want, called from the Sphinx

    :param sphinx.application.Sphinx app: the object to add builder or something.
    """

    #
    # reset dirs to unicode, otherwise several 'replace(SEP, os.sep)'
    # codes make bad string with MBCS.  
    #
    if sys.version_info[0] <= 2:
        app.srcdir = to_unicode(app.srcdir)
        app.confdir = to_unicode(app.confdir)
        app.outdir = to_unicode(app.outdir)
        app.doctreedir = to_unicode(app.doctreedir)

    #
    # The original make_id() targets HTML 4.01 and CSS1,
    # we need replace the function to use unicode directly in identifier.
    # (when the function returns empty string, :meth:`docutils.nodes.document.set_id()`
    #  makes 'id1' or so.)
    #
    docutils.nodes.make_id = my_make_id

    #
    # The function forces unicode to str with '%r', so we need replace.
    #
    sphinx.directives.other.TocTree.run = my_toctree_run
    return {'version': '2.0.5', 'parallel_read_safe': False}
