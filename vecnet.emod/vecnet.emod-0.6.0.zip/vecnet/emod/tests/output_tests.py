import os
import unittest
from vecnet.emod.output.binnedreport import BinnedReport

base_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(base_dir, "output")

class Tests(unittest.TestCase):

    def setUp(self):
        pass

    def test_2(self):
        vector_species_report = BinnedReport(os.path.join(base_dir, "2", "VectorSpeciesReport.json"))
        self.assertEqual(vector_species_report.channels, [u'Adult Vectors',
                                                          u'Daily EIR',
                                                          u'Daily HBR',
                                                          u'Infectious Vectors'])
        self.assertEqual(vector_species_report.get_axis_number("Vector Species"), 0)
        self.assertEqual(vector_species_report.get_meanings_per_axis("Vector Species"), [u'farauti'])
        self.assertEqual(sum(vector_species_report.get_data('Adult Vectors', "Vector Species", 'farauti')), 1034462.0)
        self.assertEqual(vector_species_report.axis, ["Vector Species"])
        self.assertRaises(KeyError,
                          vector_species_report.get_data,
                          'Adult Vectors', "Vector Species", 'non-existing species')
        self.assertRaises(KeyError,
                          vector_species_report.get_data,
                          'Adult Vectors', "non-existing axis", 'farauti')
        self.assertIsNone(vector_species_report.get_units(u'Daily EIR'))
