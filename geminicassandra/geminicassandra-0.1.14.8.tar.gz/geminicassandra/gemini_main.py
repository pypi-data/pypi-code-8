#!/usr/bin/env python
import os.path
import sys
import argparse
import geminicassandra.version


def examples(parser, args):

    print
    print "[load] - load a VCF file into a geminicassandra database:"
    print "   geminicassandra load -v my.vcf my.db"
    print "   geminicassandra load -v my.vcf -t snpEff my.db"
    print "   geminicassandra load -v my.vcf -t VEP my.db"
    print

    print "[stats] - report basic statistics about your variants:"
    print "   geminicassandra stats --tstv my.db"
    print "   geminicassandra stats --tstv-coding my.db"
    print "   geminicassandra stats --sfs my.db"
    print "   geminicassandra stats --snp-counts my.db"
    print

    print "[query] - explore the database with ad hoc queries:"
    print "   geminicassandra query -q \"select * from variants where is_lof = 1 and aaf <= 0.01\" my.db"
    print "   geminicassandra query -q \"select chrom, pos, gt_bases.NA12878 from variants\" my.db"
    print "   geminicassandra query -q \"select chrom, pos, in_omim, clin_sigs from variants\" my.db"
    print

    print "[dump] - convenient \"data dumps\":"
    print "   geminicassandra dump --variants my.db"
    print "   geminicassandra dump --genotypes my.db"
    print "   geminicassandra dump --samples my.db"
    print

    print "[region] - access variants in specific genomic regions:"
    print "   geminicassandra region --reg chr1:100-200 my.db"
    print "   geminicassandra region --gene TP53 my.db"
    print

    print "[tools] - there are also many specific tools available"
    print "   1. Find compound heterozygotes."
    print "     geminicassandra comp_hets my.db"
    print

    exit()

def main():
    #########################################
    # create the top-level parser
    #########################################
    parser = argparse.ArgumentParser(prog='geminicassandra', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--version", help="Installed geminicassandra version",
                        action="version",
                        version="%(prog)s " + str(geminicassandra.version.__version__))
    parser.add_argument('--annotation-dir', dest='annotation_dir',
                             help='Path to the annotation database.\n'
                                'This argument is optional and if given will take precedence over the default location stored in the geminicassandra config file.')
    subparsers = parser.add_subparsers(title='[sub-commands]', dest='command')

    #########################################
    # $ geminicassandra examples
    #########################################
    parser_examples = subparsers.add_parser('examples',
                                            help='show usage examples')
    parser_examples.set_defaults(func=examples)

    #########################################
    # $ geminicassandra load
    #########################################
    parser_load = subparsers.add_parser('load',
                                        help='load a VCF file in geminicassandra database')
    parser_load.add_argument('-db', dest='contact_points',
                             default = "127.0.0.1",
                             help='The IP adresses at which the Cassandra cluster is reachable.')
    parser_load.add_argument('-ks', 
                            dest='keyspace',
                            default = 'gemini_keyspace',
                            metavar = 'STRING',
                            help="The Cassandra keyspace in which the data should be stored.")
                             
    parser_load.add_argument('-v', dest='vcf',
                             help='The VCF file to be loaded.')
    parser_load.add_argument('-t', dest='anno_type',
                             default=None, choices=["snpEff", "VEP"],
                             help="The annotations to be used with the input vcf.")
    parser_load.add_argument('-p', dest='ped_file',
                             help='Sample information file in PED+ format.',
                             default=None)
    parser_load.add_argument('--skip-gerp-bp',
                             dest='skip_gerp_bp',
                             action='store_true',
                             help='Do not load GERP scores at base pair resolution. Loaded by default.',
                             default=False)
    parser_load.add_argument('--skip-cadd',
                             dest='skip_cadd',
                             action='store_true',
                             help='Do not load CADD scores. Loaded by default',
                             default=False)
    parser_load.add_argument('--skip-gene-tables',
                             dest='skip_gene_tables',
                             action='store_true',
                             help='Do not load gene tables. Loaded by default.',
                             default=False)
    parser_load.add_argument('--skip-info-string',
                             dest='skip_info_string',
                             action='store_true',
                             help='Do not load INFO string from VCF file to reduce DB size. Loaded by default',
                             default=False)
    parser_load.add_argument('--no-load-genotypes',
                             dest='no_load_genotypes',
                             action='store_true',
                             help='Genotypes exist in the file, but should not be stored.',
                             default=False)
    parser_load.add_argument('--no-genotypes',
                             dest='no_genotypes',
                             action='store_true',
                             help='There are no genotypes in the file (e.g. some 1000G VCFs)',
                             default=False)
    parser_load.add_argument('--cores', dest='cores',
                             default=1,
                             type=int,
                             help="Number of cores to use to load in parallel.")
    parser_load.add_argument('--scheduler', dest='scheduler', default=None,
                             choices=["lsf", "sge", "slurm", "torque"],
                             help='Cluster scheduler to use.')
    parser_load.add_argument('--queue', dest='queue',
                             default=None, help='Cluster queue to use.')
    parser_load.add_argument('--passonly',
                             dest='passonly',
                             default=False,
                             action='store_true',
                             help="Keep only variants that pass all filters.")
    parser_load.add_argument('--test-mode',
                         dest='test_mode',
                         action='store_true',
                         help='Load in test mode (faster)',
                         default=False)
    parser_load.add_argument('--timing-log',
                             dest = "timing_log",
                             default = None,
                             help = "File to log time taken for loading")
    parser_load.add_argument('--exp-id',
                             dest = "exp_id",
                             default = "",
                             help = "Identifier for the test run")
    parser_load.add_argument('--buffer-size',
                             dest = "buffer_size",
                             default = 333,
                             type=int,
                             help = "buffer size when loading")
    parser_load.add_argument('--replication',
                             dest= "replication",
                             default = 1,
                             type=int,
                             help="replication factor for the Cassandra cluster")
    parser_load.add_argument('--max_queue',
                             dest= "max_queue",
                             default = 120,
                             type=int,
                             help="queue length (per core) for batched inserts to Cassandra")

    def load_fn(parser, args):
        import gemini_load
        gemini_load.load(parser, args)

    parser_load.set_defaults(func=load_fn)

    #########################################
    # $ geminicassandra amend
    #########################################
    parser_amend = subparsers.add_parser('amend',
                                         help="Amend an already loaded GEMINI database.")
    parser_amend.add_argument('db',
                              metavar='db',
                              help='The name of the database to be amended.')
    parser_amend.add_argument('--sample',
                              metavar='sample',
                              default=None,
                              help='New sample information file to load')
    def amend_fn(parser, args):
        import gemini_amend
        gemini_amend.amend(parser, args)
    parser_amend.set_defaults(func=amend_fn)

    #########################################
    # $ geminicassandra load_chunk
    #########################################
    parser_loadchunk = subparsers.add_parser('load_chunk',
                                             help='load a VCF file in geminicassandra database')
    parser_loadchunk.add_argument('-db', dest='contact_points',
                             default = "127.0.0.1",
                             help='The IP adresses at which the Cassandra cluster is reachable.')
    parser_loadchunk.add_argument('-ks', 
                                 dest='keyspace',
                                 default = 'gemini_keyspace',
                                 metavar = 'STRING',
                                 help="The Cassandra keyspace in which the data should be stored.")
    parser_loadchunk.add_argument('-v',
                                  dest='vcf',
                                  help='The VCF file to be loaded.')
    parser_loadchunk.add_argument('-t',
                                  dest='anno_type',
                                  default=None,
                                  metavar='STRING',
                                  help="The annotations to be used with the input vcf. Options are:\n"
                                  "  snpEff  - Annotations as reported by snpEff.\n"
                                  "  VEP     - Annotations as reported by VEP.\n"
                                  )
    parser_loadchunk.add_argument('-o',
                                  dest='offset',
                                  help='The starting number for the variant_ids',
                                  default=None)
    parser_loadchunk.add_argument('-p',
                                  dest='ped_file',
                                  help='Sample information file in PED+ format.',
                                  default=None)
    parser_loadchunk.add_argument('--no-load-genotypes',
                                  dest='no_load_genotypes',
                                  action='store_true',
                                  help='Genotypes exist in the file, but should not be stored.',
                                  default=False)
    parser_loadchunk.add_argument('--no-genotypes',
                                  dest='no_genotypes',
                                  action='store_true',
                                  help='There are no genotypes in the file (e.g. some 1000G VCFs)',
                                  default=False)
    parser_loadchunk.add_argument('--skip-gerp-bp',
                                  dest='skip_gerp_bp',
                                  action='store_true',
                                  help='Do not load GERP scores at base pair resolution. Loaded by default.',
                                  default=False)
    parser_loadchunk.add_argument('--skip-cadd',
                                 dest='skip_cadd',
                                 action='store_true',
                                 help='Do not load CADD scores. Loaded by default',
                                 default=False)
    parser_loadchunk.add_argument('--skip-gene-tables',
                             dest='skip_gene_tables',
                             action='store_true',
                             help='Do not load gene tables. Loaded by default.',
                             default=False)
    parser_loadchunk.add_argument('--skip-info-string',
                                  dest='skip_info_string',
                                  action='store_true',
                                  help='Do not load INFO string from VCF file to reduce DB size. Loaded by default',
                                  default=False)
    parser_loadchunk.add_argument('--passonly',
                                  dest='passonly',
                                  default=False,
                                  action='store_true',
                                  help="Keep only variants that pass all filters.")
    parser_loadchunk.add_argument('--test-mode',
                         dest='test_mode',
                         action='store_true',
                         help='Load in test mode (faster)',
                         default=False)
    parser_loadchunk.add_argument('--buffer-size',
                             dest = "buffer_size",
                             default = 333,
                             type=int,
                             help = "buffer size when loading")
    parser_loadchunk.add_argument('--replication',
                             dest= "replication",
                             default = 1,
                             type=int,
                             help="replication factor for the Cassandra cluster")
    parser_loadchunk.add_argument('--max_queue',
                             dest= "max_queue",
                             default = 120,
                             type=int,
                             help="queue length (per core) for batched inserts to Cassandra")
    
    def loadchunk_fn(parser, args):
        import gemini_load_chunk
        gemini_load_chunk.load(parser, args)
    parser_loadchunk.set_defaults(func=loadchunk_fn)

    #########################################
    # $ geminicassandra query
    #########################################
    parser_query = subparsers.add_parser('query',
            help='issue ad hoc SQL queries to the DB')
    parser_query.add_argument('-db', dest='contact_points',
                             default = "127.0.0.1",
                             help='The IP adresses at which the Cassandra cluster is reachable.')
    parser_query.add_argument('-ks', dest='keyspace',
                             default = "gemini_keyspace",
                             help='The Cassandra keyspace in which the data is stored.')
    parser_query.add_argument('-q',
            dest='query',
            metavar='QUERY_STR',
            help='The query to be issued to the database')
    parser_query.add_argument('--gt-filter',
            dest='gt_filter',
            metavar='STRING',
            help='Restrictions to apply to genotype values')
    parser_query.add_argument('--show-samples',
                              dest='show_variant_samples',
                              action='store_true',
                              default=False,
                              help=('Add a column of all sample names with a variant to each '
                                    'variant.'))
    parser_query.add_argument('--show-families',
                              dest='show_families',
                              action='store_true',
                              default=False,
                              help=('Add a column listing all of the families '
                                    'with a variant to each variant.'))
    parser_query.add_argument('--family-wise',
                              dest='family_wise',
                              default=False,
                              action='store_true',
                              help=('Perform the sample-filter on a family-wise '
                                    'basis.'))
    parser_query.add_argument('--min-kindreds',
                              dest='min_kindreds',
                              default=1,
                              type=int,
                              help=('Minimum number of families for a variant passing '
                                    'a family-wise filter to be in.'))
    parser_query.add_argument('--sample-delim',
                              dest='sample_delim',
                              metavar='STRING',
                              help='The delimiter to be used with the --show-samples option.',
                              default=',')
    
    parser_query.add_argument('--cores',
                             dest='cores',
                             default=1,
                             type=int,
                             help="Number of cores to use to interpret gt-filter wildcards in parallel.")

    parser_query.add_argument('--header',
                              dest='use_header',
                              action='store_true',
                              help='Add a header of column names to the output.',
                              default=False)
    parser_query.add_argument('--sample-filter',
                              dest='sample_filter',
                              help='SQL filter to use to filter the sample table',
                              default=None)
    parser_query.add_argument('--in',
                              dest='in_subject',
                              nargs='*',
                              help=('A variant must be in either all, none or any '
                                    'samples passing the --sample-query filter.'),
                              choices=['all', 'none', 'any', 'only', 'not'],
                              default=['any'])
    parser_query.add_argument('--format',
                              dest='format',
                              default='default',
                              help='Format of output (JSON, TPED or default)')
    parser_query.add_argument('--region',
                              dest='region',
                              default=None,
                              help=('Restrict query to this region, '
                                    'e.g. chr1:10-20.'))
    parser_query.add_argument('--carrier-summary-by-phenotype',
                              dest='carrier_summary',
                              default=None,
                              help=('Output columns of counts of carriers and '
                                    'non-carriers stratified by the given '
                                    'sample phenotype column'))
    parser_query.add_argument('--dgidb',
                              dest='dgidb',
                              action='store_true',
                              help='Request drug-gene interaction info from DGIdb.',
                              default=False)
    parser_query.add_argument('--test-mode',
                              dest='testing',
                              action='store_true',
                              help='Sort variants by start, samples by sample_id. ONLY TO BE USED FOR UNIT TESTS',
                              default=False)
    def query_fn(parser, args):
        import gemini_query
        gemini_query.query(parser, args)

    parser_query.set_defaults(func=query_fn)

    

    #########################################
    # $ geminicassandra region
    #########################################
    parser_region = subparsers.add_parser('region',
            help='extract variants from specific genomic loci')
    parser_region.add_argument('-db', dest='contact_points',
                             default = "127.0.0.1",
                             help='The IP adresses at which the Cassandra cluster is reachable.')
    parser_region.add_argument('--reg',
            dest='region',
            metavar='STRING',
            help='Specify a chromosomal region chr:start-end')
    parser_region.add_argument('--gene',
            dest='gene',
            metavar='STRING',
            help='Specify a gene of interest')
    parser_region.add_argument('--header',
            dest='use_header',
            action='store_true',
            help='Add a header of column names to the output.',
            default=False)
    parser_region.add_argument('--columns',
            dest='columns',
            metavar='STRING',
            help='A list of columns that you would like returned. Def. = "*"',
            )
    parser_region.add_argument('--filter',
            dest='filter',
            metavar='STRING',
            help='Restrictions to apply to variants (SQL syntax)')
    parser_region.add_argument('--show-samples',
                               dest='show_variant_samples',
                               action='store_true',
                               default=False,
                                help=('Add a column of all sample names with a variant to each '
                                      'variant.'))
    parser_region.add_argument('--format',
                              dest='format',
                              default='default',
                              help='Format of output (JSON, TPED or default)')
    def region_fn(parser, args):
        import gemini_region
        gemini_region.region(parser, args)
    parser_region.set_defaults(func=region_fn)

    #########################################
    # $ geminicassandra stats
    #########################################
    parser_stats = subparsers.add_parser('stats',
            help='compute useful variant stastics')
    parser_stats.add_argument('-db', dest='contact_points',
                             default = "127.0.0.1",
                             help='The IP adresses at which the Cassandra cluster is reachable.')
    parser_stats.add_argument('--tstv',
            dest='tstv',
            action='store_true',
            help='Report the overall ts/tv ratio.',
            default=False)
    parser_stats.add_argument('--tstv-coding',
            dest='tstv_coding',
            action='store_true',
            help='Report the ts/tv ratio in coding regions.',
            default=False)
    parser_stats.add_argument('--tstv-noncoding',
            dest='tstv_noncoding',
            action='store_true',
            help='Report the ts/tv ratio in non-coding regions.',
            default=False)
    parser_stats.add_argument('--snp-counts',
            dest='snp_counts',
            action='store_true',
            help='Report the count of each type of SNP (A->G, G->T, etc.).',
            default=False)
    parser_stats.add_argument('--sfs',
            dest='sfs',
            action='store_true',
            help='Report the site frequency spectrum of the variants.',
            default=False)
    parser_stats.add_argument('--mds',
            dest='mds',
            action='store_true',
            help='Report the pairwise genetic distance between the samples.',
            default=False)
    parser_stats.add_argument('--vars-by-sample',
            dest='variants_by_sample',
            action='store_true',
            help='Report the number of variants observed in each sample.',
            default=False)
    parser_stats.add_argument('--gts-by-sample',
            dest='genotypes_by_sample',
            action='store_true',
            help='Report the count of each genotype class obs. per sample.',
            default=False)
    parser_stats.add_argument('--summarize',
            dest='query',
            metavar='QUERY_STR',
            default=None,
            help='The query to be issued to the database to summarize')
    parser_stats.add_argument('--gt-filter',
            dest='gt_filter',
            metavar='STRING',
            help='Restrictions to apply to genotype values')
    def stats_fn(parser, args):
        import gemini_stats
        gemini_stats.stats(parser, args)
    parser_stats.set_defaults(func=stats_fn)

    #########################################
    # geminicassandra annotate
    #########################################
    parser_get = subparsers.add_parser('annotate',
            help='Add new columns for custom annotations')
    parser_get.add_argument('db',
            metavar='db',
            help='The name of the database to be updated.')
    parser_get.add_argument('-f',
            dest='anno_file',
            help='The TABIX\'ed BED file containing the annotations')
    parser_get.add_argument('-c',
            dest='col_names',
            help='The name(s) of the column(s) to be added to the variant table.')
    parser_get.add_argument('-a',
            dest='anno_type',
            help='How should the annotation file be used? (def. extract)',
            default="extract",
            choices=['boolean', 'count', 'extract'])
    parser_get.add_argument('-e',
            dest='col_extracts',
            help='Column(s) to extract information from for list annotations.')
    parser_get.add_argument('-t',
            dest='col_types',
            help='What data type(s) should be used to represent the new values '
                 'in the database? '
                 'Any of {integer, float, text}')
    parser_get.add_argument('-o',
            dest='col_operations',
            help='Operation(s) to apply to the extract column values '
                  'in the event that a variant overlaps multiple annotations '
                  'in your annotation file (-f).'
                  'Any of {mean, median, min, max, mode, list, uniq_list, first, last}')
    def annotate_fn(parser, args):
        import gemini_annotate
        gemini_annotate.annotate(parser, args)
    parser_get.set_defaults(func=annotate_fn)

    

    #########################################
    # geminicassandra db_info
    #########################################
    parser_get = subparsers.add_parser('db_info',
            help='Get the names and types of cols. database tables')
    parser_get.add_argument('db',
            metavar='db',
            help='The name of the database to be updated.')
    def dbinfo_fn(parser, args):
        import gemini_dbinfo
        gemini_dbinfo.db_info(parser, args)
    parser_get.set_defaults(func=dbinfo_fn)

    #########################################
    # $ geminicassandra comp_hets
    #########################################
    parser_comp_hets = subparsers.add_parser('comp_hets',
            help='Identify compound heterozygotes')
    parser_comp_hets.add_argument('db',
            metavar='db',
            help='The name of the database to be created.')
    parser_comp_hets.add_argument('--columns',
            dest='columns',
            metavar='STRING',
            help='A list of columns that you would like returned. Def. = "*"',
            )
    parser_comp_hets.add_argument('--filter',
            dest='filter',
            metavar='STRING',
            help='Restrictions to apply to variants (SQL syntax)')
    parser_comp_hets.add_argument('--only-affected',
            dest='only_affected',
            action='store_true',
            help='Report solely those compound heterozygotes impacted a sample \
                  labeled as affected.',
            default=False)
    parser_comp_hets.add_argument('--families',
            dest='families',
            help='Restrict analysis to a specific set of 1 or more (comma) separated) families',
            default=None)
    parser_comp_hets.add_argument('--ignore-phasing',
            dest='ignore_phasing',
            action='store_true',
            help='Ignore phasing when screening for compound hets. \
                  Candidates are inherently _putative_.',
            default=False)
    def comp_hets_fn(parser, args):
        import tool_compound_hets
        tool_compound_hets.run(parser, args)
    parser_comp_hets.set_defaults(func=comp_hets_fn)



    #########################################
    # $ geminicassandra browser
    #########################################
    parser_browser = subparsers.add_parser('browser',
            help='Browser interface to geminicassandra')
    parser_browser.add_argument('db', metavar='db',
            help='The name of the database to be queried.')
    def browser_fn(parser, args):
        import gemini_browser
        gemini_browser.browser_main(parser, args)
    parser_browser.set_defaults(func=browser_fn)

    #########################################
    # $ geminicassandra update
    #########################################
    parser_update = subparsers.add_parser("update", help="Update geminicassandra software and data files.")
    parser_update.add_argument("--devel", help="Get the latest development version instead of the release",
                               action="store_true", default=False)
    parser_update.add_argument("--dataonly", help="Only update data, not the underlying libraries.",
                               action="store_true", default=False)
    parser_update.add_argument("--extra", help="Add additional non-standard genome annotations to include",
                               action="append", default=[], choices=["gerp_bp","cadd_score"])
    parser_update.add_argument("--tooldir", help="Directory for third party tools (ie /usr/local) update")
    parser_update.add_argument("--sudo", help="Use sudo for tool installation commands",
                               dest="sudo", action="store_true", default=False)
    def update_fn(parser, args):
        import gemini_update
        gemini_update.release(parser, args)
    parser_update.set_defaults(func=update_fn)


    #######################################################
    # parse the args and call the selected function
    #######################################################
    args = parser.parse_args()

    # make sure database is found if provided
    if len(sys.argv) > 2 and sys.argv[1] not in \
       ["load", "merge_chunks", "load_chunk"]:
        if hasattr(args, "db") and args.db is not None and not os.path.exists(args.db):
            sys.stderr.write("Requested GEMINI database (%s) not found. "
                             "Please confirm the provided filename.\n"
                             % args.db)
    elif len(sys.argv) > 2 and sys.argv[1] == "load":
        if xor(args.scheduler, args.queue):
            parser.error("If you are using the IPython parallel loading, you "
                         "must specify both a scheduler with --scheduler and a "
                         "queue to use with --queue.")
    try:
        args.func(parser, args)
    except IOError, e:
        if e.errno != 32:  # ignore SIGPIPE
            raise

def xor(arg1, arg2):
    return bool(arg1) ^ bool(arg2)


if __name__ == "__main__":
    main()
