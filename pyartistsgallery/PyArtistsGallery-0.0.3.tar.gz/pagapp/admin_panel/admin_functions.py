"""Functions, which performs administrator's tasks.

Functions, which able to delete, edit, create albums, change password
for current user and so on.
"""

import string
import random
import re

from flask import request, flash, current_app
from flask_login import current_user

from pagapp.models import db
from pagapp.models.albums import Albums
from pagapp.support_functions import flash_form_errors, remove_danger_symbols
from pagapp.admin_panel.save_picture_functions import save_file


def change_password(form):
    """Changes password for current user."""
    if form.submit_button.data is False:
        return

    current_app.logger.debug("Changing password.")
    if request.method == 'POST' and form.validate():
        current_app.logger.debug("Form within {} function validated.".format(
            change_password.__name__))
        new_password = remove_danger_symbols(form.new_password.data)
        current_user.set_new_password(new_password)
        db.session.commit()
        flash("Password successfully changed", category='success')
    else:
        current_app.logger.debug(
            "Form within {} function didn't validated.".format(
                change_password.__name__))
        flash_form_errors(form)


def add_new_album(form):
    """Adds new album to database."""
    if form.submit_button.data is False:
        return

    current_app.logger.debug("Adding new album...")

    if request.method == 'POST' and form.validate():
        current_app.logger.debug("Form within {} function validated.".format(
            change_password.__name__))
        album_name = remove_danger_symbols(form.album_name.data)
        album_description = remove_danger_symbols(form.album_description.data)

        url_part = album_name.lower()
        url_part = url_part.strip(string.punctuation)
        whitespace_re = re.compile('[' + string.whitespace + ']')
        url_part = whitespace_re.sub('-', url_part)

        if Albums.query.filter_by(url_part=url_part).count() != 0:
            current_app.logger.debug("Given URL: {} already exists.".format(
                url_part))
            url_part += ''.join(
                random.choice(
                    string.ascii_letters + string.digits
                ) for _ in range(5))

        new_album = Albums(url_part, album_name, album_description)

        db.session.add(new_album)
        db.session.commit()
        flash("New album successfully added.", category='success')
    else:
        current_app.logger.debug(
            "Form within {} function didn't validated.".format(
                add_new_album.__name__))
        flash_form_errors(form)

    # Clear form input fields to show placeholders.
    form.album_name.data = ''
    form.album_description.data = ''


def upload_files(form):
    """Uploads file to gallery.

    This function uploads file to the gallery and updates field 'album'
    of UploadForm. We should have up-to-date list of albums in select
    dropdown and in field 'album' to pass throw form's validation.
    """
    form.album.choices = [
        (
            str(album.id),
            album.album_name
        ) for album in Albums.query.all()]

    if form.submit_button.data is False:
        return

    current_app.logger.debug("Starting file upload...")
    current_app.logger.debug("form.validate(): " + str(form.validate()))

    if request.method == 'POST' and form.validate():
        save_file(form.file_name,
                  form.album.data,
                  remove_danger_symbols(form.name.data),
                  remove_danger_symbols(form.description.data))
    else:
        current_app.logger.debug(
            "Form within {} function didn't validated.".format(
                upload_files.__name__))
        flash_form_errors(form)
