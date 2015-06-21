"""Blueprint with views for API calls."""

from flask import Blueprint

application_api = Blueprint('api', __name__, url_prefix='/api')

from pagapp.application_api.album_api import *
from pagapp.application_api.pictures_api import *
