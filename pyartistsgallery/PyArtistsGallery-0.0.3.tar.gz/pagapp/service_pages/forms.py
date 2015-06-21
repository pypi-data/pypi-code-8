"""Forms, which using in "first run" page."""

from flask_wtf import Form
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class FirstRunForm(Form):
    """First-run form.

    Form, which using in web page, which
    shows at first run of application.
    """

    gallery_title = StringField(
        "Gallery title:",
        validators=[DataRequired()],
        description="Gallery title name")
    username = StringField(
        "Administrator name:",
        validators=[DataRequired()],
        description="Name of gallery administrator")
    password = PasswordField(
        "Administrator's password",
        validators=[DataRequired()],
        description="Password of the gallery administrator")
    password2 = PasswordField(
        "Retype  administrator's password",
        validators=[DataRequired(),
                    EqualTo('password',
                            message="Passwords must match")],
        description="Retype password")
    submit_button = SubmitField(
        "Save settings",
        description="Save settings")
