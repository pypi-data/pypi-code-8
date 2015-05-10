#!/usr/bin/env python

import abc
import cassandra
from cassandra.cluster import Cluster
import collections
import json
import re
import sys

import compression
from gemini_constants import HOM_ALT, HOM_REF, HET, UNKNOWN
from gemini_subjects import get_subjects
from gemini_utils import (OrderedDict, itersubclasses, partition_by_fn)
from sql_utils import ensure_columns
from collections import namedtuple
from geminicassandra.query_expressions import Basic_expression, AND_expression,\
    NOT_expression, OR_expression, rows_as_set, GT_wildcard_expression
from geminicassandra.sql_utils import get_query_parts
from cassandra.query import ordered_dict_factory, tuple_factory
from string import strip


# geminicassandra imports
class RowFormat:
    """A row formatter to output rows in a custom format.  To provide
    a new output format 'foo', implement the class methods and set the
    name field to foo.  This will automatically add support for 'foo' to
    anything accepting the --format option via --format foo.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def name(self):
        return

    @abc.abstractmethod
    def format(self, row):
        """ return a string representation of a GeminiRow object
        """
        return '\t'.join([str(row.row[c]) for c in row.row])

    @abc.abstractmethod
    def format_query(self, query):
        """ augment the query with columns necessary for the format or else just
        return the untouched query
        """
        return query

    @abc.abstractmethod
    def predicate(self, row):
        """ the row must pass this additional predicate to be output. Just
        return True if there is no additional predicate"""
        return True

    @abc.abstractmethod
    def header(self, fields):
        """ return a header for the row """
        return "\t".join(fields)

class DefaultRowFormat(RowFormat):

    name = "default"

    def __init__(self, args):
        pass

    def format(self, row):
        return '\t'.join([str(row.row[c]) for c in row.row])

    def format_query(self, query):
        return query

    def predicate(self, row):
        return True

    def header(self, fields):
        """ return a header for the row """
        return "\t".join(fields)

class CarrierSummary(RowFormat):
    """
    Generates a count of the carrier/noncarrier status of each feature in a given
    column of the sample table

    Assumes None == unknown.
    """
    name = "carrier_summary"

    def __init__(self, args):
        subjects = get_subjects(args)
        self.carrier_summary = args.carrier_summary

        # get the list of all possible values in the column
        # but don't include None, since we are treating that as unknown.
        self.column_types = list(set([getattr(x, self.carrier_summary)
                                      for x in subjects.values()]))
        self.column_types = [i for i in self.column_types if i is not None]
        self.column_counters = {None: set()}
        for ct in self.column_types:
            self.column_counters[ct] = set([k for (k, v) in subjects.items() if
                                            getattr(v, self.carrier_summary) == ct])


    def format(self, row):
        have_variant = set(row.variant_samples)
        have_reference = set(row.HOM_REF_samples)
        unknown = len(set(row.UNKNOWN_samples).union(self.column_counters[None]))
        carrier_counts = []
        for ct in self.column_types:
            counts = len(self.column_counters[ct].intersection(have_variant))
            carrier_counts.append(counts)
        for ct in self.column_types:
            counts = len(self.column_counters[ct].intersection(have_reference))
            carrier_counts.append(counts)

        carrier_counts.append(unknown)
        carrier_counts = map(str, carrier_counts)
        return '\t'.join([str(row.row[c]) for c in row.row] + carrier_counts)

    def format_query(self, query):
        return query

    def predicate(self, row):
        return True

    def header(self, fields):
        """ return a header for the row """
        header_columns = self.column_types
        if self.carrier_summary == "affected":
            header_columns = self._rename_affected()
        carriers = [x + "_carrier" for x in map(str, header_columns)]
        noncarriers = [ x + "_noncarrier" for x in map(str, header_columns)]
        fields += carriers
        fields += noncarriers
        fields += ["unknown"]
        return "\t".join(fields)

    def _rename_affected(self):
        header_columns = []
        for ct in self.column_types:
            if ct == True:
                header_columns.append("affected")
            elif ct == False:
                header_columns.append("unaffected")
        return header_columns

class TPEDRowFormat(RowFormat):

    X_PAR_REGIONS = [(60001, 2699520), (154931044, 155260560)]
    Y_PAR_REGIONS = [(10001, 2649520), (59034050, 59363566)]

    name = "tped"
    NULL_GENOTYPES = ["."]
    PED_MISSING = ["0", "0"]
    VALID_CHROMOSOMES = map(str, range(1, 23)) + ["X", "Y", "XY", "MT"]
    POSSIBLE_HAPLOID = ["X", "Y"]

    def __init__(self, args):
        gq = GeminiQuery(args.db)
        subjects = get_subjects(args, skip_filter=True)
        # get samples in order of genotypes
        self.samples = [gq.idx_to_sample_object[x] for x in range(len(subjects))]

    def format(self, row):
        VALID_CHROMOSOMES = map(str, range(1, 23)) + ["X", "Y", "XY", "MT"]
        chrom = row['chrom'].split("chr")[1]
        chrom = chrom if chrom in VALID_CHROMOSOMES else "0"
        start = str(row.row['start'])
        """end = str(row.row['end'])
        ref = row['ref']
        alt = row['alt']"""
        geno = [re.split('\||/', x) for x in row.row['gts'].split(",")]
        geno = [self._fix_genotype(chrom, start, genotype, self.samples[i].sex)
                for i, genotype in enumerate(geno)]
        genotypes = " ".join(list(flatten(geno)))
        name = str(row['variant_id'])
        return " ".join([chrom, name, "0", start, genotypes])

    def format_query(self, query):
        NEED_COLUMNS = ["chrom", "rs_ids", "start", "ref", "alt", "gts", "type", "variant_id"]
        return ensure_columns(query, NEED_COLUMNS)

    def predicate(self, row):
        geno = [re.split("\||/", x) for x in row['gts']]
        geno = list(flatten(geno))
        num_alleles = len(set(geno).difference(self.NULL_GENOTYPES))
        return num_alleles > 0 and num_alleles <= 2 and row['type'] != "sv"

    def _is_haploid(self, genotype):
        return len(genotype) < 2

    def _has_missing(self, genotype):
        return any([allele in self.NULL_GENOTYPES for allele in genotype])

    def _is_heterozygote(self, genotype):
        return len(genotype) == 2 and (genotype[0] != genotype[1])

    def _in_PAR(self, chrom, start):
        if chrom == "X":
            for region in self.X_PAR_REGIONS:
                if start > region[0] and start < region[1]:
                    return True
        elif chrom == "Y":
            for region in self.Y_PAR_REGIONS:
                if start > region[0] and start < region[1]:
                    return True
        return False

    def _fix_genotype(self, chrom, start, genotype, sex):
        """
        the TPED format has to have both alleles set, even if it is haploid.
        this fixes that setting Y calls on the female to missing,
        heterozygotic calls on the male non PAR regions to missing and haploid
        calls on non-PAR regions to be the haploid call for both alleles
        """
        if sex == "2":
            # set female Y calls and haploid calls to missing
            if self._is_haploid(genotype) or chrom == "Y" or self._has_missing(genotype):
                return self.PED_MISSING
            return genotype
        if chrom in self.POSSIBLE_HAPLOID and sex == "1":
            # remove the missing genotype calls
            genotype = [x for x in genotype if x not in self.NULL_GENOTYPES]
            # if all genotypes are missing skip
            if not genotype:
                return self.PED_MISSING
            # heterozygote males in non PAR regions are a mistake
            if self._is_heterozygote(genotype) and not self._in_PAR(chrom, start):
                return self.PED_MISSING
            # set haploid males to be homozygous for the allele
            if self._is_haploid(genotype):
                return [genotype[0], genotype[0]]

        # if a genotype is missing or is haploid set it to missing
        if self._has_missing(genotype) or self._is_haploid(genotype):
            return self.PED_MISSING
        else:
            return genotype

    def header(self, fields):
        return None

class JSONRowFormat(RowFormat):

    name = "json"

    def __init__(self, args):
        pass

    def format(self, row):
        """Emit a JSON representation of a given row
        """
        return json.dumps(row.row)

    def format_query(self, query):
        return query

    def predicate(self, row):
        return True

    def header(self, fields):
        return None

'''class VCFRowFormat(RowFormat):

    name = "vcf"

    def __init__(self, args):
        self.gq = GeminiQuery(args.db)

    def format(self, row):
        """Emit a VCF representation of a given row

           TODO: handle multiple alleles
        """
        # core VCF fields
        vcf_rec = [row.row['chrom'], row.row['start'] + 1]
        if row.row['vcf_id'] is None:
            vcf_rec.append('.')
        else:
            vcf_rec.append(row.row['vcf_id'])
        vcf_rec += [row.row['ref'], row.row['alt'], row.row['qual']]
        if row.row['filter'] is None:
            vcf_rec.append('PASS')
        else:
            vcf_rec.append(row.row['filter'])
        vcf_rec += [row.row['info'], 'GT']

        # construct genotypes
        gts = list(row['gts'])
        gt_types = list(row['gt_types'])
        gt_phases = list(row['gt_phases'])
        for idx, gt_type in enumerate(gt_types):
            phase_char = '/' if not gt_phases[idx] else '|'
            gt = gts[idx]
            alleles = gt.split(phase_char)
            if gt_type == HOM_REF:
                vcf_rec.append('0' + phase_char + '0')
            elif gt_type == HET:
                # if the genotype is phased, need to check for 1|0 vs. 0|1
                if gt_phases[idx] and alleles[0] != row.row['ref']:
                    vcf_rec.append('1' + phase_char + '0')
                else:
                    vcf_rec.append('0' + phase_char + '1')
            elif gt_type == HOM_ALT:
                vcf_rec.append('1' + phase_char + '1')
            elif gt_type == UNKNOWN:
                vcf_rec.append('.' + phase_char + '.')

        return '\t'.join([str(c) if c is not None else "." for c in vcf_rec])

    def format_query(self, query):
        return query

    def predicate(self, row):
        return True

    def header(self, fields):
        """Return the original VCF's header
        """
        try:
            self.gq.run('select vcf_header from vcf_header')
            return str(self.gq.next()).strip()
        except:
            sys.exit("Your database does not contain the vcf_header table. Therefore, you cannot use --header.\n")'''

class GeminiRow(object):

    def __init__(self, row, 
                 variant_samples=None,
                 HET_samples=None, HOM_ALT_samples=None,
                 HOM_REF_samples=None, UNKNOWN_samples=None,
                 info=None, formatter=DefaultRowFormat(None)):
        self.row = row
        self.info = info
        self.gt_cols = ["variant_samples", "HET_samples", "HOM_ALT_samples", "HOM_REF_samples"]
        self.formatter = formatter
        self.variant_samples = variant_samples
        self.HET_samples = HET_samples
        self.HOM_ALT_samples = HOM_ALT_samples
        self.HOM_REF_samples = HOM_REF_samples
        self.UNKNOWN_samples = UNKNOWN_samples

    def __getitem__(self, val):
        if val not in self.gt_cols:
            return self.row[val]
        else:
            return getattr(self, val)

    def __iter__(self):
        return self

    def __repr__(self):
        return self.formatter.format(self)

    def next(self):
        try:
            return self.row.keys()
        except:
            raise StopIteration


class GeminiQuery(object):

    """
    An interface to submit queries to an existing Gemini database
    and iterate over the results of the query.

    We create a GeminiQuery object by specifying database to which to
    connect::
        from geminicassandra import GeminiQuery
        gq = GeminiQuery("my.db")

    We can then issue a query against the database and iterate through
    the results by using the ``run()`` method::


        for row in gq:
            print row

    Instead of printing the entire row, one access print specific columns::

        gq.run("select chrom, start, end from variants")
        for row in gq:
            print row['chrom']

    Also, all of the underlying numpy genotype arrays are
    always available::

        gq.run("select chrom, start, end from variants")
        for row in gq:
            gts = row.gts
            print row['chrom'], gts
            # yields "chr1" ['A/G' 'G/G' ... 'A/G']

    The ``run()`` methods also accepts genotype filter::

        query = "select chrom, start, end" from variants"
        gt_filter = "gt_types.NA20814 == HET"
        gq.run(query)
        for row in gq:
            print row

    Lastly, one can use the ``sample_to_idx`` and ``idx_to_sample``
    dictionaries to gain access to sample-level genotype information
    either by sample name or by sample index::

        # grab dict mapping sample to genotype array indices
        smp2idx = gq.sample_to_idx

        query  = "select chrom, start, end from variants"
        gt_filter  = "gt_types.NA20814 == HET"
        gq.run(query, gt_filter)

        # print a header listing the selected columns
        print gq.header
        for row in gq:
            # access a NUMPY array of the sample genotypes.
            gts = row['gts']
            # use the smp2idx dict to access sample genotypes
            idx = smp2idx['NA20814']
            print row, gts[idx]
    """

    def __init__(self, db_contact_points, keyspace, include_gt_cols=False,
                 out_format=DefaultRowFormat(None)):

        self.db_contact_points = map(strip, db_contact_points.split(','))
        self.keyspace = keyspace
        self.query_executed = False
        self.for_browser = False
        self.include_gt_cols = include_gt_cols

        # try to connect to the provided database
        self._connect_to_database()

        # list of samples ids for each clause in the --gt-filter
        self.sample_info = collections.defaultdict(list)

        '''# map sample names to indices. e.g. self.sample_to_idx[NA20814] -> 323
        self.sample_to_idx = util.map_samples_to_indices(self.session)
        # and vice versa. e.g., self.idx_to_sample[323] ->  NA20814
        self.idx_to_sample = util.map_indices_to_samples(self.session)
        self.idx_to_sample_object = util.map_indices_to_sample_objects(self.session)
        self.sample_to_sample_object = util.map_samples_to_sample_objects(self.session)'''
        self.formatter = out_format
        self.predicates = [self.formatter.predicate]

    def _set_gemini_browser(self, for_browser):
        self.for_browser = for_browser

    def run(self, query, gt_filter=None, show_variant_samples=False,
            variant_samples_delim=',', predicates=None,
            needs_genotypes=False, needs_genes=False,
            show_families=False, sort_results=False, needs_sample_names=False, nr_cores = 1):
        """
        Execute a query against a Gemini database. The user may
        specify:

            1. (reqd.) an SQL `query`.
            2. (opt.) a genotype filter.
        """
        self.query = self.formatter.format_query(query).replace('==','=')
        self.gt_filter = gt_filter
        #print self.query + '; gt-filter = %s \n' % gt_filter
        self.nr_cores = nr_cores
        if self._is_gt_filter_safe() is False:
            sys.exit("ERROR: unsafe --gt-filter command.")
        '''if not self.gt_filter == None:
            self.gt_filter = self.gt_filter.replace('==','=')'''
        
        self.show_variant_samples = show_variant_samples
        self.variant_samples_delim = variant_samples_delim
        self.sort_results = sort_results
        self.needs_genotypes = needs_genotypes
        self.needs_vcf_columns = False
        if self.formatter.name == 'vcf':
            self.needs_vcf_columns = True
        self.needs_sample_names = needs_sample_names

        self.needs_genes = needs_genes
        self.show_families = show_families
        if predicates:
            self.predicates += predicates

        # make sure the SELECT columns are separated by a
        # comma and a space. then tokenize by spaces.
        self.query = self.query.replace(',', ', ')
        self.query_pieces = self.query.split()
        if not any(s.startswith("gt") for s in self.query_pieces) and \
           not any(s.startswith("(gt") for s in self.query_pieces) and \
           not any(".gt" in s for s in self.query_pieces):
            if self.gt_filter is None:
                self.query_type = "no-genotypes"
            else:
                self.gt_filter_exp = self._correct_genotype_filter()
                self.query_type = "filter-genotypes"
        else:
            if self.gt_filter is None:
                self.query_type = "select-genotypes"
            else:
                self.gt_filter_exp = self._correct_genotype_filter()
                self.query_type = "filter-genotypes"

        (self.requested_columns, self.from_table, where_clause, self.rest_of_query) = get_query_parts(self.query)
        self.extra_columns = []
        
        if where_clause != '':
            self.where_exp = self.parse_where_clause(where_clause, self.from_table)
            if not self.gt_filter is None:
                self.where_exp = AND_expression(self.where_exp, self.gt_filter_exp)
        else:
            if not self.gt_filter is None:
                self.where_exp = self.gt_filter_exp
            else:
                self.where_exp = None
            
        self._apply_query()
        self.query_executed = True
        
    def run_simple_query(self, query):
        (requested_columns, from_table, where_clause, rest_of_query) = get_query_parts(query)
        if where_clause != '':
            where_exp = self.parse_where_clause(where_clause, from_table)
        if not where_exp is None:
            matches = where_exp.evaluate(self.session, "*")
            
        if len(matches) == 0:
            return OrderedDict([])
        else:
            try:
                dink_query = "SELECT %s FROM %s" % (','.join(requested_columns), from_table)
                if matches != "*":
                    if from_table.startswith('samples'):
                        in_clause = "','".join(matches)            
                        dink_query += " WHERE %s IN ('%s')" % (self.get_partition_key(from_table), in_clause)
                    else:
                        in_clause = ",".join(map(str, matches))            
                        dink_query += " WHERE %s IN (%s)" % (self.get_partition_key(from_table), in_clause)
                dink_query += " " + rest_of_query
                self.session.row_factory = ordered_dict_factory
                return self.session.execute(dink_query)                
                
            except cassandra.protocol.SyntaxException as e:
                print "Cassandra error: {0}".format(e)
                sys.exit("The query issued (%s) has a syntax error." % query)

    def __iter__(self):
        return self

    @property
    def header(self):
        """
        Return a header describing the columns that
        were selected in the query issued to a GeminiQuery object.
        """
        h = [col for col in self.report_cols]
        if self.show_variant_samples:
            h += ["variant_samples", "HET_samples", "HOM_ALT_samples"]
        if self.show_families:
            h += ["families"]
        return self.formatter.header(h)

    def next(self):
        """
        Return the GeminiRow object for the next query result.
        """
        while (1):
            try:
                row = self.result.next()
            except Exception as e:
                sys.__stderr__.write(str(e) + "\n")
                self.cluster.shutdown()
                raise StopIteration
            variant_names = []
            het_names = []
            hom_alt_names = []
            hom_ref_names = []
            unknown_names = []
            info = None

            if 'info' in self.report_cols:
                info = compression.unpack_ordereddict_blob(row['info'])

            fields = OrderedDict()

            for col in self.report_cols:
                if col == "*":
                    continue
                if not col == "info":
                    fields[col] = row[col]
                elif col == "info":
                    fields[col] = self._info_dict_to_string(info)

            if self.show_variant_samples or self.needs_sample_names:
                
                het_names = self._get_variant_samples(row['variant_id'], HET)
                hom_alt_names = self._get_variant_samples(row['variant_id'], HOM_ALT)
                hom_ref_names = self._get_variant_samples(row['variant_id'], HOM_REF)
                unknown_names = self._get_variant_samples(row['variant_id'], UNKNOWN)
                variant_names = het_names | hom_alt_names
                
                if self.show_variant_samples:
                    fields["variant_samples"] = \
                        self.variant_samples_delim.join(variant_names)
                    fields["HET_samples"] = \
                        self.variant_samples_delim.join(het_names)
                    fields["HOM_ALT_samples"] = \
                        self.variant_samples_delim.join(hom_alt_names)
                    
            if self.show_families:
                families = map(str, list(set([self.sample_to_sample_object[x].family_id
                                              for x in variant_names])))
                fields["families"] = self.variant_samples_delim.join(families)
            
            gemini_row = GeminiRow(fields, variant_names, het_names, hom_alt_names,
                                   hom_ref_names, unknown_names, info,
                                   formatter=self.formatter)

            if not all([predicate(gemini_row) for predicate in self.predicates]):
                continue

            if not self.for_browser:
                return gemini_row
            else:
                return fields
            
    def _get_variant_samples(self, variant_id, gt_type):
        query = "SELECT sample_name from samples_by_variants_gt_type WHERE variant_id = %s AND gt_type = %s"
        self.session.row_factory = tuple_factory
        return rows_as_set(self.session.execute(query, (variant_id, gt_type)))    

    def _group_samples_by_genotype(self, gt_types):
        """
        make dictionary keyed by genotype of list of samples with that genotype
        """
        key_fn = lambda x: x[1]
        val_fn = lambda x: self.idx_to_sample[x[0]]
        return partition_by_fn(enumerate(gt_types), key_fn=key_fn, val_fn=val_fn)

    def _connect_to_database(self):
        """
        Establish a connection to the requested Gemini database.
        """
        # open up a new database
        
        self.cluster = Cluster(self.db_contact_points)
        self.session = self.cluster.connect(self.keyspace)

    def _is_gt_filter_safe(self):
        """
        Test to see if the gt_filter string is potentially malicious.

        A future improvement would be to use pyparsing to
        traverse and directly validate the string.
        """
        if self.gt_filter is None or len(self.gt_filter.strip()) == 0:
            return True

        # avoid builtins
        # http://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
        if "__" in self.gt_filter:
            return False

        # avoid malicious commands
        evil = [" rm ", "os.system"]
        if any(s in self.gt_filter for s in evil):
            return False

        # make sure a "gt" col is in the string
        valid_cols = ["gts.", "gt_types.", "gt_phases.", "gt_quals.",
                      "gt_depths.", "gt_ref_depths.", "gt_alt_depths.", "gt_copy_numbers.",
                      "[gts].", "[gt_types].", "[gt_phases].", "[gt_quals].", "[gt_copy_numbers].",
                      "[gt_depths].", "[gt_ref_depths].", "[gt_alt_depths]."]
        if any(s in self.gt_filter for s in valid_cols):
            return True

        # assume the worst
        return False

    def _execute_query(self):
        if len(self.matches) == 0:
            print "No results!"
            self.report_cols = []
            self.result = iter([])
        else:
            try:
                query = "SELECT %s FROM %s" % (','.join(self.requested_columns + self.extra_columns), self.from_table)
                if self.matches != "*":
                    if self.from_table != 'samples':
                        in_clause = ",".join(map(str, self.matches))            
                        query += " WHERE %s IN (%s)" % (self.get_partition_key(self.from_table), in_clause)
                    else:
                        in_clause = "','".join(self.matches)            
                        query += " WHERE %s IN ('%s')" % (self.get_partition_key(self.from_table), in_clause)
                query += " " + self.rest_of_query
                self.session.row_factory = ordered_dict_factory
                res = self.session.execute(query)  
                if self.sort_results:
                    if self.from_table == 'variants':
                        res = sorted(res, key = lambda x: x['start'])   
                    elif self.from_table == 'samples':
                        res = sorted(res, key = lambda x: x['sample_id'])
                      
                self.report_cols = filter(lambda x: not x in self.extra_columns, res[0].keys())
                self.result = iter(res)
                
            except cassandra.protocol.SyntaxException as e:
                print "Cassandra error: {0}".format(e)
                sys.exit("The query issued (%s) has a syntax error." % query)

    def _apply_query(self):
        """
        Execute a query. Intercept gt* columns and
        replace sample names with indices where necessary.
        """
        if self.needs_genes:
            self.requested_columns.append("gene")

        '''if self.needs_vcf_columns:
            self.query = self._add_vcf_cols_to_query()'''
        
        self.matches = "*"
        if not self.where_exp is None:
            self.matches = self.where_exp.evaluate(self.session, "*")

        if self._query_needs_genotype_info():
            # break up the select statement into individual
            # pieces and replace genotype columns using sample
            # names with sample indices
            self._split_select()
                
        if self.show_families or self.show_variant_samples or self.needs_sample_names:
            if (not 'variant_id' in self.requested_columns) and (not "*" in self.requested_columns):
                self.extra_columns.append('variant_id')
        if self.sort_results and self.from_table == 'variants' and not 'start' in self.requested_columns:
            self.extra_columns.append('start')
        self._execute_query()
        

    def _get_matching_sample_ids(self, wildcard):
        
        if wildcard.strip() != "*":        
            query = self.parse_where_clause(wildcard, 'samples')
        else:
            query = Basic_expression('samples', 'name', "")
        return list(query.evaluate(self.session, '*'))


    def get_partition_key(self, table):
        
        key = self.cluster.metadata.keyspaces[self.keyspace].tables[table].partition_key[0].name
        return key
    
    def _correct_genotype_filter(self):
        """
        This converts a raw genotype filter that contains
        'wildcard' statements into a filter that can be eval()'ed.
        Specifically, we must convert a _named_ genotype index
        to a _numerical_ genotype index so that the appropriate
        value can be extracted for the sample from the genotype
        numpy arrays.

        For example, without WILDCARDS, this converts:
        --gt-filter "(gt_types.1478PC0011 == 1)"

        to:
        (gt_types[11] == 1)

        With WILDCARDS, this converts things like:
            "(gt_types).(phenotype==1).(==HET)"

        to:
            "gt_types[2] == HET and gt_types[5] == HET"
        """
        return self.parse_clause(self.gt_filter, self.gt_base_parser, 'variants')
    
    def parse_where_clause(self, where_clause, table):
        return self.parse_clause(where_clause, lambda x: self.where_clause_to_exp(table, self.get_partition_key(table), x), table)
    
    def parse_clause(self, clause, base_clause_parser, table):
        
        clause = clause.strip()    
        depth = 0
        min_depth = 100000 #Arbitrary bound on nr of nested clauses.
        
        in_wildcard_clause = False
        
        for i in range(0,len(clause)):
            if clause[i] == '[':
                in_wildcard_clause = True
            elif clause[i] == ']':
                in_wildcard_clause = False
            elif in_wildcard_clause: #currently in wildcard thingy, so doesn't mean anything. Move on.
                continue
            elif clause[i] == '(':
                depth += 1
            elif clause[i] == ')':
                depth -= 1
            elif i < len(clause) - 2:
                if clause[i:i+2] == "||":
                    if depth == 0:
                        left = self.parse_clause(clause[:i].strip(), base_clause_parser, table)
                        right = self.parse_clause(clause[i+2:].strip(), base_clause_parser, table)
                        return OR_expression(left, right)
                    else:
                        min_depth = min(min_depth, depth)
                elif clause[i:i+2] == "&&":
                    if depth == 0:
                        left = self.parse_clause(clause[:i].strip(), base_clause_parser, table)
                        right = self.parse_clause(clause[i+2:].strip(), base_clause_parser, table)
                        return AND_expression(left, right)
                    else:
                        min_depth = min(min_depth, depth)   
                elif i < len(clause) - 3:                
                    if clause[i:i+3] == "NOT":
                        if depth == 0:
                            body = self.parse_clause(clause[i+3:].strip(), base_clause_parser, table)
                            return NOT_expression(body, table, self.get_partition_key(table))
                        else:
                            min_depth = min(min_depth, depth)
        if depth == 0:
            if min_depth < 100000:
                #Strip away all brackets to expose uppermost boolean operator
                return self.parse_clause(clause[min_depth:len(clause)-min_depth], base_clause_parser, table)
            else:
                #No more boolean operators, strip all remaining brackets
                token = clause.strip('(').strip(')')
                return base_clause_parser(token)       
        else:
            sys.exit("ERROR in %s. Brackets don't match" % clause)
    
    def where_clause_to_exp(self, table, cols, clause):
        
        target_table = self.get_table_from_where_clause(table, clause)
        exp = Basic_expression(target_table, cols, clause)
        return exp
    
    def get_table_from_where_clause(self, table, where_clause):
        
        where_clause = where_clause.replace('==','=')
        clauses = where_clause.split("and")
        
        has_range_clause = False
        range_clauses = filter(lambda x: '<' in x or '>' in x, clauses)    
        if len(range_clauses) > 1:
            sys.exit("ERROR: only one range clause within single table possible")
        elif len(range_clauses) == 1:
            range_clause = range_clauses[0] 
            has_range_clause = True
            i = 0
            for op in ["<", ">"]:
                temp = range_clause.find(op)
                if temp > -1:
                    i = temp
                    break
            range_col = range_clause[0:i].strip()
            
        eq_clauses = filter(lambda x: not ('<' in x or '>' in x), clauses)
        eq_clauses = map(lambda x: x.split('='), eq_clauses)
        eq_columns = map(lambda x: x[0].strip(), eq_clauses)
        
        relevant_tables = self.get_relevant_tables(table)
        
        for t in relevant_tables:
            if all(x in eq_columns for x in t.partition_key):
                other_cols = filter(lambda x: not x in t.partition_key, eq_columns)
                if all (x in t.clustering_key[:len(other_cols)] for x in other_cols):
                    if has_range_clause:
                        if range_col == t.clustering_key[len(other_cols)]:
                            return t.name
                    else:
                        return t.name
        
        sys.exit("ERROR: No suitable table found for query: %s" % where_clause)
        
    def get_relevant_tables(self, table):
        
        Row = namedtuple('Row', 'name partition_key clustering_key')
        tables = self.cluster.metadata.keyspaces[self.keyspace].tables
        interesting_tables = filter(lambda x: x.startswith(table), tables.keys())
        res = []
        for table in interesting_tables:
            res.append(Row(table, map(lambda y: y.name, tables[table].partition_key),\
                            map(lambda y: y.name, tables[table].clustering_key)))
        return res
    
    def gt_base_parser(self, clause):
        if (clause.find("gt") >= 0 or clause.find("GT") >= 0) and not '[' in clause:
            return self.gt_filter_to_query_exp(clause.replace('==', '='))
        elif (clause.find("gt") >= 0 or clause.find("GT") >= 0) and '[' in clause:
            dink = self.parse_gt_wildcard(clause)
            #print dink.to_string()
            return dink
        else:
            sys.exit("ERROR: invalid --gt-filter command")   
        
    def gt_filter_to_query_exp(self, gt_filter):
        
        i = -1
        operators = ['!=', '<=', '>=', '=', '<', '>']
        for op in operators:
            temp = gt_filter.find(op)
            if temp > -1:
                i = temp
                break
                    
        if i > -1:
            left = gt_filter[0:i].strip()
            clause = self._swap_genotype_for_number(gt_filter[i:].strip())
        else:
            sys.exit("ERROR: invalid --gt-filter command 858.")
                
        not_exp = False
        if clause.startswith('!'):
            not_exp = True
            clause = clause[1:]
                        
        (column, sample) = left.split('.', 1)
                
        exp = Basic_expression('variants_by_samples_' + column, 'variant_id' , "sample_name = '" + sample + "' AND " + column + clause)
        if not_exp:
            return NOT_expression(exp, 'variants', 'variant_id')
        else:
            return exp
    
    def parse_gt_wildcard(self, token):
        
        if token.count('.') != 3 or \
            token.count('[') != 4 or \
            token.count(']') != 4:
            sys.exit("Wildcard filter should consist of 4 elements. Exiting.")
    
        (column, wildcard, wildcard_rule, wildcard_op) = token.split('.')
        column = column.strip('[').strip(']').strip()
        wildcard = wildcard.strip('[').strip(']').strip().replace('==', '=')
        wildcard_rule = wildcard_rule.strip('[').strip(']').strip()
        wildcard_op = wildcard_op.strip('[').strip(']').strip()
        
        if not (wildcard_op.lower().strip() in ['any', 'all', 'none'] or wildcard_op.lower().strip().startswith('count')):
            sys.exit("Unsupported wildcard operation: (%s). Exiting." % wildcard_op)
                    
        sample_names = self._get_matching_sample_ids(wildcard)
    
        # Replace HET, etc. with 1, et.session to avoid eval() issues.
        wildcard_rule = self._swap_genotype_for_number(wildcard_rule)
        wildcard_rule = wildcard_rule.replace('==', '=')
        
        actual_nr_cores = min(len(sample_names), self.nr_cores)
        
        return GT_wildcard_expression(column, wildcard_rule, wildcard_op, sample_names, self.db_contact_points, self.keyspace, actual_nr_cores) 
    
    def _swap_genotype_for_number(self, token):
                
        if any(g in token for g in ['HET', 'HOM_ALT', 'HOM_REF', 'UNKNOWN']):
            token = token.replace('HET', str(HET))
            token = token.replace('HOM_ALT', str(HOM_ALT))
            token = token.replace('HOM_REF', str(HOM_REF))
            token = token.replace('UNKNOWN', str(UNKNOWN))
        return token

    def _split_select(self):
        """
        Build a list of _all_ columns in the SELECT statement
        and segregated the non-genotype specific SELECT columns.

        This is used to control how to report the results, as the
        genotype-specific columns need to be eval()'ed whereas others
        do not.

        For example: "SELECT chrom, start, end, gt_types.1478PC0011"
        will populate the lists as follows:

        select_columns = ['chrom', 'start', 'end']
        all_columns = ['chrom', 'start', 'end', 'gt_types[11]']
        """
        
        self.select_columns = []
        self.all_columns_new = []
        self.all_columns_orig = []

        # iterate through all of the select columns and clear
        # distinguish the genotype-specific columns from the base columns
        if "from" not in self.query.lower():
            sys.exit("Malformed query: expected a FROM keyword.")
        
        tokens_to_be_removed = set()
        for token in self.requested_columns:
            # it is a WILDCARD
            if (token.find("gt") >= 0 or token.find("GT") >= 0) \
                and '.(' in token and ').' in token:
                # break the wildcard into its pieces. That is:
                # (COLUMN).(WILDCARD)
                (column, wildcard) = token.split('.')

                # remove the syntactic parentheses
                wildcard = wildcard.strip('(').strip(')')
                column = column.strip('(').strip(')')

                # convert "gt_types.(affected==1)"
                # to: gt_types[3] == HET and gt_types[9] == HET
                sample_info = self._get_matching_sample_ids(wildcard)

                # maintain a list of the sample indices that should
                # be displayed as a result of the SELECT'ed wildcard
                for sample in sample_info:
                    wildcard_col = column + '_' + sample
                    self.requested_columns.append(wildcard_col)
                tokens_to_be_removed.add(token)
        
        for token in tokens_to_be_removed:
            self.requested_columns.remove(token)
            
    def _info_dict_to_string(self, info):
        """
        Flatten the VCF info-field OrderedDict into a string,
        including all arrays for allelic-level info.
        """
        if info is not None:
            return ';'.join(['%s=%s' % (key, value) if not isinstance(value, list) \
                             else '%s=%s' % (key, ','.join([str(v) for v in value])) \
                             for (key, value) in info.items()])
        else:
            return None

    def _tokenize_query(self):
        tokens = list(flatten([x.split(",") for x in self.query.split(" ")]))
        return tokens

    def _query_needs_genotype_info(self):
        tokens = self._tokenize_query()
        requested_genotype = "variants" in tokens and \
                            (any([x.startswith("gt") for x in tokens]) or \
                             any([x.startswith("(gt") for x in tokens]) or \
                             any(".gt" in x for x in tokens))
        return requested_genotype or \
               self.include_gt_cols or \
               self.show_variant_samples or \
               self.needs_genotypes

def select_formatter(args):
    SUPPORTED_FORMATS = {x.name.lower(): x for x in
                         itersubclasses(RowFormat)}

    if hasattr(args, 'carrier_summary') and args.carrier_summary:
        return SUPPORTED_FORMATS["carrier_summary"](args)

    if not args.format in SUPPORTED_FORMATS:
        raise NotImplementedError("Conversion to %s not supported. Valid "
                                  "formats are %s."
                                  % (args.format, SUPPORTED_FORMATS))
    else:
        return SUPPORTED_FORMATS[args.format](args)


def flatten(l):
    """
    flatten an irregular list of lists
    example: flatten([[[1, 2, 3], [4, 5]], 6]) -> [1, 2, 3, 4, 5, 6]
    lifted from: http://stackoverflow.com/questions/2158395/

    """
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el,
                                                                   basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el
            
def fold(function, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        try:
            initializer = next(it)
        except StopIteration:
            raise TypeError('reduce() of empty sequence with no initial value')
    accum_value = initializer
    for x in it:
        accum_value = function(x, accum_value)
    return accum_value

if __name__ == "__main__":

    db = sys.argv[1]

    gq = GeminiQuery(db)

    print "test a basic query with no genotypes"
    query = "select chrom, start, end from variants limit 5"
    gq.run(query)
    for row in gq:
        print row

    print "test a basic query with no genotypes using a header"
    query = "select chrom, start, end from variants limit 5"
    gq.run(query)
    print gq.header
    for row in gq:
        print row

    print "test query that selects a sample genotype"
    query = "select chrom, start, end, gts.NA20814 from variants limit 5"
    gq.run(query)
    for row in gq:
        print row

    print "test query that selects a sample genotype and uses a header"
    query = "select chrom, start, end, gts.NA20814 from variants limit 5"
    gq.run(query)
    print gq.header
    for row in gq:
        print row

    print "test query that selects and _filters_ on a sample genotype"
    query = "select chrom, start, end, gts.NA20814 from variants limit 50"
    db_filter = "gt_types.NA20814 == HET"
    gq.run(query, db_filter)
    for row in gq:
        print row

    print "test query that selects and _filters_ on a sample genotype and uses a filter"
    query = "select chrom, start, end, gts.NA20814 from variants limit 50"
    db_filter = "gt_types.NA20814 == HET"
    gq.run(query, db_filter)
    print gq.header
    for row in gq:
        print row

    print "test query that selects and _filters_ on a sample genotype and uses a filter and a header"
    query = "select chrom, start, end, gts.NA20814 from variants limit 50"
    db_filter = "gt_types.NA20814 == HET"
    gq.run(query, db_filter)
    print gq.header
    for row in gq:
        print row

    print "demonstrate accessing individual columns"
    query = "select chrom, start, end, gts.NA20814 from variants limit 50"
    db_filter = "gt_types.NA20814 == HET"
    gq.run(query, db_filter)
    for row in gq:
        print row['chrom'], row['start'], row['end'], row['gts.NA20814']
