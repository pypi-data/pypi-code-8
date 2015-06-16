import os
import pkg_resources
import functools
import inspect
from portfolio import (Portfolio, utils, abort)
from flask_login import current_user
from flask_assets import (Environment, Bundle)

# Views
from contact_page import contact_page
from error_page import error_page
from maintenance_page import maintenance_page
from post_admin import post_admin
from post_reader import post_reader
from user_account import user_account
from user_admin import user_admin

def _register(app):
    def setup_config(app):
        if app.config.get("APP_NAME"):
            Portfolio.set_context__(APP_NAME=app.config.get("APP_NAME"))
        if app.config.get("APP_VERSION"):
            Portfolio.set_context__(APP_VERSION=app.config.get("APP_VERSION"))

        # OAUTH LOGIN
        if app.config.get("LOGIN_OAUTH_ENABLE"):
            _sl = app.config.get("LOGIN_OAUTH_CREDENTIALS")
            if _sl and isinstance(_sl, dict):
                client_ids = {}
                buttons = []
                for name, prop in _sl.items():
                    if isinstance(prop, dict):
                        if prop["ENABLE"]:
                            _name = name.lower()
                            client_ids[_name] = prop["CLIENT_ID"]
                            buttons.append(_name)

            Portfolio.set_context__(LOGIN_OAUTH_ENABLED=True,
                           LOGIN_OAUTH_CLIENT_IDS=client_ids,
                           LOGIN_OAUTH_BUTTONS=buttons)

    def register_templates(app):
        _name = ".".join(__name__.split(".")[:-1])
        path = pkg_resources.resource_filename(_name, "templates")
        utils.add_path_to_jinja(app, path)

    def register_static():
        _dir = os.path.dirname(os.path.dirname(__file__))
        env = Portfolio.assets
        env.load_path = [
            Portfolio._app.static_folder,
            os.path.join(_dir, 'static'),
        ]

        env.register(
            'bluebook_js',
            Bundle(
                "portfolio/vendor/authomatic/authomatic.js",
                "portfolio/js/s3upload.js",
                "portfolio/js/hello.js",
                "portfolio/js/portfolio.js",
                output='portfolio.js'
            )
        )
        env.register(
            'bluebook_css',
            Bundle(
                'portfolio/css/portfolio.css',
                'portfolio/css/bootstrap-social-btns.css',
                output='portfolio.css'
            )
        )

    setup_config(app)
    register_templates(app)
    register_static()

Portfolio.bind(_register)


def with_user_roles(roles):
    """
    with_user_roles(roles)

    It allows to check if a user has access to a view by adding the decorator
    with_user_roles([])

    Requires flask-login

    In your model, you must have a property 'role', which will be invoked to
    be compared to the roles provided.

    If current_user doesn't have a role, it will throw a 403

    If the current_user is not logged in will throw a 401

    * Require Flask-Login
    ---
    Usage

    @app.route('/user')
    @login_require
    @with_user_roles(['admin', 'user'])
    def user_page(self):
        return "You've got permission to access this page."
    """
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.is_authenticated():

                if not hasattr(current_user, "role"):
                    raise AttributeError("<'role'> doesn't exist in login 'current_user'")
                if current_user.role not in roles:
                    return abort(403)
            else:
                return abort(401)
            return f(*args, **kwargs)
        return wrapped
    return wrapper

