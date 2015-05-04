#!/usr/bin/env python
# −*− coding: UTF−8 −*−
"""Present a Ansible dynamic inventory for RBC/CloudStack

Usage:
  rbc-inventory (--host=HOST|--list)  [--refresh-cache]  [--prefix=PREFIX] [--cache_file=FILE]

Examples:
    To use the inventory, add a inventory file to your Ansible directory, the inventory should be a
    executable shell script with the following example content:
    #!/bin/bash
    RBC_SECRETKEY=xxxx
    RBC_APIKEY=xxxx
    rbc-inventory $@

Options:
  --refresh-cache                    Refresh the local inventory cache from source
  --prefix=PREFIX                    prefix all groups with this value, [default: None]
  --cache_file=FILE                  use this file for cache, [default: .rbc-inventory]
  --host=HOST                        run inventory for this host only
  --list                             run inventory for all hosts
  -h --help                          Show this screen.
  --version                          Show version.

"""
import os, sys, time, hashlib, random, base64, operator, re, json, translitcodec, time
from os import path
from config import read_config
from connection import conn
from docopt import docopt

__cli_name__ = "rbc-inventory"
from rbc_tools import __version__

# This slugify from http://flask.pocoo.org/snippets/5/
_punct_re = re.compile(r'[\t !"#$%&\'()*/<=>?@\[\\\]^_`{|},.]+')


def clear_cache(args):
    return os.remove(args['--cache_file']) if os.path.exists(args['--cache_file']) else False

def update_cache(c, args):
    try:
        i = inventory(c, args)
        with open(args['--cache_file'], 'w') as f:
            f.write(i)
    except Exception as e:
        print e
        # if we can't update cache - just use the old one
        pass
    return True


def is_cache_valid(args):
    if path.isfile(args['--cache_file']):
        mod_time = os.path.getmtime(args['--cache_file'])
        current_time = time.time()
        if (mod_time + 600) > current_time:
            return True
    return False

def load_inventory_from_cache(args):
    with open(args['--cache_file']) as f:
        cache = f.read()
    return json.dumps(json.loads(cache))


def slugify(text, delim=u'_'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = word.encode('translit/long')
        if word:
            result.append(word)
    return unicode(delim.join(result))

def prefix_key(key, prefix):
    if prefix:
        return "%s_%s" % (prefix, key)
    return key

def inventory(c, args):
    inv_args = {'state': 'Running'}
    res = c.list_virtualmachines(**inv_args)
    if args['--list']:
        _meta = dict((i.nics[0].ipaddress, {
            'rbc_hypervisor': i.hypervisor,
            'rbc_memory': i.memory,
            'rbc_cpuspeed': i.cpuspeed,
            'rbc_networkname': i.nics[0].networkname,
            'rbc_template': i.templatename,
            'rbc_account': i.account
        }) for i in res)
    # return dict
    ret = {}
    # groups
    groups = dict.fromkeys(set([ g.group for g in res if 'group' in g.__dict__ ]), None)
    for g in groups.keys():
        groups[g] = []
    for i in [ r for r in res if 'group' in r.__dict__ ]:
        groups[i.group].append(i.nics[0].ipaddress)
    ret.update(groups)
    # offerings
    offerings = dict.fromkeys(set([ i.serviceofferingname for i in res ]), None)
    for o in offerings.keys():
        offerings[o] = []
    for i in [ r for r in res]:
        offerings[i.serviceofferingname].append(i.nics[0].ipaddress)
    ret.update(offerings)
    # zones
    zones = dict.fromkeys(set([ i.zonename for i in res ]), None)
    for o in zones.keys():
        zones[o] = []
    for i in [ r for r in res]:
        zones[i.zonename].append(i.nics[0].ipaddress)
    ret.update(zones)
    # tags
    tags = dict.fromkeys(set([ ["tag_%s_%s" % (t.key, slugify(t.value)) for t in i.tags] for i in res if len(i.tags) > 0][0]), None)
    for t in tags.keys():
        tags[t] = []
    for i in [ r for r in res if len(r.tags) > 0]:
        for t in i.tags:
            tags["tag_%s_%s" % (t.key, slugify(t.value))].append(i.nics[0].ipaddress)
    ret.update(tags)
    account = { i.account: []}
    for i in [ r for r in res]:
        account[i.account].append(i.nics[0].ipaddress)
    ret.update(account)
    if args['--prefix']:
        prefix = args['--prefix']
        if prefix == "None":
            prefix = None
    # create the "prefixed" dict
    ret_prefixed = dict((prefix_key(k, prefix), v) for k, v in ret.items())
    if args['--list']:
        ret_prefixed.update({'_meta': _meta})
    return json.dumps(ret_prefixed)


def main():
    config = read_config()
    c = conn(config, method='post')
    args = docopt(__doc__, version='%s %s' % (__cli_name__, __version__))
    if args['--refresh-cache']:
        clear_cache(args)
    if args['--list']:
        try:
            if is_cache_valid(args):
                print load_inventory_from_cache(args)
            else:
                update_cache(c, args)
                print load_inventory_from_cache(args)
            #print inventory(c, args)
            sys.exit(0)
        except Exception as e:
            print "error creating inventory: %s"  % e
            sys.exit(1)
    if args['--host']:
        return {}


