#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 CloudRunner.IO
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 or earlier, use backport
    from ordereddict import OrderedDict
import logging
import os
import re

LANG_BASH = "bash"
LANG_PS = "ps"

CRN_SHEBANG = re.compile("^#!\s*([\/\w]*cloudrunner)\s*(.*)", re.M)
SECTION_SPLIT = re.compile("(^#!\s*switch\s*\[.*\].*)", re.M)
SELECTOR = re.compile('(?P<selector>^#!\s*switch\s*'
                      '\[(?P<selectors>.*)\])(?P<args>.*)$')
ARGS = re.compile("(^#!\s*ARG\s+(?P<arg_k>[^=]+)=(?P<arg_v>.*)$)", re.M)
INCLUDES = re.compile("(^#!\s*include\s+(?P<args>.*)$)", re.M)
PARAMS = re.compile('(?P<sel>\S*)(?P<param>\$\S+)')
USR_BIN_ENV = re.compile("#!\s*/usr/bin/env\s*(?P<lang>\w+)")
LANG = re.compile("^#!\s*(?P<lang>[\/\w]*)\s*(?:$|\r?\n)")

if os.name != 'nt':
    DEFAULT_LANG = LANG_BASH
else:
    DEFAULT_LANG = LANG_PS

LOG = logging.getLogger()


def parse_selectors(section):
    """
        Parse section to check if it is a node selector
    """
    match = SELECTOR.match(section)
    if match:
        selectors = match.group(2)
        args = match.group(3)
        return selectors, args
    return (None, None)


def parse_includes(section):
    """
        Parse section to check if it is a node selector
    """
    includes = INCLUDES.findall(section)
    return includes


def substitute_includes(section, callback=None):

    def inner(match_obj):
        return callback(match_obj.group(2))
    return INCLUDES.sub(inner, section)


def has_params(targets):
    params = PARAMS.findall(targets)
    return params


def parse_lang(section):
    """
        Parse the script language based on the shebang
    """
    is_env = USR_BIN_ENV.match(section.strip())
    if is_env:
        lang = is_env.group(1)
        return lang
    else:
        match = LANG.match(section.strip())
        if match:
            command = match.group(1).lower()
            lang = command.rpartition('/')[2]
            return lang
    return DEFAULT_LANG


def is_script(section):
    """
        Test if this is a script(has shebang)
    """
    is_env = USR_BIN_ENV.match(section.strip())
    if is_env:
        lang = is_env.group(1)
        return lang
    else:
        match = LANG.match(section.strip())
        if match:
            command = match.group(1).lower()
            lang = command.rpartition('/')[2]
            return lang
    return None


def remove_shebangs(script):
    return LANG.sub('', script)


class ParseError(Exception):
    pass


class Args(object):

    def __init__(self, *args, **kwargs):
        self._items = OrderedDict()
        for arg in args:
            k, _, v = arg.partition('=')
            k = k.lstrip('-')
            if not kwargs.get('flatten'):
                self._items.setdefault(k, []).append(v)
            else:
                self._items[k] = v

    def get(self, k, default=None):
        return self._items.get(k, default)

    def items(self):
        return self._items.items()

    def __getattr__(self, k, default=None):
        return self._items.get(k, default)

    def __contains__(self, k):
        return k in self._items

    def __getitem__(self, k):
        return self._items['k']


class Section(object):

    def __init__(self):
        self.timeout = None
        self.args = Args()
        self.args_string = ''
        self.header = ""
        self.body = ""
        self.lang = ""
        self.target = ''

    @property
    def script(self):
        return "%s\n%s" % (self.header, self.body)


def parse_content(content, include_substitute=None):
    try:
        args = []
        m_args = ARGS.findall(content)
        for match in m_args:
            args.append({match[1]: match[2]})
        args = Args(*args)

        lang = parse_lang(content)
        if include_substitute:
            body = substitute_includes(content, callback=include_substitute)
        else:
            body = content

        return body, lang, args
    except Exception, exc:
        LOG.error(exc)
        raise ParseError("Error parsing script")


def parse_common_opts(script):
    opts = CRN_SHEBANG.match(script)
    if opts:
        return opts.groups(1)
    else:
        return None
