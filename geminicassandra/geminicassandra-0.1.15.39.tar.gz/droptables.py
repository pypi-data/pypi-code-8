#!/usr/bin/env python

from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

answer = raw_input('Drop all geminicassandra tables (y | n)? ')

if answer.lower().startswith(('j', 'y', 'oui', 'si')):

	keyspaces = ['test_query_db', 'test4_snpeff_db', 'test_family_db', 'test_clinvar_db', 'test3_snpeff_db', 'test_vcf_id_snpeff_vcf_db', 'extended_ped_test_db', 'thousand_g_snippet_db', 'test2_snpeff_db', 'test_snpeff_vcf_db', 'passonly_db', 'test4_snpeff_ped_db']
	print 'Dropping geminicassandra tables...'
	cluster = Cluster()
	for ks in keyspaces:
		session = cluster.connect(ks)
		tables = ["variants", "samples", "version", "resources", "variant_impacts",
			  "variants_by_samples_gt_type", "variants_by_samples_gt_depth", "variants_by_sub_type_call_rate", "variants_by_gene", "variants_by_samples_gt", "variants_by_chrom_start",
		   	"samples_by_phenotype", "samples_by_sex", "vcf_header", "version", "resources", "samples_by_variants_gt_type", "sample_genotype_counts"]
		for table in tables:
			session.execute('DROP TABLE IF EXISTS %s' % table )

print "Dropping tables finished."
