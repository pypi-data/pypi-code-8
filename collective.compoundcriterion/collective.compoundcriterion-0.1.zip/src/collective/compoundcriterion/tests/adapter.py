# encoding: utf-8


class TestingCompoundCrietrionFilterAdapter(object):

    def __init__(self, context):
        self.context = context

    @property
    def query(self):
        return {'Title': {'query': u'special_text_to_find'}}


class SampleCompoundCrietrionFilterAdapter(object):

    def __init__(self, context):
        self.context = context

    @property
    def query(self):
        return {'Title': {'query': u'title_with_sample_text'}}
