"""Handlers for pictures' API calls"""

import json
from flask import request, current_app
from flask_login import login_required

from pagapp.application_api import application_api
from pagapp.models import db
from pagapp.models.pictures import Pictures
from pagapp.support_functions import remove_danger_symbols
from pagapp.application_api.html_generators import generate_action_buttons_html, \
    generate_thumbnail_html


def _generate_picture_table_item(picture):
    return {
        'thumbnail': generate_thumbnail_html(picture.path_to_thumbnail),
        'name': picture.name,
        'description': picture.description,
        'upload_date': picture.upload_date.strftime('%d.%m.%Y %H:%M:%S'),
        'size': picture.size,
        'actions': generate_action_buttons_html(
            picture.id, picture.name, picture.description,
            'editPictureModal', 'deletePicture'
        )
    }


@application_api.route('/get-pictures-list', methods=['POST'])
@login_required
def get_pictures_list():
    """Returns list of pictures.

    Returns JSON array, which contains
    list of pictures from one album.
    Album ID can be found within POST request.
    Sample result:
    [
        {
            'thumbnail': '',
            'name': 'Picture name',
            'description': 'Picture description',
            'upload_date': '',
            'size': '',
            'actions': ''
        },
        ...
    ]
    """
    album_id = remove_danger_symbols(request.json['album_id'])
    return json.dumps(
        [_generate_picture_table_item(picture
                                      ) for picture in Pictures.query.filter_by(
            album_id=album_id).all()])


@application_api.route('/delete-picture', methods=['POST'])
@login_required
def delete_picture():
    """Deletes picture with given ID if it is one picture in the database."""
    picture_id = remove_danger_symbols(request.form['picture_id'])
    picture = Pictures.query.filter_by(id=picture_id)
    if picture.count() != 1:
        current_app.logger.error(
            "Count of pictures with given ID ({}) is more than 1.".format(
                picture_id))
        return 'Cannot delete picture, too much IDs!', 404
    else:
        current_app.logger.debug("Deleting picture with ID {}.".format(
            picture_id))
        db.session.delete(picture.first())
        db.session.commit()
        return '', 200


@application_api.route('/edit-picture', methods=['POST'])
@login_required
def edit_picture():
    "Edit picture with given ID, name and description."
    picture_id = remove_danger_symbols(request.form['picture_id'])
    picture = Pictures.query.filter_by(id=picture_id)

    if picture.count() == 0:
        current_app.logger.error(
            "Picture with given ID ({}) does not exists.".format(picture_id))
        return 'Picture does not exists!', 404
    if picture.count() != 1:
        current_app.logger.error(
            "Count of pictures with given ID ({}) is more than 1.".format(
                picture_id))
        return 'Cannot edit picture, too much IDs!', 404

    picture_name = remove_danger_symbols(request.form['picture_name'])
    picture_description = remove_danger_symbols(
        request.form['picture_description'])

    current_app.logger.debug(
        "Editing picture with ID {}. New name: {}. New description: {}.".format(
            picture_id, picture_name, picture_description))
    picture.first().name = picture_name
    picture.first().description = picture_description
    db.session.commit()
    return '', 200
