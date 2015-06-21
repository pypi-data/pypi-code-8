"""Blueprint with admin panel.

Contains administrator panel.

Contents:
pages -- HTML code for admin panel.
admin_functions.py -- function, which performs administrator's tasks.
forms.py -- forms, using in admin panel.
views.py -- views, using in admin panel.
"""

from flask import Blueprint

admin_panel = Blueprint('admin_panel', __name__,
                        template_folder='pages',
                        url_prefix='/admin')

from pagapp.admin_panel.views import *
