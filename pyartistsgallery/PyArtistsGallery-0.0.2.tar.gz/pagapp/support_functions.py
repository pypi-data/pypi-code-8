"""Different support functions for PyArtistsGallery.

I place here some functions, which do not match to any
blueprint or widely use with all blueprints.
"""

from sqlalchemy.orm.exc import ObjectDeletedError
from sqlalchemy.exc import OperationalError
from flask import flash, Markup, current_app
from flask_login import LoginManager

from pagapp.models.users import Users
from pagapp.models.configuration import Configuration

lm = LoginManager()


@lm.user_loader
def load_user(uid):
    """Loads user by user's ID.

    Argument:
    uid -- user's ID (from database).
    Result:
    User object from database.
    """
    current_app.logger.debug("load_user({}) called.".format(uid))
    try:
        result = Users.query.get(int(uid))
    except ObjectDeletedError:
        result = None
    return result


def flash_form_errors(form):
    """Shows errors from Flask-WTF form.

    Argument:
    form -- errors will be taken and parsed from this form.
    """
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                "Error in the %s field - %s" % (getattr(form, field).label.text,
                                                error),
                category='warning')


def is_first_run():
    """Is application running first time or not.

    Function returns True if some config fields do
    not filled - in this case we consider, what application
    run at first time.
    Function returns False if all configuration fields in database
    are filled.
    """

    try:
        if len(Configuration.query.all()) == 0:
            return True

        if len(Users.query.all()) == 0:
            return True
    except OperationalError:
        return True

    return False


def remove_danger_symbols(string):
    """Removes possibly dangerous HTML/JS code from given string."""
    safe_string = Markup(string).striptags()
    safe_string = Markup.escape(safe_string).__str__()
    return safe_string
