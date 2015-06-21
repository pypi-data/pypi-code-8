"""Form, using in blueprint with public pages.

This module contains simple login form.
"""

from flask import current_app
from flask_wtf import Form
from flask_wtf.form import ValidationError
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from pagapp.models.users import Users
from pagapp.support_functions import remove_danger_symbols


class LoginForm(Form):
    """Form, where user can enter login and password.

    Form provides two fields: for login and for password and validates
    entered credentials.
    """

    login = StringField(
        "Login name:",
        validators=[DataRequired()],
        description="Login name")
    password = PasswordField(
        "Password:",
        validators=[DataRequired()],
        description="Password")
    submit_button = SubmitField(
        "Let me in",
        description="Login button")

    @staticmethod
    def validate_login(form, field):
        """Login field validator."""
        del form
        username = remove_danger_symbols(field.data)
        user = Users.query.filter_by(nickname=username).first()
        if user is None:
            current_app.logger.error(
                "User {} does not exists in the database [{}].".format(
                    username, LoginForm.__name__))
            raise ValidationError(
                'User \"%s\" does not exists in the database.' %
                field.data)

    @staticmethod
    def validate_password(form, field):
        """Password field validator.

        If given password does not match with user's password from
        database - send warning to user.
        """
        username = remove_danger_symbols(form.login.data)
        password = remove_danger_symbols(field.data)
        user = Users.query.filter_by(nickname=username).first()
        if user is not None:
            if user.check_password(password) is False:
                current_app.logger.error(
                    "Given password and password from database are not " +
                    "match [{}]".format(LoginForm.__name__))
                raise ValidationError('Wrong password.')
