import bootstrap
import unittest

from cifparser.valuetree import ValueTree, dump, load
from cifparser.path import ROOT_PATH, make_path

class TestValueTreeDumpLoad(unittest.TestCase):

    def test_load_valuetree_from_dict(self):
        "A ValueTree should load from a dict"
        obj = {
            'field1': 'value1',
            'field2': ['item1', 'item2', 'item3'],
            'object1': {
                'field3': 'value3',
                'field4': ['item4', 'item5'],
                },
            }
        values = load(obj)
        self.assertEqual(values.get_field(ROOT_PATH, 'field1'), 'value1')
        self.assertListEqual(values.get_field_list(ROOT_PATH, 'field2'),
                             ['item1', 'item2', 'item3'])
        self.assertTrue(values.contains_container(make_path('object1')))
        self.assertEqual(values.get_field(make_path('object1'), 'field3'), 'value3')
        self.assertListEqual(values.get_field_list(make_path('object1'), 'field4'),
                             ['item4', 'item5'])

    def test_dump_valuetree_to_dict(self):
        "A ValueTree should dump to a dict"
        values = ValueTree()
        values.put_field(ROOT_PATH, 'field1', 'value1')
        values.put_field_list(ROOT_PATH, 'field2', ['item1', 'item2', 'item3'])
        values.put_container(make_path('object1'))
        values.put_field(make_path('object1'), 'field3', 'value3')
        values.put_field_list(make_path('object1'), 'field4', ['item4', 'item5'])
        obj = dump(values)
        self.assertDictEqual(obj, {
            'field1': 'value1',
            'field2': ['item1', 'item2', 'item3'],
            'object1': {
                'field3': 'value3',
                'field4': ['item4', 'item5'],
                },
        })
