import re
import unittest
import xml.etree.ElementTree as ET

from bidon.data import ForeignModelWrapper


class Person(ForeignModelWrapper):
  attrs = dict(
    first_name=None,
    last_name=None,
    company_id=None)
  mapping = dict(
    first_name=("first_name", lambda s: s.strip()),
    last_name=("last_name", lambda s: s.strip()),
    company_id=("company", lambda d: int(d["id"])))


class PersonXML(ForeignModelWrapper):
  attrs = dict(id=None, first_name=None, last_name=None, company_id=None, company_name=None)
  mapping = dict(
    id=("id", lambda i: int(i), None),
    first_name=("first_name", ),
    last_name=("last_name", ),
    company_id=("company", ("id", int, None)),
    company_name=("company/name", ))


class DataForeignModelWrapperTestCase(unittest.TestCase):
  def test_create_raw(self):
    d = {
      "first_name": "Trey",
      "last_name": "Cucco",
      "company": {
        "id": 188,
        "name": "ACME" }}
    p = Person.create(d)
    self.assertEqual(p.first_name, "Trey")
    self.assertEqual(p.last_name, "Cucco")
    self.assertEqual(p.company_id, 188)

  def test_create_xml(self):
    xmlt = """<person id="1">
      <first_name>Trey</first_name>
      <last_name>Cucco</last_name>
      <company id="1">
        <name>ACME</name>
      </company>
    </person>"""
    root = ET.fromstring(xmlt)
    p = PersonXML.create(root, mapping_format="xml")
    self.assertEqual(p.id, 1)
    self.assertEqual(p.company_id, 1)
    self.assertEqual(p.company_name, "ACME")
    self.assertEqual(p.first_name, "Trey")
    self.assertEqual(p.last_name, "Cucco")
