import json

from omnomnom import exceptions
from omnomnom.models import Message


class BasicMarshaller(object):

    def prepare_request(self, msg):
        # Given omnomnom.models.Message build request
        # that's send to service
        raise NotImplementedError

    def process_request_data(self, data):
        # Given raw request data send to socket
        # returns omnomnom.models.Message
        raise NotImplementedError

    def prepare_response(self, result=None, err=None):
        # Given executable result or error
        # prepares response that's send to client
        raise NotImplementedError

    def process_response_data(self, data):
        # Given raw response data build data structure
        # that's usable for client
        raise NotImplementedError


class LoadDumpMarshaller(BasicMarshaller):
    executable_field = 'executable'

    def dumps(self, data):
        raise NotImplementedError

    def loads(self, data):
        raise NotImplementedError

    def prepare_request(self, msg):
        request = {
            'executable': msg.executable,
            'args': msg.args,
            'kwargs': msg.kwargs,
        }
        return self.dumps(request)

    def process_request_data(self, data):
        data = self.loads(data)

        try:
            executable = data[self.executable_field]
        except KeyError:
            msg = u"No executable defined in message"
            raise exceptions.DemarshallingExeption(msg)

        args = data.get('args', ())
        kwargs = data.get('kwargs', {})
        return Message(
            executable=executable,
            args=args, kwargs=kwargs
        )

    def prepare_response(self, result=None, err=None):
        if err and not isinstance(err, (str, unicode)):
            err = str(err)
        response = {
            'result': result,
            'error': err
        }
        return self.dumps(response)

    def process_response_data(self, data):
        return self.loads(data)


class JsonMarshaller(LoadDumpMarshaller):

    def dumps(self, data):
        return json.dumps(data).encode('utf-8')

    def loads(self, data):
        return json.loads(data.decode('utf-8'))


class BsonMarshaller(LoadDumpMarshaller):

    def dumps(self, data):
        import bson
        return bson.dumps(data)

    def loads(self, data):
        import bson
        return bson.loads(data)


class MsgPackMarshaller(LoadDumpMarshaller):

    def dumps(self, data):
        import msgpack
        return msgpack.packb(data, use_bin_type=True)

    def loads(self, data):
        import msgpack
        return msgpack.unpackb(data, encoding='utf-8')