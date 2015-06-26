from restart.art import RESTArt
from restart.resource import Resource

art = RESTArt()

@art.route(methods=['GET'])
class Greeting(Resource):
    name = 'greeting'

    def read(self, request):
        return {'hello': 'world'}
