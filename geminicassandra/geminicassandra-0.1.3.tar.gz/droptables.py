#!/usr/bin/env python

from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

answer = raw_input('Drop all geminicassandra tables (y | n)? ')

if answer.lower().startswith(('j', 'y', 'oui', 'si')):
	print 'Dropping geminicassandra tables...'
	cluster = Cluster()
	session = cluster.connect('gemini_keyspace')
	tables = ["variants", "samples", "version", "resources", "variant_impacts",
		  "variants_by_samples_gt_type", "variants_by_samples_gt_depth", "variants_by_sub_type_call_rate", 
		   "samples_by_phenotype", "samples_by_sex", "vcf_header", "version", "resources", "samples_by_variants_gt_type"]
	for table in tables:
		session.execute('DROP TABLE IF EXISTS %s' % table )

print "Dropping tables finished."
