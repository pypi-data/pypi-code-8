import bootstrap
import io
import unittest

import cifparser.parser
from cifparser.path import ROOT_PATH, make_path

class TestCIFParser(unittest.TestCase):

    multi_line_data = \
"""
field1 = value1
field2 = value2
object1:
    field3 = value3
    object2:
        field4 = value4
        object3:
            field5 = value5
    field6 = value6
    object4:
        field7 = value7
field8 = value8
object5:
        field9 = value9
"""

    deep_path_data = \
"""
toplevel:
    this.is.deep:
        field1 = value1
    shallow:
        field2 = value2
field3 = value3
"""

    field_key_with_spaces_data = \
"""
toplevel:
    nospaces = foo
    with single spaces = bar
    with   extra space = baz
"""

    value_continuation_data = \
"""
toplevel:
    field1 = first line
           | second line
           | third line
    field2 = value2
field3 = value3
"""

    list_continuation_data = \
"""
toplevel:
    field1 = list item 1
           , list item 2
           , list item 3
    field2 = value2
field3 = value3
"""

    def test_load_multi_line(self):
        "a CIF parser should parse a multi-line document"
        cifparser.parser.print_ast(io.StringIO(self.multi_line_data))
        values = cifparser.parser.parse_file(io.StringIO(self.multi_line_data))
        self.assertEquals(values.get_field(ROOT_PATH, 'field1'), ' value1')
        self.assertEquals(values.get_field(ROOT_PATH, 'field2'), ' value2')
        self.assertEquals(values.get_field(make_path('object1'), 'field3'), ' value3')
        self.assertEquals(values.get_field(make_path('object1'), 'field6'), ' value6')
        self.assertEquals(values.get_field(make_path('object1.object2'), 'field4'), ' value4')
        self.assertEquals(values.get_field(make_path('object1.object2.object3'), 'field5'), ' value5')
        self.assertEquals(values.get_field(make_path('object1.object4'), 'field7'), ' value7')
        self.assertEquals(values.get_field(ROOT_PATH, 'field8'), ' value8')
        self.assertEquals(values.get_field(make_path('object5'), 'field9'), ' value9')

    def test_load_field_keys_with_spaces(self):
        "a CIF parser should parse a multi-line document with keys that have embedded space"
        cifparser.parser.print_ast(io.StringIO(self.field_key_with_spaces_data))
        values = cifparser.parser.parse_file(io.StringIO(self.field_key_with_spaces_data))
        self.assertEquals(values.get_field(make_path('toplevel'), 'nospaces'), ' foo')
        self.assertEquals(values.get_field(make_path('toplevel'), 'with single spaces'), ' bar')
        self.assertEquals(values.get_field(make_path('toplevel'), 'with   extra space'), ' baz')

    def test_load_deep_path(self):
        "a CIF parser should parse a multi-line document with deep paths"
        cifparser.parser.print_ast(io.StringIO(self.deep_path_data))
        values = cifparser.parser.parse_file(io.StringIO(self.deep_path_data))
        self.assertEquals(values.get_field(make_path('toplevel.this.is.deep'), 'field1'), ' value1')
        self.assertEquals(values.get_field(make_path('toplevel.shallow'), 'field2'), ' value2')
        self.assertEquals(values.get_field(ROOT_PATH, 'field3'), ' value3')

    def test_load_value_continuation_data(self):
        "a CIF parser should parse a multi-line document with value continuations"
        cifparser.parser.print_ast(io.StringIO(self.value_continuation_data))
        values = cifparser.parser.parse_file(io.StringIO(self.value_continuation_data))
        self.assertEquals(values.get_field(make_path('toplevel'), 'field1'), ' first line\n second line\n third line')
        self.assertEquals(values.get_field(make_path('toplevel'), 'field2'), ' value2')
        self.assertEquals(values.get_field(ROOT_PATH, 'field3'), ' value3')

    def test_load_list_continuation_data(self):
        "a CIF parser should parse a multi-line document with list continuations"
        cifparser.parser.print_ast(io.StringIO(self.list_continuation_data))
        values = cifparser.parser.parse_file(io.StringIO(self.list_continuation_data))
        self.assertListEqual(values.get_field_list(make_path('toplevel'), 'field1'),
            [' list item 1', ' list item 2', ' list item 3'])
        self.assertEquals(values.get_field(make_path('toplevel'), 'field2'), ' value2')
        self.assertEquals(values.get_field(ROOT_PATH, 'field3'), ' value3')
