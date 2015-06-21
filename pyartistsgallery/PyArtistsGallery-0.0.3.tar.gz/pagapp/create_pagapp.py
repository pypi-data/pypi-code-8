"""Functions which instantiate web application."""

from os import makedirs
from os.path import dirname, exists
from flask import Flask
from logging import ERROR, Formatter, getLogger, DEBUG
from logging.handlers import RotatingFileHandler

from pagapp.models import db
from pagapp.support_functions import lm
from pagapp.public_pages import public_pages
from pagapp.admin_panel import admin_panel
from pagapp.service_pages import service_pages
from pagapp.application_api import application_api


def check_folders(app):
    """Checks is folders exists and creates it if not.

    This function checks for upload folders.
    """
    upload_directory = dirname(app.config['UPLOAD_FOLDER'])
    if not exists(upload_directory):
        app.logger.error(
            "Directory for uploads ({}) does not exists! ".format(
                app.config['UPLOAD_FOLDER']) +
            "Trying to create new one...")
        makedirs(upload_directory)
    else:
        app.logger.info("Directory for uploads exists.")

    thumbnail_directory = dirname(app.config['UPLOAD_FOLDER'] + 'thumbnails/')
    if not exists(thumbnail_directory):
        app.logger.error(
            "Directory for thumbnails ({}) does not exists! ".format(
                app.config['UPLOAD_FOLDER'] + 'thumbnails/') +
            "Trying to create new one...")
        makedirs(thumbnail_directory)
    else:
        app.logger.info("Directory for thumbnails exists.")


def setup_logging(app):
    """Setup logging facility.

    This function switch logging output to the file
    if application does not in debug mode.
    """
    if app.debug is False:
        # Application log.
        handler = RotatingFileHandler(
            app.config['APP_LOG_FILE'],
            mode='a',
            maxBytes=app.config['APP_LOG_FILE_MAX_BYTES'],
            backupCount=app.config['APP_LOG_FILE_BACKUP_COUNT'],
            encoding=None,
            delay=False)
        handler.setLevel(ERROR)
        handler.setFormatter(Formatter(
            '[%(asctime)s] %(filename)s:%(lineno)s ' +
            '- %(levelname)s - %(message)s'))
        app.logger.addHandler(handler)

        # HTTP queries log.
        handler = RotatingFileHandler(
            app.config['HTTP_LOG_FILE'],
            mode='a',
            maxBytes=app.config['HTTP_LOG_FILE_MAX_BYTES'],
            backupCount=app.config['HTTP_LOG_FILE_BACKUP_COUNT'],
            encoding=None,
            delay=False)
        log = getLogger('werkzeug')
        log.setLevel(DEBUG)
        log.addHandler(handler)


def register_blueprints(app):
    """Register application's blueprints"""
    app.register_blueprint(public_pages)
    app.register_blueprint(admin_panel)
    app.register_blueprint(service_pages)
    app.register_blueprint(application_api)


def create_pagapp(path_to_config, debug):
    """Flask application creator.

    Creates PyArtistsGallery application with configuration,
    red from given path_to_config.
    """
    app = Flask(__name__)
    app.debug = debug
    app.config.from_object(path_to_config)
    app.static_folder = app.config['STATIC_FOLDER']
    app.template_folder = app.config['TEMPLATES_FOLDER']

    db.init_app(app)
    lm.init_app(app)

    register_blueprints(app)
    setup_logging(app)
    check_folders(app)

    app.logger.info("Application starting...")
    return app
