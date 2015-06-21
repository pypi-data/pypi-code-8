"""Functions, which help save uploaded files."""

import os
import random
import string

from datetime import datetime
from flask import current_app, flash
from flask_login import current_user
from os.path import join
from PIL import Image

from pagapp.models import db
from pagapp.models.pictures import Pictures


def create_thumbnail(path_to_image, path_to_thumbnail):
    """Creates thumbnail from given image.

    Idea of this function was taken from:
    http://united-coders.com/christian-harms/image-resiz
    ing-tips-every-coder-should-know/
    """
    image = Image.open(path_to_image)

    # preresize image with factor 2, 4, 8 and fast algorithm
    factor = 1
    size = current_app.config['THUMBNAIL_SIZE']
    while image.size[0] / factor > 2 * size['x'] and \
            image.size[1] / factor > 2 * size['y']:
        factor *= 2
    if factor > 1:
        image.thumbnail(
            (image.size[0] / factor, image.size[1] / factor), Image.NEAREST)

    x1 = y1 = 0
    x2, y2 = image.size
    width_ratio = 1.0 * x2 / size['x']
    height_ratio = 1.0 * y2 / size['y']
    if height_ratio > width_ratio:
        y1 = int(y2 / 2 - size['y'] * width_ratio / 2)
        y2 = int(y2 / 2 + size['y'] * width_ratio / 2)
    else:
        x1 = int(x2 / 2 - size['x'] * height_ratio / 2)
        x2 = int(x2 / 2 + size['x'] * height_ratio / 2)
    image = image.crop((x1, y1, x2, y2))
    image.thumbnail((size['x'], size['y']), Image.ANTIALIAS)
    image.save(path_to_thumbnail)


def save_file(filename_field, album_id, name, description):
    extension = filename_field.data.filename.split(sep='.')[-1].lower()
    if extension not in current_app.config['ALLOWED_EXTENSIONS']:
        current_app.logger.error(
            'User tried to upload file with unsupported extension: {}'.format(
                extension))
        flash('Unupported extension!', category='error')
        return
    file_name = ''.join(random.choice(
        string.ascii_letters + string.digits
    ) for _ in range(20)) + '.{}'.format(extension)

    file_path = join(current_app.config['UPLOAD_FOLDER'], file_name)
    file_path_web = join(
        '/static/' + current_app.config['UPLOAD_FOLDER_RELATIVE'], file_name)

    thumbnail_path = join(current_app.config['UPLOAD_FOLDER'] + 'thumbnails/',
                          file_name)
    thumbnail_path_web = join(
        '/static/' +
        current_app.config['UPLOAD_FOLDER_RELATIVE'] +
        'thumbnails/', file_name)

    current_app.logger.info("Saving file: " + file_name + " to: " + file_path)

    if Pictures.query.filter_by(path_to_image=file_path_web).count() != 0:
        warn_message = 'File already saved in {}.'.format(file_path)
        current_app.logger.warning(warn_message)
        flash(warn_message, category='warning')
        return

    filename_field.data.save(file_path)
    create_thumbnail(file_path, thumbnail_path)
    current_app.logger.info('Thumbnail saved in: {}.'.format(thumbnail_path))

    picture_row_data = {
        'album_id': album_id,
        'uploader_id': current_user.id,
        'upload_date': datetime.now(),
        'path_to_image': file_path_web,
        'path_to_thumbnail': thumbnail_path_web,
        'name': name,
        'description': description,
        'size': round(os.stat(file_path).st_size / 1024, 3)
    }
    new_picture = Pictures(picture_row_data)
    db.session.add(new_picture)
    db.session.commit()

    flash("File successfully uploaded.", category='success')
