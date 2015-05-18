from os import environ

from flask import request, Flask, jsonify
from imgurpython.client import ImgurClient
from imgurpython.helpers import error as imgur_exc
from redis import exceptions as redis_exc
from werkzeug.exceptions import BadRequest

from imgtohttps.lib import EmptyUrlError
from imgtohttps.logic import process
from imgtohttps.storage import storage


EXCEPTIONS = (
    KeyError,
    TypeError,
    BadRequest,
    EmptyUrlError,
    imgur_exc.ImgurClientError,
    redis_exc.ConnectionError
)

app = Flask(__name__)
app.config.from_object(environ.get('APP_SETTINGS', 'config.Development'))
storage.init_app(app)
app.imgur_client = ImgurClient(app.config['IMGUR_CLIENT_ID'], app.config['IMGUR_CLIENT_SECRET'])


@app.route('/', methods=['POST'])
def index():
    return jsonify(url=process(request.get_json()['url']))


def error_handler(error):
    return jsonify(error=str(error))

for exc in EXCEPTIONS:
    app.register_error_handler(exc, error_handler)

if __name__ == '__main__':
    app.run()
