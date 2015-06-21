"""PyArtistsGallery configuration.

List of options:
GALLERY_TITLE -- title of the gallery, which shown on every page.
SQLALCHEMY_DATABASE_URI -- absolute path to SQLite database.
STATIC_FOLDER -- path to folder with css, js and other static files.
TEMPLATES_FOLDER -- path to folder with base templates.
xxx_LOG_FILE -- path log file.
xxx_LOG_FILE_MAX_BYTES -- maximal size of log file, before it is closed, saved
as 'logfile.N' and new file opened.
xxx_LOG_FILE_BACKUP_COUNT -- maximal value of N.

There are two types of log files:
 APP - application level log.
 HTTP - HTTP queries from weuzkreug.
"""

import os
import random
import string


class Config:
    ############################################################
    # Base settings.
    ############################################################
    _BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
                              os.path.join(_BASEDIR, 'pagapp.db')
    SQLALCHEMY_DATABASE_VERSION = '3c73f5517a2'
    STATIC_FOLDER = os.path.join(_BASEDIR, 'static/')
    TEMPLATES_FOLDER = os.path.join(_BASEDIR, 'templates/')
    THUMBNAIL_SIZE = {'x': 75, 'y': 75}  # in px

    ############################################################
    # Log files.
    ############################################################
    APP_LOG_FILE = os.path.join(_BASEDIR, 'pagapp.log')
    APP_LOG_FILE_MAX_BYTES = 102400
    APP_LOG_FILE_BACKUP_COUNT = 10
    HTTP_LOG_FILE = os.path.join(_BASEDIR, 'pagapp-http.log')
    HTTP_LOG_FILE_MAX_BYTES = 102400
    HTTP_LOG_FILE_BACKUP_COUNT = 10

    ############################################################
    # Upload settings.
    ############################################################
    UPLOAD_FOLDER_RELATIVE = 'uploads/'
    UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, UPLOAD_FOLDER_RELATIVE)
    ALLOWED_EXTENSIONS = ['png', 'bmp', 'tiff', 'jpg', 'jpeg']

    ############################################################
    # Specific settings for Flask-WTForm. Do not edit!
    ############################################################
    WTF_CSRF_ENABLED = True
    SECRET_KEY_LENGTH = 30
    SECRET_KEY = ''.join(
        random.choice(
            string.ascii_letters + string.digits
        ) for _ in range(SECRET_KEY_LENGTH))
