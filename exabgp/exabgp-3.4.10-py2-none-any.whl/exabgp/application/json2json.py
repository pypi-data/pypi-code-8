#!/usr/bin/env python
# encoding: utf-8
"""
parser.py

Created by Thomas Mangin on 2014-12-22.
Copyright (c) 2009-2015 Exa Networks. All rights reserved.
"""



parsed = """
{ "exabgp": "3.4.8", "time": 1429629254, "host" : "mangin.local", "pid" : "62376", "ppid" : "62374", "type": "open", "neighbor": { "ip": "127.0.0.1", "address": { "local": "127.0.0.1", "peer": "127.0.0.1"}, "asn": { "local": "1", "peer": "1"}, "direction": "sent", "open": { "version": 4, "asn": 1, "hold_time": 180, "router_id": "1.2.3.4", "capabilities": { "1": { "name": "multiprotocol", "families": [ "ipv4/unicast" ] }, "65": { "name": "asn4", "asn4": 1 }, "69": { "name": "addpath", "ipv4/unicast": "send/receive" }, "64": { "name": "graceful restart","time": 360,"address family flags": { "ipv4/unicast": [ "restart" ]} ,"restart flags": [ "forwarding" ] } , "2": { "name": "route-refresh", "variant": "RFC" }, "70": { "name": "enhanced-route-refresh" }, "71": { "name": "operational" }, "68": { "name": "multisession", "variant": "RFC" ,"capabilities": [ 1 ] } } } } }
json decoded : {u'pid': u'62376', u'exabgp': u'3.4.8', u'host': u'mangin.local', u'neighbor': {u'ip': u'127.0.0.1', u'direction': u'sent', u'open': {u'router_id': u'1.2.3.4', u'version': 4, u'hold_time': 180, u'asn': 1, u'capabilities': {u'1': {u'families': [u'ipv4/unicast'], u'name': u'multiprotocol'}, u'2': {u'variant': u'RFC', u'name': u'route-refresh'}, u'64': {u'restart flags': [u'forwarding'], u'address family flags': {u'ipv4/unicast': [u'restart']}, u'name': u'graceful restart', u'time': 360}, u'65': {u'asn4': 1, u'name': u'asn4'}, u'71': {u'name': u'operational'}, u'70': {u'name': u'enhanced-route-refresh'}, u'68': {u'variant': u'RFC', u'name': u'multisession', u'capabilities': [1]}, u'69': {u'name': u'addpath', u'ipv4/unicast': u'send/receive'}}}, u'asn': {u'peer': u'1', u'local': u'1'}, u'address': {u'peer': u'127.0.0.1', u'local': u'127.0.0.1'}}, u'time': 1429629254, u'ppid': u'62374', u'type': u'open'}
"""

consolidate = """
{ "exabgp": "3.4.8", "time": 1429629890, "host" : "mangin.local", "pid" : "62881", "ppid" : "62878", "type": "open", "header": "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00550104000100B40102030438020601040001000102", "body": "0641040000000102064504000101030208400681680001018002020200020246000202470002034401000203440101", "neighbor": { "ip": "127.0.0.1", "address": { "local": "127.0.0.1", "peer": "127.0.0.1"}, "asn": { "local": "1", "peer": "1"}, "direction": "sent", "open": { "version": 4, "asn": 1, "hold_time": 180, "router_id": "1.2.3.4", "capabilities": { "1": { "name": "multiprotocol", "families": [ "ipv4/unicast" ] }, "65": { "name": "asn4", "asn4": 1 }, "69": { "name": "addpath", "ipv4/unicast": "send/receive" }, "64": { "name": "graceful restart","time": 360,"address family flags": { "ipv4/unicast": [ "restart" ]} ,"restart flags": [ "forwarding" ] } , "2": { "name": "route-refresh", "variant": "RFC" }, "70": { "name": "enhanced-route-refresh" }, "71": { "name": "operational" }, "68": { "name": "multisession", "variant": "RFC" ,"capabilities": [ 1 ] } } } } }
"""

import os
import sys
import json

def decode (string):
	loaded = json.loads(string)
	if not 'header' in loaded:
		print >> sys.stderr, 'invalid line', string
		return

	if not 'body' in loaded:
		print >> sys.stderr, 'invalid line', string
		return

	return loaded['header'] + loaded['body']

def encode (string):
	if not string:
		return
	return string

print encode(decode(consolidate))


running = 50
while running:

	line = sys.stdin.readline().strip()

	if not line:
		running -= 1
		continue
	running = 50

	print encode(decode(line))
