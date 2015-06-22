from portfolio import Portfolio


import re
import functools
from flask import abort
from portfolio import Portfolio, utils
from flask_login import current_user
from flask_assets import (Environment, Bundle)
import humanize
import jinja2
import mistune

class ViewError(Exception):
    pass

class ModelError(Exception):
    pass

# Views
from error_page import error_page
from maintenance_page import maintenance_page

# Register template and static path
_pkg = ".".join(__name__.split(".")[:-1])  # get the parent module name
Portfolio.register_component_template_static(_pkg)


def _setup(app):
    def setup_config(app):
        if app.config.get("APP_NAME"):
            Portfolio.__(APP_NAME=app.config.get("APP_NAME"))
        if app.config.get("APP_VERSION"):
            Portfolio.__(APP_VERSION=app.config.get("APP_VERSION"))

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

            Portfolio.__(LOGIN_OAUTH_ENABLED=True,
                           LOGIN_OAUTH_CLIENT_IDS=client_ids,
                           LOGIN_OAUTH_BUTTONS=buttons)

    def register_static():
        env = Portfolio.assets
        env.register(
            'portfolio_js',
            Bundle(
                "portfolio/vendor/authomatic/authomatic.js",
                "portfolio/js/s3upload.js",
                "portfolio/js/hello.js",
                "portfolio/js/portfolio.js",
                output='portfolio.js'
            )
        )
        env.register(
            'portfolio_css',
            Bundle(
                'portfolio/css/portfolio.css',
                'portfolio/css/bootstrap-social-btns.css',
                output='portfolio.css'
            )
        )

    setup_config(app)
    register_static()

Portfolio.bind(_setup)

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


def to_date(dt, format="%m/%d/%Y"):
    return "" if not dt else dt.strftime(format)

def strip_decimal(amount):
    return amount.split(".")[0]

def bool_to_yes(b):
    return "Yes" if b is True else "No"

def bool_to_int(b):
    return 1 if b is True else 0

def nl2br(s):
    """
    {{ s|nl2br }}

    Convert newlines into <p> and <br />s.
    """
    if not isinstance(s, basestring):
        s = str(s)
    s = re.sub(r'\r\n|\r|\n', '\n', s)
    paragraphs = re.split('\n{2,}', s)
    paragraphs = ['<p>%s</p>' % p.strip().replace('\n', '<br />') for p in paragraphs]
    return '\n\n'.join(paragraphs)


jinja2.filters.FILTERS.update({
    "currency": utils.to_currency,
    "strip_decimal": strip_decimal,
    "date": to_date,
    "time_ago": utils.time_ago,
    "int": int,
    "slug": utils.slugify,
    "intcomma": humanize.intcomma,
    "intword": humanize.intword,
    "naturalday": humanize.naturalday,
    "naturaldate": humanize.naturaldate,
    "naturaltime": humanize.naturaltime,
    "naturalsize": humanize.naturalsize,
    "bool_to_yes": bool_to_yes,
    "bool_to_int": bool_to_int,
    "nl2br": nl2br,
    "markdown": mistune.markdown
})



def maintenance_page(template=None):
    """
    Create the Maintenance view
    Must be instantiated

    import maintenance_view
    MaintenanceView = maintenance_view()

    :param view_template: The directory containing the view pages
    :return:
    """
    if not template:
        template = "Portfolio/MaintenancePage/index.html"

    class Maintenance(Portfolio):
        @classmethod
        def register(cls, app, **kwargs):
            super(cls, cls).register(app, **kwargs)

            if cls.get_config("MAINTENANCE_ON"):
                @app.before_request
                def on_maintenance():
                    return cls.render(layout=template), 503
    return Maintenance

MaintenanceV = maintenance_page()



