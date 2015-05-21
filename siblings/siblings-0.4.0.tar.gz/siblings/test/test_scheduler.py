from __future__ import print_function, absolute_import
import random
import shutil
import unittest
import tempfile
import os

from ..scheduler import *

data = [{'NCBITaxonId': 9999, 'UniProtSpeciesCode': 'Test1', 'SciName': 'Test Species 1',
         'Release': 'test_v1',
         'xrefs': [('P11144', 'Ensembl Protein', 'ENSP253232'),
             ('P11144', 'GI', '15243233')],
         'Entries':[{'Id': 'P11144', 'Sequence': 'ADRIAN', 'cDNA': 'GCAGACAGAATAGCAAAC'},
                   {'Id': 'P12321', 'Sequence': 'ADRIAAAN', 'cDNA': 'GCAGACAGAATAGCAGCAGCAAAC'}]},
        {'NCBITaxonId': 9122, 'UniProtSpeciesCode': 'Test2', 'SciName': 'Test Species 2',
         'Release': 'v1: 22-12-2015',
         'xrefs': [('NP2111', 'UniProtKB/SwissProt', 'P14412_TEST2'),
             ('NP21444', 'EntrezGene', '34222')],
         'Entries':[{'Id': 'NP2111', 'Sequence': 'GCANLVSRLE', 'cDNA': 'GGATGCGCAAACCTAGTAAGCAGACTAGAA'},
                    {'Id': 'NP21444', 'Sequence': 'NNSRLLNRDL', 'cDNA': 'AACAACAGCAGACTACTAAACAGAGACCTA'},
                    {'Sequence': 'IAVTIGAIVY', 'cDNA': 'ATAGCAGTAACAATAGGAGCAATAGTATAC'}]}]

class TestGenomeAdder(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        fn = os.path.join(self.dir, 'main.h5')
        self.writer = Writer(fn, {})

    def tearDown(self):
        self.writer.close()
        shutil.rmtree(self.dir)

    def test_add_genome(self):
        self.writer.add_genome(data[0])
        self.writer.init_db()
        self.assertEqual(len(list(self.writer.find_missing_alignments())), 1)
        gs = self.writer._get_node('summarytab')
        self.assertEqual(len(gs), 1)
        self.assertEqual(gs[0]['TotEntries'], len(data[0]['Entries']))
        try:
            genome = self.writer._get_node('/Genomes/tax{0:d}'.format(data[0]['NCBITaxonId']))
            en1 = genome.Entries[0]
            self.assertEqual(en1['CanonicalId'], data[0]['Entries'][0]['Id'])
            self.assertEqual(genome.SequenceBuffer[en1['SequenceBufferOffset']:
                                                   en1['SequenceBufferOffset']+en1['SequenceBufferLength']]
                             .tostring(),
                             data[0]['Entries'][0]['Sequence'])
        except Exception as e:
            self.assertTrue(False, 'cannot access genome db')


class TestScheduler(TestGenomeAdder):
    def setUp(self):
        super(TestScheduler, self).setUp()
        for genome in data:
            self.writer.add_genome(genome)

    def test_pairstat_status(self):
        tab = self.writer._get_node('pairstattab')
        enum = tab.get_enum('Status')
        self.assertEqual(tab[0]['Status'], enum.NEW)
        self.writer.add_genomepair_to_jobqueue(
            tab[0]['Genome1'], tab[0]['Genome2'])
        req = self.writer._next_request()
        self.assertEqual(tab[0]['Status'], enum.QUEUED)
        reply = {'rID': req.rID, 'genome1': req.genome1, 'genome2': req.genome2,
                 'matches': numpy.array([(1,2,999,21,1,5,2,5,222,-21,88,251,22,111,75)],
                                        dtype=tables.dtype_from_descr(MatchesTableFmt))}
        self.writer.store_reply(reply)
        self.assertEqual(tab[0]['Status'], enum.COMPUTED)

    def test_queue_generator(self):
        # check whether all pairs are queued for queueing
        missing_alignments = list(self.writer.find_missing_alignments())
        expected_nr_pairs = len(data)*(len(data)+1)/2
        self.assertEqual(len(missing_alignments), expected_nr_pairs)
        for g1, g2 in missing_alignments:
            self.writer.add_genomepair_to_jobqueue(g1, g2)
        last_req = None
        for i in range(expected_nr_pairs):
            req = self.writer._next_request()
            if not last_req is None:
                self.assertNotEqual(req.rID, last_req.rID)
            last_req = req
            for d1 in data:
                if d1['NCBITaxonId'] == req.genome1:
                    seqs1 = [z['Sequence'] for z in d1['Entries']]
                    for p in req.group1:
                        self.assertIn(p['seq'], seqs1)
                    break
            for d2 in data:
                if d2['NCBITaxonId'] == req.genome2:
                    seqs2 = [z['Sequence'] for z in d2['Entries']]
                    for p in req.group2:
                        self.assertIn(p['seq'], seqs2)
                    break
        self.assertRaises(QueueEmptyError, self.writer._next_request)

    def test_add_genome(self):
        self.assertRaises(ImportDataError, self.writer.add_genome, data[0])

    def test_timing_stats(self):
        tot = collections.defaultdict(int)
        users = ['cbrg', 'ucl', 'xxx']
        hosts = ['mir', 'linneus52', 'h332.bla.somehost.longdomname.ch']
        fieldlen = 20
        for run in range(10):
            rep = {'user': random.choice(users), 'host': random.choice(hosts),
                   'cputime': random.random()*300}
            tot[(rep['user'][0:fieldlen], rep['host'][0:fieldlen])] += rep['cputime']
            self.writer._update_timingstats(rep)
        for row in self.writer._get_node('timingtab'):
            expected_time = tot[(row['User'], row['Host'])]
            self.assertAlmostEqual(row['Total_time'], expected_time, delta=expected_time*1e-7,
                                   msg='computing time differs for {}/{}: {} != {} (delta {})'
                                   .format(row['User'], row['Host'], row['Total_time'], expected_time,
                                           expected_time * 1e-7))

    def test_mark_error(self):
        self.writer.MAX_RETRY_ON_ERROR = 2
        self.writer.TIMEOUT = 0
        for i, (g1, g2) in enumerate(self.writer.find_missing_alignments()):
            self.writer.add_genomepair_to_jobqueue(g1, g2)
            if i > 1:
                break
        last_req = None
        for i in range(self.writer.MAX_RETRY_ON_ERROR + 5):
            req = self.writer._next_request()
            self.writer.mark_job_as_error(req.rID)
            if last_req and last_req.rID != req.rID:
                break
            last_req = req
        self.assertEqual(i, self.writer.MAX_RETRY_ON_ERROR + 1, "unexpected number of retry of failed jobs")