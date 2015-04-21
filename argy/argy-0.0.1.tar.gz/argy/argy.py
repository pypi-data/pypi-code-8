import re
import argparse
import inspect


def argy(function):
    ap = argparse.ArgumentParser()
    function_args = inspect.getargspec(function)
    doc_map = _create_doc_map(function)
    type_map = _create_type_map(function)
    args = []

    defaults = len(function_args.defaults)
    required = [True]*len(function_args.args)
    required[-defaults:] = [False] * defaults
    for a, required in zip(function_args.args, required):
        tpe = type_map.get(a)
        if required:
            ap.add_argument(a, type=tpe, help=doc_map[a])
        else:
            ap.add_argument("--{}".format(a), type=tpe,
                            help=doc_map[a])

    args = vars(ap.parse_args())
    print function(**args)


def _create_doc_map(function):
    doc_str = function.__doc__
    doc_map = {}
    for line in doc_str.splitlines():
        m = re.match(r'\s*:param (?P<arg>.+?):(?P<doc>.+)', line)
        if m:
            doc_map[m.groupdict()['arg']] = m.groupdict()['doc']
    return doc_map


def _create_type_map(function):
    doc_str = function.__doc__
    type_map = {}
    for line in doc_str.splitlines():
        m = re.match(r'\s*:type (?P<arg>.+?):(?P<type>.+)', line)
        if m:
            tpe = eval(m.groupdict()['type'])
            if tpe:
                type_map[m.groupdict()['arg']] = tpe
    return type_map
