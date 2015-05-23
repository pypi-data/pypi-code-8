import string
import types
import cProfile
import pstats
import tempfile
import json

import tornado.web

class ProfileMeta(type):
    def __new__(mcs, cls_name, bases, attrs):
        supported_methods = map(string.lower, 
            tornado.web.RequestHandler.SUPPORTED_METHODS)
        for attr in attrs:
            if attr in supported_methods and \
                isinstance(attrs[attr], types.FunctionType):
                attrs[attr] = ProfileMeta.profile(attrs[attr])
        return super(ProfileMeta, mcs).__new__(mcs, cls_name, bases, attrs)

    @staticmethod
    def profile(f):
        def _inner(self, *args, **kwargs):
            if not self.get_argument('profile', None):
                return f(self, *args, **kwargs)

            sortby = self.get_argument('sortby', None)
            if sortby not in pstats.Stats.sort_arg_dict_default:
                sortby = 'cumulative'

            amount_number = tuple()
            if self.get_argument("amount_number", None):
                try:
                    amount_number = (int(self.get_argument("amount_number")), )
                except Exception:
                    pass
            amount = amount_number + tuple(self.get_arguments("amount", []))

            temp = tempfile.NamedTemporaryFile()
            temp_stats = tempfile.NamedTemporaryFile()
            try:
                self.write, write = lambda *a, **kw: None, self.write
                cProfile.runctx("f(self, *args, **kwargs)", globals(), locals(), temp.name)
                self.write = write

                pstats.Stats(temp.name, stream=temp_stats).sort_stats(sortby).print_stats(*amount)
                temp_stats.seek(0)
                self.write(ProfileMeta.to_json(temp_stats.read()))
            finally:
                temp.close()
                temp_stats.close()
        return _inner

    @staticmethod
    def to_json(content):
        def combile_adjacent_chars(s, ch=" "):
            while s.count(ch*2):
                s = s.replace(ch*2, ch)
            return s

        d = {}
        d['origin'] = content
        d['detail'] = []
        d['parse_code'] = 0
        d['parse_message'] = ""

        try:
            lines = [combile_adjacent_chars(line).split(' ', 5) for line in filter(lambda s: s, map(string.strip, content.split('\n'))[6:])]
            for line in lines[1:]:
                d['detail'].append(dict(zip(lines[0], line)))
        except Exception as e:
            d['parse_code'] = 1
            d['parse_message'] = str(e)
        return json.dumps(d)

