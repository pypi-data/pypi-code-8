import bootstrap
import unittest

import cifparser.grammar
from cifparser.path import make_path

class TestCIFGrammar(unittest.TestCase):

    def test_parse_comment_line(self):
        "a CIF lexer should tokenise '#' + <RestOfLine> as a comment"
        indent,result = cifparser.grammar.parse_line("# this is a comment")
        self.assertIsInstance(result, cifparser.grammar.Comment)
        result_fields = vars(result)
        other_fields = vars(cifparser.grammar.Comment(" this is a comment"))
        self.assertDictEqual(result_fields, other_fields)

    def test_parse_objectdef_line(self):
        "a CIF lexer should tokenise <PathSegment> + ':' as a simple object definition"
        indent,result = cifparser.grammar.parse_line("object:")
        self.assertIsInstance(result, cifparser.grammar.ObjectDef)
        result_fields = vars(result)
        other_fields = vars(cifparser.grammar.ObjectDef(make_path('object')))
        self.assertDictEqual(result_fields, other_fields)

    def test_parse_deep_objectdef_line(self):
        "a CIF lexer should tokenise *(<PathSegment> + '.') + <PathSegment> + ':' as a deep object definition"
        indent,result = cifparser.grammar.parse_line("deep.nested.object:")
        self.assertIsInstance(result, cifparser.grammar.ObjectDef)
        result_fields = vars(result)
        other_fields = vars(cifparser.grammar.ObjectDef(make_path('deep','nested','object')))
        self.assertDictEqual(result_fields, other_fields)

    def test_parse_listitemdef_line(self):
        "a CIF lexer should tokenise '-' + <PathSegment> + ':' as a simple list item definition"
        indent,result = cifparser.grammar.parse_line("- object:")
        self.assertIsInstance(result, cifparser.grammar.ListItemDef)
        result_fields = vars(result)
        other_fields = vars(cifparser.grammar.ListItemDef(make_path('object')))
        self.assertDictEqual(result_fields, other_fields)

    def test_parse_deep_listitemdef_line(self):
        "a CIF lexer should tokenise '-' + *(<PathSegment> + '.') + <PathSegment> + ':' as a deep list item definition"
        indent,result = cifparser.grammar.parse_line("- deep.nested.object:")
        self.assertIsInstance(result, cifparser.grammar.ListItemDef)
        result_fields = vars(result)
        other_fields = vars(cifparser.grammar.ListItemDef(make_path('deep','nested','object')))
        self.assertDictEqual(result_fields, other_fields)

    def test_parse_fielddef_line(self):
        "a CIF lexer should tokenise <FieldDef> + '=' + <RestOfLine> as a field definition"
        indent,result = cifparser.grammar.parse_line("foo = bar")
        self.assertIsInstance(result, cifparser.grammar.FieldDef)
        result_fields = vars(result)
        other_fields = vars(cifparser.grammar.FieldDef('foo', ' bar'))
        self.assertDictEqual(result_fields, other_fields)

    def test_parse_valuecontinuation_line(self):
        "a CIF lexer should tokenise '|' + <RestOfLine> as a value continuation"
        indent,result = cifparser.grammar.parse_line("| this is a continuation")
        self.assertIsInstance(result, cifparser.grammar.ValueContinuation)
        result_fields = vars(result)
        other_fields = vars(cifparser.grammar.ValueContinuation(' this is a continuation'))
        self.assertDictEqual(result_fields, other_fields)

    def test_parse_listcontinuation_line(self):
        "a CIF lexer should tokenise ',' + <RestOfLine> as a list continuation"
        indent,result = cifparser.grammar.parse_line(", this is a continuation")
        self.assertIsInstance(result, cifparser.grammar.ListContinuation)
        result_fields = vars(result)
        other_fields = vars(cifparser.grammar.ListContinuation(' this is a continuation'))
        self.assertDictEqual(result_fields, other_fields)
