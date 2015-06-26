from __future__ import absolute_import

from restart.art import RESTArt
from restart.resource import Resource


art = RESTArt()


@art.route(methods=['GET'])
class Greeting(Resource):
    name = 'greeting'

    def read(self, request):
        return {'hello': 'world'}


if __name__ == '__main__':
    from restart.api import API
    api = API(art)
    api.run(debug=True)
