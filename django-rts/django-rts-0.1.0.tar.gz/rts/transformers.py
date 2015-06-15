__author__ = 'josvanvelzen'


class Transformer(object):
    def transform(self, source):
        raise NotImplementedError('.transform(source) must be implemented')


class SimpleKeyMappingTransformer(Transformer):
    key_map = None

    def transform(self, source):
        assert isinstance(self.key_map, dict), "key_map property is not a dict"

        return {self.key_map[x]: source[x] for x in list(self.key_map.keys())}
