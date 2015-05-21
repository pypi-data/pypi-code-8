import unittest
import tables
import numpy as np
import siblings
import tempfile
import os
from ..tablesformat import *

# functions to initialize and destroy sample hdf5 files of the right structure
NR_GENOMES = 2
NR_PROTEINS = 3


def setup_h5file(fn):
    f = tb.open_file(fn, 'w', tables.Filters(complevel=5, complib='zlib', fletcher32=True))
    gs = f.create_table('/Genomes', 'Summaries', Genome, createparents=True)
    xref = f.create_table('/Genomes', 'XRefs', XRef, createparents=True)

    mgs = dict()
    for i in range(1, NR_GENOMES + 1):
        tax = 1000 + i
        mgs[tax] = f.create_group('/Matches', "tax{0:d}".format(tax), createparents=True)

        fg = tb.open_file(tempfile.mktemp(suffix=".h5"), 'w')
        protein_node = fg.create_group('/', 'Proteins')
        protein_row = fg.create_table(protein_node, 'Entries', Protein).row
        seq_arr = fg.create_earray(protein_node, 'SequenceBuffer', tb.StringAtom(1), (0,))
        dna_arr = fg.create_earray(protein_node, 'DNABuffer', tb.StringAtom(1), (0,))
        off = 0
        for nr in range(1, NR_PROTEINS + 1):
            protein_row['EntryNr'] = nr
            protein_row['SequenceBufferOffset'] = off
            protein_row['SequenceBufferLength'] = 10 * nr
            protein_row['DNABufferOffset'] = 3 * off
            protein_row['DNABufferLength'] = 3 * 10 * nr
            protein_row.append()
            aa_seq = str(chr(nr + i + 64)) * (10 * nr)
            dna_seq = str(chr(nr + i + 64)) * (30 * nr)
            seq_arr.append(np.ndarray((10 * nr,), buffer=aa_seq.encode('ascii'),
                                     dtype=tb.StringAtom(1)))
            dna_arr.append(np.ndarray((30 * nr,), buffer=dna_seq.encode('ascii'),
                                     dtype=tb.StringAtom(1)))

            xref_row = xref.row
            sources = dict(xref.get_enum('XRefSource'))
            for source in list(sources.keys()):
                xref_row['NCBITaxonId'] = tax
                xref_row['EntryNr'] = nr
                xref_row['XRefSource'] = sources[source]
                xref_row['XRefId'] = source + ":" + str(nr)
                xref_row.append()
        f.create_external_link('/Genomes', "tax{0:d}".format(tax), protein_node)
        seq_arr.flush
        dna_arr.flush
        fg.close()

        gs_row = gs.row
        gs_row['NCBITaxonId'] = tax
        gs_row['UniProtSpeciesCode'] = "SYNG" + str(i)
        gs_row['SciName'] = "Synthetic genome " + str(i)
        gs_row['TotEntries'] = NR_PROTEINS
        gs_row['DBRelease'] = "0.99"
        gs_row.append()

        for j in range(1, i + 1):
            mf = tb.open_file(tempfile.mktemp(suffix=".h5"), 'w')
            mg = mf.create_table('/', 'tax%d_tax%d' % (1000 + j, 1000 + i), Matches)
            match_row = mg.row
            for k in range(i - j, NR_PROTEINS + 1):
                match_row['EntryNr1'] = (k - j % NR_PROTEINS) + 1
                match_row['EntryNr2'] = k + 1
                match_row['Score'] = 300 // (k + 1 - i + j)
                match_row['PamDistance'] = 20 * (k + 1 - i + j) // 300
                match_row['PamVariance'] = 40
                match_row['Start1'] = 1 + k
                match_row['End1'] = 10 * i
                match_row['Start2'] = 1 + 2 * k
                match_row['End2'] = 10 * i
                match_row.append()
            mf.set_node_attr(mg, 'g1', 1000 + j)
            mf.set_node_attr(mg, 'g2', 1000 + i)
            mg.flush()
            f.create_external_link('/Matches/tax{}'.format(1000 + j),
                                   "tax{}".format(tax), mg)
            if i != j:
                f.create_external_link('/Matches/tax{}'.format(tax),
                                       "tax{}".format(1000 + j), mg)
            mf.close()
    f.close()


def destroy_h5file(fn):
    f = tb.open_file(fn, "r")
    # extract file names and put in set (remove duplicates)
    files_to_rem = set([z.target.split(":")[0] for z in
                        f.walk_nodes(classname="ExternalLink")])
    for lnk in files_to_rem:
        os.unlink(lnk)
    f.close()
    os.unlink(fn)


class ToyExampleTestCase(unittest.TestCase):
    _filename = None

    @classmethod
    def setUpClass(cls):
        cls._filename = tempfile.mktemp(suffix=".h5")
        setup_h5file(cls._filename)

    @classmethod
    def tearDownClass(cls):
        destroy_h5file(cls._filename)

    def setUp(self):
        self._reader = siblings.Reader(self._filename)

    def tearDown(self):
        self._reader.close()


class ReaderTester(ToyExampleTestCase):
    def test_genomes(self):
        genomes = self._reader.genomesid
        expected = [1000 + z for z in range(1, NR_GENOMES + 1)]
        self.assertListEqual(genomes, expected)

    def test_get_matches_simple(self):
        res = self._reader.get_matches_between_genomes(1001, 1002)
        # expected = [(1,2,300.0,0.0,2,20,3,20,40.0,0,0),(2,3,150.0,0.0,3,20,5,20,40.0,0,0),
        # (3,4,100.0,0.0,4,20,7,20,40.0,0,0)]
        col = siblings.enum(*res['colnames'])
        self.assertEqual(len(res['data']), 3)
        for (i, row) in enumerate(res['data']):
            self.assertTrue((row[col.EntryNr1] == i + 1) and
                            (row[col.EntryNr2] == i + 2) and (row[col.Score] == 300 / (i + 1)))

    def test_get_matches_with_filter(self):
        filters = ['2>EntryNr1', 'Score<200 & Score>100', 'Start2>Start1 & Start2>5']
        for i, f in enumerate(filters):
            filter_obj = self._reader.query_filter(f)
            res = self._reader.get_matches_between_genomes(1001, 1002, filter_obj=filter_obj)
            self.assertEqual(len(res['data']), 1)
            col = siblings.enum(*res['colnames'])
            row = res['data'][0]
            self.assertTrue((row[col.EntryNr1 == i + 1]) and (row[col.EntryNr2] == i + 2)
                            and (row[col.Score] == 300 / (i + 1)) and (row[col.Start2] == 2 * i + 3))

    def test_get_matches_reversed_genomeorder_and_filter(self):
        filters = ['2>EntryNr2', 'Score<200 & Score>100', 'Start2<Start1 & Start1>5']
        for i, f in enumerate(filters):
            filter_obj = self._reader.query_filter(f)
            res = self._reader.get_matches_between_genomes(1002, 1001, filter_obj=filter_obj)
            self.assertEqual(len(res['data']), 1)
            col = siblings.enum(*res['colnames'])
            row = res['data'][0]
            self.assertTrue((row[col.EntryNr2 == i + 1]) and (row[col.EntryNr1] == i + 2)
                            and (row[col.Score] == 300 / (i + 1)) and (row[col.Start1] == 2 * i + 3))

    def test_xrefmapping(self):
        f = siblings.QueryFilter('Score<200 & Score>100')
        idtype = self._reader.returnid_factory('Ensembl Gene', 'WikiGene')
        res = self._reader.get_matches_between_genomes(1002, 1001, filter_obj=f, returnid=idtype)
        self.assertEqual(res['data'][0][0], ('Ensembl Gene:' + str(3)).encode('ascii'))

    def test_get_homologs(self):
        filters = [None, 'Score<200 & Score>100', 'EntryNr2 < EntryNr1']
        for i, cur_filter in enumerate(filters):
            filter_obj = siblings.QueryFilter(cur_filter)
            res = self._reader.get_homologs_of_gene(1001, 1, filter_obj=filter_obj)
            self.assertEqual(len(res['data']), 2 - i)
            for z in res['data']:
                self.assertEqual(z[0], 1)

    def test_sequence(self):
        self.assertEqual(1, 1)


class XRefId(ToyExampleTestCase):
    def test_invalid_xreftype(self):
        self.assertRaises(KeyError, self._reader.returnid_factory, 'UniProt', 'Ensembl')

    def test_map2xrefs(self):
        prim = 'UniProtKB/TrEMBL';
        idtype = self._reader.returnid_factory(prim, 'SourceID')
        t = idtype.convert_ids([(1, 2, 3), (2, 3, 4)], 0, 1001)
        for i, z in enumerate(t):
            self.assertEqual(z[0], (prim + ":" + str(i + 1)).encode('ascii'))


class GenomeOrderSwapperTester(ToyExampleTestCase):
    def test_matches_cols(self):
        swapper = self._reader.orderSwapper
        for col in Matches.columns.keys():
            self.assertEqual(swapper.columns[col], Matches.columns.get(col)._v_pos,
                             'column ordering for ' + col + 'does not match')

    def test_cols_to_swap(self):
        swapper = self._reader.orderSwapper
        queries = {"EntryNr1": "EntryNr2", "Score": "Score", "Start2": "Start1"}
        for q in queries:
            self.assertEqual(swapper.swap_column_name(q), queries[q])


class QueryTester(ToyExampleTestCase):
    def test_simple_query(self):
        queries = {"EntryNr1==1": "(EntryNr1 == 1)", "EntryNr2 == 5": "(EntryNr2 == 5)",
                   "PamDistance <6": "(PamDistance < 6)", "Score>=12.651": "(Score >= 12.651)"}
        formatter = siblings.KernelQueryVisitor(self._reader.orderSwapper)
        for q in queries.keys():
            query = siblings.QueryFilter(q)
            formatter.visit(query)
            fmt = formatter.get_formatted_query()
            self.assertEqual(fmt, queries[q], 'failed for ' + queries[q] + ": " + fmt)

    def test_reverse_cols(self):
        queries = {'500<EntryNr1': '(EntryNr1 > 500)', '32.5 <= Score': '(Score >= 32.5)',
                   '40 == PamDistance': '(PamDistance == 40)'}
        formatter = siblings.KernelQueryVisitor(self._reader.orderSwapper)
        for q in queries.keys():
            query = siblings.QueryFilter(q)
            formatter.visit(query)
            fmt = formatter.get_formatted_query()
            self.assertEqual(fmt, queries[q], 'failed for ' + queries[q] + ": " + fmt)

    def test_swap_cols(self):
        queries = {'500<EntryNr1': '(EntryNr2 > 500)', '32.5 <= Score': '(Score >= 32.5)',
                   'EntryNr1 == PamDistance': '(EntryNr2 == PamDistance)'}
        formatter = siblings.KernelQueryVisitor(self._reader.orderSwapper, swap=True)
        for q in queries.keys():
            query = siblings.QueryFilter(q)
            formatter.visit(query)
            fmt = formatter.get_formatted_query()
            self.assertEqual(fmt, queries[q], 'failed for ' + queries[q] + ": " + fmt)
