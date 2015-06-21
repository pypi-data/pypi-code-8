"""Blueprint with different service pages.

Contains Web-page for update application and a
special web-page which shows on the first run of
application.

Contents:
pages -- Web pages for current blueprint module.
views.py - views for current blueprint.
"""

from flask import Blueprint

service_pages = Blueprint('service_pages', __name__,
                          template_folder='pages')

from pagapp.service_pages.views import *
