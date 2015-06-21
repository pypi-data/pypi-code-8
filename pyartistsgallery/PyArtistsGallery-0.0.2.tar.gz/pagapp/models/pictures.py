"""Description of "pictures" table from database.

List of classes:
Pictures -- contains description of "pictures" table.
"""

from pagapp.models import db


class Pictures(db.Model):
    """Class with description of "pictures" table inside.

    Table "pictures" contains next fields:
    id -- unique id of picture.
    album_id -- id of album, which contain picture inside.
    path_to_image -- path to corresponding image.
    path_to_thumbnail -- path to corresponding thumbnail.
    name -- name of picture.
    description -- description of the picture.
    upload_date -- date, when picture was uploaded.
    uploader_id -- ud of user, who uploaded picture.
    """

    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    path_to_image = db.Column(db.String(), index=True, nullable=False)
    path_to_thumbnail = db.Column(db.String(), index=True, nullable=False)
    name = db.Column(db.String(), index=True, nullable=False)
    description = db.Column(db.String(), index=True, nullable=False)
    upload_date = db.Column(db.DateTime(), index=True, nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    size = db.Column(db.Integer, index=True)

    def __init__(self, row_data):
        """Saves picture data in internal structures.

        Overrides default form constructor.

        Argument:
        row_data -- dictionary with picture's data. Dictionary
        should has the next fields:
            album_id -- id of album, which contains picture.
            uploader_id -- id of user, who uploaded picture.
            upload_date -- date, when picture was uploaded.
            path_to_image -- path to file with picture.
            path_to_thumbnail -- path to file with thumbnail for picture.
            name -- name of the picture. If name is omitted - empty string
        should be inserted.
            description -- description of the picture. If description is
        omitted - empty string should be inserted.
            size -- size of uploaded file
        """
        self.album_id = row_data['album_id']
        self.path_to_image = row_data['path_to_image']
        self.path_to_thumbnail = row_data['path_to_thumbnail']
        self.upload_date = row_data['upload_date']
        self.uploader_id = row_data['uploader_id']
        try:
            self.name = row_data['name']
        except KeyError:
            self.name = ''
        try:
            self.description = row_data['description']
        except KeyError:
            self.description = ''
        self.size = row_data['size']

    def __repr__(self):
        """Prints instance contents in debug session."""
        return 'Album ID: {}, Uploader ID: {}, Date: {}, Path: {}|{}, ' \
               'Name: {}, Description: {}, Size: {} KB'. \
            format(str(self.album_id),
                   str(self.uploader_id),
                   str(self.upload_date),
                   self.path_to_image,
                   self.path_to_thumbnail,
                   self.name,
                   self.description,
                   self.size)
