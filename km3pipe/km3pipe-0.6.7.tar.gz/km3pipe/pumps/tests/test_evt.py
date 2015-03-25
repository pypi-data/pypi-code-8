from __future__ import division, absolute_import, print_function

__author__ = 'tamasgal'

from km3pipe.testing import *
from km3pipe.pumps import EvtPump


class TestEvtParser(TestCase):

    def setUp(self):
        self.valid_evt_header = "\n".join((
            "start_run: 1",
            "cut_nu: 0.100E+03 0.100E+09-0.100E+01 0.100E+01",
            "spectrum: -1.40",
            "end_event:",
            "start_event: 12 1",
            "track_in: 1 -389.951 213.427 516 -0.204562 -0.60399 -0.770293 9.092 0 5 40.998",
            "hit: 1 44675 1 1170.59 5 2 1 1170.59",
            "end_event:",
            "start_event: 13 1",
            "track_in:  1 272.695 -105.613 516 -0.425451 -0.370522 -0.825654 2431.47 0 5 -1380",
            "track_in:  2 272.348 -106.292 516 -0.425451 -0.370522 -0.825654 24670.7 1.33 5 -1484",
            "track_in:  3 279.47 -134.999 516 -0.425451 -0.370522 -0.825654 164.586 26.7 5 601.939",
            "hit: 1 20140 1 1140.06 5 1 1 1140.06",
            "hit: 2 20159 1 1177.14 5 1 1 1177.14",
            "hit: 3 20164 1 1178.19 5 1 1 1178.19",
            "hit: 4 20170 1 1177.23 5 1 1 1177.23",
            "hit: 5 20171 2 1177.25 5 1 2 1177.25",
            "end_event:",
            "start_event: 14 1",
            "track_in:  1 40.256 -639.888 516 0.185998 0.476123 -0.859483 10016.1 0 5 -1668",
            "hit: 1 33788 1 2202.81 5 1 1 2202.81",
            "hit: 2 33801 1 2248.95 5 1 1 2248.95",
            "hit: 3 33814 1 2249.2 5 1 1 2249.2",
            "end_event:"
        ))
        self.no_evt_header = "\n".join((
            "start_event: 12 1",
            "track_in: 1 -389.951 213.427 516 -0.204562 -0.60399 -0.770293 9.092 0 5 40.998",
            "hit: 1 44675 1 1170.59 5 2 1 1170.59",
            "end_event:",
            "start_event: 13 1",
            "track_in:  1 272.695 -105.613 516 -0.425451 -0.370522 -0.825654 2431.47 0 5 -1380",
            "track_in:  2 272.348 -106.292 516 -0.425451 -0.370522 -0.825654 24670.7 1.33 5 -1484",
            "track_in:  3 279.47 -134.999 516 -0.425451 -0.370522 -0.825654 164.586 26.7 5 601.939",
            "hit: 1 20140 1 1140.06 5 1 1 1140.06",
            "hit: 2 20159 1 1177.14 5 1 1 1177.14",
            "hit: 3 20164 1 1178.19 5 1 1 1178.19",
            "hit: 4 20170 1 1177.23 5 1 1 1177.23",
            "hit: 5 20171 2 1177.25 5 1 2 1177.25",
            "end_event:",
            "start_event: 14 1",
            "track_in:  1 40.256 -639.888 516 0.185998 0.476123 -0.859483 10016.1 0 5 -1668",
            "hit: 1 33788 1 2202.81 5 1 1 2202.81",
            "hit: 2 33801 1 2248.95 5 1 1 2248.95",
            "hit: 3 33814 1 2249.2 5 1 1 2249.2",
            "end_event:"
        ))
        self.corrupt_evt_header = "foo"

        self.pump = EvtPump()
        self.pump.blob_file = StringIO(self.valid_evt_header)

    def tearDown(self):
        self.pump.blob_file.close()

    def test_parse_header(self):
        raw_header = self.pump.extract_header()
        self.assertEqual(['1'], raw_header['start_run'])
        self.assertAlmostEqual(-1.4, float(raw_header['spectrum'][0]))
        self.assertAlmostEqual(1, float(raw_header['cut_nu'][2]))

#    def test_incomplete_header_raises_value_error(self):
#        temp_file = StringIO(self.corrupt_evt_header)
#        pump = EvtPump()
#        pump.blob_file = temp_file
#        with self.assertRaises(ValueError):
#            pump.extract_header()
#        temp_file.close()

    def test_record_offset_saves_correct_offset(self):
        self.pump.blob_file = StringIO('a'*42)
        offsets = [1, 4, 9, 12, 23]
        for offset in offsets:
            self.pump.blob_file.seek(0, 0)
            self.pump.blob_file.seek(offset, 0)
            self.pump._record_offset()
        self.assertListEqual(offsets, self.pump.event_offsets)

    def test_event_offset_is_at_first_event_after_parsing_header(self):
        raw_header = self.pump.extract_header()
        self.assertEqual(88, self.pump.event_offsets[0])

    def test_rebuild_offsets(self):
        self.pump.extract_header()
        self.pump._cache_offsets()
        self.assertListEqual([88, 233, 700], self.pump.event_offsets)

    def test_rebuild_offsets_without_header(self):
        self.pump.blob_file = StringIO(self.no_evt_header)
        self.pump.extract_header()
        self.pump._cache_offsets()
        self.assertListEqual([0, 145, 612], self.pump.event_offsets)

    def test_cache_enabled_triggers_rebuild_offsets(self):
        self.pump.cache_enabled = True
        self.pump.prepare_blobs()
        self.assertEqual(3, len(self.pump.event_offsets))

    def test_cache_disabled_doesnt_trigger_cache_offsets(self):
        self.pump.cache_enabled = False
        self.pump.prepare_blobs()
        self.assertEqual(1, len(self.pump.event_offsets))

    def test_get_blob_triggers_cache_offsets_if_cache_disabled_and_asking_for_not_indexed_event(self):
        self.pump.cache_enabled = False
        self.pump.prepare_blobs()
        self.assertEqual(1, len(self.pump.event_offsets))
        blob = self.pump.get_blob(2)
        self.assertListEqual(['14', '1'], blob['start_event'])
        self.assertEqual(3, len(self.pump.event_offsets))

    def test_get_blob_raises_index_error_for_wrong_index(self):
        self.pump.prepare_blobs()
        with self.assertRaises(IndexError):
            self.pump.get_blob(23)

    def test_get_blob_returns_correct_event_information(self):
        self.pump.prepare_blobs()
        blob = self.pump.get_blob(0)
        self.assertTrue(blob.has_key('raw_header'))
        self.assertEqual(['1'], blob['raw_header']['start_run'])
        self.assertListEqual(['12', '1'], blob['start_event'])
        self.assertListEqual([[1.0, 44675.0, 1.0, 1170.59, 5.0, 2.0, 1.0, 1170.59]],
                             blob['hit'])

    def test_get_blob_returns_correct_events(self):
        self.pump.prepare_blobs()
        blob = self.pump.get_blob(0)
        self.assertListEqual(['12', '1'], blob['start_event'])
        blob = self.pump.get_blob(2)
        self.assertListEqual(['14', '1'], blob['start_event'])
        blob = self.pump.get_blob(1)
        self.assertListEqual(['13', '1'], blob['start_event'])

    def test_process_returns_correct_blobs(self):
        self.pump.prepare_blobs()
        blob = self.pump.process()
        self.assertListEqual(['12', '1'], blob['start_event'])
        blob = self.pump.process()
        self.assertListEqual(['13', '1'], blob['start_event'])
        blob = self.pump.process()
        self.assertListEqual(['14', '1'], blob['start_event'])

    def test_process_raises_stop_iteration_if_eof_reached(self):
        self.pump.prepare_blobs()
        self.pump.process()
        self.pump.process()
        self.pump.process()
        with self.assertRaises(StopIteration):
            self.pump.process()

    def test_pump_acts_as_iterator(self):
        self.pump.prepare_blobs()
        event_numbers = []
        for blob in self.pump:
            event_numbers.append(blob['start_event'][0])
        self.assertListEqual(['12', '13', '14'], event_numbers)

