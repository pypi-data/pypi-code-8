import collections
import tables as tb
import numpy as np
import numpy.lib.recfunctions as rfc
import logging
import re
from contextlib import contextmanager

from .common import package_logger
from .visit import *
from .tablesformat import Matches as MatchesTableFmt



def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


def swap_columns(data, swapCols):
    """function to swap a set of column pairs in the data array"""
    for z in data:
        for swap in swapCols:
            z[swap[0]], z[swap[1]] = z[swap[1]], z[swap[0]]


def reverse_operator(op):
    """adjusted operators for reversed lhs and rhs"""
    if op == '<':
        rev = '>'
    elif op == '<=':
        rev = '>='
    elif op == '>':
        rev = '<'
    elif op == '>=':
        rev = '<='
    elif op in {'==', '!=', '&', '|', 'in'}:
        rev = op
    else:
        raise Exception(u"operator not implemented")
    return rev


class KernelFilterNotSupported(Exception):
    pass


class QueryFilter(object):
    def __init__(self, condition_str=None):
        self.conditions = []
        if condition_str is not None:
            for condition in condition_str.split('&'):
                self.append_condition(condition)

    def append_condition(self, condition):
        match = re.match(r'\s*([\w.]+)\s*([<=>!]{1,2}|in)\s*([\w.]+)\s*', condition)
        if match is None:
            raise KernelFilterNotSupported(u'cannot parse condition "{0:s}"'.format(condition))

        tup = match.groups()
        self.conditions.append(Condition(*tup))


class Condition(object):
    def __init__(self, col, operator, comp):
        if col.isalnum() and not col.isdigit():
            # col argument seems to be column identifier
            self.col, self.comp, self.op = col, comp, operator
        elif comp.isalnum() and not comp.isdigit():
            # comp argument seems to be a column identifier, but col not. swap them, reverse operator
            self.col, self.comp = comp, col
            self.op = reverse_operator(operator)


class GenomeOrderSwapper(object):
    """This class handles the swapping of column ids, column position and QueryFilters
    introduced by the ordering of the matches columns."""

    def __init__(self, cols):
        self.columns = dict(zip(cols, range(len(cols))))

        def _swap_nr(name):
            res = name
            if name[-1].isdigit():
                nr = int(name[-1])
                assert (1 <= nr <= 2)
                res = name[0:-1] + str(3 - nr)
            return res

        self.swapCols = dict(zip(cols, map(_swap_nr, cols)))
        self.swapColNrs = [self.columns[_swap_nr(val)] for val in cols]
        self.swapNrs = [(self.columns[key], self.columns[val]) for key, val in self.swapCols.items()
                        if self.columns[key] < self.columns[val]]

    def swap_columns_in_matches(self, data):
        """ function to swap the columns in the matches array"""
        for i in range(len(data)):
            data[i] = tuple([data[i][z] for z in self.swapColNrs])

    def swap_column_name(self, name):
        return self.swapCols[name]


class KernelQueryVisitor(object):
    def __init__(self, swap_handler, swap=False):
        self.swapper = swap_handler
        self.do_swap = swap
        self.op_stack = []
        self.queries = []

    def push_operator(self, op):
        self.op_stack.append(op)

    def pop_operator(self):
        try:
            op = self.op_stack.pop()
            if len(self.queries) > 1:
                combined = op.join(self.queries)
                self.queries = [combined]
        except IndexError:
            raise IndexError(u"cannot pop from empty operator stack in KernelQueryVisitor")

    @on('node')
    def visit(self, node):
        pass

    @when(Condition)
    def visit(self, node):
        if node.op == "in":
            raise KernelFilterNotSupported("'in' operator not supported")
        if not self.do_swap:
            self.queries.append("({0:s} {1:s} {2:s})".format(node.col, node.op, node.comp))
        else:
            swapped_col = self.swapper.swap_column_name(node.col)
            swapped_comp = node.comp
            if swapped_comp.isalnum() and not swapped_comp.isdigit():
                swapped_comp = self.swapper.swap_column_name(swapped_comp)

            self.queries.append("({0:s} {1:s} {2:s})".format(swapped_col, node.op, swapped_comp))

    @when(QueryFilter)
    def visit(self, node):
        self.push_operator('&')
        for condition in node.conditions:
            self.visit(condition)
        self.pop_operator()


    def get_formatted_query(self):
        if len(self.op_stack) > 0 or len(self.queries) != 1:
            raise Exception("malformed query")
        return self.queries.pop()


class NotFound(Exception):
    pass

class Reader(object):
    """ This is the main database class. It handles queries to the hdf5 siblings files"""

    def __init__(self, filename, mode='r', logger=None):
        self.logger = logger if logger is not None else package_logger
        self._fh = tb.open_file(filename, mode)
        self.logger.info(u"File {0:s} opened (mode: {1:s})".format(filename, mode))
        self.orderSwapper = GenomeOrderSwapper(self.columnnames)

    def close(self):
        self.logger.info(u"closing main hdf5 file")
        self._fh.close()
        self._fh = None

    @property
    def genomesid(self):
        """returns the NCBI Taxonomy ID for all available genomes.

        This is the internal Siblings genomes ID. See :py:meth:`get_genomes`
        for a method to access summary information on the genomes."""
        return self._fh.get_node(u'/Genomes/Summaries').cols.NCBITaxonId[:].tolist()

    def get_genomes(self, columns=None):
        """Returns summary information on the available genomes.

        This method returns summary information in the form of a :py:class:`numpy.ndarray`.
        The returned columns are

        * ``NCBITaxonId``, the internal (stable) ID for the genome as
          assigned by NCBI.
        * ``TotEntries``, the number of proteins in the genome
        * ``SciName``, the scientific name of the genome
        * ``DBRelease``, the source and release information (e.g. source
          of genome, assembly build and release date or version).
        * ``UniProtSpeciesCode``, a (usually) 5-letter code for the species,
          managed and assigned by the UniProt consortium.

        :returns: :class:`numpy.ndarray`
        """
        data = self._fh.get_node('/Genomes/Summaries').read()
        if not columns is None:
            data = data[columns]
        return data

    @property
    def columnnames(self):
        """Returns all the column names of the Matches table"""
        return tb.dtype_from_descr(MatchesTableFmt).names

    @staticmethod
    def query_filter(filter_str):
        """Converts a query string into a QueryFilter object

        This is a convenience method which creates a :py:class:`QueryFilter` object
        to work with.

        :return: a QueryFilter object"""
        return QueryFilter(filter_str)

    def returnid_factory(self, primary, fallback):
        """creates the necessary objects to retrieve matches with the desired type of Ids"""
        return ReturnIdType(self._fh.get_node('/Genomes/XRefs'), primary, fallback)

    def get_matches_between_genomes(self, genome1, genome2, filter_obj=None, returnid=None, **kw):
        """
        This method returns the matches between a genome pair fulfilling the
        filtering criterions. the returned ids are simply the EntryNr in the 
        respective genomes.
        """
        self.logger.debug(u"started method get_matches_between_genomes call")
        try:
            tab = self._fh.get_node(u"/Matches/tax{0:d}/tax{1:d}".format(genome1, genome2))()
        except tb.NoSuchNodeError:
            raise NotFound(u"Invalid genome pair {}/{}".format(genome1, genome2))
        res = {'colnames': tab.colnames}
        swap_order = tab.get_attr('g1') != genome1
        if filter_obj is None:
            res['data'] = tab[:].tolist()
        else:
            query_formatter = KernelQueryVisitor(self.orderSwapper, swap_order)
            query_formatter.visit(filter_obj)
            fmt = query_formatter.get_formatted_query()
            res['data'] = [tuple(row[:]) for row in tab.where(fmt)]
        if swap_order:
            self.orderSwapper.swap_columns_in_matches(res['data'])

        if returnid is not None:
            res['data'] = returnid.convert_ids(res['data'], self.orderSwapper.columns['EntryNr1'], genome1)
            res['data'] = returnid.convert_ids(res['data'], self.orderSwapper.columns['EntryNr2'], genome2)
        tab._v_file.close()
        self.logger.debug(u"ended method get_matches_between_genomes call")
        return res

    def get_homologs_of_gene(self, genome, entry, filter_obj=QueryFilter(), returnid=None, **kw):
        """Returns all homologs for a given query gene in all other species.

        :param genome: the NCBITaxonomy entry of the query gene's genome.
        :param entry: the entry number of the query gene.
        :param filter_obj: a filtering object py::siblings::db::QueryFilter to
          select subsets of all possible matches, i.e. to select with a more
          stringent parameter set.
        :param retrunid: a ReturnIdType object to convert internal entry numbers
          to some supported xref ids.
        """
        self.logger.debug(u"entered method get_homologs_of_gene")
        res_list = []

        filter_obj.append_condition(u"EntryNr1 == {0:d}".format(entry))
        for g in self.genomesid:
            matches_in_genome = self.get_matches_between_genomes(genome, g, filter_obj=filter_obj, returnid=returnid)
            res_list.extend(matches_in_genome['data'])

        res = {'data': res_list, 'fields': matches_in_genome['colnames']}
        self.logger.debug("finished get_homologs_of_gene")
        return res

    def get_genome_sequences(self, genome, cDNA=False, entry_nrs=None):
        """Get the protein sequences of a query genome.

        The method returns a list of dicts with the protein sequence and
        -- if selected with the boolean flag cdna -- the coding DNA
        sequence for a set of selected entries.

        :param int genome: the NCBI taxonomy id of the query genome.
        :param entry_nrs: the query entry numbers. By default, all entry
         numbers are returned.
        :param bool cdna: boolean flag whether or not the corresponding cDNA
         sequences should be returned.
        :return: a list of dicts ``EntryNr``, ``Sequence`` and
         ``cDNA`` elements for the requested entry numbers.
        """
        try:
            genome_node = self._fh.get_node('/Genomes/tax{0:d}'.format(genome))()
        except (ValueError, tb.NoSuchNodeError):
            raise NotFound(u"Invalid genome {}".format(genome))
        seqbuf = genome_node.SequenceBuffer
        dnabuf = genome_node.DNABuffer
        res = []
        for row in genome_node.Entries.iterrows():
            if (entry_nrs is None) or row['EntryNr'] in entry_nrs:
                el = dict(EntryNr=row['EntryNr'], Sequence=seqbuf[row['SequenceBufferOffset']:
                    row['SequenceBufferOffset'] + row['SequenceBufferLength']].tostring())
                if cDNA:
                    el['cDNA'] = dnabuf[row['DNABufferOffset']:row['DNABufferOffset']+row['DNABufferLength']].tostring()
                res.append(el)
        genome_node._v_file.close()
        return res

    def mapSpecies(self, query):
        pass

    def get_timings_stats(self):
        timings = collections.defaultdict(list)
        for row in self._fh.get_node('/stats/timings'):
            timings[row['User']].append(
                {'host': row['Host'], 'jobs': row['Total_nr_jobs'],
                 'time_tot': row['Total_time'],
                 'time_job': {'avg': row['Total_time']/row['Total_nr_jobs'],
                              'var': (row['Total_time']**2 - row['Total_time2'])/row['Total_nr_jobs']}})
        return timings


class ReturnIdType(object):
    """the minimum number of matches requested to convert necessary to prefetch
    all xrefs of that species"""
    MIN_FETCH_ALL = 1000

    def __init__(self, tab, primary, fallback=None):
        xref_enum = tab.get_enum('XRefSource');
        self.primary = self.fallback = xref_enum[primary]
        if fallback is not None:
            self.fallback = xref_enum[fallback]
        self.xref_tab = tab

    def fetch_xrefs(self, nrs, genome):
        id_map = dict()
        rows = self.xref_tab.where(
            '(NCBITaxonId==%d) & ((XRefSource==%d) | (XRefSource==%d))' %
            (genome, self.primary, self.fallback))
        for row in rows:
            if row['XRefSource'] == self.primary or row['EntryNr'] not in id_map:
                id_map[row['EntryNr']] = row['XRefId']
        return id_map

    def convert_ids(self, data, col, genome):
        id_map = self.fetch_xrefs(frozenset(z[col] for z in data), genome)
        new = [(z[0:col] + (id_map[z[col]],) + z[col + 1:]) for z in data if id_map[z[col]] is not None]
        return new
