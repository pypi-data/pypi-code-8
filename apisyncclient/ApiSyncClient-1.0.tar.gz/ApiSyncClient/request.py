import json
from .responce import Response


class Request:
    def __init__(self, sender, chain):
        self._sender = sender
        self.chain = chain

    def __getattr__(self, item):
        return Request(self._sender, self.chain+[item])

    def __call__(self, *args, **kwargs):
        method = '.'.join(self.chain)
        result = json.loads(self._sender.send(method, **kwargs).decode())

        return Response(method=method, kwargs=kwargs, **result)
