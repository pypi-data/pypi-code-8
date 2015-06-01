# -*- coding: utf-8 -*-
"""
jinja2rst – A Simple Tool for Documenting Jinja2 Template-Files
"""
#
# Copyright 2015 by Hartmut Goebel <h.goebel@crazy-compilers.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import print_function

import re

__author__ = "Hartmut Goebel <h.goebel@crazy-compilers.com>"
__copyright__ = "Copyright 2015 by Hartmut Goebel <h.goebel@crazy-compilers.com>"
__licence__ = "GNU General Public License version 3 (GPL v3)"
__version__ = "0.1"

STATE_TEXT = 0
STATE_JINJA = 1


def setup_patterns():

    # Create rst patterns, copied from `docutils/parsers/rst/states.py`
    # Function has been placed in the public domain.

    class Struct:
        """Stores data attributes for dotted-attribute access."""
        def __init__(self, **keywordargs):
            self.__dict__.update(keywordargs)

    enum = Struct()
    enum.formatinfo = {
          'parens': Struct(prefix='(', suffix=')', start=1, end=-1),
          'rparen': Struct(prefix='', suffix=')', start=0, end=-1),
          'period': Struct(prefix='', suffix='.', start=0, end=-1)}
    enum.formats = enum.formatinfo.keys()
    enum.sequences = ['arabic', 'loweralpha', 'upperalpha',
                      'lowerroman', 'upperroman'] # ORDERED!
    enum.sequencepats = {'arabic': '[0-9]+',
                         'loweralpha': '[a-z]',
                         'upperalpha': '[A-Z]',
                         'lowerroman': '[ivxlcdm]+',
                         'upperroman': '[IVXLCDM]+',}

    pats = {}
    pats['nonalphanum7bit'] = '[!-/:-@[-`{-~]'
    pats['alpha'] = '[a-zA-Z]'
    pats['alphanum'] = '[a-zA-Z0-9]'
    pats['alphanumplus'] = '[a-zA-Z0-9_-]'
    pats['enum'] = ('(%(arabic)s|%(loweralpha)s|%(upperalpha)s|%(lowerroman)s'
                    '|%(upperroman)s|#)' % enum.sequencepats)

    for format in enum.formats:
        pats[format] = '(?P<%s>%s%s%s)' % (
              format, re.escape(enum.formatinfo[format].prefix),
              pats['enum'], re.escape(enum.formatinfo[format].suffix))

    patterns = {
          'bullet': u'[-+*\u2022\u2023\u2043]( +|$)',
          'enumerator': r'(%(parens)s|%(rparen)s|%(period)s)( +|$)' % pats,
          }
    for name, pat in patterns.items():
        patterns[name] = re.compile(pat)
    return patterns


PATTERNS = setup_patterns()

def get_indent(line):
    stripped_line = line.lstrip()
    indent = len(line) - len(stripped_line)
    if (PATTERNS['bullet'].match(stripped_line) or
        PATTERNS['enumerator'].match(stripped_line)):
        indent += len(stripped_line.split(None, 1)[0])+1
    return indent

HASH_STATE_UNKNOWN = 0
HASH_STATE_TRUE = 1
HASH_STATE_FALSE = -1

def convert(lines):
    state = STATE_JINJA
    last_text_line = last_code_line = ''
    last_indent = ''
    has_hash_prefix = HASH_STATE_UNKNOWN
    for line in lines:
        line = line.rstrip()
        if state == STATE_JINJA:
            if line.startswith('{#'):
                # start of comment / documentation
                if last_code_line != '':
                    yield ''  # end code block
                last_code_line = last_text_line = ''
                if line.endswith('#}'):
                    # need to handle jinja2-special characters
                    s = e = 3
                    if line[2] == '-': s = 4
                    if line[-2] == '-': e = 4
                    line = line[s:-e].rstrip()
                    yield line
                    # simulate end of text block
                    if line:
                        yield ''
                    # do not change the state!
                    last_text_line = line
                    last_indent = get_indent(line)* ' '
                else:
                    # :todo: verify line is empty
                    state = STATE_TEXT
                    has_hash_prefix = HASH_STATE_UNKNOWN
            else:
                # code line
                if not last_text_line.endswith('::'):
                    # no code-block starter yet
                    yield last_indent + '::'
                    yield ''
                    # avoid taking this branch a second time
                    last_text_line = '::'
                if line:
                    yield last_indent + '  ' + line
                else:
                    yield ''
                last_code_line = line

        else:
            # state = STATE_TEXT
            assert last_code_line == ''
            if line.endswith('#}'):
                # end of text block
                yield ''
                state = STATE_JINJA
            else:
                if has_hash_prefix == HASH_STATE_UNKNOWN:
                    # first text-line, check for hash prefix
                    if line.startswith('# '):
                        has_hash_prefix = HASH_STATE_TRUE
                    else:
                        has_hash_prefix = HASH_STATE_FALSE
                if has_hash_prefix == HASH_STATE_TRUE:
                    # todo: verify line starts with `# `
                    line = line[2:]
                yield line
                last_text_line = line
                last_indent = get_indent(line)* ' '


def convert_text(jinja_text):
    return '\n'.join(convert(jinja_text.splitlines()))
    

def convert_file(infilename, outfilename):
    with open(infilename) as infh:
        with open(outfilename, "w") as outfh:
            for l in convert(infh.readlines()):
                print(l.rstrip(), file=outfh)
