import dicttoxml
import json


class Serializer:
    def serialize(self, obj, **kwargs):
        raise NotImplementedError('.serialize(obj, **kwargs) must be implemented')

    def deserialize(self, data, **kwargs):
        raise NotImplementedError('.deserialize(data, **kwargs) must be implemented')


class JSONSerializer(Serializer):
    def serialize(self, obj, **kwargs):
        return json.dumps(obj, **kwargs)

    def deserialize(self, data, **kwargs):
        return json.loads(data, **kwargs)


class XMLSerializer(Serializer):
    def serialize(self, obj, **kwargs):
        return dicttoxml.dicttoxml(obj, **kwargs)