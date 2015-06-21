"""Description of 'alembic_version' table

This table uses by flask-migrate for performing
updates.
"""

from pagapp.models import db


class AlembicVersion(db.Model):
    """Table 'alembic_version' used in database upgrades

    Table contains next fields:
    version_num -- database version.
    """

    __tablename__ = 'alembic_version'
    version_num = db.Column(db.String(32), nullable=False, primary_key=True)

    def __init__(self, version):
        """Initializes database version and other fields."""
        self.version_num = version

    def __repr__(self):
        """Prints instance contents in debug session."""
        return 'Version: {}'.format(self.version_num)
