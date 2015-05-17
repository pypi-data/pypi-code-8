# Copyright 2015 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of cifparser.  cifparser is BSD-licensed software;
# for copyright information see the LICENSE file.

import functools
import pyparsing as pp

@functools.total_ordering
class Path(object):
    """
    """
    def __init__(self, segments):
        self.segments = segments

    def __str__(self):
        return '.'.join(self.segments) if len(self.segments) > 0 else '.'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.segments == other.segments

    def __lt__(self, other):
        return self.segments < other.segments

    def __hash__(self):
        return hash(str(self))

    def __iter__(self):
        return iter(self.segments)

    def __add__(self, other):
        return Path(self.segments + make_path(other).segments)

ROOT_PATH = Path([])

pp.quotedString.setParseAction(pp.removeQuotes)
pathsegment_parser = pp.Word(pp.alphanums) ^ pp.quotedString
path_parser = pp.ZeroOrMore(pathsegment_parser + pp.Literal('.')) + pathsegment_parser

def path_parse_action(tokens):
    return Path(list(filter(lambda x: x != '.', tokens)))
path_parser.setParseAction(path_parse_action)

def make_path(*path_or_str_or_segments):
    """
    :param path_or_str_or_segments:
    :return:
    :rtype: cifparser.path.Path
    """
    if len(path_or_str_or_segments) == 0:
        return ROOT_PATH
    elif len(path_or_str_or_segments) == 1:
        single_item = path_or_str_or_segments[0]
        if isinstance(single_item, Path):
            return single_item
        if isinstance(single_item, str):
            try:
                return path_parser.parseString(single_item, True).asList()[0]
            except:
                raise ValueError()
        raise TypeError()
    else:
        segments = path_or_str_or_segments
        return sum(map(lambda x: make_path(x), segments), ROOT_PATH)
