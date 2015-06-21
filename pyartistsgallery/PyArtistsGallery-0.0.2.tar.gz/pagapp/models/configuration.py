"""Description of 'Configuration' table from database.

List of classes:
Configuration - contains description of table.
"""

from pagapp.models import db


class Configuration(db.Model):
    """Class with description of 'configuration' table.

    This table contains next fields:
    id -- id of record.
    gallery_title -- title name of installed gallery.

    This table can contain only one row - all another rows
    (two, three, etc) will be ignored.
    """

    id = db.Column(db.Integer, primary_key=True)
    gallery_title = db.Column(db.String(128), nullable=False)

    def __init__(self, gallery_title):
        """Saves user-provided data in the database.

        Arguments:
        gallery_title -- title of installed gallery.
        """
        self.gallery_title = gallery_title

    def __repr__(self):
        """Prints instance contents in debug session."""
        return 'Title: {}'.format(self.gallery_title)
