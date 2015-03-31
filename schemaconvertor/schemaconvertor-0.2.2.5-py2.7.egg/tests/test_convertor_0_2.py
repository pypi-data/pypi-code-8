#!/usr/bin/env python
# encoding: utf-8

import sys
from unittest import TestCase

from schemaconvertor.convertor import (
    Schema, SchemaConst, ObjAsDictAdapter, SchemaConvertor)


class TestObjAsDictAdapter(TestCase):
    class Parent(object):
        pclsval = 1

        def __init__(self):
            self.pinsval = 2

    class Child(Parent):
        cclsval = 3

        def __init__(self):
            super(TestObjAsDictAdapter.Child, self).__init__()
            self.cinsval = 4

        def __getattr__(self, name):
            if name == "dynamicval":
                return 5

    def test_base_method(self):
        parent = self.Parent()
        parent_dict = ObjAsDictAdapter(parent)

        self.assertEqual(parent_dict["pclsval"], parent.pclsval)
        self.assertEqual(parent_dict["pinsval"], parent.pinsval)
        self.assertIn("pclsval", iter(parent_dict))
        self.assertIn("pinsval", iter(parent_dict))

    def test_inherit(self):
        child = self.Child()
        child_dict = ObjAsDictAdapter(child)

        self.assertEqual(child_dict["pclsval"], child.pclsval)
        self.assertEqual(child_dict["pinsval"], child.pinsval)
        self.assertEqual(child_dict["cclsval"], child.cclsval)
        self.assertEqual(child_dict["cinsval"], child.cinsval)
        self.assertIn("pclsval", iter(child_dict))
        self.assertIn("pinsval", iter(child_dict))
        self.assertIn("cclsval", iter(child_dict))
        self.assertIn("cinsval", iter(child_dict))

    def test_dynamic_attr(self):
        child = self.Child()
        child_dict = ObjAsDictAdapter(child)

        self.assertEqual(child_dict["dynamicval"], child.dynamicval)
        self.assertNotIn("dynamicval", iter(child_dict))

        child.dynamicval = 6
        self.assertEqual(child_dict["dynamicval"], child.dynamicval)
        self.assertIn("dynamicval", iter(child_dict))

    def test_dict_interface(self):
        child = self.Child()
        parent = self.Parent()
        child_dict = ObjAsDictAdapter(child)
        parent_dict = ObjAsDictAdapter(parent)

        self.assertEqual(parent_dict.get("cinsval"), None)
        self.assertEqual(
            parent_dict.get("cinsval", child_dict["cinsval"]),
            child_dict.get("cinsval"))

        self.assertGreater(len(parent_dict), 0)
        self.assertEqual(parent_dict.keys(), list(parent_dict.iterkeys()))
        self.assertEqual(parent_dict.values(), list(parent_dict.itervalues()))
        self.assertEqual(parent_dict.items(), list(parent_dict.iteritems()))
        self.assertEqual(len(parent_dict), len(list(parent_dict)))


class TestSchema(TestCase):
    def test_field_default_value(self):
        schema = Schema({})
        self.assertEqual(schema.version, schema.VERSION)
        self.assertEqual(schema.origin_schema, {})
        self.assertEqual(schema.parent, None)
        self.assertEqual(schema.compiled, False)  # lazy
        self.assertEqual(schema.type, SchemaConst.S_UNDEFINED)
        self.assertEqual(schema.items, SchemaConst.S_DISABLED)
        self.assertEqual(schema.properties_schemas, SchemaConst.S_DISABLED)
        self.assertEqual(schema.pattern_properties_schemas, SchemaConst.S_DISABLED)
        self.assertEqual(schema.typeof_schemas, SchemaConst.S_DISABLED)
        self.assertEqual(schema.typeof_default_schema, SchemaConst.S_DISABLED)
        self.assertEqual(schema.compiled, True)
        self.assertEqual(schema.encoding, SchemaConst.V_ENCODING)
        self.assertEqual(schema.decoderrors, SchemaConst.V_DECODERR)

    def test_version(self):
        schema = Schema({
            "type": "string"
        })
        self.assertEqual(schema.version, Schema.VERSION)
        self.assertTrue(schema.check_version())

        schema = Schema({
            "version": Schema.VERSION,
            "type": "string"
        })
        self.assertEqual(schema.version, Schema.VERSION)
        self.assertTrue(schema.check_version())

        schema = Schema({
            "version": "0.2",
            "type": "string"
        })
        self.assertNotEqual(schema.version, Schema.VERSION)
        self.assertTrue(schema.check_version())

        schema = Schema({
            "version": "0.0.0.0",
            "type": "string"
        })
        self.assertEqual(schema.version, "0.0.0.0")
        self.assertFalse(schema.check_version())

        schema = Schema({
            "version": "0.0.0.0",
            "type": "array",
            "items": {
                "type": "string"
            }
        })
        self.assertEqual(schema.version, "0.0.0.0")
        self.assertEqual(schema.items.version, "0.0.0.0")

    def test_parent(self):
        schema = Schema({
            "version": "0.2",
            "type": "array",
            "items": {
                "type": "string"
            }
        })
        self.assertIs(schema.items.parent, schema)
        self.assertIs(schema.parent, None)

    def test_short(self):
        schema1 = Schema({
            "version": "0.2",
            "type": "array",
            "items": "string"
        })
        schema2 = Schema({
            "version": "0.2",
            "type": "array",
            "items": {
                "type": "string"
            }
        })
        self.assertEqual(schema1.items.type, schema2.items.type)

        schema = Schema("string")
        self.assertEqual(schema.type, "string")

    def test_encoding(self):
        schema = Schema({
            "version": "0.2",
            "type": "array",
            "items": {
                "type": "string"
            }
        })
        self.assertEqual(schema.encoding, "utf-8")
        self.assertEqual(schema.items.encoding, "utf-8")
        self.assertEqual(schema.decoderrors, "strict")
        self.assertEqual(schema.items.decoderrors, "strict")

        schema = Schema({
            "version": "0.2",
            "encoding": "gbk",
            "decoderrors": "ignore",
            "type": "array",
            "items": {
                "type": "string"
            }
        })
        self.assertEqual(schema.encoding, "gbk")
        self.assertEqual(schema.items.encoding, "gbk")
        self.assertEqual(schema.decoderrors, "ignore")
        self.assertEqual(schema.items.decoderrors, "ignore")

        schema = Schema({
            "version": "0.2",
            "encoding": "gbk",
            "decoderrors": "ignore",
            "type": "array",
            "items": {
                "type": "string",
                "encoding": "utf-8",
                "decoderrors": "replace",
            }
        })
        self.assertEqual(schema.encoding, "gbk")
        self.assertEqual(schema.items.encoding, "utf-8")
        self.assertEqual(schema.decoderrors, "ignore")
        self.assertEqual(schema.items.decoderrors, "replace")


class TestSchemaConvertor(TestCase):
    def test_string_encoding(self):
        convertor = SchemaConvertor({
            "type": "string"
        })
        self.assertEqual(convertor(u"刘奕聪"), u"刘奕聪")
        self.assertEqual(convertor(u"刘奕聪".encode("utf-8")), u"刘奕聪")

        convertor = SchemaConvertor({
            "encoding": "utf-8",
            "type": "string"
        })
        self.assertEqual(convertor(u"刘奕聪"), u"刘奕聪")
        self.assertEqual(convertor(u"刘奕聪".encode("utf-8")), u"刘奕聪")

        convertor = SchemaConvertor({
            "encoding": "gbk",
            "type": "string"
        })
        self.assertEqual(convertor(u"刘奕聪"), u"刘奕聪")
        self.assertEqual(convertor(u"刘奕聪".encode("gbk")), u"刘奕聪")

    def test_string_decoderr(self):
        convertor = SchemaConvertor({
            "encoding": "utf-8",
            "type": "string"
        })

        with self.assertRaises(UnicodeDecodeError):
            self.assertEqual(convertor(u"刘奕聪".encode("gbk")), u"刘奕聪")

        convertor = SchemaConvertor({
            "encoding": "utf-8",
            "decoderrors": "ignore",
            "type": "string"
        })
        self.assertIsInstance(convertor(u"刘奕聪".encode("gbk")), unicode)
        self.assertNotEqual(convertor(u"刘奕聪".encode("gbk")), u"刘奕聪")

        convertor = SchemaConvertor({
            "encoding": "utf-8",
            "decoderrors": "replace",
            "type": "string"
        })
        self.assertIsInstance(convertor(u"刘奕聪".encode("gbk")), unicode)
        self.assertNotEqual(convertor(u"刘奕聪".encode("gbk")), u"刘奕聪")
