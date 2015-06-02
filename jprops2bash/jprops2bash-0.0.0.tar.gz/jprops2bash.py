#!/usr/bin/env python

import collections
import sys

import jprops


def do_replacements(s, mappings):
    for old, new in mappings.items():
        s = s.replace(old, new)
    return s


def key_transform(key):
    key = do_replacements(key, {'.': '_',
                                ':': '_',
                                '-': '_'})
    return key.upper()


def value_transform(value):
    return do_replacements(value, {"\n": "\\n",
                                   "'": """'"'"'"""})


def jprops2bash(fh, key_transform=key_transform, value_transform=value_transform):
    props_dict = jprops.load_properties(fh, collections.OrderedDict)

    for key, value in props_dict.items():
        key = key_transform(key)
        value = value_transform(value)
        yield """{key}='{value}'""".format(key=key, value=value)


def main():
    for line in jprops2bash(sys.stdin):
        print(line)


if __name__ == '__main__':
    sys.exit(main())
