"""Functions to operate with whole database."""

from flask import current_app
from flask_migrate import Migrate, upgrade

from pagapp.models import db
from pagapp.models.alembic_version import AlembicVersion


def create_database():
    """Creates database schema."""
    current_app.logger.info("Creating new database...")
    db.create_all()
    version = AlembicVersion(
        version=current_app.config['SQLALCHEMY_DATABASE_VERSION'])
    db.session.add(version)
    current_app.logger.info(
        "Created new database with version {} by the path: {}.".format(
            current_app.config['SQLALCHEMY_DATABASE_VERSION'],
            current_app.config['SQLALCHEMY_DATABASE_URI']))
    # db.session.commit()
    # Will commit inside the first_run() function:
    # look at pagapp.service_pages.views.


def upgrade_database():
    """Upgrades current database."""
    current_app.logger.info("Upgrading the database...")
    migrate = Migrate(current_app, db)
    upgrade(directory='migrations')
    current_app.logger.info("Database updated.")
    del migrate


def is_upgrade_ready():
    """Checks - is we need update database."""
    db_version = AlembicVersion.query.first().version_num
    code_version = current_app.config['SQLALCHEMY_DATABASE_VERSION']
    if db_version != code_version:
        current_app.logger.info("We should update DB.")
        current_app.logger.info("DB version: {}".format(db_version))
        current_app.logger.info("Version in config: {}".format(code_version))
        return True
    else:
        return False
