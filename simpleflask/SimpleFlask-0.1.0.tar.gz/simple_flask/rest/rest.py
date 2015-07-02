from flask import Flask
from flask.ext.cors import CORS
from simple_flask.core.core import say_hallo
from simple_flask_blueprint.rest.blueprint_rest import bp


class RootREST:

    def __init__(self, host, run_flask):
        self.host = host
        self.run_flask = run_flask
        self.app = Flask(__name__)
        CORS(self.app,
             resources={
                 r'/*': {
                     'origins': '*',
                     'headers': ['Content-Type']
                 }
             }
        )
        self.app.register_blueprint(bp, url_prefix='/blueprint')

        # Root service.
        @self.app.route('/', methods=['GET'])
        def say_hello_service():
            return say_hallo()

        # Root service.
        @self.app.route('/<name>/', methods=['GET'])
        def say_hello_to_guest_service(name):
            return say_hallo(name)

        # Run Flask.
        if self.run_flask:                              # pragma: no cover
            self.app.run(host=self.host, debug=True)    # pragma: no cover


def run_engine(host):                                   # pragma: no cover
    RootREST(host, True)                                # pragma: no cover

if __name__ == '__main__':                              # pragma: no cover
    run_engine('localhost')                             # pragma: no cover
