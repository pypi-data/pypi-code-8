from os import environ

from flask import request, Flask
from imgurpython.client import ImgurClient
from imgurpython.helpers import error as imgur_exc
from redis import exceptions as redis_exc
from werkzeug.exceptions import BadRequest

from imgtohttps import logic
from imgtohttps.lib import Link
from imgtohttps.lib import EmptyUrlError
from imgtohttps.lib import json
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
app.config.from_object(environ.get('APP_SETTINGS', 'settings.Development'))
storage.init_app(app)
app.imgur_client = ImgurClient(app.config['IMGUR_CLIENT_ID'], app.config['IMGUR_CLIENT_SECRET'])


@app.route('/upload', methods=['POST'])
@json
def upload():
    link = Link(request.get_json().get('url'))
    return {"url": logic.upload(link).secure}


@app.route('/process', methods=['POST'])
@json
def process():
    link = Link(request.get_json().get('url'))
    return {"url": logic.process(link).secure}


@json
def error_handler(error):
    return {"error": str(error)}

for exc in EXCEPTIONS:
    app.register_error_handler(exc, error_handler)

if __name__ == '__main__':
    app.run()
