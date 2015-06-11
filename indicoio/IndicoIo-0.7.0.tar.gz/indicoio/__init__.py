from functools import partial

Version, version, __version__, VERSION = ('0.7.0',) * 4

JSON_HEADERS = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
    'client-lib': 'python',
    'version-number': VERSION
}

from indicoio.text.sentiment import political, posneg
from indicoio.text.sentiment import posneg as sentiment
from indicoio.text.lang import language
from indicoio.text.tagging import text_tags
from indicoio.images.fer import fer
from indicoio.images.features import facial_features
from indicoio.images.features import image_features
from indicoio.utils.multi import predict_image, predict_text

from indicoio.config import API_NAMES

apis = dict((api, globals().get(api)) for api in API_NAMES)

for api in apis:
    globals()[api] = partial(apis[api])
    globals()['batch_' + api] = partial(apis[api], batch=True)
