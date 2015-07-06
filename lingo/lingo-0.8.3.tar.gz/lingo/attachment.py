import uuid
import base64
import mimetypes

class Attachment(object):
    def __init__(self, **kwargs):
        self.stub = False
        self.name = None
        self.content_type = None
        self.data = None
        self.length = None
        self._new = True
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def fromFile(self, name, data_or_file_obj, content_type = None):
        final_data = data_or_file_obj.read() if hasattr(data_or_file_obj, 'read') else data_or_file_obj
        params = dict(
            _new = True,
            stub = False,
            name = name,
            content_type = content_type or mimetypes.guess_type(name)[0] or 'application/octet-stream',
            data = final_data,
            length = len(final_data)
        )
        return self(**params)

    @classmethod
    def fromDatabase(self, name, data):
        return self(**data, dict(name = name, _new = False))

class CouchDBAttachment(Attachment):
    @classmethod
    def fromDatabase(self, name, data):
        if not data['stub'] and 'data' in data:
            data['data'] = base64.b64decode(data['data'])
        return Attachment.fromDatabase(self, name, data)

