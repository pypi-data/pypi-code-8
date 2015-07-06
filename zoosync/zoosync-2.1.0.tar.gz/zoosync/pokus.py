#! /usr/bin/python
import sys

d = {}

d['a'] = ['va1', 'va2', 'va3']
d['b'] = ['vb1']
d['c'] = ['vc1']

for k, v in d.items():
	v.append('pokus')

for k, v in d.items():
	print('%s' % (k))
	print('  => %s' % v)

for k, v in sorted(d.items()):
	print('%s' % (k))
	print('  => %s' % v)

print('pokus stderr', file = sys.stderr)
