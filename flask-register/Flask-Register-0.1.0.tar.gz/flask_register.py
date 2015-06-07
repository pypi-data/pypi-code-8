# -*- coding: utf-8 -*-
from flask import current_app, redirect, url_for
from functools import wraps

__version__ = '0.1.0'
__author__ = 'Cryptos An'
__license__ = 'MIT'
__copyright__ = '(c) 2015 by {0}'.format(__author__)
__all__ = ['RegisterManager']


class RegisterManager(object):

    """Provider to control a view function of Register form.
    """

    def __init__(self, app):
        """Initialize a register manager

        :param app: the Flask instance, which is running.
        """
        # Add a instance of Register Manager to an app of Flask.
        app.register_manager = self

        # Has a name of view function, where you want to redirect to.
        self._redirect_view = None

        # Has a value of register manager turned on/off.
        # The instance provides register, if the variable has a True (Default).
        self._register_enabled = app.config.get('REGISTER_ENABLED', True)

    def is_enabled(self):
        """Return a boolean, if Register is enabled, else disabled.
        """
        return self._register_enabled

    def save_redirect_view(self, view):
        """Save a redirection name of view using when Register is disabled.

        :param view: A name of a view function.
        """
        self._redirect_view = view

    def load_redirect_view(self):
        """Return a string to get a redirection name of view.
        """
        # Checks if the variable has saved a name of view before, else None.
        if self._redirect_view is None:
            raise ValueError('The type is None, try save_redirect_view again.')
        return self._redirect_view


def register_required(f):
    """A decorator that use a Register view with, it will show the view,
    if ``REGISTER_ENABLED`` has True.
    usage:

        @app.route('/register')
        @register_required
        def register():
            pass

    """
    @wraps(f)
    def decorated_register(*args, **kwargs):
        if current_app.register_manager.is_enabled():
            return f(*args, **kwargs)
        return redirect(url_for(
            current_app.register_manager.load_redirect_view()))
    return decorated_register
