# -*- coding: utf-8 -*-
''' Klarna API - ILT

Defines class to hold information about a ILT question
'''

# Copyright 2015 Klarna AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# python3k campatibility
from __future__ import print_function
import sys
if sys.version_info >= (3,):
    basestring = str


class Info(object):
    def __init__(self, url):
        if sys.version_info >= (3,):
            from urllib.request import urlopen
        else:
            # Wrap urllib2's urlopen to support __exit__
            import contextlib
            import urllib2

            def urlopen(*args):
                return contextlib.closing(urllib2.urlopen(*args))

        import json
        with urlopen(url) as r:
            self._data = json.loads(r.read().decode())

    def get_questions(self, keys):
        def mkquestion(key, data):
            if 'values' in data:
                values = [Value(v['value'], v['text']) for v in data['values']]
            else:
                values = None

            return Question(key, data['text'],
                Question.Pre if data.get('pre', False) else Question.Ilt,
                data['type'],
                values
            )
        qdata = self._data['questions']
        return [mkquestion(key, qdata[key]) for key in keys]

    def get_dictionary(self):
        return self._data['dictionary']


class Value(object):
    ''' ILT Enumeration value '''

    def __init__(self, value, text):
        self.value = value
        self.text = text

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.text


# pre_ilt - don't send to KO
class Question(object):
    ''' Holds information about a ILT question to ask the customer

        key: the name of the field to set in income_info with the answer
            to this question.
        text: the text of the question display to the customer
        answer_type: the type of input (enum, integer)
        answer_values: list of possible answers for the enum type
    '''

    Pre = object()
    Ilt = object()

    @property
    def is_select(self):
        return self.answer_type == 'enum'

    def __init__(self, key, text, question_type, answer_type, values):
        self.key = key
        self.text = text
        self.question_type = question_type
        self.answer_type = answer_type
        self.answer_values = values

    def __repr__(self):
        return 'Question(%s, %r, %r)' % (self.key,
            self.answer_type,
            self.answer_values)
