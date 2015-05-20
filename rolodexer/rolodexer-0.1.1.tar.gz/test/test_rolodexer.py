#!/usr/bin/env python

from __future__ import print_function

import unittest
import rolodexer
import json

sample_input = """
Booker T., Washington, 87360, 373 781 7380, yellow
Chandler, Kerri, (623)-668-9293, pink, 123123121
James Murphy, yellow, 83880, 018 154 6474
asdfawefawea
""".strip()

sample_output = """
{
  "entries": [
    {
      "color": "yellow",
      "firstname": "James",
      "lastname": "Murphy",
      "phonenumber": "018-154-6474",
      "zipcode": "83880"
    },
    {
      "color": "yellow",
      "firstname": "Booker T.",
      "lastname": "Washington",
      "phonenumber": "373-781-7380",
      "zipcode": "87360"
    }
  ],
  "errors": [
    1,
    3
  ]
}
""".strip()

class RolodexerTests(unittest.TestCase):
    
    def setUp(self):
        self.maxDiff = 1000
    
    def test_tokenize(self):
        # all of these should tokenize (even with invalid individual terms)
        line0 = 'Booker T., Washington, 87360, 373 781 7380, yellow'
        line1 = 'Chandler, Kerri, (623)-668-9293, pink, 123123121'
        line2 = 'James Murphy, yellow, 83880, 018 154 6474'
        
        terms0 = rolodexer.tokenize(line0)
        terms1 = rolodexer.tokenize(line1)
        terms2 = rolodexer.tokenize(line2)
        
        self.assertEqual(len(terms0), 5)
        self.assertEqual(len(terms1), 5)
        self.assertEqual(len(terms2), 4) # first/last are single term
    
    def test_classify(self):
        terms = [
            u'yellow', u'373 781 7380', u'87360',
            u'Washington', u'Booker T.']
        
        out = rolodexer.classify(terms)
        keys = out.keys()
        
        self.assertTrue(u'phonenumber' in keys)
        self.assertTrue(u'firstname' in keys)
        self.assertTrue(u'lastname' in keys)
        self.assertTrue(u'color' in keys)
        self.assertTrue(u'zipcode' in keys)
        
        phonefield = rolodexer.PhoneNumberField()
        
        self.assertEqual(out[u'color'],          terms[0])
        self.assertEqual(out[u'phonenumber'],    phonefield.format(terms[1]))
        self.assertEqual(out[u'zipcode'],        terms[2])
        self.assertEqual(out[u'lastname'],       terms[3])
        self.assertEqual(out[u'firstname'],      terms[4])
    
    def _test_bad_line_raises(self):
        """ assertRaises() is holding some sort of grudge
            against my entire bloodline, for some reason
        """
        # from rolodexer import RDZipCodeError, RolodexerError
        lines = sample_input.splitlines()
        for idx, line in enumerate(lines):
            terms = rolodexer.tokenize(line)
            # with self.assertRaises(RDZipCodeError):
            self.assertRaises(
                Exception, 
                rolodexer.classify, terms)
    
    def test_tokenize_classify(self):
        # from pprint import pprint
        entries = []
        errors  = []
        lines = sample_input.splitlines()
        for idx, line in enumerate(lines):
            terms = rolodexer.tokenize(line)
            try:
                cterms = rolodexer.classify(terms)
            except rolodexer.RolodexerError:
                errors.append(idx)
            else:
                keys = cterms.keys()
                
                self.assertTrue(u'phonenumber' in keys)
                self.assertTrue(u'firstname' in keys)
                self.assertTrue(u'lastname' in keys)
                self.assertTrue(u'color' in keys)
                self.assertTrue(u'zipcode' in keys)
                
                entries.append(cterms)
        
        output_dict = { u"entries": entries, u"errors": errors }
        # pprint(output_dict)
        
        sample_output_dict = json.loads(sample_output)
        self.assertItemsEqual(
            output_dict, sample_output_dict)
    
    def test_json_format(self):
        pass
    
    def test_file_read(self):
        from os.path import join, dirname
        entries = []
        errors  = []
        inpth = join(dirname(dirname(__file__)), 'data', 'data.in')
        with open(inpth, 'rb') as fh:
            idx = 0
            while True:
                linen = fh.readline()
                if not linen:
                    break
                line = linen.strip()
                tokens = rolodexer.tokenize(line)
                try:
                    terms = rolodexer.classify(tokens)
                except rolodexer.RolodexerError:
                    errors.append(idx)
                else:
                    entries.append(terms)
                idx += 1
            output_dict = { u"entries": entries, u"errors": errors }
            output_json = json.dumps(output_dict, indent=2, sort_keys=True)
            print(output_json)

if __name__ == '__main__':
    unittest.main()

if __name__ == '__yodogg__':
    line = sample_input.splitlines()[0]
    
    while True:
        partition   = line.rpartition(',')
        first       = partition[:-2][0].strip()
        last        = partition[-1:][0].strip()
        if not first and not last:
            break
        line = first
        print(last)
