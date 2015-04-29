from flask import Blueprint
from . import routes

govuk_template = Blueprint('govuk_template',__name__)

routes.register_routes(govuk_template)
