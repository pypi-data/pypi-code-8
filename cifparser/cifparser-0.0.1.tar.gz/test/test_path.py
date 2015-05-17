import bootstrap
import unittest
import datetime

import cifparser.path

class TestPath(unittest.TestCase):

    def test_make_path_from_string_with_a_single_segment(self):
        "make_path should make a path from a string with a single segment"
        path = cifparser.path.make_path("foobar")
        self.assertListEqual(path.segments, ["foobar"])

    def test_make_path_from_string_with_multiple_segments(self):
        "make_path should make a path from a string with multiple segments"
        path = cifparser.path.make_path("foo.bar.baz")
        self.assertListEqual(path.segments, ["foo", "bar", "baz"])

    def test_make_path_from_string_with_quoted_segments(self):
        "make_path should make a path from a string with quoted segments"
        path = cifparser.path.make_path('foo."bar baz".qux')
        self.assertListEqual(path.segments, ["foo", "bar baz", "qux"])
        path = cifparser.path.make_path("foo.'bar baz'.qux")
        self.assertListEqual(path.segments, ["foo", "bar baz", "qux"])

    def test_make_path_from_string_with_restricted_characters_in_quotes(self):
        "make_path should make a path from a string with restricted characters in quotes"
        path = cifparser.path.make_path('foo."bar=baz".qux')
        self.assertListEqual(path.segments, ["foo", "bar=baz", "qux"])

    def test_make_path_from_single_path(self):
        "make_path return the supplied Path object unmodified"
        path1 = cifparser.path.make_path("foobar")
        path2 = cifparser.path.make_path(path1)
        self.assertListEqual(path1.segments, path2.segments)
        self.assertEquals(id(path1), id(path2))

    def test_make_path_from_a_list_of_single_segments(self):
        "make_path should make a path from a list of single-segment strings"
        path = cifparser.path.make_path("foo", "bar", "baz")
        self.assertListEqual(path.segments, ["foo", "bar", "baz"])

    def test_make_path_from_a_list_of_paths(self):
        "make_path should make a path from a list of Path objects"
        path1 = cifparser.path.make_path("foo")
        path2 = cifparser.path.make_path("bar")
        path3 = cifparser.path.make_path("baz")
        path = cifparser.path.make_path(path1, path2, path3)
        self.assertListEqual(path.segments, ["foo", "bar", "baz"])

    def test_make_path_from_a_list_of_strings_with_multiple_segments(self):
        "make_path should make a path from a list of multiple-segment strings"
        path = cifparser.path.make_path("foo.bar", "baz.qux")
        self.assertListEqual(path.segments, ["foo", "bar", "baz", "qux"])
